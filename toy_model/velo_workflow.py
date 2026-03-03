#!/usr/bin/env python3
"""
Unified Velo Toy workflow.

Subcommands
-----------
1) generate
   Batched Velo Toy worker that records full events per parameter combo.

   For each row in the selected batch from --params:
     - Builds geometry and generates events (truth)
     - Applies noise (ghost/drop) and reconstructs
     - Saves a compressed snapshot (.pkl.gz) containing:
           params, truth_event, noisy_event, reco_tracks, reco_event,
           classical_solution, disc_solution, hamiltonian
     - Appends a lightweight index row to events_index.csv
       in the given job output directory.

2) aggregate
   Process ONE batch of saved event snapshots:
     - scans runs_dir/batch_<batch>/*/events_index.csv
     - loads each events_*.pkl.gz
     - runs EventValidator(noisy, reco)
     - writes (in the *batch folder* out_dir = runs_dir/batch_<batch>/):
         event_store.pkl.gz   (params + metrics; optionally full objects)
         metrics.csv          (flat table for quick analysis)
         events_index.csv     (merged per-job indices for the batch)
"""

from __future__ import annotations

import argparse
import csv
import gzip
from pathlib import Path
import sys

import numpy as np
import pandas as pd

from toy_model.state_event_model import *
from toy_model.state_event_generator import StateEventGenerator
from toy_model import state_event_model
from toy_model.simple_hamiltonian import SimpleHamiltonianFast, get_tracks_fast, construct_event
from toy_model.toy_validator import EventValidator as evl

# Prefer dill for broader object support; fall back to pickle
try:
    import dill as _pickle
except ImportError:  # pragma: no cover
    import pickle as _pickle


# =====================================================================
# Shared configuration
# =====================================================================

DZ_MM = 33.0
LAYERS = 5

MODULE_IDS = list(range(1, LAYERS + 1))
LX_MM = [80.0] * LAYERS
LY_MM = [80.0] * LAYERS
ZS_MM = [DZ_MM * l for l in range(1, LAYERS + 1)]

# Default events/particles per *job combo* (can be overridden via params)
DEFAULT_N_PARTICLES_PER_EVENT = [5, 3, 5]

# Predefined density configurations
DENSITY_CONFIGS = {
    "sparse": [5, 3, 2],           # 10 total tracks
    "default": [5, 3, 5],          # 13 total tracks  
    "medium": [10, 10, 10],        # 30 total tracks
    "dense": [20, 20, 20, 20, 20], # 100 total tracks across 5 events
}

# Threshold shaping
THETA_MIN = 0.000015


def parse_n_particles(config_str: str) -> list:
    """Parse n_particles config: either a name like 'sparse' or comma-sep ints like '5,3,2'."""
    if config_str in DENSITY_CONFIGS:
        return DENSITY_CONFIGS[config_str]
    # Try parsing as comma-separated integers
    return [int(x.strip()) for x in config_str.split(",")]


# =====================================================================
# Shared helpers
# =====================================================================

def epsilon_window(meas_err, coll_noise, dz, scale, theta_min):
    theta_s = scale * coll_noise
    theta_r = np.arctan((scale * meas_err) / dz) if dz != 0 else 0.0
    theta_m = theta_min

    threshold = np.sqrt(theta_s**2 + theta_r**2 + theta_m**2)
    eps_thresh = threshold
    return eps_thresh, threshold


