# 1-Bit HHL track simulation toy model by Xenofon Chiotopoulos

## MIT License
# https://github.com/Xenofon-Chiotopoulos/OneBQF?tab=MIT-1-ov-file

# Copyright (c) 2025 Xenofon Chiotopoulos
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the \"Software\"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.'
# THE SOFTWARE IS PROVIDED \"AS IS\", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.'

#--------------------------------------------------------------------------------------
# Credit
# This is a modified version of the Python file toy_validator.py published here: 
# https://github.com/Xenofon-Chiotopoulos/OneBQF/blob/main/toy_model/toy_validator.py
#--------------------------------------------------------------------------------------

#------------------------------------------------------------------------------------------------------
# Reco maps
# Updated by Alain Chancé
# Replaced the following lines:
# self.rec_track_hits: Dict[int, set] = {
#     t.track_id: {h.hit_id for h in t.hits} for t in rec_tracks.tracks
# }
# by the following ones copied from class EventValidator in module toy_validator.py
# https://github.com/Xenofon-Chiotopoulos/Tracking_Toy_model/blob/main/src/toy_model/toy_validator.py
# self.rec_track_hits = {
#     track.track_id: {hit.hit_id for hit in track.hits} 
#     for track in rec_tracks
# }
#------------------------------------------------------------------------------------------------------


# file: toy_validator.py
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Dict, List, Optional, Tuple
import numpy as np

# Project-level types (import from your codebase if available)
from toy_model.state_event_generator import Event, Track
import pandas as pd  



# -----------------------------------------------------------------------------
# Data structures
# -----------------------------------------------------------------------------

@dataclass
class Match:
    """
    Association summary for a reconstructed track r_i against its *best* truth t_j.

    Notation:
      - R_i := set of hit IDs on reconstructed track r_i
      - T_j := set of hit IDs on truth track t_j
      - |R_i|, |T_j| := hit counts on those tracks
      - |R_i ∩ T_j| := number of shared hits ("correct hits")
      - purity  p_ij := |R_i ∩ T_j| / |R_i|
      - complete c_ij := |R_i ∩ T_j| / |T_j| # hit efficiency
    """
    # Always recorded (even if the match fails acceptance cuts)
    best_truth_id: Optional[int]      # argmax-purity truth (may be None if no hits)
    rec_hits: int                     # |R_i|
    truth_hits: int                   # |T_j| for best_truth_id (0 if none)
    correct_hits: int                 # |R_i ∩ T_j|
    purity: float                     # p_ij
    completeness: float               # c_ij

    # Acceptance / bookkeeping
    candidate: bool = True            # passed reco-level gate (min_rec_hits)
    accepted: bool = False            # passed match-level gates
    truth_id: Optional[int] = None    # accepted truth_id (None if rejected)
    is_clone: bool = False            # marked as clone during primary selection

# -----------------------------------------------------------------------------
# Event Validator
# -----------------------------------------------------------------------------