def dump_pickle(obj, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with gzip.open(path, "wb") as f:
        _pickle.dump(obj, f, protocol=_pickle.HIGHEST_PROTOCOL)


def append_index_row(index_csv: Path, row_dict: dict) -> None:
    index_csv.parent.mkdir(parents=True, exist_ok=True)
    new_file = not index_csv.exists()
    with open(index_csv, "a", newline="") as f:
        w = csv.DictWriter(f, fieldnames=row_dict.keys())
        if new_file:
            w.writeheader()
        w.writerow(row_dict)


def make_detector():
    return state_event_model.PlaneGeometry(
        module_id=MODULE_IDS, lx=LX_MM, ly=LY_MM, z=ZS_MM
    )


# =====================================================================
# Subcommand: generate  (event generation + reconstruction)
# =====================================================================

def run_one(meas, coll, ghost, drop, repeat, e_win, thresh_flag, erf_sigma, n_particles_config, outdir: Path, phi_max=0.02):
    # Parse n_particles configuration
    n_particles_per_event = parse_n_particles(n_particles_config)
    events = len(n_particles_per_event)
    total_particles = int(np.sum(n_particles_per_event))
    
    # Reproducible randomness per combo - seed based on repeat index
    np.random.seed(repeat)

    Detector = make_detector()
    eps_win, threshold = epsilon_window(meas, coll, DZ_MM, e_win, THETA_MIN)

    seg = StateEventGenerator(
        Detector,
        phi_min=phi_max,
        phi_max=phi_max,
        # theta_min=0.02,
        # theta_max=0.02,
        events=events,
        n_particles=n_particles_per_event,
        measurement_error=float(meas),
        collision_noise=float(coll),
    )

    phi, theta = seg.phi_max, seg.theta_max

    seg.generate_random_primary_vertices({"x": 1, "y": 1, "z": 1})

    event_particles = [
        [{"type": "MIP", "mass": 0.511, "q": 1} for _ in range(total_particles)]
        for _ in range(events)
    ]
    seg.generate_particles(event_particles)
    event_tracks = seg.generate_complete_events()  # "truth" with associations

    # Inject noise and reconstruct
    false_tracks = seg.make_noisy_event(drop_rate=float(drop), ghost_rate=float(ghost))
    ham = SimpleHamiltonianFast(epsilon=float(eps_win), gamma=2.0, delta=1.0, theta_d=erf_sigma)
    ham.construct_hamiltonian(event=event_tracks, convolution=thresh_flag)

    classical_solution = ham.solve_classicaly()
    discretized_solution = (classical_solution > 0.45).astype(int)

    rec_tracks = get_tracks_fast(ham, discretized_solution, false_tracks)
    reco_event = construct_event(
        event_tracks.detector_geometry,
        rec_tracks,
        [t.hits for t in rec_tracks],
        [t.segments for t in rec_tracks],
        event_tracks.detector_geometry.module_id,
    )

    tag = (
        f"m{meas}_c{coll}_g{ghost}_d{drop}_r{repeat}_s{e_win}"
        f"_t_{thresh_flag}_e_{erf_sigma}_np_{n_particles_config}_phi{float(phi)}_theta{float(theta)}"
    )
    snapshot_path = outdir / f"events_{tag}.pkl.gz"
    payload = {
        "params": {
            "hit_res": float(meas),
            "multi_scatter": float(coll),
            "ghost_rate": float(ghost),
            "drop_rate": float(drop),
            "repeat": int(repeat),
            "scale": float(e_win),
            "epsilon": float(ham.epsilon),
            "layers": LAYERS,
            "dz_mm": DZ_MM,

            "thresh_flag": thresh_flag,
            "eps_win": float(eps_win),
            "theta_threshold": float(threshold),
            "erf_sigma": float(erf_sigma),
            "phi_max": float(phi),
            "theta_max": float(theta),
            "n_particles_config": n_particles_config,
            "n_particles_per_event": n_particles_per_event,
            "total_particles": total_particles,
            "events": events,
        },
        "truth_event": event_tracks,      # before ghosts/drops
        "noisy_event": false_tracks,      # after ghosts/drops
        "reco_tracks": rec_tracks,        # reconstructed tracks
        "reco_event": reco_event,         # reconstructed event
        "classical_solution": classical_solution,
        "disc_solution": discretized_solution,
        "hamiltonian": ham,
    }
    dump_pickle(payload, snapshot_path)

    # Lightweight index row for quick discovery without unpickling
    index_csv = outdir / "events_index.csv"
    append_index_row(
        index_csv,
        {
            "file": snapshot_path.name,
            "hit_res": meas,
            "multi_scatter": coll,
            "ghost_rate": ghost,
            "drop_rate": drop,
            "repeat": int(repeat),
            "epsilon": float(ham.epsilon),
            "scale": e_win,
            "layers": LAYERS,
            "events": events,
            "particles_total": total_particles,
            "n_particles_config": n_particles_config,
            "thresh_flag": thresh_flag,
        },
    )


def cmd_generate(args: argparse.Namespace) -> None:
    """Implements the 'generate' subcommand."""
    outdir = args.outdir
    outdir.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(args.params)
    if "batch" not in df.columns:
        raise ValueError("params.csv must contain a 'batch' column.")

    sub = df[df["batch"] == args.batch]
    print(f"[INFO] [generate] Processing batch {args.batch} with {len(sub)} combos -> {outdir}")

    failures = 0
    for i, row in sub.iterrows():
        try:
            # Get n_particles config, default to "default" if not in params
            n_particles_config = str(row.get("n_particles", "default"))
            # Get phi_max, default to 0.02 for backwards compatibility
            phi_max = float(row.get("phi_max", 0.02))
            
            run_one(
                float(row["meas"]),
                float(row["coll"]),
                float(row["ghost"]),
                float(row["drop"]),
                int(row["repeat"]),
                int(row["e_win"]),
                int(row["step_flag"]),
                float(row["erf_sigma"]),
                n_particles_config,
                outdir,
                phi_max=phi_max,
            )
        except Exception as e:
            failures += 1
            print(f"[WARN] [generate] combo at row {i} failed: {e}")

    if failures:
        print(f"[INFO] [generate] Completed with {failures} failures.")
    else:
        print("[INFO] [generate] All combos completed successfully.")


# =====================================================================
# Subcommand: aggregate  (post-processing + metrics)
# =====================================================================

def load_snapshot(p: Path):
    with gzip.open(p, "rb") as f:
        return _pickle.load(f)


def dump_event_store(store: dict, path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    with gzip.open(path, "wb") as f:
        _pickle.dump(store, f, protocol=_pickle.HIGHEST_PROTOCOL)


def cmd_aggregate(args: argparse.Namespace) -> None:
    """
    Aggregate all job results for one batch.

    - Reads per-job events_index.csv files
    - Loads snapshots and computes metrics
    - Writes in out_dir (= runs_dir/batch_<batch>):
        event_store.pkl.gz
        metrics.csv
        events_index.csv   (merged per-job indices)
    """
    runs_dir = args.runs_dir.resolve()
    out_dir = args.out_dir.resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    batch_dir = runs_dir / f"batch_{args.batch}"
    if not batch_dir.exists():
        print(f"[ERROR] [aggregate] Missing batch folder: {batch_dir}", file=sys.stderr)
        sys.exit(2)

    job_dirs = sorted([p for p in batch_dir.iterdir() if p.is_dir()])
    if not job_dirs:
        print(f"[WARN] [aggregate] No job directories under {batch_dir}")

    event_store = {}
    metrics_rows = []
    processed = 0
    index_frames = []

    for job in job_dirs:
        idx = job / "events_index.csv"
        if not idx.exists():
            continue

        try:
            df_idx = pd.read_csv(idx)
            df_idx["job"] = job.name
            index_frames.append(df_idx)
        except Exception as e:
            print(f"[WARN] [aggregate] Could not read {idx}: {e}")
            continue

        for _, row in df_idx.iterrows():
            fname = str(row.get("file", ""))
            if not fname:
                continue
            event_path = job / fname
            if not event_path.exists():
                print(f"[WARN] [aggregate] Missing snapshot {event_path}")
                continue

            try:
                snap = load_snapshot(event_path)
            except Exception as e:
                print(f"[WARN] [aggregate] Failed to load {event_path}: {e}")
                continue

            params = snap.get("params", {})
            truth = snap.get("truth_event", None)
            noisy = snap.get("noisy_event", None)
            reco = snap.get("reco_event", None)

            try:
                validator = evl(noisy, reco)
                metrics = validator.compute_metrics()
            except Exception as e:
                print(f"[WARN] [aggregate] Validator failed on {event_path}: {e}")
                metrics = {}

            entry = {
                "params": params,
                "metrics": metrics,
            }
            if args.store_full:
                entry.update({"truth": truth, "noisy": noisy, "reco": reco})

            event_store[fname] = entry

            flat = {"file": fname}
            flat.update({f"p_{k}": v for k, v in params.items()})
            if isinstance(metrics, dict):
                flat.update({f"m_{k}": v for k, v in metrics.items()})
            metrics_rows.append(flat)

            processed += 1
            if args.verbose and processed % 50 == 0:
                print(f"[INFO] [aggregate] batch {args.batch}: processed {processed} snapshots...")
            if args.max_files and processed >= args.max_files:
                break

        if args.max_files and processed >= args.max_files:
            break

    store_path = out_dir / "event_store.pkl.gz"
    dump_event_store(event_store, store_path)

    df_metrics = pd.DataFrame(metrics_rows)
    (out_dir / "metrics.csv").write_text(df_metrics.to_csv(index=False))

    if index_frames:
        df_index_all = pd.concat(index_frames, ignore_index=True)
        (out_dir / "events_index.csv").write_text(df_index_all.to_csv(index=False))

    print(f"[OK] [aggregate] batch {args.batch}: wrote {store_path}")
    print(f"[OK] [aggregate] batch {args.batch}: wrote {out_dir / 'metrics.csv'}")
    if index_frames:
        print(f"[OK] [aggregate] batch {args.batch}: wrote {out_dir / 'events_index.csv'}")
    print(f"[INFO] [aggregate] batch {args.batch}: total snapshots processed: {processed}")


# =====================================================================
# Top-level CLI
# =====================================================================

def build_arg_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(
        description="Unified Velo Toy workflow: generate events and aggregate metrics."
    )
    subparsers = ap.add_subparsers(dest="command", required=True)

    gen = subparsers.add_parser(
        "generate",
        help="Generate and store event snapshots for a given batch."
    )
    gen.add_argument("--params", type=Path, required=True, help="Path to params.csv")
    gen.add_argument("--batch", type=int, required=True, help="Batch id to process")
    gen.add_argument(
        "--outdir",
        type=Path,
        required=True,
        help="Destination directory for outputs (e.g. runs_X/batch_0/123.0)",
    )
    gen.set_defaults(func=cmd_generate)

    agg = subparsers.add_parser(
        "aggregate",
        help="Aggregate event snapshots for one batch, compute metrics, and store results."
    )
    agg.add_argument(
        "--runs-dir",
        type=Path,
        required=True,
        help="Root runs dir containing batch_* folders (each with job subdirs)",
    )
    agg.add_argument("--batch", type=int, required=True, help="Batch id to process")
    agg.add_argument(
        "--out-dir",
        type=Path,
        required=True,
        help="Batch output directory (e.g. runs_X/batch_0)",
    )
    agg.add_argument(
        "--store-full",
        action="store_true",
        help="Also store truth/noisy/reco objects in event_store (memory heavy)",
    )
    agg.add_argument(
        "--max-files",
        type=int,
        default=None,
        help="Limit number of files (debug / testing)",
    )
    agg.add_argument(
        "--verbose",
        action="store_true",
        help="Print progress messages every 50 snapshots",
    )
    agg.set_defaults(func=cmd_aggregate)

    return ap


def main():
    parser = build_arg_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()