class EventValidator:
    """
    LHCb-style event validator for track performance (VELO-oriented), with explicit
    R_i/T_j notation and standardized accounting.

    Conventions (aligned with TrackChecker-style reports):

      1) Reco-level gate ("candidate tracks"): a reco track r_i is considered
         *candidate* only if it passes a minimal quality selection (default: a
         hit-count threshold). Non-candidates are excluded from *all* denominators.

      2) Match-level acceptance (among candidates): a track is *accepted* if its
         best truth association satisfies purity ≥ purity_min (default 0.7) and,
         optionally, completeness ≥ completeness_min and correct_hits ≥ min_shared_hits.

      3) Ghosts: candidate reco tracks that fail the acceptance.

      4) Primary vs clones: for a given truth t_j, among all accepted recos mapped
         to t_j, select the primary with the largest |R_i ∩ T_j| (tie-break by higher
         purity); others are clones.

    Metrics emitted (all under 'm_*' keys for compatibility with pipeline):
      - m_reconstruction_efficiency: matched reconstructible truths / reconstructible truths
      - m_ghost_rate: ghosts / candidate_reco
      - m_clone_fraction_total: clones / candidate_reco
      - m_clone_fraction_among_matched: clones / accepted_reco
      - m_purity_all_matched: mean purity over accepted reco (incl. clones)
      - m_purity_primary_only: mean purity over primaries only
      - m_hit_efficiency_mean: mean completeness over primaries (unweighted)
      - m_hit_efficiency_weighted: |T|-weighted completeness over primaries

    Tables:
      - Per-track table (one row per candidate reco): enables post-hoc retuning.
      - Per-truth table (one row per truth): primary info per truth.

    Fast retuning:
      - recompute_from_track_table(...) re-derives all metrics for arbitrary gates
        without re-doing hit intersections.
    """

    # -------------------------------------------------------------------------
    # Init
    # -------------------------------------------------------------------------
    def __init__(
        self,
        truth_event: Event,
        rec_tracks: List[Track],
        reconstructible_filter: Optional[Callable[[Track], bool]] = None,
    ):
        self.truth_event = truth_event
        self.rec_tracks = rec_tracks

        # Truth maps
        self.truth_tracks: Dict[int, Track] = {t.track_id: t for t in truth_event.tracks}
        self.truth_track_hits: Dict[int, set] = {
            tid: {h.hit_id for h in t.hits} for tid, t in self.truth_tracks.items()
        }

        #------------------------------------------------------------------------------------------------------
        # Reco maps
        # Updated by Alain Chancé
        # Replaced the following lines:
        # self.rec_track_hits: Dict[int, set] = {
        #     t.track_id: {h.hit_id for h in t.hits} for t in rec_tracks.tracks
        # }
        # by the following ones copied from class EventValidator in module toy_validator.py
        # https://github.com/Xenofon-Chiotopoulos/Tracking_Toy_model/blob/main/src/toy_model/toy_validator.py
        self.rec_track_hits = {
            track.track_id: {hit.hit_id for hit in track.hits} 
            for track in rec_tracks
        }
        #------------------------------------------------------------------------------------------------------

        # Reconstructible truth selection
        if reconstructible_filter is None:
            self.reconstructible_truth_ids = set(self.truth_tracks.keys())
        else:
            self.reconstructible_truth_ids = {
                t.track_id for t in truth_event.tracks if reconstructible_filter(t)
            }

        # For heuristics (e.g. deriving min_rec_hits), use reconstructible truths only
        recon_truth_lengths = (
            len(self.truth_tracks[tid].hits) for tid in self.reconstructible_truth_ids
        )
        self.max_hits_in_recon_truth = max(recon_truth_lengths, default=0)

    # -------------------------------------------------------------------------
    # Matching
    # -------------------------------------------------------------------------
    def match_tracks(
        self,
        purity_min: float = 0.7,                # GOOD and ghost threshold (purity-based per Instructions.pdf)
        completeness_min: Optional[float] = 0.7,  # optional extra gate for GOOD if enforce_completeness=True
        min_rec_hits: Optional[int | float] = None,
        min_shared_hits: int = 0,
        enforce_completeness: bool = False,     # keep optional completeness gate for GOOD
        ) -> Tuple[Dict[int, Match], Dict[int, List[int]], List[int]]:
        """
        Build best matches and the pre-clone truth→recs index.
        GOOD acceptance is driven by purity ≥ purity_min (per Instructions.pdf).
        """
        # Reco-level gate; by default keep all reconstructed tracks
        if min_rec_hits is None:
            min_rec_hits = purity_min * self.max_hits_in_recon_truth
        else:
            min_rec_hits = int(np.ceil(min_rec_hits)) 

        rec_best: Dict[int, Match] = {}
        truth_to_recs: Dict[int, List[int]] = {}
        candidate_rec_ids: List[int] = []

        for rec_id, R_i in self.rec_track_hits.items():
            r_size = len(R_i)
            # print(f"Processing reco track {rec_id} with {r_size} hits")
            if r_size < min_rec_hits:
                rec_best[rec_id] = Match(
                    best_truth_id=None, rec_hits=r_size, truth_hits=0, correct_hits=0,
                    purity=0.0, completeness=0.0, candidate=False, accepted=False, truth_id=None
                )
                # print(f"  Rejected as non-candidate (|R|={r_size} < {min_rec_hits})")
                continue
            # print(f"  Accepted as candidate (|R|={r_size} ≥ {min_rec_hits})")

            candidate_rec_ids.append(rec_id)

            # Best association by (purity, correct, completeness)
            best_truth = None
            best_purity = -1.0
            best_correct = -1
            best_comp = -1.0
            best_truth_hits = 0

            if r_size > 0:
                for truth_id, T_j in self.truth_track_hits.items():
                    correct = len(R_i & T_j)
                    purity = correct / r_size if r_size else 0.0
                    t_size = len(T_j) if len(T_j) > 0 else 1
                    completeness = correct / t_size

                    better = (
                        (purity > best_purity)
                        or (purity == best_purity and correct > best_correct)
                        or (purity == best_purity and correct == best_correct and completeness > best_comp)
                    )
                    if better:
                        best_truth = truth_id
                        best_purity = purity
                        best_correct = correct
                        best_comp = completeness
                        best_truth_hits = len(T_j)

            m = Match(
                best_truth_id=best_truth,
                rec_hits=r_size,
                truth_hits=best_truth_hits if best_truth is not None else 0,
                correct_hits=max(0, best_correct),
                purity=max(0.0, best_purity),
                completeness=max(0.0, best_comp),
                candidate=True,
                accepted=False,
                truth_id=None,
                is_clone=False,
            )

            # GOOD acceptance: purity is the primary criterion (per Instructions.pdf)
            passes_purity = (m.purity >= purity_min)
            # print(f"  Best match: truth {m.best_truth_id} |R∩T|={m.correct_hits}, purity={m.purity:.3f}, completeness={m.completeness:.3f}")
            passes_comp = (m.completeness >= completeness_min) if enforce_completeness else True
            # passes_shared = (m.correct_hits >= min_shared_hits)


            if (m.best_truth_id is not None) and passes_purity and passes_comp:
                m.accepted = True
                m.truth_id = m.best_truth_id
                truth_to_recs.setdefault(m.truth_id, []).append(rec_id)

            rec_best[rec_id] = m

        return rec_best, truth_to_recs, candidate_rec_ids



    # -------------------------------------------------------------------------
    # Primary selection
    # -------------------------------------------------------------------------
    def _primary_reco_per_truth(
        self, truth_to_recs: Dict[int, List[int]], rec_best: Dict[int, Match]
    ) -> Tuple[Dict[int, int], List[int]]:
        """Choose one primary reco per truth (max correct hits; tie-break by purity)."""
        primary: Dict[int, int] = {}
        clones: List[int] = []
        for truth_id, rec_ids in truth_to_recs.items():
            if not rec_ids:
                continue
            rec_ids_sorted = sorted(
                rec_ids,
                key=lambda r: (rec_best[r].correct_hits, rec_best[r].purity),
                reverse=True,
            )
            primary[truth_id] = rec_ids_sorted[0]
            clones.extend(rec_ids_sorted[1:])
        return primary, clones

    # -------------------------------------------------------------------------
    # Metrics (event summary)
    # -------------------------------------------------------------------------
    def compute_metrics(
        self,
        purity_min: float = 0.7,             # GOOD and ghost threshold (purity-based per Instructions.pdf)
        completeness_min: float = 0.7,       # optional extra gate for GOOD if enforce_completeness=True
        min_rec_hits: Optional[int | float] = None,
        min_shared_hits: int = 0,
        enforce_completeness: bool = False,
    ) -> dict:
        """
        GOOD (efficient) tracks: purity ≥ purity_min (after clone removal).
        GHOSTS: purity < purity_min (among candidates, excluding clones).
        Per Instructions.pdf: "Good reconstructed tracks where at least 70% of the
        reconstructed hits are also present in the matched true track" (this is purity).
        """
        rec_best, truth_to_recs_pre, candidate_rec_ids = self.match_tracks(
            purity_min=purity_min,
            completeness_min=completeness_min,
            min_rec_hits=min_rec_hits,
            min_shared_hits=min_shared_hits,
            enforce_completeness=enforce_completeness,
        )

        # Clone removal: only primaries remain GOOD
        primary, clones = self._primary_reco_per_truth(truth_to_recs_pre, rec_best)

        # Counters
        N_true = len(self.truth_tracks)  # all generated truth tracks
        N_rec  = sum(1 for rid in self.rec_track_hits
                    if rec_best.get(rid, Match(None,0,0,0,0.0,0.0,False)).candidate)

        good_ids     = set(primary.values())
        clone_ids    = set(clones)

        # GHOSTS: purity < threshold (purity-based per Instructions.pdf), among candidates and not clones
        ghost_rec_ids = [
            rid for rid in rec_best
            if rec_best[rid].candidate
            and (rec_best[rid].purity < float(purity_min))
            and (rid not in clone_ids)
        ]

        N_rec_good  = len(good_ids)
        N_rec_clone = len(clone_ids)
        N_rec_ghost = len(ghost_rec_ids)

        # Averages over GOOD primaries
        if N_rec_good > 0:
            purity_avg = float(np.mean([rec_best[rid].purity for rid in good_ids]))
            comp_mean  = float(np.mean([rec_best[rid].completeness for rid in good_ids]))
            w = np.array([rec_best[rid].truth_hits for rid in good_ids], dtype=float)
            c = np.array([rec_best[rid].completeness for rid in good_ids], dtype=float)
            comp_weighted = float((c * w).sum() / w.sum()) if w.sum() > 0 else 0.0
        else:
            purity_avg = comp_mean = comp_weighted = 0.0

        # Performance per your definitions 
        eps_track_eff   = (N_rec_good / N_true) if N_true else 0.0
        eps_track_ghost = (N_rec_ghost / N_rec) if N_rec else 0.0

        # Classic truth-level reference 
        matched_truth_ids = set(primary.keys())
        total_reconstructible = len(self.reconstructible_truth_ids)
        recon_eff_truth_level = (
            len(matched_truth_ids & self.reconstructible_truth_ids) / total_reconstructible
            if total_reconstructible else 0.0
        )

        return {
            # Clean counters
            "n_true_tracks": N_true,
            "n_rec_tracks": N_rec,
            "n_rec_good": N_rec_good,
            "n_rec_ghost": N_rec_ghost,
            "n_rec_clone": N_rec_clone,

            # Performance 
            "track_efficiency_good_over_true": eps_track_eff,     # GOOD by completeness
            "track_ghost_rate_over_rec": eps_track_ghost,         # GHOST by completeness

            # Hit quality (GOOD primaries)
            "hit_purity_mean_primary": purity_avg,
            "hit_efficiency_mean_primary": comp_mean,
            "hit_efficiency_weighted_primary": comp_weighted,

            # IDs (optional)
            "good_primary_rec_ids": sorted(int(x) for x in good_ids),
            "ghost_rec_ids": sorted(int(x) for x in ghost_rec_ids),
            "clone_rec_ids": sorted(int(x) for x in clone_ids),

            # Legacy m_* (kept for plotting)
            "m_total_truth_tracks": N_true,
            "m_total_reconstructible_truth": total_reconstructible,
            "m_total_rec_candidates": N_rec,
            "m_reconstruction_efficiency": recon_eff_truth_level,
            "m_ghost_rate": eps_track_ghost,
            "m_clone_fraction_total": (N_rec_clone / N_rec) if N_rec else 0.0,
            "m_clone_fraction_among_matched": (N_rec_clone / (N_rec_good + N_rec_clone)) if (N_rec_good + N_rec_clone) else 0.0,
            "m_purity_all_matched": purity_avg,
            "m_purity_primary_only": purity_avg,
            "m_hit_efficiency_mean": comp_mean,
            "m_hit_efficiency_weighted": comp_weighted,
            "m_n_ghosts": N_rec_ghost,
            "m_n_clones": N_rec_clone,
            "m_n_matched_reco": N_rec_good + N_rec_clone,
            "m_n_matched_truth": len(matched_truth_ids),
        }


    # -------------------------------------------------------------------------
    # Pretty print
    # -------------------------------------------------------------------------
    def print_metrics(
        self,
        completeness_min: float = 0.7,          # GOOD and ghost threshold now completeness-based
        purity_min: float = 0.7,                # optional extra gate for GOOD if enforce_purity=True
        min_rec_hits: Optional[int | float] = None,
        min_shared_hits: int = 0,
    ) -> None:
        m = self.compute_metrics(
            purity_min=purity_min,
            completeness_min=completeness_min,
            min_rec_hits=min_rec_hits,
            min_shared_hits=min_shared_hits,
        )
        w = 92
        line = "=" * w
        print(line)
        print(" EVENT VALIDATION METRICS (standardized) ".center(w))
        print(line)

        def row(label: str, val):
            if isinstance(val, float):
                print(f"{label:<64}{val:>27.4f}")
            else:
                print(f"{label:<64}{str(val):>27}")

        # Sizes
        row("Truth tracks (all)", m["m_total_truth_tracks"])
        row("Truth tracks (reconstructible)", m["m_total_reconstructible_truth"])
        row("Reco tracks (candidates after reco-level gate)", m["m_total_rec_candidates"])

        # Efficiencies and rates
        print("-" * w)
        row("Reconstruction efficiency (truth-level)", m["m_reconstruction_efficiency"])
        row("Ghost rate (per candidate reco)", m["m_ghost_rate"])
        row("Clone fraction (per candidate reco)", m["m_clone_fraction_total"])
        row("Clone fraction (among matched reco)", m["m_clone_fraction_among_matched"])

        # Quality
        print("-" * w)
        row("Purity (all matched reco)", m["m_purity_all_matched"])
        row("Purity (primaries only)", m["m_purity_primary_only"])
        row("Hit efficiency / completeness (mean, primaries)", m["m_hit_efficiency_mean"])
        row("Hit efficiency / completeness (|T|-weighted, primaries)", m["m_hit_efficiency_weighted"])

        # Counts
        print("-" * w)
        row("Matched truths", m["m_n_matched_truth"])
        row("Matched recos", m["m_n_matched_reco"])
        row("Ghost recos", m["m_n_ghosts"])
        row("Clone recos", m["m_n_clones"])

        # Gate summary
        print("-" * w)
        gates = [f"completeness≥{completeness_min:.2f}"]
        if purity_min is not None and purity_min > 0:
            gates.append(f"purity≥{purity_min:.2f} (optional)")
        if min_rec_hits is None:
            gates.append(f"|R|≥ceil(0.7·max|T|_reconstructible) = {int(np.ceil(0.7 * self.max_hits_in_recon_truth))}")
        else:
            gates.append(f"|R|≥{int(np.ceil(min_rec_hits))}")
        if min_shared_hits > 0:
            gates.append(f"|R∩T|≥{min_shared_hits}")

        print("Gates applied: " + ", ".join(gates))
        print(line)

    # -------------------------------------------------------------------------
    # Tables (require pandas)
    # -------------------------------------------------------------------------
    def build_track_table(self, rec_best: Dict[int, Match]) -> "pd.DataFrame":
        """
        One row per *candidate* reco (after reco-level gate).

        Columns:
          rec_id, best_truth_id, accepted_truth_id, candidate, accepted,
          rec_hits, truth_hits, correct_hits, purity, completeness
        """
        if pd is None:
            raise RuntimeError("pandas is required for build_track_table()")
        rows = []
        for rid, m in rec_best.items():
            if not m.candidate:
                continue
            rows.append({
                "rec_id": int(rid),
                "best_truth_id": (int(m.best_truth_id) if m.best_truth_id is not None else np.nan),
                "accepted_truth_id": (int(m.truth_id) if m.truth_id is not None else np.nan),
                "candidate": bool(m.candidate),
                "accepted": bool(m.accepted),
                "rec_hits": int(m.rec_hits),
                "truth_hits": int(m.truth_hits),
                "correct_hits": int(m.correct_hits),
                "purity": float(m.purity),
                "completeness": float(m.completeness),
            })
        return pd.DataFrame(rows)

    def build_truth_table(self, truth_to_recs: Dict[int, List[int]], rec_best: Dict[int, Match]) -> "pd.DataFrame":
        """
        One row per truth track with primary info (if any).
        """
        if pd is None:
            raise RuntimeError("pandas is required for build_truth_table()")
        rows = []
        for tid, T in self.truth_tracks.items():
            recs = truth_to_recs.get(tid, [])
            primary_id = None
            if recs:
                recs_sorted = sorted(
                    recs, key=lambda r: (rec_best[r].correct_hits, rec_best[r].purity), reverse=True
                )
                primary_id = recs_sorted[0]
            rows.append({
                "truth_id": int(tid),
                "reconstructible": bool(tid in self.reconstructible_truth_ids),
                "truth_hits": int(len(T.hits)),
                "n_matched_reco": int(len(recs)),
                "primary_rec_id": (int(primary_id) if primary_id is not None else np.nan),
                "primary_completeness": (float(rec_best[primary_id].completeness) if primary_id is not None else np.nan),
                "primary_purity": (float(rec_best[primary_id].purity) if primary_id is not None else np.nan),
            })
        return pd.DataFrame(rows)

    # -------------------------------------------------------------------------
    # Fast retuning from per-track table (no re-matching needed)
    # -------------------------------------------------------------------------
    def recompute_from_track_table(
        self,
        track_df: pd.DataFrame,
        purity_min: float = 0.7,
        completeness_min: float = 0.7,
        min_shared_hits: int = 0,
    ) -> dict:
        """
        Recompute the full set of metrics for arbitrary thresholds *without*
        re-doing hit intersections. Requires build_track_table() output.
        """
        if pd is None:
            raise RuntimeError("pandas is required for recompute_from_track_table()")

        # Filter candidates
        cand = track_df[track_df["candidate"] == True].copy()  # noqa: E712

        # Acceptance by gates (applied to best association)
        mask = (cand["purity"] >= float(purity_min)) & (cand["correct_hits"] >= int(min_shared_hits))
        if completeness_min is not None:
            mask &= (cand["completeness"] >= float(completeness_min))
        acc = cand[mask].copy()

        # Truth -> recs among accepted (for clones/primaries)
        truth_to_recs: Dict[int, List[int]] = {}
        for tid, grp in acc.groupby("best_truth_id", dropna=True):
            if np.isnan(tid):
                continue
            truth_to_recs[int(tid)] = grp["rec_id"].astype(int).tolist()

        # Primary/clone split
        primary: Dict[int, int] = {}
        clones: List[int] = []
        for tid, rec_ids in truth_to_recs.items():
            if not rec_ids:
                continue
            rec_ids_sorted = sorted(
                rec_ids,
                key=lambda r: (int(cand.loc[cand.rec_id == r, "correct_hits"].values[0]),
                               float(cand.loc[cand.rec_id == r, "purity"].values[0])),
                reverse=True,
            )
            primary[tid] = rec_ids_sorted[0]
            clones.extend(rec_ids_sorted[1:])

        # Counts
        total_rec_candidates = int(len(cand))
        n_ghosts = int(total_rec_candidates - len(acc))
        total_reconstructible = int(len(self.reconstructible_truth_ids))
        matched_truth_ids = set(primary.keys()) & self.reconstructible_truth_ids

        # Metrics
        ghost_rate = (n_ghosts / total_rec_candidates) if total_rec_candidates else 0.0
        clone_fraction_total = (len(clones) / total_rec_candidates) if total_rec_candidates else 0.0
        clone_fraction_among_matched = (len(clones) / len(acc)) if len(acc) else 0.0
        recon_eff = (len(matched_truth_ids) / total_reconstructible) if total_reconstructible else 0.0

        # Purity/completeness of primaries
        prim_mask = cand.rec_id.isin(primary.values())
        purity_primary = float(cand.loc[prim_mask, "purity"].mean()) if prim_mask.any() else 0.0
        purity_all = float(acc["purity"].mean()) if len(acc) else 0.0
        comp_primary_mean = float(cand.loc[prim_mask, "completeness"].mean()) if prim_mask.any() else 0.0
        w = cand.loc[prim_mask, "truth_hits"].to_numpy(dtype=float)
        c = cand.loc[prim_mask, "completeness"].to_numpy(dtype=float)
        comp_primary_w = float((c * w).sum() / w.sum()) if w.sum() > 0 else 0.0

        return {
            "m_reconstruction_efficiency": recon_eff,
            "m_ghost_rate": ghost_rate,
            "m_clone_fraction_total": clone_fraction_total,
            "m_clone_fraction_among_matched": clone_fraction_among_matched,
            "m_purity_all_matched": purity_all,
            "m_purity_primary_only": purity_primary,
            "m_hit_efficiency_mean": comp_primary_mean,
            "m_hit_efficiency_weighted": comp_primary_w,
            "m_total_rec_candidates": total_rec_candidates,
            "m_n_ghosts": n_ghosts,
            "m_n_clones": len(clones),
            "m_n_matched_reco": len(acc),
            "m_n_matched_truth": len(matched_truth_ids),
        }

    # -------------------------------------------------------------------------
    # Optional: truth-length binning (useful diagnostics)
    # -------------------------------------------------------------------------
    def truth_length_bins(
        self,
        truth_to_recs: Dict[int, List[int]],
        bins: Tuple[int, ...] = (5, 8, 12, 16, 999),
    ) -> pd.DataFrame:
        """
        Return a table with efficiency vs truth length bins (helps validate min_rec_hits choice).
        """
        if pd is None:
            raise RuntimeError("pandas is required for truth_length_bins()")

        # Build bin edges
        edges = (0,) + bins
        def label_for(L: int) -> str:
            for a, b in zip(edges[:-1], edges[1:]):
                if a <= L < b:
                    return f"[{a},{b})"
            return f"[{edges[-1]},∞)"

        rows = []
        for tid, T in self.truth_tracks.items():
            L = len(T.hits)
            rows.append({
                "truth_id": int(tid),
                "truth_hits": int(L),
                "bin": label_for(L),
                "matched": int(tid in truth_to_recs),
                "reconstructible": int(tid in self.reconstructible_truth_ids),
            })
        return pd.DataFrame(rows)