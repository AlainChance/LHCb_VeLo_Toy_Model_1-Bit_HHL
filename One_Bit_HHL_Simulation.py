# 1-Bit HHL track simulation toy model

## MIT License

# MIT_License Copyright (c) 2026 Alain Chancé
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

"""
Fast particle track reconstruction in the LHCb VELO using classical angle sorting and Ising-like optimization.

# Useful links

## The Large Hadron Collider beauty (LHCb) experiment at CERN
* [The Large Hadron Collider beauty (LHCb) experiment](https://home.cern/science/experiments/lhcb)
* [LHCb Taking a closer look at LHC](https://www.lhc-closer.es/taking_a_closer_look_at_lhc/0.lhcb)

## Algorithms for Track Reconstruction
* [Alain Chancé, *A Toy Model for Reconstructing Particle Tracks at LHCb at CERN with Quantum Computing*, 30 Oct. 2025, LHCb_VeLo_Toy_Model_1-Bit_HHL.pdf](https://github.com/AlainChance/LHCb_VeLo_Toy_Model_1-Bit_HHL/blob/main/LHCb_VeLo_Toy_Model_1-Bit_HHL.pdf)
* [Xenofon Chiotopoulos, Davide Nicotra, George Scriven, Kurt Driessens, Marcel Merk, Jochen Schütz, Jacco de Vries, Mark H. M. Winands, *TrackHHL: The 1-Bit Quantum Filter for Particle Trajectory Reconstruction*, 12 Jan 2026, arXiv:2601.07766](https://doi.org/10.48550/arXiv.2601.07766)
* [Xenofon Chiotopoulos, *TrackHHL: A Quantum Computing Algorithm for Track Reconstruction at the LHCb*](https://indico.cern.ch/event/1338689/contributions/6010017/attachments/2951297/5188722/CHEP_ppt.pdf)
* Xenofon Chiotopoulos, Miriam Lucio Martinez, Davide Nicotra, Jacco A. de Vries, Kurt Driessens, Marcel Merk, and Mark H. M. Winands, *TrackHHL: A Quantum Computing Algorithm for Track Reconstruction at the LHCb*, EPJ Web of Conferences 337, 01181 (2025), [https://doi.org/10.1051/epjconf/202533701181](https://doi.org/10.1051/epjconf/202533701181)
* [D. Nicotra et al., *A Quantum Algorithm for Track Reconstruction in the LHCb Vertex Detector*, arXiv:2308.00619v2, 7 Oct 2023](https://arxiv.org/pdf/2308.00619)
* [Cámpora Pérez, D. H., Neufeld, N. & Riscos Núñez, A. Search by triplet: An efficient local track reconstruction algorithm
for parallel architectures. J. Comput. Sci. 54, 101422, DOI: 10.1016/j.jocs.2021.101422 (2021)](https://arxiv.org/pdf/2207.03936)

## Qiskit
* [Install Qiskit](https://quantum.cloud.ibm.com/docs/en/guides/install-qiskit#install-qiskit)
* [Introduction to Qiskit patterns](https://quantum.cloud.ibm.com/docs/en/guides/intro-to-patterns)

## Sample-based quantum diagonalization (SQD)
* [Alain Chancé, Demonstrating chemistry simulations with Sample-based Quantum Diagonalization (SQD)](https://github.com/AlainChance/SQD_Alain)
* [Sample-based quantum diagonalization (SQD) overview](https://quantum.cloud.ibm.com/docs/en/guides/qiskit-addons-sqd)
* [Qiskit addons team, Bounding the subspace dimension in Qiskit addon: sample-based quantum diagonalization (SQD)](https://qiskit.github.io/qiskit-addon-sqd/how_tos/choose_subspace_dimension.html)

## Energetics of quantum computing
* [informatique quantique état de l’art, perspective et défis, Olivier Ezratty, SFGP, Paris, 5 novembre 2025](https://www.oezratty.net/Files/Conferences/Olivier%20Ezratty%20Informatique%20Quantique%20SFGP%20Nov2025.pdf)

## Efficiency of quantum algorithms
* [Høyer, P.; Neerbek, J.; Shi, Y. (2001). *Quantum complexities of ordered searching, sorting, and element distinctness*. 28th International Colloquium on Automata, Languages, and Programming. Lecture Notes in Computer Science. Vol. 2076. pp. 62–73. arXiv:quant-ph/0102078. doi:10.1007/3-540-48224-5_29. ISBN 978-3-540-42287-7](https://arxiv.org/abs/quant-ph/0102078)

---

# The Large Hadron Collider beauty (LHCb) experiment at CERN
The LHCb Experiment at CERN is a general-purpose detector at the Large Hadron Collider (LHC) and specializes in investigating the slight differences between matter and antimatter by studying a type of particle called the "beauty quark", or "b quark".

It uses a series of subdetectors to detect mainly forward particles – those thrown forwards by the collision in one direction. The first subdetector is mounted close to the collision point, with the others following one behind the other over a length of 20 meters.
The 5600-tonne LHCb detector is made up of a forward spectrometer and planar detectors. It is 21 meters long, 10 meters high and 13 meters wide, and sits 100 meters below ground near the town of Ferney-Voltaire, France. 

As of 2024, more than 1600 members from 98 institutes in 22 countries, including 1100 authors.
Source: https://home.cern/science/experiments/lhcb 

---

# Particle track reconstruction in the LHCb Vertex Locator (VELO)
In the High Luminosity phase of the Large Hadron Collider (HL-LHC), thousands of particles are produced simultaneously. Particles leave energy hits in detector layers. Hits are reconstructed into particle tracks. Tracks reveal Primary Vertices (collision points). Tracks in the LHCb Vertex Locator (VELO) can be modeled as straight lines intersecting the z-axis because it is the sub-detector closest to the LHCb collision point and it contains a negligible magnetic field.

---

## Classical sort-by-angle theta particle track reconstruction
In the XY projection, these straight lines pass through the origin. As a result, energy hits are likely to have a constant phase in polar coordinates when projected onto the XY plane (see Section 3, *Search by triplet — Sort by φ*, in [ALGO-10](https://arxiv.org/pdf/2207.03936)).  

We have developed the following functions:
- `plot_hits_polar()`, which displays a plot in Radians of hits projected onto the XY plane. See for example [LHCb_VeLo_Toy_Model_1-Bit_HHL/8_particles/6_layers/Noiseless/Polar_Plot_8_p_6_l_noiseless.png](https://github.com/AlainChance/LHCb_VeLo_Toy_Model_1-Bit_HHL/blob/main/8_particles/6_layers/Noiseless/Polar_Plot_8_p_6_l_noiseless.png).
- `cluster_by_last_column()`, which clusters hits by the last-column polar angle `theta` of an array of hits.
- `create_tracks()`, which performs a second‑stage clustering step inside each θ‑cluster to declone tracks.
- `segment_intersects_z_axis()`, which checks whether a line intersects the z-axis and finds the corresponding primary vertex.  
- `find_tracks()`, which reconstructs tracks from these clusters and finds all primary vertices.

## Split clone tracks by direction
We have developed the function `split_clone_by_direction()` which splits a θ-cluster into physically distinct clone tracks by clustering the 3D direction vectors of consecutive hit segments. A θ-cluster groups hits with similar azimuthal angle φ. When multiple particles share nearly identical φ (common in dense VELO-like geometries), they may be merged into a single cluster. These "clone clusters" must be separated into individual tracks. The most stable discriminator between clone tracks is the *direction* of their local segments. For a true straight track, the direction vector between consecutive modules is nearly constant. Clone tracks, even if close in φ, exhibit distinct 3D directions.

### Efficient implementation
The function `find_tracks()` has successfully reconstructed toy events with several thousands of particles in less than a fraction of a second, as shown in the following Jupyter notebooks:
  - [1024_particles/7_layers/Find_tracks/HHL_1024_particles_7_layers_find_tracks.ipynb](https://github.com/AlainChance/LHCb_VeLo_Toy_Model_1-Bit_HHL/blob/main/1024_particles/7_layers/Find_tracks/HHL_1024_particles_7_layers_find_tracks.ipynb)
  - [2256_particles/8_layers/Find_tracks/HHL_2256_particles_8_layers_find_tracks.ipynb](https://github.com/AlainChance/LHCb_VeLo_Toy_Model_1-Bit_HHL/blob/main/2256_particles/8_layers/Find_tracks/HHL_2256_particles_8_layers_find_tracks.ipynb)
  - [5000_particles/7_layers/Find_tracks/HHL_5000_particles_7_layers_find_tracks.ipynb](https://github.com/AlainChance/LHCb_VeLo_Toy_Model_1-Bit_HHL/blob/main/5000_particles/7_layers/Find_tracks/HHL_5000_particles_7_layers_find_tracks.ipynb)

### Note on computational complexity
The computational bottleneck in the function `cluster_by_last_column()` is the comparison-based sorting step, for which both classical and bounded-error quantum query complexities are $O(n. log n)$; quantum algorithms do not reduce the asymptotic number of comparisons required.

Høyer, P.; Neerbek, J.; Shi, Y. (2001). "Quantum complexities of ordered searching, sorting, and element distinctness". 
28th International Colloquium on Automata, Languages, and Programming. Lecture Notes in Computer Science. 
Vol. 2076. pp. 62–73. [arXiv:quant-ph/0102078](https://arxiv.org/abs/quant-ph/0102078). doi:10.1007/3-540-48224-5_29. ISBN 978-3-540-42287-7.

---

## Ising-like optimization using matrix inversion
The Hamiltonian $𝐻(𝑆)$ is parametrized in terms of doublets $𝑆$, these doublets are possible connections between two hits in subsequent detector layers and take a binary value to indicate if they actively contribute to a track, $S_i$ ∈ {0, 1}. It includes three terms:

- The angular term $𝐻_{𝑎𝑛𝑔}$ is the most important as it determines if a set of doublets $𝑆_𝑖$ and $𝑆_𝑗$ are aligned within $\varepsilon$.
- $𝐻_{spec}(𝑆)$ makes the spectrum of $A$ positive.
- $𝐻_{gap}(𝑆)$ ensures gap in the solution spectrum.

Matrix inversion yields the solution of reconstructed tracks. The resulting vector $𝑆$ of real values is subsequently discretized to obtain an "on"/"off" status by setting a threshold $𝑇$.

---

## Efficient implementation of the Ising-like optimization

### Fast construction of the Hamiltonian $H(S)$
The function `construct_segments()` of the class `SimpleHamiltonian` in the module [toy_model/simple_hamiltonian.py](https://github.com/AlainChance/LHCb_VeLo_Toy_Model_1-Bit_HHL/blob/main/toy_model/simple_hamiltonian.py) is enhanced to identify segments with matching values of `theta` during their creation and to append them to the list `segment_in_indices`, along with their corresponding segment IDs in the list `segment_indices`. The function `construct_hamiltonian()` then considers only doublets $S_i$ and $S_j$ of segments in `segment_in_indices`. This modification significantly improves the performance of the preprocessing step.

### Smart error detection and recovery
The class `One_Bit_HHL` in the module
[One_Bit_HHL_Simulation.py](https://github.com/AlainChance/LHCb_VeLo_Toy_Model_1-Bit_HHL/blob/main/One_Bit_HHL_Simulation.py)
implements a post-processing step consistent with the IBM Qiskit pattern methodology (*Post-process results*):

*“This can involve a range of classical data-processing steps, such as … or post-selection based on inherent properties of the problem …”*

(see [Introduction to Qiskit patterns](https://quantum.cloud.ibm.com/docs/en/guides/intro-to-patterns)).

* The function `get_tracks_smart()` performs the following steps:

  * Identifies active segments in the first three layers from both the classical solution and the 1-bit HHL quantum solution.
  * Reconstructs tracks using only segments that intersect the z-axis.
  * Adds missed segments intersecting the z-axis and extends active segments to all outer layers.

* The function `segment_intersects_z_axis()` computes segment–axis intersections. The intersection points define the reconstructed primary vertices.

* The function `analyze_p_vertices()` clusters and summarizes primary-vertex candidates identified by `segment_intersects_z_axis()`. It groups vertices by z-value and returns averaged primary-vertex (PV) positions.

---

## Solving the system of linear equations classically
The function `classical_simulation()` of the class `One_Bit_HHL` in the module `One_Bit_HHL_Simulation.py` uses only the first three layers of the toy event created by the function `setup_events()` in the same module.

The system of linear equations $𝐴𝑆=𝑏$ is solved using [scipy.sparse.linalg.cg](https://docs.scipy.org/doc/scipy-1.12.0/reference/generated/scipy.sparse.linalg.cg.html):

```python
sol, _ = sci.sparse.linalg.cg(A, vector_b, atol=0)
```
The discretized solution is obtained by setting a threshold `T_classical` in the list of configuration parameters `param`:
```python
T_classical = param["T_classical"]
disc_sol = (sol > T_classical).astype(int)
```

---

## Solving the system of linear equations with the 1-Bit HHL algorithm
The Harrow–Hassidim–Lloyd (HHL) algorithm promises a complexity improvement over the best classical alternatives for solving sparse systems of linear equations. However, its practical implementation faces considerable challenges. The Quantum Phase Estimation (QPE) step results in prohibitively deep circuits, making the algorithm unfeasible on currently available hardware short of fault-tolerant quantum computing.

The 1-Bit HHL algorithm, presented in the paper [TrackHHL: A Quantum Computing Algorithm for Track Reconstruction at the LHCb](https://doi.org/10.1051/epjconf/202533701181), applies a first-order Suzuki–Trotter decomposition to approximate the time-evolution operator. By restricting the QPE accuracy to a single bit, the algorithm can efficiently determine whether a phase is close to zero or significantly different.

The function `HHL_simulation()` of the class `One_Bit_HHL` in the module `One_Bit_HHL_Simulation.py` uses only the first three layers of the toy event created by the function `setup_events()` in the same module.

The discretized solution is obtained by setting a threshold `T_hhl` in the list of configuration parameters `param`:
```python
T_hhl = param["T_hhl"]
disc_x_hhl = (x_hhl > T_hhl).astype(int)
```

---

# Installation

## Requirements
Be sure you have the following installed:

* Qiskit SDK v2.1 or later, with visualization support (`pip install 'qiskit[visualization]'`)
* 'qiskit-aer' library (`pip install qiskit-aer`)
* Qiskit runtime 0.40 or later (`pip install qiskit-ibm-runtime`)
* [eco2AI](https://github.com/sb-ai-lab/Eco2AI) is optional (`pip install eco2ai`)

## Clone the repository LHCb_VeLo_Toy_Model_1-Bit_HHL
`git clone https://github.com/AlainChance/LHCb_VeLo_Toy_Model_1-Bit_HHL`

---

# Set-up your own 1-Bit HHL track simulation toy model simulation
Duplicate the Jupyter notebook [HHL_1024_particles_7_layers_find_tracks.ipynb](https://github.com/AlainChance/LHCb_VeLo_Toy_Model_1-Bit_HHL/blob/main/1024_particles/7_layers/Find_tracks/HHL_1024_particles_7_layers_find_tracks.ipynb), rename it and customize the configuration parameters:
```python
config = {
    #--------------------
    # Simulation options
    #--------------------
    "dz": 20,                           # layer spacing (mm)
    "layers": 7,                        # Number of layers
    "n_particles": [256, 256, 256, 256],    # Number of particles
    "p_vertices": [(0,0,4), (0,0,6), (0,0,8), (0,0,10)],  # Primary vertices
    #------------------
    # Noise parameters
    #------------------
    "measurement_error": 0.0,           # HIT RESOLUTION (sigma on measurement) (sigma)
    "collision_noise": 1.0e-7,          # MULTIPLE SCATTERING (angular noise proxy)
    "ghost_rate": 1e-2,                 # Ghost (fake) track rate
    "drop_rate": 0.0,                   # Hit drop (inefficiency) rate
    #-----------------
    # Display options
    #-----------------
    "display_particles": False,         # Whether to display initial particle states
    "display_hits": False,              # Whether to display hits
    "display_ghost_hits": True,         # Whether to display ghost hits
    "display_tracks": False,            # Whether to display events and ghost tracks
    "display_clusters": False,          # Whether to display clusters found by find_tracks()
    "display_false_clusters": True,     # Whether to display clusters rejected by find_tracks()
    "display_clone_splitting": True,    # Whether to display clone splitting information
    "display_clustering": True,         # Whether to display clustering information
    "do_plot_tracks": False,            # Whether to plot events and ghost tracks 
    "do_spectrum": False,               # Whether to analyze the classical solution spectrum
    "do_print_counts": False,           # Whether to print raw measurement counts
    "resolution": 2000,                 # Resolution for plots of tracks - Increase for finer mesh
    "do_draw": False,                   # Whether to draw the HHL circuit
    #---------------------------------------
    # Classical diagonalisation run options
    #---------------------------------------
    "do_solve_scipy": False,            # Whether to solve classically using scipy.sparse.linalg.cg
    "T_classical": None,                # Threshold for discretizing classical solutions
    #----------------------------------
    # Classical find_tracks parameters
    #----------------------------------
    "tol": None,                        # Tolerance for floating point comparison
    "tol_clusters": None,               # Tolerance for cluster_by_last_column()
    "tol_clone": None,                  # Tolerance for decloning tracks
    "tol_intersects": None,             # Tolerance for segment_intersects_z_axis()
    #------------------------------------------
    # Files containing token (API key) and CRN
    #------------------------------------------
    "token_file": "Token.txt",          # Token file
    "CRN_file": "CRN.txt",              # CRN file
    #-------------------------------
    # Quantum computing run options
    #-------------------------------
    "T_hhl": None,                                      # Threshold for discretizing 1-Bit HHL solutions - None: to be computed
    "backend_name": "AerSimulator noiseless",           # AerSimulator noiseless or Fake QPU or real IBM cloud backend name
    "job_id": None,                                     # job_id of a previously run job
    "run_on_QPU": False,                                # Whether to run the quantum circuit on the target hardware
    "nshots": 2000000,                                  # Number of shots
    'opt_level': 1,                                     # Optimization level
    "poll_interval": 5,                                 # Poll interval in seconds for job monitor
    "timeout": 600,                                     # Time out in seconds for job monitor
    #-------------------------------------
    # eco2AI Tracker options
    # https://github.com/sb-ai-lab/Eco2AI
    #-------------------------------------
    "do_eco2ai": True,                                   # Whether to use the eco2AI Tracker
    "project_name": "One_Bit_HHL",                       # Project name
    "experiment_description": "HHL_1024_p_7_l_find_tracks", # Experiment description
    "eco2ai_file_name": "HHL_1024_p_7_l_find_tracks.csv",   # eco2AI file name
    #---------------------------------------------------------------------------------
    # Ballpark figure (kW) for the power consumption of the IBM cloud backend
    # "The power consumption of a quantum computer is about 15-25kW"
    # https://www.capgemini.com/insights/expert-perspectives/green-quantum-computing/
    #---------------------------------------------------------------------------------
    "power_QPU": 25,                    # Ballpark figure (kW) for the power consumption of the IBM cloud backend
}
```

---

# Credits
The Jupyter notebooks in this repository [LHCb_VeLo_Toy_Model_1-Bit_HHL](https://github.com/AlainChance/LHCb_VeLo_Toy_Model_1-Bit_HHL) and the Python file [One_Bit_HHL_Simulation.py](https://github.com/AlainChance/LHCb_VeLo_Toy_Model_1-Bit_HHL/blob/main/One_Bit_HHL_Simulation.py) are derived from the following sources:

* GitHub repository [OneBQF](https://github.com/Xenofon-Chiotopoulos/OneBQF/tree/main) owned by Xenofon Chiotopoulos and more specifically:
   - Module [OneBQF.py](https://github.com/Xenofon-Chiotopoulos/OneBQF/blob/main/quantum_algorithms/OneBQF.py)
   - Jupyter notebook [example.ipynb](https://github.com/Xenofon-Chiotopoulos/OneBQF/blob/main/example.ipynb).

* Jupyter notebook [George_Sandbox.ipynb](https://github.com/GeorgeWilliam1999/LHCb_VeLo_Toy_Model/blob/main/George_Sandbox.ipynb) owned by George William Scriven, [GeorgeWilliam1999](https://orcid.org/0009-0004-9997-1647).

* Relevant documentation can be found in the Jupyter notebook [Tracking Toy Model Demo](https://github.com/Xenofon-Chiotopoulos/Tracking_Toy_model/blob/main/example_notebook.ipynb) in the public repository [Tracking_Toy_model](https://github.com/Xenofon-Chiotopoulos/Tracking_Toy_model/tree/main) owned by Xenofon Chiotopoulos.

---

# Additions by Alain Chancé
## Energetics Analysis
* **Assumption:**
  A ballpark estimate for a typical modern IBM-class superconducting quantum computer (including cryogenics and supporting infrastructure, while idle or lightly used) is approximately **15–25 kW**.
  Source: [*Green Quantum Computing*, Capgemini, 8 May 2023](https://www.capgemini.com/insights/expert-perspectives/green-quantum-computing/).

* The `One_Bit_HHL` class integrates the [eco2AI](https://github.com/sb-ai-lab/Eco2AI) tracking feature, a python library which accumulates statistics about power consumption and CO2 emission during running code. The Eco2AI is licensed under a [Apache licence 2.0](https://www.apache.org/licenses/LICENSE-2.0).

---

## Class ToleranceEstimator
The class ToleranceEstimator provides unified statistical estimators for:
  - φ-clustering tolerance (tol_clusters_est)
  - clone-track splitting tolerance (tol_clone_est)

---

## Module One_Bit_HHL_Simulation.py
The module [One_Bit_HHL_Simulation.py](https://github.com/AlainChance/LHCb_VeLo_Toy_Model_1-Bit_HHL/blob/main/One_Bit_HHL_Simulation.py) defines a new class `One_Bit_HHL`.

### New data structures of the class One_Bit_HHL
The function `find_tracks()` of the class `One_Bit_HHL` in the module [One_Bit_HHL_Simulation.py](https://github.com/AlainChance/LHCb_VeLo_Toy_Model_1-Bit_HHL/blob/main/One_Bit_HHL_Simulation.py) creates the following data structures and stores them in the parameter list `self.param`:

  - `hit_by_index`: dictionary keyed by the index of the `hit`. Indices are always unique, even when `hit_id` is not.
  - `array_hits`: NumPy array of hits with `theta` as last column.

```python
hit_by_index = {i: hit for i, hit in enumerate(list_hits)}
param["hit_by_index"] = hit_by_index
```

```python
array_hits = np.array([ [i, hit.hit_id, hit.x, hit.y, hit.z, hit.module_id, hit.theta] for i, hit in enumerate(list_hits) ], dtype=float)
param["array_hits"] = array_hits
```

The function `setup_Hamiltonian()` of the class `One_Bit_HHL` stores in the parameter list the following lists returned by the function `construct segments()` in the module `simple_hamiltonian.py`:

```python
    ham.construct_segments(event=event_tracks)

    param["segment_indices"] = ham.segment_indices
    param["segment_in_indices"] = ham.segment_in_indices
```

### New properties of the class SimpleHamiltonian
The module [simple_hamiltonian.py](https://github.com/AlainChance/LHCb_VeLo_Toy_Model_1-Bit_HHL/blob/main/toy_model/simple_hamiltonian.py) is derived from the module [OneBQF/toy_model/simple_hamiltonian.py](https://github.com/Xenofon-Chiotopoulos/OneBQF/blob/main/toy_model/simple_hamiltonian.py).

The following properties have been added:
  - `segment_in_indices`: list of segments with matching values of `theta`
  - `segment_indices`: list of corresponding segment ID's

```python
    self.segment_indices = [segment.segment_id for segment in self.segment_in_indices]
```

### Updated data classes in the module state_event_model.py
The module [state_event_model.py](https://github.com/AlainChance/LHCb_VeLo_Toy_Model_1-Bit_HHL/blob/main/toy_model/state_event_model.py) is derived from the module [OneBQF/toy_model/state_event_model.py](https://github.com/Xenofon-Chiotopoulos/OneBQF/blob/main/toy_model/[state_event_model.py).

The following import statements have been added or updated:
```python
from dataclasses import dataclass, field
import math
```

In the data class `Hit`, the following two fields have been added:
  - `theta` stores the phase of a hit in polar coordinates when projected onto the XY plane
  - `index`: stores the index of the hit in an array of hits


```python
theta: float = field(init=False)  # Phase in polar coordinates when projected onto the XY plane
index: int = field(init=False)    # Index of the hit in an array of hits

def __post_init__(self): 
    self.theta = math.atan2(self.y, self.x)
    self.index = 0
```

In the data class `Segment`, new fields `module_id`, `track_id` and `theta` have been added:
```python
module_id: int = field(init=False)  # Module id of the hit in the outer module
track_id: int = field(init=False)   # Track id of the hit in the outer module
theta: float = field(init=False)    # Phase in polar coordinates when projected onto the XY plane

def __post_init__(self):
    self.module_id = self.hits[1].module_id
    self.track_id = self.hits[1].track_id
    self.theta = math.atan2(self.hits[1].y - self.hits[0].y, self.hits[1].x - self.hits[0].x)

def p0(self):
    return [self.hits[0].x, self.hits[0].y, self.hits[0].z]

def p1(self):
    return [self.hits[1].x, self.hits[1].y, self.hits[1].z]
```

## New functions of the class One_Bit_HHL in the module One_Bit_HHL_Simulation.py
The following functions are copied from the class SQD in [SQD_Alain.py](https://github.com/AlainChance/SQD_Alain/blob/main/SQD_Alain.py):
  - setup_backend()
  - check_size()
  - get_QPU_usage()
  - get_classical_power_usage()

The following function is derived from the module [OneBQF/toy_model/simple_hamiltonian.py](https://github.com/Xenofon-Chiotopoulos/OneBQF/blob/main/toy_model/simple_hamiltonian.py):
- find_segments() derived from function find_segments()

New functions:
  - analyze_p_vertices()
  - check_intersection()
  - classical_simulation()
  - cluster_by_last_column()
  - create_tracks()
  - display_all_clusters()
  - display_all_hits()
  - display_all_tracks()
  - display_p_vertices()
  - find_tracks()
  - gen_indices()
  - get_tracks_smart()
  - HHL_simulation()
  - intersects_origin()
  - intersects_z_axis()
  - plot_event()
  - plot_hits_polar()
  - setup_Hamiltonian()
  - run_qc()
  - run_simulation()
  - segment_intersects_z_axis()

"""

# Import common packages first
import psutil
import sys
import os
import time
import pandas as pd

import warnings

from copy import deepcopy

import numpy as np

from collections import defaultdict

import matplotlib.pyplot as plt

import scipy as sci
import scipy.sparse as ss

#------------------------------------------------------------------------------------------------------------------------
# Import qiskit.aer
# Additional circuit methods. On import, Aer adds several simulation-specific methods to QuantumCircuit for convenience. 
# These methods are not available until Aer is imported (import qiskit_aer). 
# https://qiskit.github.io/qiskit-aer/apidocs/circuit.html
#------------------------------------------------------------------------------------------------------------------------
import qiskit_aer

#---------------------
# Import AerSimulator
#---------------------
from qiskit_aer import AerSimulator

# Import Qiskit ecosystems
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler
from qiskit_ibm_runtime import SamplerOptions

# Import Qiskit libraries
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.circuit.library import PhaseGate

#-------------------------------------
# Import Fake provider for backend V2
#-------------------------------------
# from qiskit_ibm_runtime import fake_provider
# https://quantum.cloud.ibm.com/docs/en/api/qiskit-ibm-runtime/fake-provider-fake-provider-for-backend-v2
# https://github.com/Qiskit/qiskit-ibm-runtime/blob/stable/0.40/qiskit_ibm_runtime/fake_provider/fake_provider.py
from qiskit_ibm_runtime.fake_provider import FakeProviderForBackendV2
from qiskit_ibm_runtime.fake_provider import FakeTorino

#-----------------------------------------------------------------------
# Import from Qiskit Aer noise module (kept for optional fake backends)
#-----------------------------------------------------------------------
from qiskit_aer.noise import (
    NoiseModel,
    QuantumError,
    ReadoutError,
    depolarizing_error,
    pauli_error,
    thermal_relaxation_error,
)

#---------------------------
# Import StatevectorSampler
#---------------------------
from qiskit.primitives import StatevectorSampler

# Import qiskit classes
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager

from toy_model.state_event_generator import *
from toy_model import state_event_model
from toy_model.simple_hamiltonian import SimpleHamiltonian
from toy_model.simple_hamiltonian import get_tracks
from toy_model.toy_validator import EventValidator as evl
from toy_model.state_event_model import module, Event

# HHL algorithm
from OneBQF import OneBQF as onebqf

warnings.filterwarnings("ignore")

#-----------------------------------------------------------------------------------------
# If the code is running in an IPython terminal, then from IPython.display import display
# else if it is running in a plain Python shell or script: 
# we assign display = print and array_to_latex = identity
#-----------------------------------------------------------------------------------------
try:
    shell = get_ipython().__class__.__name__
except NameError:
    shell = None

if shell == 'TerminalInteractiveShell':
    # The code is running in an IPython terminal
    from IPython.display import display
    
elif shell == None:
    # The code is running in a plain Python shell or script: 
    # we assign display = print and array_to_latex = identity
    display = print
    array_to_latex = lambda x: x

#--------------------------------------------------------
# Print version of Qiskit, Qiskit Aer and Qiskit runtime
#--------------------------------------------------------
import qiskit
print(f"Qiskit version: {qiskit.__version__}")

import qiskit_aer
print(f"Qiskit Aer version: {qiskit_aer.__version__}")

import qiskit_ibm_runtime
print(f"Qiskit runtime version: {qiskit_ibm_runtime.__version__}")

#----------------------------------------------------------------------------------------
# Define the class ToleranceEstimator which provides unified statistical estimators for:
#   - φ-clustering tolerance (tol_clusters_est)
#   - clone-track splitting tolerance (tol_clone_est)
# Author: Alain Chancé
#----------------------------------------------------------------------------------------
class ToleranceEstimator:
    """
    Unified statistical estimators for:
      - φ-clustering tolerance (tol_clusters_est)
      - clone-track splitting tolerance (tol_clone_est)
    """

    #--------------------------------------------------------
    # Define the function estimate_intra_cluster_theta_std()
    #--------------------------------------------------------
    @staticmethod
    def estimate_intra_cluster_theta_std(clusters, layers, 
                                         n_sample_clusters=5,
                                         alpha=1.5,
                                         tol_min=1e-4,
                                         tol_max=1e-2):
        """
        Estimate tol_clusters_est from intra-cluster θ spread.
        """
        if len(clusters) == 0:
            return None

        sample_indices = np.random.choice(
            len(clusters),
            size=min(n_sample_clusters, len(clusters)),
            replace=False
        )

        intra_stds = []

        for ci in sample_indices:
            c = clusters[ci]
            if len(c) < 2:
                continue

            theta_vals = c[:, 6]

            if len(theta_vals) > layers:
                theta_vals = theta_vals[:layers]

            intra_stds.append(np.std(theta_vals))

        if not intra_stds:
            return None

        mean_std = np.mean(intra_stds)
        tol = max(alpha * mean_std, tol_min)
        tol = min(tol, tol_max)

        return tol, mean_std

    #------------------------------------------------
    # Define the function estimate_clone_tolerance()
    #------------------------------------------------
    @staticmethod
    def estimate_clone_tolerance(track_hits,
                                 alpha=1.0,
                                 tol_min=1e-6,
                                 tol_max=1e-2,
                                 alpha_dyn=True):

        if len(track_hits) < 2:
            return tol_min, 0.0

        temp_segments = []
        for i in range(len(track_hits) - 1):
            # Only build a segment if module_id increases
            if track_hits[i+1].module_id > track_hits[i].module_id:
                s = Segment(
                    hits=[track_hits[i], track_hits[i+1]],
                    segment_id=i
                )
                temp_segments.append(s)

        if not temp_segments:
            return tol_min, 0.0

        theta_seg_values = np.array([s.theta for s in temp_segments], dtype=float)
        theta_seg_std = np.std(theta_seg_values)

        #-------------------------------------------------------------------------------
        # The scale factor alpha determines how many sigmas define a decloning boundary
        # Adapt alpha dynamically
        #-------------------------------------------------------------------------------
        if alpha_dyn:
            if theta_seg_std < 1.0e-6:
                alpha = 1.0
            elif theta_seg_std > 1.0e-3:
                alpha = 1.5
            else:
                alpha = 1.2

        tol_clone_est = max(alpha * theta_seg_std, tol_min)
        tol_clone_est = min(tol_clone_est, tol_max)

        return tol_clone_est, theta_seg_std
#---------------------------------------------------------------------------------------


#------------------------------
# Define the class One_Bit_HHL
# Author: Alain Chancé
#------------------------------
class One_Bit_HHL:
    def __init__(self,
                 #--------------------
                 # Simulation options
                 #--------------------
                 dz = 20,                           # layer spacing (mm)
                 layers = 3,                        # Number of layers
                 n_particles = [32],                # Number of particles
                 p_vertices = [(0,0,10)],           # Primary vertices
                 do_draw = False,                   # Whether to draw the HHL circuit
                 #------------------
                 # Noise parameters
                 #------------------
                 measurement_error = 0.0,           # HIT RESOLUTION (sigma on measurement) (sigma)
                 collision_noise = 0.0,             # MULTIPLE SCATTERING (angular noise proxy)
                 ghost_rate = 1e-2,                 # ghost (fake) track rate
                 drop_rate = 0.0,                   # hit drop (inefficiency) rate
                 #-----------------
                 # Display options
                 #-----------------
                 display_particles = True,          # Whether to display initial particle states
                 display_hits = False,              # Whether to display hits
                 display_ghost_hits = False,        # Whether to display ghost hits
                 display_tracks = True,             # Whether to display events and ghost tracks
                 display_clusters = False,          # Whether to display clusters found by find_tracks()
                 display_false_clusters = False,    # Whether to display false clusters found by find_tracks()
                 display_clone_splitting = False,   # Whether to display clone splitting information
                 display_clustering = False,        # Whether to display clustering information
                 do_plot_tracks = True,             # Whether to plot events and ghost tracks
                 do_plot_heat_map = False,          # Whether to plot the heat map
                 do_spectrum = False,               # Whether to analyze the classical solution spectrum
                 do_print_counts = False,           # Whether to print raw measurement counts
                 do_print_outer_segs = False,       # Whether to print segments in modules greater than 3       
                 resolution = 25,                   # Resolution for plots of tracks - Increase for finer mesh
                 #----------------------------------
                 # Classical find_tracks parameters
                 #----------------------------------
                 tol = 1.0e-7,                      # Tolerance for floating point comparison
                 tol_clusters = None,               # Minimum value of the tolerance for clustering, cluster_by_last_column()
                 tol_clone = None,                  # Minimum value of the decloning tolerance
                 tol_intersects = None,             # Tolerance for segment_intersects_z_axis()
                 #----------------------------------------------------------------------------------------------------------
                 # A simulated primary vertex is defined as reconstructed if a primary vertex is found within 2 mm
                 # of its true position. See Primary Vertex Reconstruction Efficiency and Resolution in [ALGO-2]
                 # [Aaij, R., Adinolfi, M., Aiola, S. et al. A Comparison of CPU and GPU Implementations for the LHCb 
                 # Experiment Run 3 Trigger. Comput Softw Big Sci 6, 1 (2022)](https://doi.org/10.1007/s41781-021-00070-2)
                 #-----------------------------------------------------------------------------------------------------------
                 tol_vertices = 1.0,                # Tolerance for clustering primary vertices (mm)
                 #---------------------------------------
                 # Classical diagonalisation run options
                 #---------------------------------------
                 do_solve_scipy = True,             # Whether to solve classically using scipy.sparse.linalg.cg
                 T_classical = 0.45,                # Threshold for discretizing classical solutions
                 #------------------------------------------
                 # Files containing token (API key) and CRN
                 #------------------------------------------
                 token_file = "Token.txt",           # Token file
                 CRN_file = "CRN.txt",               # CRN file
                 #-------------------------------
                 # Quantum computing run options
                 #-------------------------------
                 T_hhl = None,                      # Threshold for discretizing 1-Bit HHL solutions - None: to be computed
                 backend_name = None,                # IBM cloud backend name
                 job_id = None,                      # job_id of a previously run job
                 run_on_QPU = True,                  # Whether to run the quantum circuit on the target hardware
                 nshots = 5000,                      # Number of shots
                 opt_level = 3,                      # Optimization level
                 poll_interval = 5,                  # Poll interval in seconds for job monitor
                 timeout = 600,                      # Time out for job monitor
                 #-------------------------------------
                 # eco2AI Tracker options
                 # https://github.com/sb-ai-lab/Eco2AI
                 #-------------------------------------
                 do_eco2ai = False,                                # Whether to use the eco2AI Tracker
                 project_name = "One_Bit_HHL",                     # Project name
                 experiment_description = "HHL",                   # Experiment description
                 eco2ai_file_name = "HHL.csv",                     # eco2AI file name
                 #---------------------------------------------------------------------------------
                 # Ballpark figure (kW) for the power consumption of the IBM cloud backend
                 # "The power consumption of a quantum computer is about 15-25kW"
                 # https://www.capgemini.com/insights/expert-perspectives/green-quantum-computing/
                 #---------------------------------------------------------------------------------
                 power_QPU = 25,                                   # Ballpark figure (kW) for the power consumption of the IBM cloud backend
                ):

        # Initialize self.backend and self.pm to None
        self.backend = None
        self.pm = None

        #--------------------------
        # Print simulation options
        #--------------------------
        text = f" Simulation options"
        line = "-" * (len(text) + 1)
        print(f"\n{line}\n{text}\n{line}")
        
        print("layer spacing (mm), dz:", dz)
        print("layers:", layers)
        print(f"n_particles: {n_particles}, Total number: {sum(n_particles)}")
        print("primary_vertices:", p_vertices)
        
        #-----------------------
        # Print display options
        #-----------------------
        text = f" Display options"
        line = "-" * (len(text) + 1)
        print(f"\n{line}\n{text}\n{line}")
        
        print("do_draw:", do_draw)
        print("display_particles:", display_particles)        # Whether to display initial particle states
        print("display_hits:", display_hits)                  # Whether to display hits
        print("display_ghost_hits:", display_ghost_hits)      # Whether to display ghost hits
        print("display_tracks:", display_tracks)              # Whether to display tracks
        print("display_clusters:", display_clusters)          # Whether to display clusters found by find_tracks()
        print("display_false_clusters:", display_false_clusters)    # Whether to display false clusters found by find_tracks()
        print("display_clone_splitting:", display_clone_splitting)  # Whether to display clone splitting information
        print("display_clustering:", display_clustering)      # Whether to display clustering information
        print("do_plot_tracks:", do_plot_tracks)              # Whether to plot events and ghost tracks
        print("do_plot_heat_map:", do_plot_heat_map)          # Whether to plot the heat map
        print("do_spectrum:", do_spectrum)
        print("do_print_counts:", do_print_counts)
        print("do_print_outer_segs", do_print_outer_segs)     # Whether to print segments in modules greater than 3
        print("resolution:", resolution)

        #------------------------
        # Print noise parameters
        #------------------------
        text = f" Noise parameters"
        line = "-" * (len(text) + 1)
        print(f"\n{line}\n{text}\n{line}")

        print("measurement hit resolution:", measurement_error)
        print("ghost (fake) track rate:", ghost_rate)
        print("hit drop (inefficiency) rate:", drop_rate)

        #----------------------------------------
        # Print classical find_tracks parameters
        #----------------------------------------
        #--------------------------------------------------------------------------------------
        # Anchoring clustering and clone splitting tolerances to the parameter collision noise 
        #--------------------------------------------------------------------------------------
        if collision_noise is None:
            collision_noise = 0.0
            
        if tol is None:
            tol = 1.0e-7

        if tol_clusters is None:
            tol_clusters = max(10.0 * collision_noise, tol)

        if tol_clone is None:
            tol_clone = max(3.0 * collision_noise, tol)
            
        if tol_intersects is None:
            tol_intersects = min(max(1.0e4 * collision_noise, tol), 2.0)

        text = f" Anchoring clustering and clone splitting tolerances of the classical function find_tracks() to the parameter collision noise"
        line = "-" * (len(text) + 1)
        print(f"\n{line}\n{text}\n{line}")
        
        print(f"Multiple scattering collision noise, collision_noise: {collision_noise:.2e}")
        print(f"Tolerance for floating point comparison, tol: {tol:.2e}")
        print(f"Minimum value of the tolerance for clustering, cluster_by_last_column(), tol_clusters: {tol_clusters:.2e}")
        print(f"Minimum value of the decloning tolerance, tol_clone: {tol_clone:.2e}")
        print(f"Tolerance for segment_intersects_z_axis(), tol_intersects: {tol_intersects:.2e}")

        #---------------------------------------------------------------------------------------------------
        # The tolerance for clustering vertices is set to 1 mm with the aim of finding every primary vertex 
        # within 2 mm of its true position.
        #----------------------------------------------------------------------------------------------------
        if tol_vertices is None:
            tol_vertices = 1.0    # 1 mm

        print(f"Tolerance for clustering vertices, tol_vertices: {tol_vertices:.2e}")

        #---------------------------------------------
        # Print classical diagonalisation run options
        #---------------------------------------------
        text = " Classical diagonalisation run options"
        line = "-" * (len(text) + 1)
        print(f"\n{line}\n{text}\n{line}")
        
        print("do_solve_scipy:", do_solve_scipy)              # Whether to solve classically using scipy.sparse.linalg.cg
        print("T_classical:", T_classical)                    # Threshold for discretizing classical solutions
        
        #-------------------------------------
        # Print Quantum computing run options
        #-------------------------------------
        text = " Quantum computing run options"
        line = "-" * (len(text) + 1)
        print(f"\n{line}\n{text}\n{line}")

        print("T_hhl:", T_hhl)                                # Threshold for discretizing 1-Bit HHL solutions
        
        print("Backend name:", backend_name)
        
        if job_id is not None:
            print("job_id:", job_id)
        
        print("Run on QPU:", run_on_QPU)

        if run_on_QPU:
            print("Number of shots:", nshots)
        
        print("Optimization level:", opt_level)

        #-------------------------------------
        # Print eco2AI Tracker options
        # https://github.com/sb-ai-lab/Eco2AI
        #-------------------------------------
        text = " eco2AI Tracker options"
        line = "-" * (len(text) + 1)
        print(f"\n{line}\n{text}\n{line}")
        
        if do_eco2ai:
            print("project_name:", project_name)
            print("experiment_description:", experiment_description)
            print("eco2ai_file_name:", eco2ai_file_name)
            
        #---------------------------------------------------------------------------------
        # Print Ballpark figure (kW) for the power consumption of the IBM cloud backend
        # "The power consumption of a quantum computer is about 15-25kW"
        # https://www.capgemini.com/insights/expert-perspectives/green-quantum-computing/
        #---------------------------------------------------------------------------------
        power_QPU = min(max(15.0, power_QPU), 25.0)
        print("\nBallpark figure (kW) for QPU power consumption:", power_QPU)

        #-------------------------
        # Set up param dictionary
        #-------------------------
        self.param = {
            #--------------------
            # Simulation options
            #--------------------
            "dz": dz,                                        # Distance between detector layers (mm)
            "layers": layers,                                # Number of detection layers
            "n_particles": n_particles,                      # Number of particles
            "p_vertices": p_vertices,                        # Primary vertices
            "do_draw": do_draw,                              # Whether to draw the HHL circuit
            "num_time_qubits": 1,                            # Number of time qubits set to one
            #------------------
            # Noise parameters
            #------------------
            "measurement_error": measurement_error,          # HIT RESOLUTION (sigma on measurement) (sigma)
            "collision_noise": collision_noise,              # MULTIPLE SCATTERING (angular noise proxy)
            "ghost_rate": ghost_rate,                        # ghost (fake) track rate
            "drop_rate": drop_rate,                          # hit drop (inefficiency) rate
            #-----------------
            # Display options
            #-----------------
            "display_particles": display_particles,          # Whether to display initial particle states
            "display_hits": display_hits,                    # Whether to display hits
            "display_ghost_hits": display_ghost_hits,        # Whether to display ghost hits
            "display_tracks": display_tracks,                # Whether to display events and ghost tracks
            "display_clusters": display_clusters,            # Whether to display clusters found by find_tracks()
            "display_false_clusters": display_false_clusters,    # Whether to display false clusters found by find_tracks()
            "display_false_clusters": display_false_clusters,    # Whether to display false clusters found by find_tracks()
            "display_clone_splitting": display_clone_splitting,  # Whether to display clone splitting information
            "display_clustering": display_clustering,        # Whether to display clustering information
            "do_plot_tracks": do_plot_tracks,                # Whether to plot events and ghost tracks
            "do_plot_heat_map": do_plot_heat_map,            # Whether to plot the heat map
            "do_spectrum": do_spectrum,                      # Whether to analyze the classical solution spectrum
            "do_print_counts": do_print_counts,              # Whether to print raw measurement counts
            "do_print_outer_segs": do_print_outer_segs,      # Whether to print segments in modules greater than 3
            "resolution": resolution,                        # Resolution for plots of tracks - Increase for finer mesh
            #----------------------------------
            # Classical find_tracks parameters
            #----------------------------------
            "tol": tol,                                      # Tolerance for floating point comparison
            "tol_clusters": tol_clusters,                    # Minimum value of the tolerance for clustering, cluster_by_last_column()
            "tol_clone": tol_clone,                          # Minimum value of the decloning tolerance
            "tol_intersects": tol_intersects,                # Tolerance for segment_intersects_z_axis()
            #----------------------------------------------------------------------------------------------------------
            # A simulated primary vertex is defined as reconstructed if a primary vertex is found within 2 mm
            # of its true position. See Primary Vertex Reconstruction Efficiency and Resolution in [ALGO-2]
            # [Aaij, R., Adinolfi, M., Aiola, S. et al. A Comparison of CPU and GPU Implementations for the LHCb 
            # Experiment Run 3 Trigger. Comput Softw Big Sci 6, 1 (2022)](https://doi.org/10.1007/s41781-021-00070-2)
            #-----------------------------------------------------------------------------------------------------------
            "tol_vertices": tol_vertices,                    # Tolerance for clustering vertices
            #---------------------------------------
            # Classical diagonalisation run options
            #---------------------------------------
            "do_solve_scipy": do_solve_scipy if isinstance(do_solve_scipy, bool) else True, # Whether to use scipy.sparse.linalg.cg
            "T_classical": T_classical if T_classical is not None else 0.45,  # Threshold for discretizing classical solutions
            #------------------------------------------
            # Files containing token (API key) and CRN
            #------------------------------------------
            "token_file": token_file,                        # Token file
            "CRN_file": CRN_file,                            # CRN file
            #-------------------------------
            # Quantum computing run options
            #-------------------------------
            "T_hhl": T_hhl,                                  # Threshold for discretizing 1-Bit HHL solutions
            "backend_name": backend_name,                    # IBM cloud backend name
            "job_id": job_id,                                # job_id
            "run_on_QPU": run_on_QPU if isinstance(run_on_QPU, bool) else True, # Whether to run HHL_simulation()
            "nshots": nshots,                                # Number of shots
            "opt_level":opt_level,                           # Optimization level
            "poll_interval": poll_interval,                  # Poll interval in seconds for job monitor
            "timeout": timeout,                              # Time out in seconds for gob monitor
            #-------------------------------------
            # eco2AI Tracker options
            # https://github.com/sb-ai-lab/Eco2AI
            #-------------------------------------
            "do_eco2ai": do_eco2ai,                           # Whether to use the eco2AI Tracker
            "project_name": project_name,                     # Project name
            "experiment_description": experiment_description, # Experiment description
            "eco2ai_file_name": eco2ai_file_name,             # File name
            #---------------------------------------------------------------------------------
            # Ballpark figure (kW) for the power consumption of the IBM cloud backend
            # "The power consumption of a quantum computer is about 15-25kW"
            # https://www.capgemini.com/insights/expert-perspectives/green-quantum-computing/
            #---------------------------------------------------------------------------------
            "power_QPU": power_QPU,                           # Ballpark figure (kW) for the power consumption of the IBM cloud backend
            #------------------
            # Shared variables
            #------------------
            "job": None,                                     # job = service.job(job_id) if job_is provided
            "n_qubits": 2,                                   # Number of qubits in the HHL circuit, set by function run_HHL()
            "init_particles": [],                            # List of initial particle state dictionaries for each event based on the primary vertices
            "event_tracks": [],                              # Full event created by setup_events() of class Event (state_event_model.py)
            "false_tracks": [],                              # Event with ghost hits
            "true_hits": [],                                 # List of true hits computed by the function generate_complete_events()
            "ghost_hits": [],                                # List of ghost hits computed by the function make_noisy_event()
            "hits":[],                                       # List of all true and ghost hits computed by the function make_noisy_event()
            #----------- Data maintained by the function find_tracks() ---------------------------------------------
            "hit_by_index": {},                              # Dictionary keyed by the index of the hit
            "array_hits": None,                              # NumPy array of hits with theta as last column
            "ghost_clusters": [],                            # list of ghost clusters
            "false_clusters": [],                            # List of false clusters
            "false_tracks": [],                              # List of false tracks that do not intersect the z-axis
            "found_clusters": [],                            # List of clusters
            "found_tracks": [],                              # List of tracks
            "found_segments": [],                            # List of segments
            "found_ghost_hits": [],                          # List of ghost hits
            "found_p_vertices": [],                          # List of primary vertices
            "found_event": None,                             # Reconstructed event
            #---------------------------------------------------------------------------------------------------------
            "modules": [],                                   # List of modules
            "rec_event": None,                               # Reconstructed event from discretized classical solution
            "hhl_rec_event": None,                           # Reconstructed event from discretized HHL solution
            "ham": None,                                     # Hamiltonian operator
            "segment_indices": [],                           # List of segment indices computed by the modified function construct_segments()
            "segment_in_indices": [],                        # List of segment with an id in segment_indices
            "A": None,                                       # Hamiltonian matrix       
            "circuit": None,                                 # HHL Quantum circuit returned by function HHL_simulation()
            "detector_geometry": None,                       # Geometry of the detector
            "counts": None,                                  # Raw measurement counts set by function HHL_simulation()
            "correct_indices": None,                         # Correct indices set by function classical_simulation()
            "hhl_correct_indices": None,                     # HHL correct indices set by function HHL_simulation
            #---------------------------------------------------------------------------------------------------------
            "QPU_usage": None,                               # Qiskit Runtime usage in seconds returned by function get_QPU_usage
            "QPU_power_consumption": None,                   # QPU power consumption returned by function get_QPU_usage
            "eco2ai_tracker": None,                          # eco2AI tracker
            "duration": None,                                # Duration of classical processing returned by get_classical_power_usage
            "classical_power_usage": None,                   # Classical power usage returned by get_classical_power_usage
            "__init__ failed": False                         # Boolean set to True by __init__ if it encountered a problem
        }
            
        #--------------------------------------------------------
        # If do_eco2ai is True, try importing the eco2AI library
        #--------------------------------------------------------
        if do_eco2ai:
            try:
                import eco2ai
            except Exception as e:
                print(f"Error importing the eco2AI library: {e}")
                print(f"Install eco2AI with the command 'pip install eco2ai'")
                do_eco2ai = False
                self.param['do_eco2ai'] = False

        #-----------------------------------------
        # Start an instance of the eco2AI Tracker
        # https://github.com/sb-ai-lab/Eco2AI
        #-----------------------------------------
        if do_eco2ai:

            # Delete eco2ai_file_name to reset duration counter
            if os.path.isfile(eco2ai_file_name): 
                try: 
                    os.remove(eco2ai_file_name) 
                    print(f"\nDeleted: {eco2ai_file_name}") 
                except Exception as e: 
                    print(f"\nError deleting file: {e}")
            
            tracker = eco2ai.Tracker(
                project_name = project_name, 
                experiment_description = experiment_description,
                file_name = eco2ai_file_name
            )
            self.param['eco2ai_tracker'] = tracker

            tracker.start()
            print(f"eco2AI tracker started")

        #---------------------------------------------------
        # Get Qiskit Runtime account credentials from files
        # Author: Alain Chancé 
        #---------------------------------------------------
        token_file = self.param['token_file']
        CRN_file = self.param['CRN_file']
        
        if os.path.isfile(token_file):
            f = open(token_file, "r") 
            token = f.read() # Read token from token_file
            print("Token read from file: ", token_file)
            f.close()

            if os.path.isfile(CRN_file):
                f = open(CRN_file, "r") 
                crn = f.read() # Read CRN code from token_file
                print("CRN code read from file: ", CRN_file)
                f.close()
                
                # Save the Qiskit Runtime account credentials
                QiskitRuntimeService.save_account(channel="ibm_cloud", token=token, instance=crn, set_as_default=True, overwrite=True)

                # Open Plan users cannot submit session jobs. Workloads must be run in job mode or batch mode.
                # https://quantum.cloud.ibm.com/docs/en/guides/run-jobs-session
        
        return

    #-----------------------------------------------------------------
    # Define the function setup_backend()
    # Derived from class SQD in SQD_Alain.py
    # https://github.com/AlainChance/SQD_Alain/blob/main/SQD_Alain.py
    # Author: Alain Chancé
    #-----------------------------------------------------------------
    def setup_backend(self):

        if self.param is None:
            print("setup_backend: missing parameter param")
            return None 
        param = self.param
        
        #-------------------------------------------------------------------------------------------
        # Instantiate the service
        # Once the account is saved on disk, you can instantiate the service without any arguments:
        # https://docs.quantum.ibm.com/api/migration-guides/qiskit-runtime
        #-------------------------------------------------------------------------------------------
        try:
            self.service = QiskitRuntimeService()
        except:
            print(f"Error creating an instance of QiskitRuntimeService(): {e}")
            self.service = None

        service = self.service
        
        backend_name = param['backend_name']
        n_qubits = param['n_qubits']
        opt_level = param['opt_level']
        
        print("backend_name:", backend_name)
        
        if service is None or backend_name == "AerSimulator noiseless":
            # Use AerSimulator(method='statevector')
            # https://docs.quantum.ibm.com/migration-guides/local-simulators#aersimulator
            self.backend = AerSimulator(method='statevector')
            print("\nUsing AerSimulator with method statevector and noiseless")

            self.sampler = StatevectorSampler()

        else:
            self.backend = None
            if backend_name is None or backend_name == "None":
                # Assign least busy device to backend
                # https://quantum.cloud.ibm.com/docs/en/api/qiskit-ibm-runtime/qiskit-runtime-service#least_busy
                try:
                    self.backend = service.least_busy(min_num_qubits=n_qubits, simulator=False, operational=True)
                    backend_name = self.backend.name
                    param['backend_name'] = self.backend.name

                    # Print the least busy device
                    print(f"The least busy device: {self.backend}")
                    
                except Exception as e:
                    print(f"No suitable backend found with minimum: {n_qubits} qubits - Default to 'fake_torino'")
                    backend_name = "fake_torino"

            if not backend_name[:4] in ['None', 'ibm_', 'fake']:
                print(f"Unknown backend name: {backend_name} - Default to 'fake_torino'")
                backend_name = "fake_torino"

            if backend_name[:4] == "ibm_":

                if backend_name == "ibm_torino":
                    self.backend = service.backend(backend_name)
                    opts = SamplerOptions()
                    opts.dynamical_decoupling.enable = True
                    opts.twirling.enable_measure = True
                    self.sampler = Sampler(mode=self.backend, options=opts)

                else:
                    # Get the operational real backends that have a minimum of n_qubits
                    # https://quantum.cloud.ibm.com/docs/en/api/qiskit-ibm-runtime/qiskit-runtime-service
                    try:
                        backends = service.backends(backend_name, min_num_qubits=n_qubits, simulator=False, operational=True)
                        self.backend = backends[0]
                        backend_name = self.backend.name
                        param['backend_name'] = self.backend.name
                        self.sampler = Sampler(mode=self.backend)
                    except Exception as e:
                        print(f"No suitable backend found with name {backend_name} and minimum: {n_qubits} qubits - Default to 'fake_torino'")
                        backend_name = "fake_torino"

            if backend_name[:4] == "fake":
                # https://quantum.cloud.ibm.com/docs/en/api/qiskit-ibm-runtime/fake-provider-fake-provider-for-backend-v2
                # https://github.com/Qiskit/qiskit-ibm-runtime/blob/stable/0.40/qiskit_ibm_runtime/fake_provider/fake_provider.py
                fake_provider = FakeProviderForBackendV2()
                try:
                    backend = fake_provider.backend(backend_name)
                except Exception as e:
                    print(f"Unknown fake backend name: {backend_name} - Default to 'fake_torino'")
                    backend_name = "fake_torino"
                    backend = FakeTorino()
                
                noise_model = NoiseModel.from_backend(backend)
                self.backend = AerSimulator(method='statevector', noise_model=noise_model)
                param['backend_name'] = self.backend.name
                self.sampler = StatevectorSampler()
                print("\nUsing AerSimulator with method statevector and noise model from", backend_name)

        #-----------------------------------------------------------------------------
        # Generate preset pass manager
        # https://docs.quantum.ibm.com/migration-guides/local-simulators#aersimulator
        #-----------------------------------------------------------------------------
        self.pm = generate_preset_pass_manager(backend=self.backend, optimization_level=opt_level)
        
        if isinstance(self.backend, AerSimulator):
            # Check that there is enough memory to perform a simulation with AerSimulator
            self.check_size()
                    
        else: 
            print(f"Backend name: {self.backend.name}\n"
                  f"Version: {self.backend.version}\n"
                  f"Number of qubits: {self.backend.num_qubits}"
                 )
        return

    #---------------------------------------------------------------------------------------------------------------------
    # Define the function check_size() which checks that there is enough memory to perform a simulation with AerSimulator
    # Derived from class SQD in SQD_Alain.py
    # https://github.com/AlainChance/SQD_Alain/blob/main/SQD_Alain.py
    # Author: Alain Chancé
    #---------------------------------------------------------------------------------------------------------------------
    def check_size(self):
        param = self.param
        
        #-----------------------------------------------------------------------------
        # Return if run_on_QPU is False or backend is not an instance of AerSimulator
        #-----------------------------------------------------------------------------
        if not param['run_on_QPU'] or not isinstance(self.backend, AerSimulator):
            return

        n_qubits = param['n_qubits']
        
        # Statevector simulator requires 2**instruction.num_qubits data of type complex:
        # Let's compute the amount of memory required to store 2**n_qubits numbers of data type complex128
        # Amount of memory required to store one quantum circuit that simulates a permutation operation
        # https://numpy.org/doc/stable/reference/arrays.dtypes.html
        mem_circuit = np.dtype(np.complex128).itemsize*8*2**n_qubits/10**9
    
        # Get available memory for processes
        # https://www.geeksforgeeks.org/how-to-get-current-cpu-and-ram-usage-in-python/
        mem_avail = psutil.virtual_memory()[1]/10**9

        # Check that there is enough available memory for the statevector simulation
        if mem_circuit > mem_avail:
        
            print(f"Available memory for processes (GB): {mem_avail} < Amount of memory required by AerSimulator: {mem_circuit}")
        
            # Set run_on_QPU to False
            self.param['run_on_QPU'] = False

        return

    #-------------------------------------------------------------------------------------------------------------------------
    # Define the function cluster_by_last_column()
    #
    # This method clusters rows of a NumPy array whose last column values differ by less than `tol`. 
    # It uses NumPy plus sorting.
    # 
    # Input parameters:
    #  - arr: NumPy array of floats
    #  - tol: tolerance
    #
    # Returns:
    #  - list of rows clustered around the values of the last column.
    #
    # 
    # Author: Alain Chancé
    #-------------------------------------------------------------------------------------------------------------------------
    """
    NOTE ON θ‑BASED CLUSTERING AND WHY ORDERING IS NOT REQUIRED HERE
    
    1. Tracks in the LHCb Vertex Locator (VELO) can be modeled as straight lines intersecting the
        z-axis because it is the sub-detector closest to the LHCb collision point and it contains
        a negligible magnetic field. In the XY projection, these straight lines pass through the
        origin. As a result, energy hits are likely to have a constant phase in polar coordinates
        when projected onto the XY plane (see Section 3, *Search by triplet — Sort by φ*, in
        [ALGO-10](https://arxiv.org/pdf/2207.03936)). Grouping by the phase θ naturally isolates
        hits belonging to the same azimuthal “slice” of the detector.
    
    2. The VELO geometry ensures that hits from different layers (module_id) but belonging to the
        same physical track will still share nearly identical θ values. This makes θ a robust and
        discriminating clustering variable even in the presence of noise, missing layers, or
        imperfect hit patterns.
    
    3. The purpose of sorting by θ inside this function is purely to identify contiguous groups
        within a tolerance. It does not impose any physical ordering on the hits themselves. The
        physical structure (layer ordering, radial separation, and full 3D coordinates) is carried
        by the hits, not by their position in the array.
    
    4. Downstream logic (track construction and z-axis intersection tests) relies on the geometry
        of the hits and segments, not on the order in which hits appear inside a cluster. As long
        as hits share a consistent θ, any pair of hits from the cluster forms a segment with the
        correct XY direction for physics-based validation.
    
    Because of these properties, θ‑based clustering is both efficient and physically grounded, and
    does not require preserving any particular hit order beyond grouping hits with similar θ values.
    -------------------------------------------------------------------------------------------------
    NOTE ON THE COMPUTATIONAL COMPLEXITY
    
    The computational bottleneck in the function cluster_by_last_column() is the comparison-based sorting step, 
    for which both classical and bounded-error quantum query complexities are O(n.log n); 
    quantum algorithms do not reduce the asymptotic number of comparisons required.
    
    Høyer, P.; Neerbek, J.; Shi, Y. (2001). "Quantum complexities of ordered searching, sorting, and element distinctness".
    28th International Colloquium on Automata, Languages, and Programming. Lecture Notes in Computer Science. 
    Vol. 2076. pp. 62–73. arXiv:quant-ph/0102078. doi:10.1007/3-540-48224-5_29. ISBN 978-3-540-42287-7.
    https://arxiv.org/abs/quant-ph/0102078
    """
    def cluster_by_last_column(self, arr, tol=1e-6):
        arr = np.asarray(arr)
        
        # Sort by last column
        idx = np.argsort(arr[:, -1])
        arr_sorted = arr[idx]
    
        clusters = []
        current_cluster = [arr_sorted[0]]
    
        for row in arr_sorted[1:]:
            if abs(row[-1] - current_cluster[-1][-1]) <= tol:
                current_cluster.append(row) 
            else: 
                clusters.append(np.array(current_cluster)) 
                current_cluster = [row] 
            
        clusters.append(np.array(current_cluster))
    
        return clusters

    #----------------------------------------------------------------------------------------------------------
    # Define the function analyze_p_vertices()
    #
    # This function clusters and summarizes primary-vertex candidates found by the function 
    # segment_intersects_z_axis() which performs segment–axis intersections.
    # It groups vertices by z-value and returns averaged primary vertex (PV) positions.
    #
    # A simulated primary vertex is defined as reconstructed if a primary vertex is found within 2 mm 
    # of its true position. See Primary Vertex Reconstruction Efficiency and Resolution in [ALGO-2]
    # [Aaij, R., Adinolfi, M., Aiola, S. et al. A Comparison of CPU and GPU Implementations for the LHCb 
    # Experiment Run 3 Trigger. Comput Softw Big Sci 6, 1 (2022)](https://doi.org/10.1007/s41781-021-00070-2)
    #
    # Author: Alain Chancé
    #----------------------------------------------------------------------------------------------------------
    def analyze_p_vertices(self, found_p_vertices, tol_vertices):
        """
        Cluster and summarize primary-vertex candidates found by segment–axis intersections.
        Groups vertices by z-value and returns averaged PV positions.
        """

        if not found_p_vertices:
            return []

        # Extract z-values
        z_values = np.array([xyz[2] for xyz in found_p_vertices])

        # Build array for 1-D clustering
        array_z = np.array([[i, z] for i, z in enumerate(z_values)], dtype=float)

        # Cluster by z using existing machinery
        clusters = self.cluster_by_last_column(array_z, tol=tol_vertices)

        primary_vertices = []
        for cluster in clusters:
            idxs = cluster[:,0].astype(int)
            z_cluster = z_values[idxs]
            z_mean = np.mean(z_cluster)

            # x,y are zero in the toy-model, but we compute them anyway for future realism
            x_mean = np.mean([found_p_vertices[i][0] for i in idxs])
            y_mean = np.mean([found_p_vertices[i][1] for i in idxs])

            primary_vertices.append((x_mean, y_mean, z_mean))

        return primary_vertices
    
    #---------------------------------------------------------------------------------------
    # Define the function create_tracks()
    #
    # This function builds a single track from a cluster of hits (no clone splitting here).
    # It mutates all lists in place and returns updated k.
    # 
    # Input parameters:
    #  - cluster
    #  - hit_by_index
    #  - tol_intersects
    #  - k
    #  - found_segments
    #  - found_tracks
    #  - found_clusters
    #  - found_p_vertices
    #  - false_tracks
    #  - false_clusters
    #
    # Mutates:
    #  - k
    #  - found_segments
    #  - found_tracks
    #  - found_clusters
    #  - found_p_vertices
    #  - false_tracks
    #  - false_clusters
    #
    # Returns:
    #  - k
    #
    # Author: Alain Chancé
    #---------------------------------------------------------------------------------------
    def create_tracks(
        self,
        cluster,
        hit_by_index,
        tol_intersects,
        k,
        found_segments,
        found_tracks,
        found_clusters,
        found_p_vertices,
        false_tracks,
        false_clusters
    ):
        """
        Build a single track from a cluster of hits (no clone splitting here).
        Mutates all lists in place and returns updated k.
        """

        # Extract hit indices (order preserved)
        cluster_hit_indices = {int(x[0]) for x in cluster}

        # Convert indices → Hit objects
        track_hits = [hit_by_index[idx] for idx in cluster_hit_indices]

        # Sort hits by module_id (inner → outer)
        track_hits = sorted(track_hits, key=lambda h: h.module_id)

        # If only one hit → nothing to build
        if len(track_hits) == 1:
            return k

        # Build segments
        track_segs = []
        for idx in range(len(track_hits) - 1):
            s = Segment(
                hits=[track_hits[idx], track_hits[idx + 1]],
                segment_id=idx
            )
            track_segs.append(s)
            found_segments.append(s)

        # Build Track object
        track = Track(
            track_id=k,
            hits=track_hits,
            segments=track_segs
        )

        # z-axis intersection test
        intersects = self.segment_intersects_z_axis(
            track.segments[0],
            found_p_vertices,
            tol=tol_intersects
        )

        if intersects:
            found_tracks.append(track)
            found_clusters.append(cluster)
            k += 1
        else:
            false_tracks.append(track)
            false_clusters.append(cluster)

        return k

    #--------------------------------------------
    # Define function split_clone_by_direction()
    #--------------------------------------------
    """
    Split a θ-cluster into physically distinct clone tracks by clustering
    the 3D direction vectors of consecutive hit segments.

    ----------------------------------------------------------------------
    Motivation
    ----------------------------------------------------------------------
    A θ-cluster groups hits with similar azimuthal angle φ. When multiple
    particles share nearly identical φ (common in dense VELO-like geometries),
    they may be merged into a single cluster. These "clone clusters" must be
    separated into individual tracks.

    The most stable discriminator between clone tracks is the *direction*
    of their local segments. For a true straight track, the direction vector
    between consecutive modules is nearly constant. Clone tracks, even if
    close in φ, exhibit distinct 3D directions.

    This method performs clone splitting by:
      1. Building Segment objects between consecutive modules.
      2. Converting each segment into a normalized direction vector.
      3. Measuring cosine similarity relative to a reference segment.
      4. Clustering the cosines using the existing 1‑D clustering engine.
      5. Mapping segment clusters back to hit clusters.

    ----------------------------------------------------------------------
    Parameters
    ----------------------------------------------------------------------
    track_hits : list[Hit]
        A list of Hit objects belonging to a θ-cluster. Hits must already
        be sorted in ascending module_id order.

    tol_clone_est : float
        The tolerance used to cluster segment direction cosines. Typically
        derived from the angular spread of θ_seg via the adaptive estimator:
            tol_clone_est = max(alpha * std(θ_seg), tol_min)
            
    hit_by_index
    
    tol_intersects
    
    k: integer
    
    found_segments
    
    found_tracks
    
    found_clusters
    
    found_p_vertices
    
    false_tracks
    
    false_clusters

    display : bool, optional (default=False)
        If True, prints diagnostic information about the segment clusters

    ----------------------------------------------------------------------
    Mutates:
    ----------------------------------------------------------------------
    hit_by_index
    tol_intersects
    k
    found_segments
    found_tracks
    found_clusters
    found_p_vertices
    false_tracks
    false_clusters

    ----------------------------------------------------------------------
    Returns
    ----------------------------------------------------------------------
    k : integer
    ----------------------------------------------------------------------
    Notes
    ----------------------------------------------------------------------
    • Segment direction vectors are extremely stable in the VELO toy-model,
      making cosine similarity a robust discriminator.

    • The clustering is performed in 1‑D (cosine space), reusing the existing
      cluster_by_last_column() machinery for consistency and speed.

    • Deduplication of hits is performed by object identity (id()), ensuring
      that Hit objects remain intact and no attributes are lost.

    • This method is designed to be called inside the clone-splitting branch
      of the main find_tracks() reconstruction loop.

    ----------------------------------------------------------------------
    Example
    ----------------------------------------------------------------------
        k = self.split_clone_by_direction(
            track_hits,
            tol_clone_est,
            hit_by_index,
            tol_intersects,
            k,
            found_segments,
            found_tracks,
            found_clusters,
            found_p_vertices,
            false_tracks,
            false_clusters,
            display=True
        )
    ----------------------------------------------------------------------
    """
    def split_clone_by_direction(
        self,
        track_hits,
        tol_clone_est,
        hit_by_index,
        tol_intersects,
        k,
        found_segments,
        found_tracks,
        found_clusters,
        found_p_vertices,
        false_tracks,
        false_clusters,
        display=False
    ):
        """
        Split a θ-cluster into clone tracks by clustering segment directions.
        """
    
        #-----------------------------------------
        # Build segments in module order
        #-----------------------------------------
        segments = []
        for i in range(len(track_hits) - 1):
            if track_hits[i+1].module_id > track_hits[i].module_id:
                segments.append(
                    Segment(hits=[track_hits[i], track_hits[i+1]], segment_id=i)
                )
    
        if len(segments) == 0:
            return k  # nothing to split
    
        #-----------------------------------------
        # Compute direction cosines relative to ref
        #-----------------------------------------
        ref = segments[0]
        cos_values = np.array([ref * s for s in segments])
    
        #----------------------------------------------------------------------
        # Cluster cosines using 1-D clustering function cluster_by_last_column
        #----------------------------------------------------------------------
        array_cos = np.array([[i, cos] for i, cos in enumerate(cos_values)], dtype=float)
        seg_clusters = self.cluster_by_last_column(array_cos, tol=tol_clone_est)
    
        #-----------------------------------------------------------------
        # Optional: avoid exact duplicates, but keep complementary tracks
        #-----------------------------------------------------------------
        seen_signatures = set()
    
        #-------------------------------------------------------------
        # For each segment cluster → build hit cluster → create track
        #-------------------------------------------------------------
        first = True
        
        for sc in seg_clusters:
            seg_indices = sc[:, 0].astype(int)
    
            # Build hits for this segment cluster
            hits = []
            for idx in seg_indices:
                hits.append(segments[idx].hits[0])
                hits.append(segments[idx].hits[1])
    
            # Deduplicate by identity and sort by module_id
            unique_hits = {}
            for h in hits:
                unique_hits[id(h)] = h
            hits = sorted(unique_hits.values(), key=lambda h: h.module_id)
    
            # Check module-ID validity
            module_ids = [h.module_id for h in hits]
            if len(module_ids) < 2:
                continue
            if len(module_ids) != len(set(module_ids)):
                continue  # reject clusters with duplicate modules
    
            # Signature using (module_id, index) → keeps complementary tracks distinct
            signature = tuple((h.module_id, h.index) for h in hits)
            if signature in seen_signatures:
                continue
            seen_signatures.add(signature)

            # Display (optional)
            if display:
                if first:
                    print("\nClusters found by the function split_clone_by_direction()")
                    print("\n    Hit Index     Hit ID          x         y         z       Theta      Module ID")
                first = False
                
                for h in hits:
                    print(f"    {h.index:6d}        {h.hit_id:6d}       {h.x:6.2f}    {h.y:6.2f}    {h.z:6.2f}    {h.theta:6.3f}       {h.module_id:4d}")
    
            # Convert Hit objects → array format expected by create_tracks
            subcluster = np.array(
                [[h.index, h.hit_id, h.x, h.y, h.z, h.module_id, h.theta] for h in hits],
                dtype=float
            )

            # Create a new track for the new segment cluster
            k = self.create_tracks(
                subcluster,
                hit_by_index,
                tol_intersects,
                k,
                found_segments,
                found_tracks,
                found_clusters,
                found_p_vertices,
                false_tracks,
                false_clusters
            )
    
        return k

    #----------------------------------------------------------------------------------------------------
    # Define function find_tracks()
    #
    # This method finds tracks using the function `cluster_by_last_column()`, which clusters 
    # rows of an array of hits around the polar coordinate theta.
    # 
    # Input parameter:
    #  - List of hits.
    #
    # Input from the parameter list:
    #  - layers: number of layers
    #  - tol_clusters: tolerance for cluster_by_last_column()
    #  - tol_intersects: tolerance for segment_intersects_z_axis()
    #  - do_plot_tracks
    #  - resolution
    #  - display_tracks
    #  - display_ghost_hits
    #  - display_clusters
    #  - display_false_clusters
    #  - display_clone_splitting
    #
    # Returns in the parameter list found data:
    #  - hit_by_index: dictionary keyed by the index of the hit
    #  - array_hits: NumPy array of hits with theta as last column
    #  - ghost_clusters: list of ghost clusters
    #  - false_clusters: list of false clusters
    #  - found_clusters: list of clusters
    #  - found_tracks: list of found tracks
    #  - found_segments: list of segments
    #  - found ghost_hits: list of ghost hits
    #  - false_tracks: list of tracks that do not intersect the z-axis
    #  - found_p_vertices: list of primary vertices
    #  - found_event: reconstructed event of the class Event defined in state_event_model.py
    #
    # Displays found data:
    #  - Number of found tracks and false clusters
    #  - list of ghost hits
    #  - List of found clusters
    #  - List of false clusters
    #  - list of found tracks
    #  - List of found primary vertices
    #  - Plot of tracks found by the function find_tracks() with ghost hits marked with a green 'x' 
    #
    # Calls
    #  - time.time()
    #  - cluster_by_last_column()
    #  - create_tracks()
    #  - split_clone_by_direction()
    #  - display_all_clusters()
    #  - display_all_tracks()
    #  - analyze_p_vertices()
    #  - display_p_vertices()
    #  - plot_event()
    #
    #
    # Author: Alain Chancé
    #----------------------------------------------------------------------------------------------------
    """
     -------------------------------------------------------------------------------------------------
     NOTE ON SORTING CLUSTERS BY module_id
    
     After θ‑based clustering, each cluster contains hits that lie within the same azimuthal slice
     of the detector. To impose a physically meaningful internal structure, we sort each cluster by
     hit.module_id (column 5 of array_hits). This ordering is justified because:
    
     1. In the VELO geometry, module_id increases monotonically with radius or |z|. Sorting by
        module_id therefore arranges hits from inner to outer detector layers, reflecting the
        natural geometric progression of a particle traversing the VELO.
    
     2. This internal ordering is not required for the θ‑based clustering itself, but it provides a
        consistent and interpretable sequence for downstream operations such as segment construction,
        diagnostics, or visualization.
    
     3. The physical meaning of the ordering is guaranteed by the detector layout, not by the
        original order of hits in array_hits. Sorting by module_id ensures that each cluster is
        internally structured in a way that corresponds to the actual detector layers.
    
     Because of these properties, sorting each cluster by module_id yields clusters that are both
     geometrically coherent and aligned with the physical traversal of tracks through the VELO.
     -----------------------------------------------------------------------------------------------
    
     -----------------------------------------------------------------------------------------------
     NOTE ON USING A SET FOR cluster_hit_indices
    
     A Python set created from an ordered list preserves insertion order as long as no elements 
     are added or removed afterward. Although sets are unordered, this does NOT break the physics 
     of the algorithm for the following reasons:
    
     1. Clustering is performed on the polar angle θ = atan2(y, x). Hits in the same cluster have
        nearly identical azimuthal direction in the XY plane, so any pair of hits from the cluster
        is already geometrically aligned.
    
     2. Each hit carries a module_id (detector layer). Even without explicit sorting, hits from
        different layers naturally form outward‑pointing segments because the detector geometry
        enforces radial or |z| separation between layers.
    
     3. Track acceptance depends only on whether a segment intersects the z‑axis. Since all hits in
        a θ‑cluster share the same azimuthal direction, any segment formed from any two hits in the
        cluster has essentially the same XY direction and therefore yields a consistent intersection
        test.
    
     4. The Segment class recomputes its own θ and module_id from the actual hit coordinates, so
        segment geometry remains physically meaningful even when the hit order is arbitrary.
    
     Because of these properties, using a set provides O(1) membership tests and automatic
     deduplication without compromising the physics. Segment order is irrelevant for this algorithm,
     and the resulting tracks remain stable, reproducible, and physically valid.
     ------------------------------------------------------------------------------------------------
    """
    def find_tracks(self, list_hits):

        if self.param is None:
            print("find_tracks: missing parameter param")
            return None
        param = self.param

        layers = param["layers"]
        do_plot_tracks = param["do_plot_tracks"]
        resolution = param["resolution"]
        display_tracks = param["display_tracks"]
        display_ghost_hits = param["display_ghost_hits"]
        display_clusters = param["display_clusters"]
        display_false_clusters = param["display_false_clusters"]
        display_clone_splitting = param["display_clone_splitting"]
        display_clustering = param["display_clustering"]

        tol_clusters = param["tol_clusters"]          # Tolerance for first pass coarse clustering for cluster_by_last_column()
        tol_clone = param["tol_clone"]                # Minimum value of the decloning tolerance for track_clusters()
        tol_intersects = param["tol_intersects"]      # Tolerance for segment_intersects_z_axis()
        tol_vertices = param["tol_vertices"]          # Tolerance for clustering primary vertices

        if list_hits is None or list_hits == []:
            print("find_tracks: input list of hits is None or empty - Exiting with no found track")
            return None

        if layers <= 1:
            print("find_tracks: more than one layer is required to find tracks - Exiting with no found track")
            return None

        # Start timing
        t0 = time.time()  # ⏱️ Start timing
      
        #--------------------------------------------------
        # Build a dictionary keyed by the index of the hit
        #--------------------------------------------------
        hit_by_index = {i: hit for i, hit in enumerate(list_hits)}
        param["hit_by_index"] = hit_by_index

        # Assign index to each Hit object
        for i, hit in enumerate(list_hits):
            hit.index = i

        #--------------------------------------------------------
        # Create a NumPy array of hits with theta as last column
        #--------------------------------------------------------
        array_hits = np.array([
            [i, hit.hit_id, hit.x, hit.y, hit.z, hit.module_id, hit.theta]
            for i, hit in enumerate(list_hits)
        ], dtype=float)
        param["array_hits"] = array_hits
        
        #--------------------------------------------------------
        # First pass: coarse clustering with config tol_clusters
        #--------------------------------------------------------
        clusters = self.cluster_by_last_column(array_hits, tol=tol_clusters)

        #-----------------------------------------------------------------
        # Unified estimator for tol_clusters_est (φ-clustering tolerance)
        #-----------------------------------------------------------------
        result = ToleranceEstimator.estimate_intra_cluster_theta_std(
            clusters=clusters,
            layers=layers,
            n_sample_clusters=5,
            alpha=1.5,
            tol_min=tol_clusters,
            tol_max=1e-2
        )

        if result is not None:
            tol_clusters_est, mean_std = result

            if display_clustering:
                text = f" find_tracks() - Refined tol_clusters_est = {tol_clusters_est:.4e} (mean intra-cluster std={mean_std:.4e})"
                line = "-" * (len(text) + 1)
                print(f"\n{line}\n{text}\n{line}")

            #-------------------------------------------------------
            # Second pass: refined clustering with tol_clusters_est
            #-------------------------------------------------------
            clusters = self.cluster_by_last_column(array_hits, tol=tol_clusters_est)

        else:
            tol_clusters_est = tol_clusters

            if display_clustering:
                text = " find_tracks() - Refined tol_clusters_est: no usable clusters, keeping original tol_clusters"
                line = "-" * (len(text) + 1)
                print(f"\n{line}\n{text}\n{line}")

        #------------------------------------------------------------------
        # Sort each cluster internally in ascending order of hit.module_id
        #------------------------------------------------------------------
        clusters = [c[np.argsort(c[:, 5])] for c in clusters]

        #----------------------------------------------------------------
        # Sort the list of clusters by the first column of the first row
        #----------------------------------------------------------------
        clusters = sorted(clusters, key=lambda c: c[0, 0])

        #------------------
        # Initialize lists
        #------------------
        found_clusters = []
        found_tracks = []
        found_segments = []
        found_p_vertices = []
        ghost_clusters = []
        false_tracks = []
        false_clusters = []

        threshold = int(layers / 2)
        k = 0

        #===========================
        # Main reconstruction loop
        #===========================
        for cluster in clusters:

            if len(cluster) > threshold:

                #-------------------------------------------
                # Compute track_hits ONCE for both branches
                #-------------------------------------------
                cluster_hit_indices = {int(x[0]) for x in cluster}
                track_hits = [hit_by_index[idx] for idx in cluster_hit_indices]
                track_hits = sorted(track_hits, key=lambda h: h.module_id)

                #------------------------------------
                # Case 1 — No clone splitting needed
                #------------------------------------
                if len(cluster) <= layers:

                    k = self.create_tracks(
                        cluster,
                        hit_by_index,
                        tol_intersects,
                        k,
                        found_segments,
                        found_tracks,
                        found_clusters,
                        found_p_vertices,
                        false_tracks,
                        false_clusters
                    )

                #--------------------------------
                # Case 2 — Clone-track splitting
                #--------------------------------
                else:
                    if display_clone_splitting:
                        text = f" Clone-track splitting"
                        line = "-" * (len(text) + 1)
                        print(f"\n{line}\n{text}\n{line}")

                        print("\n   Hit Index   Hit ID      x         y         z       Theta    Module ID")
                        for x in cluster:
                            print(f"  {x[0]:6.0f}     {x[1]:6.0f}     {x[2]:6.2f}    {x[3]:6.2f}    {x[4]:6.2f}    {x[6]:6.3f}       {x[5]:.0f}")

                    #----------------------------------------------------
                    # Unified estimator for tol_clone_est, theta_seg_std
                    #----------------------------------------------------
                    tol_clone_est, theta_seg_std = ToleranceEstimator.estimate_clone_tolerance(
                        track_hits,
                        alpha=1.0,
                        tol_min=tol_clone,
                        tol_max=2.0
                    )

                    if display_clone_splitting:
                        text = f" Estimated tol_clone (segment-based) = {tol_clone_est:.4e}  (std={theta_seg_std:.4e})"
                        line = "-" * (len(text) + 1)
                        print(f"\n{line}\n{text}\n{line}")

                    #-------------------------------------------------
                    # Split clone tracks by segment direction vectors
                    #-------------------------------------------------
                    k = self.split_clone_by_direction(
                        track_hits,
                        tol_clone_est,
                        hit_by_index,
                        tol_intersects,
                        k,
                        found_segments,
                        found_tracks,
                        found_clusters,
                        found_p_vertices,
                        false_tracks,
                        false_clusters,
                        display=display_clone_splitting
                    )

            #-----------
            # Ghost hit
            #-----------
            elif len(cluster) == 1:
                ghost_clusters.append(cluster)

            #-------------------------
            # Too small to be a track
            #-------------------------
            else:
                false_clusters.append(cluster)

        #--------------------------------------------------------------------------------------------------------------------
        # Save in the parameter list ghost clusters, false clusters, found tracks, found segments and found primary vertices
        #--------------------------------------------------------------------------------------------------------------------
        param["found_clusters"] = found_clusters
        param["found_tracks"] = found_tracks
        param["found_segments"] = found_segments
        param["found_p_vertices"] = found_p_vertices
        param["ghost_clusters"] = ghost_clusters
        param["false_tracks"] = false_tracks
        param["false_clusters"] = false_clusters

        #-------------------------
        # Display completion time
        #-------------------------
        t1 = time.time()
        text = f" ✅ find_tracks() completed in {t1 - t0:.2f} seconds "
        line = "-" * (len(text) + 1)
        print(f"\n{line}\n{text}\n{line}")

        #-------------------------------------
        # Create a list of found ghost_hits
        # Use a set for O(1) membership tests
        #-------------------------------------
        ghost_hit_indices = {int(x[0]) for cluster in ghost_clusters for x in cluster}
        found_ghost_hits = [hit_by_index[idx] for idx in ghost_hit_indices]
        param["found_ghost_hits"] = found_ghost_hits
        
        #-------------------------------------------------------------------------------------------------------
        # Create an instance of the class Event defined in the module state_event_model.py
        # LHCb_VeLo_Toy_Model_1-Bit_HHL/toy_model/state_event_model.py
        # https://github.com/AlainChance/LHCb_VeLo_Toy_Model_1-Bit_HHL/blob/main/toy_model/state_event_model.py
        #-------------------------------------------------------------------------------------------------------
        found_event = Event(
            detector_geometry = param["detector_geometry"],
            tracks = found_tracks,
            hits = list_hits,
            segments = found_segments,
            modules = param["modules"],
            ghost_hits = found_ghost_hits
        )
        param["found_event"] = found_event

        #--------------------------------
        # Get a list of primary_vertices
        #--------------------------------
        primary_vertices = self.analyze_p_vertices(found_p_vertices, tol_vertices)
        
        #--------------------------------
        # Display found primary vertices
        #--------------------------------
        text = f" find_tracks()"
        self.display_p_vertices(primary_vertices, text)

        #---------------------------------------------------------
        # Display number of found tracks, hits and false clusters
        #---------------------------------------------------------
        text = f" find_tracks() found {len(found_tracks)} tracks"

        if len(ghost_clusters) > 0:
            text += f" and {len(ghost_clusters)} ghost hits"
        
        if len(false_clusters) > 0:
            text += f" and {len(false_clusters)} false clusters"
            
        line = "-" * (len(text) + 1)
        print(f"\n{line}\n{text}\n{line}")

        #------------------------
        # Display found clusters
        #------------------------
        if display_clusters and len(found_clusters) > 0:
            self.display_all_clusters(found_clusters, text="clusters found by find_tracks()")
        
        #------------------------
        # Display false clusters
        #------------------------
        if display_false_clusters and len(false_clusters) > 0:
            self.display_all_clusters(false_clusters, text="false clusters found by the function find_tracks()")

        #--------------------------
        # Display found ghost hits
        #--------------------------
        if display_ghost_hits and len(ghost_clusters) > 0:
            self.display_all_clusters(ghost_clusters, text="ghost hits found by the function find_tracks()")
        
        #----------------------
        # Display found tracks
        #----------------------
        if display_tracks and len(found_tracks) > 0:                       
            self.display_all_tracks(found_tracks,
                                text=f" All {len(found_tracks)} tracks found by the function find_tracks()"
                               )

        #---------------------------
        # Plot reconstructed tracks
        #---------------------------
        if do_plot_tracks:          
            self.plot_event(found_event,
                            text=" Plot of tracks found by the function find_tracks() with ghost hits marked with a green 'x'",
                            resolution = resolution
                           )
        
        return
    
    #--------------------------------------------------------------------------------------------------
    # Define the function gen_indices()
    # 
    # This function generates ordered active segment indices as illustrated in Figure 2, left panel, 
    # of ALGO-3, https://cds.cern.ch/record/2950969/files/document.pdf, identical to the one returned 
    # by the modified function `construct_segments` of the class SimpleHamiltonian.
    #
    # The Jupyter notebook Test_gen_indices.ipynb,
    # https://github.com/AlainChance/LHCb_VeLo_Toy_Model_1-Bit_HHL/blob/main/Test_gen_indices.ipynb 
    # generates a list of segment indices for 2 to 8 particles and 3 layers.
    # 
    # Input parameters:
    #  - npart: number of particles, default: 2
    #  - layers: number of layers, default: 3
    # 
    # Returns:
    # - a list of ordered active segment indices
    #
    # Author: Alain Chancé
    #--------------------------------------------------------------------------------------------------
    def gen_indices(self, npart=2, layers=3):
        indices = []
        for j in range(layers-1):
            for i in range(npart):
                indices.append(i * (npart+1) + j*npart**2)
        return indices
    
    #--------------------------------------------------------------
    # Define function check_intersection(p1, d1, p2, d2, tol=1e-6)
    # 
    # Input parameters:
    # - p1, p2: numpy arrays representing points on each line
    # - d1, d2: numpy arrays representing direction vectors
    # - tol: tolerance for floating point comparison
    #
    # Returns:
    #  - intersects: boolean True if the line intersect
    #  - point: intersection
    #
    # Author: Alain Chancé
    #--------------------------------------------------------------
    def check_intersection(self, p1, d1, p2, d2, tol=1e-6):
        # Solve: p1 + t*d1 = p2 + s*d2 → system of equations
        A = np.column_stack((d1, -d2))
        b = p2 - p1

        try:
            # Solve for t and s
            ts, residuals, rank, s_vals = np.linalg.lstsq(A, b, rcond=None)
            t, s = ts
            
            # Compute points on each line
            point1 = p1 + t * d1
            point2 = p2 + s * d2

            # Check if points are close enough to be considered intersecting
            if np.allclose(point1, point2, atol=tol):
                return True, point1
            else:
                return False, None
        
        except np.linalg.LinAlgError:
            return False, None

    #---------------------------------------------------------------------
    # Define function intersects_origin(x0, y0, z0, dx, dy, dz, tol=1e-6)
    # 
    # Input parameters:
    # - (x0, y0, z0): a point on the line
    # - (dx, dy, dz): is the direction vector
    # - tol: tolerance for floating point comparison
    #
    # Returns:
    #  - intersects: boolean True if the line intersect
    #  - point: intersection
    #
    # Author: Alain Chancé
    #---------------------------------------------------------------------
    def intersects_origin(self, x0, y0, z0, dx, dy, dz, tol=1e-6):
        t_values = []

        # Avoid division by zero
        if abs(dx) > tol:
            t_values.append(-x0 / dx)
        if abs(dy) > tol:
            t_values.append(-y0 / dy)
        if abs(dz) > tol:
            t_values.append(-z0 / dz)

        # If no direction component is significant, line is a point
        if not t_values:
            return abs(x0) < tol and abs(y0) < tol and abs(z0) < tol

        # Check if all t values are approximately equal
        t_ref = t_values[0]
        if all(abs(t - t_ref) < tol for t in t_values):
            return True
        else:
            return False
    
    #---------------------------------------------------------------------
    # Define function intersects_z_axis(x0, y0, z0, dx, dy, dz, tol=1e-6)
    # 
    # Input parameters:
    # - (x0, y0, z0): a point on the line
    # - (dx, dy, dz): is the direction vector
    # - tol: tolerance for floating point comparison
    #
    # Returns:
    #  - intersects: boolean True if the line intersect
    #  - point: intersection
    #
    # Author: Alain Chancé
    #---------------------------------------------------------------------
    """
     ------------------------------------------------------------------------------------------------
     NOTE ON THE PHYSICS OF z‑AXIS INTERSECTION TESTING
    
     These functions determine whether a reconstructed segment is compatible with originating from
     the LHCb interaction point by checking if the segment intersects the z‑axis. This is physically
     well‑motivated in the VELO for the following reasons:
    
     1. In the VELO, tracks can be approximated as straight lines because the magnetic field is
        negligible in this region. Real charged‑particle trajectories therefore pass very close to
        the beamline. A genuine track segment should extrapolate back to the z‑axis at a physically
        reasonable z‑position.
    
     2. The intersection is computed analytically by solving x(t) = 0 and y(t) = 0 for the segment
        parameter t. If both solutions agree within a tolerance, the segment is considered to pass
        through the beamline. This provides a robust geometric criterion that is independent of hit
        ordering or cluster structure.
    
     3. The resulting z‑coordinate of the intersection must lie between the origin of the detector
        (z = 0) and the first VELO layer (z = dz). Intersections outside this region correspond to
        unphysical backward extrapolations or to segments that do not originate from a primary
        vertex.
    
     4. Because θ‑based clustering already ensures that hits in a cluster share a common azimuthal
        direction, any segment formed from two hits in the cluster will have a consistent XY
        direction. This makes the z‑axis intersection test stable even when the internal ordering of
        hits is arbitrary (e.g., when using a set).
    
     5. Unique primary vertices are accumulated by comparing intersection points within a tolerance.
        This allows the algorithm to identify multiple distinct primary vertices if present, while
        avoiding duplicates caused by numerical precision.
    
     Together, these properties ensure that the z‑axis intersection test is both geometrically
     rigorous and aligned with the physical behavior of tracks in the VELO. It serves as the final
     validation step for accepting or rejecting candidate tracks derived from θ‑clusters.
     ------------------------------------------------------------------------------------------------
    """
    def intersects_z_axis(self, x0, y0, z0, dx, dy, dz, tol=1e-6):
        t_values = []

        # Solve x(t) = 0 → t_x = -x0 / dx
        if abs(dx) > tol:
            t_x = -x0 / dx
        elif abs(x0) < tol:
            t_x = None  # x is always ~0
        else:
            return False, None

        # Solve y(t) = 0 → t_y = -y0 / dy
        if abs(dy) > tol:
            t_y = -y0 / dy
        elif abs(y0) < tol:
            t_y = None  # y is always ~0
        else:
            return False, None

        # Check if t_x and t_y are consistent
        if t_x is not None and t_y is not None:
            if abs(t_x - t_y) > tol:
                return False, None
            t = (t_x + t_y) / 2
        else:
            t = t_x or t_y or 0  # pick whichever is not None

        # Compute z(t)
        z = float(z0 + t * dz)
        return True, (0.0, 0.0, z)

    #---------------------------------------------------------------------------------
    # Define function segment_intersects_z_axis()
    #
    # Input parameter:
    #  - Segment: a segment object as defined in state_event_model.py
    #  - found_p_vertices: list of primary vertices or None
    #  - tol: tolerance for the intersection
    #
    # Input from the parameter list:
    #  - dz: layer spacing (mm)
    #
    # Mutates:
    #  - found_p_vertices
    #
    # Returns:
    #  - intersects: boolean True if the segment intersects the z-axis
    #
    # The list of found_p_vertices is processed by the function analyze_p_vertices().
    #
    # Author: Alain Chancé
    #---------------------------------------------------------------------------------
    def segment_intersects_z_axis(self, s: Segment, found_p_vertices, tol=1e-6):
        param = self.param

        dz = param["dz"]
        
        p0 = s.p0()
        p1 = s.p1()
        d = s.to_vect()

        intersects, xyz = self.intersects_z_axis(p0[0], p0[1], p0[2], d[0], d[1], d[2], tol=tol)
        if not intersects:
            return False
            
        intersects, xyz = self.intersects_z_axis(p1[0], p1[1], p1[2], d[0], d[1], d[2], tol=tol)
        if not intersects:
            return False

        # Reject intersection that is before the origin or beyond the first layer
        if xyz[2] <= 0 or xyz[2] >= dz or np.allclose(xyz[2], 0.0, atol=tol) or np.allclose(xyz[2], dz, atol=tol):
            return False
        
        if found_p_vertices is None:
            found_p_vertices = [xyz]
        else:
            found_p_vertices.append(xyz)
        
        return True
    
    #------------------------------------------------------------------------------------------
    # Define function find_segments()
    # Derived from function find_segments() in OneBQF/toy_model/simple_hamiltonian.py, 
    # https://github.com/Xenofon-Chiotopoulos/OneBQF/blob/main/toy_model/simple_hamiltonian.py
    #------------------------------------------------------------------------------------------
    def find_segments(self, s0: Segment, active: Segment):
        found_s = []
        for s1 in active:
            if s0.hits[0].hit_id == s1.hits[1].hit_id or \
            s1.hits[0].hit_id == s0.hits[1].hit_id:             
                found_s.append(s1)
        return found_s

    #---------------------------------------------------------------------------------------------------------
    # Define function get_tracks_smart() which does the following:
    #
    # - Lists active segments in the first three layers from the solution returned by the 1-bit HHL algorithm.
    # - Uses only active segments that intersect the z‑axis to reconstruct tracks. 
    # The points where these segments intersect the z‑axis form the list of reconstructed primary vertices.
    # - Completes the solution with missed segments that intersect the z-axis.
    # - Completes the list of active segments with hits in all the outer layers.
    #
    # This is consistent with the IBM Qiskit pattern methodology (*Post-process results*):
    # *“This can involve a range of classical data-processing steps, such as … or post-selection based 
    # on inherent properties of the problem …”*
    # (see [Introduction to Qiskit patterns](https://quantum.cloud.ibm.com/docs/en/guides/intro-to-patterns)).
    #
    # Both classical and 1-Bit HHL simulations only use the hits in the first three layers.
    #
    # This function is derived from function get_tracks_fast() in OneBQF/toy_model/simple_hamiltonian.py, 
    # https://github.com/Xenofon-Chiotopoulos/OneBQF/blob/main/toy_model/simple_hamiltonian.py
    #
    # Input parameters:
    #  - ham: simple Hamiltonian
    #  - solution: list of active segments
    #  - atol: tolerance
    #
    # Input from param data structure
    # - param["modules"]
    # - param[hits]
    #
    # Returns
    #  - event: an instance of the class Event defined in state_event_model.py
    #  - tracks_processed
    #  - good_indices: list of indices of active segments that intersects the z-axis
    #
    # Author: Alain Chancé
    #---------------------------------------------------------------------------------------------------------
    def get_tracks_smart(self, ham: SimpleHamiltonian, solution: list[int], atol=1e-6):
        param = self.param

        #-------------------------------------------
        # Retrieve parameters from param dictionary
        #-------------------------------------------
        do_print_outer_segs = param["do_print_outer_segs"]
        hits = param["hits"]
        modules = param["modules"]
        npart = sum(param["n_particles"])
        segment_indices = param["segment_indices"]
        segment_in_indices = param["segment_in_indices"]
        found_tracks = param["found_tracks"]
        found_segments = param["found_segments"]
        tol_intersects = param["tol_intersects"]
        tol_vertices = param["tol_vertices"]

        # Initialize the list of found primary vertices
        found_p_vertices = []

        #--------------------------------------------------------------------------------------------------------------------
        # List active segments from the solution returned by either the classical solution or the 1-bit HHL quantum solution
        #--------------------------------------------------------------------------------------------------------------------
        min_val = np.min(solution)
        
        active_segments = [
            segment for segment, pseudo_state in zip(ham.segments, solution)
            if pseudo_state > min_val
        ]

        #-------------------------------------------
        # Filter segments that intersect the z-axis
        #-------------------------------------------
        filtered_solution = solution.copy()

        filtered = False
        first = True
        for s in active_segments:
            intersects = self.segment_intersects_z_axis(s, found_p_vertices, tol=tol_intersects)
            if intersects:
                filtered_solution[s.segment_id] = 1
            else:
                filtered_solution[s.segment_id] = 0
                filtered = True
                if first:
                    print("\nRemoved segments that do not intersect the z-axis:")
                    print(f"\n   Segment ID         Hits           Theta         Module ID     Track ID")
                    first = False
                print(f"    {s.segment_id:4d}       {s.hits[0].hit_id:6d}   {s.hits[1].hit_id:4d}        {s.theta:6.3f}         {s.module_id:4d}           {s.track_id:4d}")

        if filtered:
            print("\nFiltered solution:")
            print(filtered_solution)

        # Update list of active segments
        active_segments = [segment for segment in ham.segments if filtered_solution[segment.segment_id] == 1]

        #------------------------------------------------------------------
        # Complete solution with missed segments that intersect the z-axis
        #------------------------------------------------------------------
        completed = False
        first = True
        
        if sum(filtered_solution) != len(segment_indices):
            completed_solution = filtered_solution.copy()

            #--------------------------------------------------------
            # Look only for segments in the list segment_in_indices
            # returned by the modified function construct_segments()
            #--------------------------------------------------------
            for s in segment_in_indices:
                if completed_solution[s.segment_id] == 1:
                    continue
                intersects = self.segment_intersects_z_axis(s, found_p_vertices, tol=tol_intersects)
                if intersects:
                    completed_solution[s.segment_id] = 1
                    completed = True
                    if first:
                        print("\nAdded new segments:")
                        print(f"\n    Segment ID        Hits           Theta         Module ID     Track ID")
                        first = False
                    print(f"    {s.segment_id:4d}       {s.hits[0].hit_id:6d}   {s.hits[1].hit_id:4d}        {s.theta:6.3f}         {s.module_id:4d}           {s.track_id:4d}")

        if completed:
            print("\nCompleted solution:")
            print(completed_solution)

            # Update list of active segments
            active_segments = [segment for segment in ham.segments if completed_solution[segment.segment_id] == 1]

        # Save list of found primary vertices in the parameter list
        param["found_p_vertices"] = found_p_vertices

        #----------------------
        # Get primary vertices
        #----------------------
        primary_vertices = self.analyze_p_vertices(found_p_vertices, tol_vertices)

        #--------------------------
        # Display primary vertices
        #--------------------------
        self.display_p_vertices(primary_vertices)

        #-------------------------------------------------------------------------------------------------------
        # Create an instance of the class Event defined in state_event_model.py
        # LHCb_VeLo_Toy_Model_1-Bit_HHL/toy_model/state_event_model.py
        # https://github.com/AlainChance/LHCb_VeLo_Toy_Model_1-Bit_HHL/blob/main/toy_model/state_event_model.py
        #-------------------------------------------------------------------------------------------------------
        event = Event(
            detector_geometry = param["detector_geometry"],
            tracks = found_tracks,
            hits = param["hits"],
            segments = found_segments,
            modules = param["modules"],
            ghost_hits = []
        )
        
        #-----------------------------------
        # Exit if there is no active segment
        #-----------------------------------
        if active_segments == []:
            return event, [], []

        #--------------------------------------
        # Compute list of good segment indices
        #--------------------------------------
        good_indices = [segment.segment_id for segment in active_segments]
        
        #-------------------------------------------------------------------
        # Complete the list of active segments with hits in the modules > 3
        # Author: Alain Chancé
        #-------------------------------------------------------------------
        for module in [module for module in modules if module.module_id > 3]:

            if module.module_id == 4 and do_print_outer_segs:
                text = " Added new segments"
                line = "-" * (len(text) + 1)
                print(f"\n{line}\n{text}\n{line}")
            
            if do_print_outer_segs:
                print(f"\nModule: {module.module_id}")
                print(f"\n   Segment ID         Hits           Theta         Module ID     Track ID")

            for s in [s for s in found_segments if s.module_id == module.module_id]:

                # Add new segment to the list of active segments
                active_segments.append(s)

                if do_print_outer_segs:
                    print(f"    {s.segment_id:4d}       {s.hits[0].hit_id:6d}   {s.hits[1].hit_id:4d}        {s.theta:6.3f}         {s.module_id:4d}           {s.track_id:4d}")

        event.tracks = found_tracks
        
        return event, found_tracks, good_indices

    #------------------------------------------------------
    # Define function display_all_clusters()
    #
    # This function displays all clusters given as input.
    #
    # Input parameters:
    #  - clusters: list of clusters
    #  - text: header text or None
    #
    # Displays:
    # - List of all clusters
    #
    # Author: Alain Chancé
    #------------------------------------------------------
    def display_all_clusters(self, clusters, text=None):

        if clusters:
            s = f" All {len(clusters)} "

            text = s + text if text else s
            
            line = "-" * (len(text) + 1)
            print(f"\n{line}\n{text}\n{line}")

            k = 0
            print(f"\n   Hit Index   Hit ID      x         y         z       Theta    Module ID")
            for cluster in clusters:
                for x in cluster:
                    print(f"  {x[0]:6.0f}     {x[1]:6.0f}     {x[2]:6.2f}    {x[3]:6.2f}    {x[4]:6.2f}    {x[6]:6.3f}       {x[5]:.0f}")
                k += 1

    #-----------------------------------
    # Define function display_all_hits()
    # Author: Alain Chancé
    #-----------------------------------
    def display_all_hits(self, hits, text=None):

        if text: 
            line = "-" * (len(text) + 1) 
            print(f"\n{line}\n{text}\n{line}")

        print(f"\n    Hit Index   Hit ID        x         y         z       Theta      Module ID")

        for hit in hits:
            print(f"    {hit.index:4d}        {hit.hit_id:4d}       {hit.x:6.2f}    {hit.y:6.2f}    {hit.z:6.2f}    {hit.theta:6.3f}       {hit.module_id:4d}")

        return
    
    #----------------------------------
    # Define function display_tracks()
    # Author: Alain Chancé
    #----------------------------------
    def display_all_tracks(self, tracks, text=None):

        if text: 
            line = "-" * (len(text) + 1) 
            print(f"\n{line}\n{text}\n{line}")
              
        for track in tracks:
            print(f"\nTrack ID: {track.track_id}")
            print(f"\n    Hit Index   Hit ID        x         y         z       Theta      Module ID")

            for hit in track.hits:
                print(f"    {hit.index:4d}        {hit.hit_id:4d}       {hit.x:6.2f}    {hit.y:6.2f}    {hit.z:6.2f}    {hit.theta:6.3f}       {hit.module_id:4d}")

            print(f"\n   Segment ID         Hits           Theta         Module ID     Track ID")
            for s in track.segments:
                print(f"    {s.segment_id:4d}       {s.hits[0].hit_id:6d}   {s.hits[1].hit_id:4d}        {s.theta:6.3f}         {s.module_id:4d}           {s.track_id:4d}")
        
        return

    #-----------------------------------------------------------------------
    # Define function display_p_vertices()
    #
    # This function displays a primary vertex or a list of primary vertices
    #
    # Input parameters:
    #  - List of primary vertices
    #  - Header text or None
    #
    # Displays:
    #  - List of primary vertices if any
    #
    # Author: Alain Chancé
    #-----------------------------------------------------------------------
    def display_p_vertices(self, list_p_vertices, text=None):
        if list_p_vertices:

            k = len(list_p_vertices)

            if k == 1:
                s = f" a primary vertex"
            else:
                s = f" {k} primary vertices"

            if text:
                text = text + " found" + s
            else:
                text = " Found" + s 

            line = "-" * (len(text) + 1)
            print(f"\n{line}\n{text}\n{line}")
            
            for p in list_p_vertices:
                print(f"({p[0]:5.3f}, {p[1]:5.3f}, {p[2]:5.3f})")
        return

    #-------------------------------------------------------------------------------------------------------
    # Define function plot_event()
    #
    # Input parameters:
    #  - event: an event of the class Event defined in the module state_event_model.py
    #  - text: text to be printed, default is None
    #  - resolution: increase for finer mesh
    #
    # Displays:
    #  - A 3D plot of tracks with ghost hits marked with a green 'x'
    #
    # This function is derived from function plot_segments defined in the module state_event_model.py
    # LHCb_VeLo_Toy_Model_1-Bit_HHL/toy_model/state_event_model.py
    # https://github.com/AlainChance/LHCb_VeLo_Toy_Model_1-Bit_HHL/blob/main/toy_model/state_event_model.py
    #
    # Author: Alain Chancé
    #-------------------------------------------------------------------------------------------------------
    def plot_event(self, event, text=None, resolution=25):

        if text is not None:
            line = "-" * (len(text) + 1)
            print(f"\n{line}\n{text}\n{line}")
        
        detector_geometry = event.detector_geometry
        tracks = event.tracks
        hits = event.hits
        ghost_hits = event.ghost_hits
        segments = event.segments
        
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        # Re-map: X-axis <- Z, Y-axis <- Y, Z-axis <- X
        X = [h.z for h in hits]
        Y = [h.y for h in hits]
        Z = [h.x for h in hits]
        ax.scatter(X, Y, Z, c='r', marker='o', s=5)
            
        # Plot lines
        for segment in segments:
            x = [h.z for h in segment.hits]
            y = [h.y for h in segment.hits]
            z = [h.x for h in segment.hits]
            ax.plot(x, y, z, c='b', linewidth=0.5)

        # Draw planes from geometry, but only show regions that are in the bulk
        
        # print(self.detector_geometry)
        for mod_id, lx, ly, zpos in detector_geometry:
            xs = np.linspace(-lx, lx, resolution)
            ys = np.linspace(-ly, ly, resolution)
            X, Y = np.meshgrid(xs, ys)
            Z = np.full_like(X, zpos, dtype=float)

            for idx in np.ndindex(X.shape):
                x_val = X[idx]
                y_val = Y[idx]
                # If not in the bulk (e.g., inside a void), mask out
                if not detector_geometry.point_on_bulk({'x': x_val, 'y': y_val, 'z': zpos}):
                    X[idx], Y[idx], Z[idx] = np.nan, np.nan, np.nan

            # Plot, using (Z, Y, X) to match the existing axis mappings
            ax.plot_surface(Z, Y, X, alpha=0.3, color='gray')

        # Scatter ghost_hits with a green 'x'
        if ghost_hits != []:
            X = [h.z for h in ghost_hits]
            Y = [h.y for h in ghost_hits]
            Z = [h.x for h in ghost_hits]
            ax.scatter(X, Y, Z, c='g', marker='x')
        
        ax.set_xlabel('Z (horizontal)')
        ax.set_ylabel('Y')
        ax.set_zlabel('X')
        plt.tight_layout()
        plt.show()

        return

    #-----------------------------------------------
    # Define function plot_hits_polar()
    #
    # Input parameters:
    #  - List of hits.
    #  - text: text to be printed, default is None.
    #
    # Returns
    #  - a polar plot.
    #
    # Author: Alain Chancé
    #-----------------------------------------------
    def plot_hits_polar(self, hits, text=None):

        if text is not None:
            line = "-" * (len(text) + 1)
            print(f"\n{line}\n{text}\n{line}")

        # Compute polar coordinates
        theta = [h.theta for h in hits]           # Angle theta
        r = [math.hypot(h.x, h.y) for h in hits]  # Radius

        fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
        ax.scatter(theta, r, s=5)                 # Scatter with small dots

        # Display tick labels in radians
        ax.set_xticks([0, np.pi/2, np.pi, 3*np.pi/2])
        ax.set_xticklabels(['0', 'π/2', 'π', '3π/2'])
        
        ax.set_title("Polar Plot of Hits in Radians")
        plt.show()

        return
    
    #---------------------------------
    # Define function setup_events()
    #---------------------------------
    def setup_events(self):
        
        if self.param is None:
            print("setup_events: missing parameter param")
            return None
        param = self.param
        
        dz = param["dz"]
        layers = param["layers"]
        n_particles = param["n_particles"]
        p_vertices = param["p_vertices"]
        measurement_error = param["measurement_error"]
        collision_noise = param["collision_noise"]
        drop_rate = param["drop_rate"]
        ghost_rate = param["ghost_rate"]
        display_particles = param["display_particles"]
        display_hits = param["display_hits"]
        display_ghost_hits = param["display_ghost_hits"]
        display_tracks = param["display_tracks"]
        do_plot_tracks = param["do_plot_tracks"]
        resolution = param["resolution"]
        tol = param["tol"]
        
        events_num = len(n_particles) # Number of events to generate
        n = np.sum(n_particles)

        #----------------------------------------------------------------------------------------
        # Check that the list of particles and the list of primary vertices have the same length
        #----------------------------------------------------------------------------------------
        if len(n_particles) != len(p_vertices):
            print("setup_events - Error: The lists of particles and primary vertices must have the same length.")
            return None

        # Start timing
        t0 = time.time()  # ⏱️ Start timing

        #-----------------------------------------------------------------------------------------
        # Define the detector geometry with multiple layers. 
        # Each layer represents a detection plane where particles leave hits as they pass through.
        # Key parameters:
        # - dz: Distance between detector layers (mm)
        # - layers: Number of detection layers
        # - lx, ly: Detector module dimensions in x and y (mm)
        # - zs: Z-positions of each layer
        #-----------------------------------------------------------------------------------------
        module_id = [l for l in range(1, layers+1)]
        lx = [33 for x in range(1, layers+1)]
        ly = [33 for x in range(1, layers+1)]
        zs = [dz*l for l in range(1, layers+1)]

        Detector = state_event_model.PlaneGeometry(module_id=module_id,lx = lx,ly = ly,z = zs)
        # Detector = state_event_model.RectangularVoidGeometry(module_id=module_id,lx = lx,ly = ly,z=zs, void_x_boundary=5, void_y_boundary=5)

        # --- State event generator setup ---
        state_event_gen = StateEventGenerator(Detector, 
                                              primary_vertices = p_vertices,
                                              events = events_num,
                                              n_particles = n_particles,
                                              measurement_error = measurement_error,
                                              collision_noise = collision_noise
                                             )
        param["detector_geometry"] = state_event_gen.detector_geometry

        #------------------------------------------------------------------------------
        # Generate random primary vertices (unit box extents in x,y,z) if not provided
        #------------------------------------------------------------------------------
        if p_vertices is None:
            p_vertices = state_event_gen.generate_random_primary_vertices({'x': 0, 'y': 0, 'z': 0})
            param["p_vertices"] = p_vertices
            print("\nRandomly generated primary vertices: ", p_vertices)

        #-----------------------------------------------------------------------------------------------------
        # Define the types of particles to simulate. 
        # We create Minimum Ionizing Particles (MIPs) - typical charged particles that traverse the detector.
        # Particle Properties:
        # - type: 'MIP' (Minimum Ionizing Particle)
        # - mass: Particle mass (MeV/c²)
        # - q: Electric charge (units of elementary charge)
        #-----------------------------------------------------------------------------------------------------
        event_particles = []
        for event in range(events_num):
            particles_list = []
            for particle in range(n):
                particle_dict = {
                    'type' : 'MIP',
                    'mass': 0.511,
                    'q': 1
                }
                particles_list.append(particle_dict)
            event_particles.append(particles_list)

        #-------------------------------------------------------------------------------------------------------------
        # Generate a list of initial particle state dictionaries for each event based on the primary vertices 
        # Calls the function generate_particles() in LHCb_VeLo_Toy_Model_1-Bit_HHL/toy_model/state_event_generator.py
        # https://github.com/AlainChance/LHCb_VeLo_Toy_Model_1-Bit_HHL/blob/main/toy_model/state_event_generator.py
        # which returns a list of particles states, each defined with the following dictionary: 
        #    {
        #       'type' : 'MIP',
        #       'x': x,
        #       'y': y,
        #       'z': z,
        #       'tx': tx,
        #       'ty': ty,
        #       'p/q': p/q  
        #    }
        #-------------------------------------------------------------------------------------------------------------
        init_particles = state_event_gen.generate_particles(event_particles)
        
        param["init_particles"] = init_particles

        if init_particles == 0:
            return None

        if display_particles:
            print("\nInitial particle states")
            for event_particles in init_particles:
                print("\nEvent particles")
                print(f"Type        Position              Direction         p/q")
                for p in event_particles:
                    print(f" {p['type']}        ({p['x']}, {p['y']}, {p['z']})         ({p['tx']:6.3f}, {p['ty']:6.3f})     {p['p/q']:4.2f}")
        
        #-------------------------------------------
        # Generate full event (hits + associations)
        #-------------------------------------------
        event_tracks = state_event_gen.generate_complete_events()
        param["event_tracks"] = event_tracks

        #-------------------
        # Display true hits
        #-------------------
        if display_hits and event_tracks.hits != []:

            text = f" All {len(event_tracks.hits)} true hits created by the function make_noisy_event()"
            self.display_all_hits(event_tracks.hits, text=text)

        #---------------------------------------------------------------------------------
        # Create a more realistic false_tracks event by adding realistic detector effects
        # Real detectors have imperfections. We can simulate:
        # - Drop rate: Probability of missing a hit (detector inefficiency)
        # - Ghost rate: Probability of fake hits (noise, electronic artifacts)
        #---------------------------------------------------------------------------------
        false_tracks = state_event_gen.make_noisy_event(drop_rate=drop_rate, ghost_rate=ghost_rate)
        
        param["false_tracks"] = false_tracks
        param["hits"] = false_tracks.hits
        
        param["ghost_hits"] = false_tracks.ghost_hits
        ghost_hits = param["ghost_hits"]

        #--------------------
        # Display ghost hits
        #--------------------
        if display_ghost_hits and ghost_hits != []:

            text = f" All {len(ghost_hits)} ghost hits created by the function make_noisy_event()"
            self.display_all_hits(ghost_hits, text=text)

        #-------------------------------------
        # Display full event tracks
        #-------------------------------------
        if display_tracks:
            self.display_all_tracks(event_tracks.tracks, text=f" All {len(event_tracks.tracks)} event tracks created by the function make_noisy_event()")

        #----------------------------------
        # Plot full event and false tracks
        #----------------------------------
        if do_plot_tracks:
            self.plot_event(false_tracks,
                            text=" Plot of event tracks created by the function make_noisy_event() with ghost hits marked with a green 'x'",
                            resolution = resolution
                           )
            self.plot_hits_polar(event_tracks.hits, text=" Polar plot of hits projected onto the XY plane")

        #-------------------------
        # Display completion time
        #-------------------------
        t1 = time.time()
        text = f" ✅ Function setup_events() completed in {t1 - t0:.2f} seconds "
        line = "-" * (len(text) + 1)
        print(f"\n{line}\n{text}\n{line}")
        
        return
    
    #--------------------------------------------------------
    # Define function plot_heat_map()
    # Heat map of sparse matrix A (value‑coded non‑zeros)
    # Adapted from the jupyter notebook George_Sandbox.ipynb
    #--------------------------------------------------------
    def plot_heat_map(self, A):
        param = self.param
        ham = param["ham"]
        do_plot_heat_map = param["do_plot_heat_map"]

        if not do_plot_heat_map:
            return

        sparse_A = ham.A if hasattr(ham, "A") else A

        #---------------------------------------------------------------
        # Get a new sparse matrix in CSR format for fast row operations
        #---------------------------------------------------------------
        if not ss.issparse(sparse_A):
            sparse_A = ss.csr_matrix(sparse_A)

        m, n = sparse_A.shape
        nnz = sparse_A.nnz
        density = nnz / (m * n)

        #---------------------------------------------------------------------------
        # Get a new sparse matrix in COO format that is easy to build incrementally
        #---------------------------------------------------------------------------
        # For large sparse matrices avoid full densification; plot only non‑zeros with value colormap
        coo = sparse_A.tocoo()

        plt.figure(figsize=(6, 6))
        sc = plt.scatter(coo.col, coo.row, c=coo.data, cmap='viridis', s=6, marker='s', linewidths=0)
        plt.gca().invert_yaxis()
        plt.colorbar(sc, label='Entry value')
        plt.title(f"Heat map (non-zeros) of A ({m}x{n})  nnz={nnz}  density={density:.4e}")
        plt.xlabel("Column index")
        plt.ylabel("Row index")
        plt.tight_layout()
        plt.show()

        return

    #---------------------------------------------------------------------------------------------------------
    # Define function setup_Hamiltonian()
    # The Hamiltonian is set up using only the list of modules in the first three layers
    # Parameters as defined in function __init__ in class SimpleHamiltonian(Hamiltonian)
    # https://github.com/AlainChance/LHCb_VeLo_Toy_Model_1-Bit_HHL/blob/main/toy_model/simple_hamiltonian.py
    # - epsilon: Regularization parameter
    # - alpha (gamma): Track continuation penalty
    # - beta (delta): Hit association strength
    #---------------------------------------------------------------------------------------------------------
    def setup_Hamiltonian(self):
        if self.param is None:
            print("setup_Hamiltonian: missing parameter param")
            return None
        param = self.param

        npart = sum(param["n_particles"])
        do_plot_heat_map = param["do_plot_heat_map"]
        do_solve_scipy = param["do_solve_scipy"]
        event_tracks = param["event_tracks"]
        run_on_QPU = param["run_on_QPU"]
        do_spectrum = param["do_spectrum"]
        tol = param["tol"]

        # Start timing
        t0 = time.time()  # ⏱️ Start timing

        #---------------------------------------------------
        # Create an instance of the class SimpleHamiltonian
        #---------------------------------------------------
        ham = SimpleHamiltonian(epsilon=1e-7, alpha=2.0, beta=1.0, theta_d=tol)
        param["ham"] = ham

        #----------------------------------------------
        # Save list of modules in param data structure
        #----------------------------------------------
        param["modules"] = event_tracks.modules

        #---------------------------------------------------
        # Get the list of modules in the first three layers
        #---------------------------------------------------
        modules_3 = [module for module in event_tracks.modules if module.module_id < 4]

        #----------------------------------------------------------------------------
        # Construct the Hamiltonian using only the modules in the first three layers
        #----------------------------------------------------------------------------
        event_tracks.modules = modules_3

        #-------------------------------------------------------------------------------------------
        # Call the modified construct_segments() method of the SimpleHamiltonian class
        # The function `construct_segments()` is enhanced to identify segments with matching values
        # of `theta` during their creation and to append them to the list `segment_in_indices`, 
        # along with their corresponding segment IDs in the list `segment_indices`. 
        # The function `construct_hamiltonian()` uses these lists.
        #-------------------------------------------------------------------------------------------
        text = " construct_segments() method of the SimpleHamiltonian class"
        line = "-" * (len(text) + 1) 
        print(f"\n{line}\n{text}\n{line}")
        
        ham.construct_segments(event=event_tracks)

        param["segment_indices"] = ham.segment_indices
        param["segment_in_indices"] = ham.segment_in_indices

        #----------------------------------------------------------------
        # Call construct_hamiltonian() method of class SimpleHamiltonian
        #----------------------------------------------------------------
        if do_solve_scipy or run_on_QPU:
            text = " construct_hamiltonian() method of the SimpleHamiltonian class"
            line = "-" * (len(text) + 1) 
            print(f"\n{line}\n{text}\n{line}")
            
            ham.construct_hamiltonian(event=event_tracks, convolution=False)
        
        #-------------------------------------------------------------------
        # Compute a dense representation of the sparse Hamiltonian matrix A
        #-------------------------------------------------------------------
        if do_solve_scipy or run_on_QPU:
            try:
                A = ham.A.todense()
            except Exception as e:
                print(f"Error computing a dense representation of the sparse Hamiltonian matrix A: {e}")
                param["A"] = None
                return
        
            param["A"] = A

            if do_plot_heat_map:
                print("\nShape of Hamiltonian matrix A:", np.shape(A))
                self.plot_heat_map(A)

            #---------------------------
            # Analyze solution spectrum
            #---------------------------
            if do_spectrum:
                vector_b = np.ones(len(A))
                self.analyze_solution_spectrum(np.array(A), np.array(vector_b))

        #-------------------------------------------------------
        # Restore the list of modules from param data structure
        #-------------------------------------------------------
        param["event_tracks"].modules = param["modules"]

        #-------------------------
        # Display completion time
        #-------------------------
        t1 = time.time()
        text = f" ✅ Fast construction of the Hamiltonian completed in {t1 - t0:.2f} seconds "
        line = "-" * (len(text) + 1)
        print(f"\n{line}\n{text}\n{line}")

        return

    #-----------------------------------------------------------------------------
    # Define function analyze_solution_spectrum()
    # Classically computes the exact solution to Ax=b and decomposes it
    # into components based on the eigenvalues of A, with added debugging prints.
    #-----------------------------------------------------------------------------
    def analyze_solution_spectrum(self, matrix_A, vector_b):

        param = self.param
        do_solve_scipy = param["do_solve_scipy"]
        run_on_QPU = param["run_on_QPU"]

        if not do_solve_scipy and not run_on_QPU:
            return

        # --- ROBUSTNESS FIX ---
        # Ensure the input vector is a 1D array ('flattened').
        vector_b = vector_b.flatten()

        if matrix_A.shape[0] != matrix_A.shape[1]:
            raise ValueError("Matrix A must be square.")
        if matrix_A.shape[0] != len(vector_b):
            raise ValueError("Matrix and vector dimensions must match.")

        # Eigendecomposition
        eig_vals, eig_vecs = np.linalg.eig(matrix_A)
        #print('Eingenvalues:', eig_vals)
        #print('Eingenvectors:', eig_vecs)
        # Change of basis
        betas = np.linalg.inv(eig_vecs) @ vector_b

        # Prepare for component calculation
        unique_eigenvalues = np.unique(np.round(eig_vals, 5))
        component_solutions = {lam: np.zeros_like(vector_b, dtype=complex) for lam in unique_eigenvalues}

        # Calculate individual solution components
        for i in range(len(eig_vals)):
            lam = eig_vals[i]
            beta = betas[i]
            u_vec = eig_vecs[:, i]
        
            key = unique_eigenvalues[np.argmin(np.abs(unique_eigenvalues - lam))]
        
            if abs(lam) > 1e-9:
                component = (beta / lam) * u_vec
            
                # --- DEBUGGING PRINT STATEMENTS ---
                #print(f"--- Loop iteration i={i} ---")
                #print(f"Eigenvalue (key): {key:.2f}")
                #print(f"Shape of component_solutions[key] (left side of +=): {component_solutions[key].shape}")
                #print(f"Shape of component (right side of +=):            {component.shape}")
                #print(lam)
                #print(u_vec)
            
                # This is the line that causes the error
                component_solutions[key] += component
            
                #print("...addition successful.\n")

        # Calculate the total solution for comparison
        total_exact_solution = np.linalg.solve(matrix_A, vector_b)

        # Plotting
        num_plots = len(unique_eigenvalues) + 1
        fig, axes = plt.subplots(num_plots, 1, figsize=(10, num_plots * 2.5), sharex=True, constrained_layout=True)
        fig.suptitle('Decomposition of the Solution Vector by Eigenvalue', fontsize=18)

        axes[0].bar(range(len(total_exact_solution)), total_exact_solution.real, color='black', alpha=0.8)
        axes[0].set_title('Total Exact Solution (x = A⁻¹b)', fontsize=14)
        axes[0].set_ylabel('Amplitude', fontsize=12)
        axes[0].grid(axis='y', linestyle='--', alpha=0.7)
    
        plot_idx = 1
        max_comp_amp = max([np.max(np.abs(comp.real)) for comp in component_solutions.values()] + [0])
        if max_comp_amp == 0: max_comp_amp = 1.0

        for lam, component_vec in sorted(component_solutions.items()):
            ax = axes[plot_idx]
            ax.bar(range(len(component_vec)), component_vec.real, color=f'C{plot_idx-1}')
            ax.set_title(f'Component from Eigenvalue λ = {lam:.2f}', fontsize=14)
            ax.set_ylabel('Amplitude', fontsize=12)
            ax.grid(axis='y', linestyle='--', alpha=0.7)
            ax.set_ylim(-max_comp_amp * 1.1, max_comp_amp * 1.1)
            plot_idx += 1

        axes[-1].set_xlabel('Index of Solution Vector Element', fontsize=12)
        plt.show()

        return

    #----------------------------------------
    # Define function classical_simulation()
    # Author: Alain Chancé
    #----------------------------------------
    def classical_simulation(self):
        param = self.param
        A = param["A"]
        do_solve_scipy = param["do_solve_scipy"]
        do_draw = param["do_draw"]
        false_tracks = param["false_tracks"]
        ham = param["ham"]
        T_classical = param["T_classical"]
        do_spectrum = param["do_spectrum"]
        do_print_counts = param["do_print_counts"]
        display_tracks = param["display_tracks"]
        do_plot_tracks = param["do_plot_tracks"]
        detector_geometry = param["detector_geometry"]
        resolution = param["resolution"]
        do_solve_scipy = param["do_solve_scipy"]
        run_on_QPU = param["run_on_QPU"]
        segment_indices = param["segment_indices"]

        # Start timing
        t0 = time.time()  # ⏱️ Start timing

        if not do_solve_scipy:
            return

        #--------------------------------------
        # Reset list of found primary vertices
        #--------------------------------------
        param["found_p_vertices"] = []
        found_p_vertices = param["found_p_vertices"]

        #----------------------------------------------------------------------------------------
        # Solve classically using scipy.sparse.linalg.cg
        # https://docs.scipy.org/doc/scipy-1.12.0/reference/generated/scipy.sparse.linalg.cg.html
        #-----------------------------------------------------------------------------------------
        text = " Solving classically with only the first three layers using scipy.sparse.linalg.cg"
        line = "-" * (len(text) + 1) 
        print(f"\n{line}\n{text}\n{line}")

        vector_b = np.ones(len(A))
            
        try:
            sol, _ = sci.sparse.linalg.cg(A, vector_b, atol=0)
        except Exception as e:
            print(f"Error solving with scipy.sparse.linalg.cg: {e}")
            return
        
        print("\nClassical solution:")
        print(sol)

        # Compute discretized solution
        disc_sol = (sol > T_classical).astype(int)

        print("\nDiscretized classical solution:")
        print(disc_sol)

        print("\nCorrect indices of classical solution:")
        correct_indices = [i for i, val in enumerate(disc_sol) if val == 1]
        print(correct_indices)
        param["correct_indices"] = correct_indices

        if correct_indices is not None and segment_indices is not None:
            print("\nCorrect indices of classical solution is equal to segment_indices returned by construct_segments():", correct_indices == segment_indices)

        #------------------------------------------------------------------------
        # Reconstruct tracks from Hamiltonian and discretized classical solution
        #------------------------------------------------------------------------
        #rec_tracks = get_tracks(ham, disc_sol, false_tracks)
        event, rec_tracks, good_indices = self.get_tracks_smart(ham, disc_sol)
        param["rec_event"] = event

        #-------------------------
        # Display completion time
        #-------------------------
        t1 = time.time()
        text = f" ✅ Classical simulation completed in {t1 - t0:.2f} seconds "
        line = "-" * (len(text) + 1)
        print(f"\n{line}\n{text}\n{line}")

        #------------------------------------------------------------------------
        # Display reconstructed event tracks from discretized classical solution
        #------------------------------------------------------------------------
        if display_tracks:
            self.display_all_tracks(rec_tracks, text=f" Reconstructed event tracks from discretized classical solution")

        #---------------------------------------------------------------------
        # Plot reconstructed event tracks from discretized classical solution
        #---------------------------------------------------------------------
        if do_plot_tracks:
            self.plot_event(event,
                            text=f" Plot of reconstructed event tracks from discretized classical solution",
                            resolution = resolution
                           )
        return

    #---------------------------------
    # Define function get_QPU_usage()
    # Author: Alain Chancé
    #---------------------------------
    def get_QPU_usage(self):

        if self.param is None:
            print("get_QPU_usage: missing parameter param")
            return None, None
        param = self.param

        if param['job'] is None:
            #---------------------
            # Retrieve the job_id
            #---------------------
            job_id = param['job_id']
            if job_id is None:
                return None, None

            #--------------------------
            # Instantiate the service
            #-------------------------
            if self.service is None:
                try:
                    self.service = QiskitRuntimeService()
                except:
                    print(f"Error creating an instance of QiskitRuntimeService(): {e}")
                    return None, None
                    
            service = self.service

            #-----------------------------------------
            # Get the job corresponding to the job_id
            #-----------------------------------------
            try:
                param['job'] = service.job(job_id)
                print(f"Successfully retrieved job with job_id: {job_id}")
            except Exception as e:
                print(f"Error retrieving job with job_id {job_id}: {e}")
                print("Error code registry, https://quantum.cloud.ibm.com/docs/en/errors")
                return None, None
        
        job = param['job']
        power_QPU = param['power_QPU']

        try:
            metrics = job.metrics()           # Fetch metrics from server
            usage = metrics.get("usage", {})
            QPU_usage = usage.get("quantum_seconds")
            param['QPU_usage'] = QPU_usage
        except Exception as e:
            print(f"Error retrieving job metrics: {e}")
            return None, None

        if QPU_usage is None:
            return None, None
        print(f"\nQiskit Runtime usage (s): {QPU_usage:.2f}")

        try:
            QPU_power_consumption = power_QPU*QPU_usage/3600.0
            param['QPU_power_consumption'] = QPU_power_consumption
            
            print("\nA rough estimate for QPU power consumption is computed as power QPU (kW) * QPU usage (h)")
            print(f"power QPU (kW): {power_QPU}")
            print(f"QPU usage (s): {QPU_usage:.2f}, (h): {QPU_usage/3600.0:.4f}")
            print(f"Rough estimate for QPU power consumption (kWh): {QPU_power_consumption:.4f}")
            
        except Exception as e:
            print(f"Error computing a rough estimate for QPU power consumption: {e}")
            return QPU_usage, None

        return QPU_usage, QPU_power_consumption

    #---------------------------------------------
    # Define function get_classical_power_usage()
    # Author: Alain Chancé
    #---------------------------------------------
    def get_classical_power_usage(self):

        if self.param is None:
            print("get_classical_power_usage: missing parameter param")
            return None, None
        param = self.param

        if not param['do_eco2ai']:
            return None, None

        eco2AI_file = param['eco2ai_file_name']

        if eco2AI_file is None:
            return None, None

        # Read the CSV file
        try:
            df = pd.read_csv(eco2AI_file, sep =',')
        except Exception as e:
            print(f"Error reading the eco2AI file: {e}")
            return None, None

        # Access columns by name
        try:
            # Sum duration (convert seconds → hours)
            duration = df["duration(s)"].sum() / 3600.0
            param['duration'] = duration

            # Sum power consumption (already in kWh)
            classical_power_usage = df["power_consumption(kWh)"].sum()
            param['classical_power_usage'] = classical_power_usage

            print(
                f"\nClassical processing - Duration (h): {duration:.4f} "
                f"- Power consumption (kWh): {classical_power_usage:.4f}"
                )
        except Exception as e:
            print(f"Error accessing the duration and power consumption of the eco2AI file: {e}")
            return None, None
        
        return duration, classical_power_usage

    #--------------------------
    # Define function run_qc()
    # Author: Alain Chancé
    #--------------------------
    def run_qc(self, nshots=None, job_id=None):

        if self.param is None:
            print("run_qc: missing parameter param")
            return None
        param = self.param

        #-------------------------------------------
        # Retrieve parameters from param dictionary
        #-------------------------------------------
        do_print_counts = param["do_print_counts"]
        isa_circuit = param["isa_circuit"]
        
        counts = None
            
        if isinstance(self.backend, AerSimulator):
            #------------------------------
            # Simulating with AerSimulator
            #------------------------------
            print("\nSimulating with AerSimulator")
            job = self.backend.run([isa_circuit], shots=nshots)
            result = job.result()
            counts = result.get_counts(isa_circuit)
            
        else:
            #---------------------------------------------------------------
            # If a valid job_id is provided, then get the corresponding job
            #---------------------------------------------------------------
            job = None
            if job_id is not None:
                try:
                    job = service.job(job_id)
                    print(f"Successfully retrieved job with job_id: {job_id}")
                except Exception as e:
                    print(f"Error retrieving job with job_id {job_id}: {e}")
                    
            if job is not None:
                try:
                    result = job.result()
                except Exception as e:
                    print(f"Error retrieving job result: {e}")
            else:
                #----------------------------------------------------
                # Running the quantum circuit on the target hardware
                #----------------------------------------------------
                print("Running the quantum circuit on the target hardware: ", self.backend.name)

                # Migrate from backend.run to Qiskit Runtime primitives
                # https://docs.quantum.ibm.com/migration-guides/qiskit-runtime
                job = self.sampler.run([isa_circuit], shots=nshots)
                param['job'] = job
                    
                param['job_id'] = job.job_id()
                print("\njob id:", param['job_id'])

                #-----------------------------------------------------------------------------
                # Monitor job
                # https://quantum.cloud.ibm.com/docs/en/api/qiskit/qiskit.providers.JobStatus
                #-----------------------------------------------------------------------------
                timeout = param['timeout']
                poll_interval = param['poll_interval']

                t0 = time.time()          # start time
                t1 = t0                   # time when status is QUEUED

                while True:
                    try:
                        status = job.status()
                    except Exception as e:
                        print(f"Error retrieving job status: {e}")
                        time.sleep(poll_interval)
                        continue

                    if status == "QUEUED" and t1 == t0:
                        t1 = time.time()
                        print(f"Waiting qpu time = {t1 - t0:.2f}, status = {status}")

                    elif status in ["VALIDATING", "RUNNING"]:
                        print(f"status = {status}")

                    elif status in ["CANCELLED", "DONE", "ERROR"]:
                        t2 = time.time()
                        print(f"Executing QPU time = {t2 - t1:.2f}, status = {status}")
                        break

                    if time.time() - t0 > timeout:
                        print("Job monitoring timed out.")
                        break

                    time.sleep(poll_interval)

                #--------------------------------
                # Wait until the job is complete
                #--------------------------------
                try:
                    result = job.result()
                except Exception as e:
                    print(f"Error retrieving job result: {e}")
                    result = None

            if result is None:
                print("\nThe job running the quantum circuit has failed")
                return
            
            else:
                # Display Qiskit Runtime usage and power consumption
                QPU_usage, QPU_power_consumption = self.get_QPU_usage()
                
                # Get results for the first (and only) PUB
                pub_result = result[0]

                #-----------------------------------------------------------------------------------------
                # Get counts for the classical register with name "c"
                #
                # The __init__ method in the class OneBQF in the module OneBQF.py sets-up 
                # a classical register with name "c" as follows:
                #
                #   self.time_qr = QuantumRegister(self.num_time_qubits, "time")
                #   self.b_qr = QuantumRegister(self.num_system_qubits, "b")
                #   self.ancilla_qr = QuantumRegister(1, "ancilla")
                #   self.classical_reg = ClassicalRegister(1 + self.num_system_qubits, "c")
                #
                # and performs a measurement as follows:
                #   qc.measure(self.ancilla_qr[0], self.classical_reg[0])
                #   qc.measure(self.b_qr, self.classical_reg[1:])

                # The following example shows how to get counts for a classical register with name "cr"
                # https://quantum.cloud.ibm.com/docs/en/api/qiskit-ibm-runtime/runtime-service
                # cr = ClassicalRegister(2, name="cr")
                # qc.measure(qr, cr)
                # print(f"Counts: {pub_result.data.cr.get_counts()}")

                # https://quantum.cloud.ibm.com/docs/en/guides/measure-qubits
                # https://quantum.cloud.ibm.com/docs/en/api/qiskit/qiskit.primitives.BitArray
                # https://quantum.cloud.ibm.com/docs/en/api/qiskit/qiskit.result.Counts
                #-----------------------------------------------------------------------------------------
                try:
                    counts = pub_result.data.c.get_counts()
                except:
                    print("Unable to get counts")
                    return None

        # Exit if counts is None
        if counts is None:
            print("The quantum circuit returned no solution")
            return None
            
        if do_print_counts:
            print("\nRaw Measurement Counts:")
            print(counts)
            print("")

        param["counts"] = counts
    
        return counts

    #----------------------------------
    # Define function HHL_simulation()
    # Author: Alain Chancé
    #----------------------------------
    def HHL_simulation(self):
        
        if self.param is None:
            print("HHL_simulation: missing parameter param")
            return None
        param = self.param

        #-------------------------------
        # Return if run_on_QPU is False
        #-------------------------------
        if not param['run_on_QPU']:
            return None
        
        layers = param["layers"]                       # Number of layers
        n_particles = param["n_particles"]             # Number of particles
        A = param["A"]
        num_time_qubits = param["num_time_qubits"]
        nshots = param["nshots"]
        do_draw = param["do_draw"]
        false_tracks = param["false_tracks"]
        ham = param["ham"]
        T_hhl = param["T_hhl"]
        do_spectrum = param["do_spectrum"]
        do_print_counts = param["do_print_counts"]
        display_tracks = param["display_tracks"]
        do_plot_tracks = param["do_plot_tracks"]
        resolution = param["resolution"]
        detector_geometry = param["detector_geometry"]
        correct_indices = param["correct_indices"]
        hhl_correct_indices = param["hhl_correct_indices"]
        segment_indices = param["segment_indices"]

        vector_b = np.ones(len(A))

        # Start timing
        t0 = time.time()  # ⏱️ Start timing

        text = " 1-Bit HHL simulation with only the first three layers"
        line = "-" * (len(text) + 1) 
        print(f"\n{line}\n{text}\n{line}")
        
        #---------------------------------------------------------------------------------------
        # 1-Bit HHL simulation with only the first three layers
        # Create an instance of the HHL algorithm.
        # Use parameters for simulation with only first 3 layers:
        # - num_time_qubits=1
        # - shots=nshots
        # https://github.com/Xenofon-Chiotopoulos/OneBQF/blob/main/quantum_algorithms/OneBQF.py
        # https://github.com/Xenofon-Chiotopoulos/OneBQF/blob/main/example.ipynb
        #---------------------------------------------------------------------------------------
        hhl_solver = onebqf(A, vector_b, num_time_qubits=1, shots=nshots, debug=False)
        
        print("\nCreating hhl_solver instance of the HHLAlgorithm as follows:")
        print("Number of time qubits:", hhl_solver.num_time_qubits)

        # Build the HHL circuit
        circuit = hhl_solver.build_circuit()
        self.param['circuit'] = circuit

        # Added by Alain Chancé
        if do_draw:
            print("\n1-bit HHL circuit")
            # Draw the circuit using matplotlib
            fig = circuit.draw(output="mpl")

            # Display the figure
            display(fig)

            # Save the figure to a file
            fig.savefig("HHL_circuit.png", bbox_inches='tight')

        param["n_qubits"] = circuit.num_qubits
        print("\nNumber of qubits in HHL circuit: ", circuit.num_qubits)

        #---------------
        # Setup backend
        #---------------
        self.setup_backend()
        
        if self.pm is None:
            return None
        
        #----------------------
        # Run the pass manager
        #----------------------
        try:
            isa_circuit = self.pm.run(circuit)
            print(f"Gate counts (w/ pre-init passes): {isa_circuit.count_ops()}")
        except:
            print("Pass manager failed to create isa_circuit")
            param['run_on_QPU'] = False
            isa_circuit = None

        self.param['isa_circuit'] = isa_circuit

        if isa_circuit is None:
            return

        #-----------------------------------
        # Print circuit and gate statistics
        #-----------------------------------
        circuit_depth = isa_circuit.decompose().depth()
        print(f"\nThe depth of the isa quantum circuit is: {circuit_depth}")
        
        gate_statistics = isa_circuit.decompose().count_ops()
        print("Gate statistics for the circuit:")
        print(gate_statistics)

        #---------------------
        # Run quantum circuit
        #---------------------
        job_id = param["job_id"]
        counts = self.run_qc(nshots=nshots, job_id=job_id)

        if counts is None:
            return None

        #----------------------------------
        # Analyze measurement counts
        # Copied from George_Sandbox.ipynb
        #----------------------------------
        if correct_indices is not None:
            refined_success = 0
            other_success = 0 
            failure = 0
            refined_failure = 0

            print("\n--- Analyzing Measurement Counts ---")
            for outcome, count in counts.items():
                if outcome[-1] == '1':
                    other_success += count
                else:
                    failure += count

            for outcome, count in counts.items():
                if outcome[-1] == '1':
                    system_bits = outcome[:-1]
                    measured_index = int(system_bits, 2)

                    if measured_index in correct_indices:
                        refined_success += count
                else:
                    refined_failure += count
    
            print(f"Success: {other_success}, Failure: {failure}")

        # Update hhl_solver property counts
        hhl_solver.counts = counts

        # Extract the HHL solution (trimmed to the original dimension)
        try:
            x_hhl, total_success = hhl_solver.get_solution(counts=counts)
        except Exception as e:
            print(f"Error retrieving HHL_solution: {e}")
            x_hhl = None

        # Exit if HHL solver did not find a solution
        if x_hhl is None:
            print("HHL solver did not find a solution")
            return
            
        print("\nExtracted HHL solution (normalized):")
        print(x_hhl)

        #------------------------------------------------------
        # Compute discretized HHL solution and correct indices
        #------------------------------------------------------
        if T_hhl is None:
            T_hhl = np.min(x_hhl) + 0.2*(np.max(x_hhl) - np.min(x_hhl))
            print("\nComputed T_hhl:", T_hhl)
        
        disc_x_hhl = (x_hhl > T_hhl).astype(int)
        print("\nDiscretized HHL solution:")
        print(disc_x_hhl)
        
        hhl_correct_indices = [i for i, val in enumerate(disc_x_hhl) if val == 1]
        print("\nIndices of HHL solution:")
        print(hhl_correct_indices)

        #------------------------------------------------------------------
        # Reconstruct tracks from Hamiltonian and discretized HHL solution
        #------------------------------------------------------------------
        event, hhl_rec_tracks, hhl_good_indices = self.get_tracks_smart(ham, disc_x_hhl)
        param["hhl_rec_event"] = event

        #----------------------------------------------------------------------------------
        # Compare good indices of HHL solution and correct indices of classical simulation
        #----------------------------------------------------------------------------------
        if hhl_good_indices is not None:
            print("\nGood indices of HHL solution:")
            print(hhl_good_indices)

            if correct_indices is not None:
                print("\nGood indices of HHL solution is equal to correct indices of classical solution:", hhl_good_indices == correct_indices)

            if segment_indices is not None:
                print("\nGood indices of HHL solution is equal to segment_indices returned by construct_segments():", hhl_good_indices == segment_indices)

        #-------------------------
        # Display completion time
        #-------------------------
        t1 = time.time()
        text = f" ✅ 1-Bit HHL quantum simulation completed in {t1 - t0:.2f} seconds "
        line = "-" * (len(text) + 1)
        print(f"\n{line}\n{text}\n{line}")

        #------------------------------------------------------------
        # Display reconstructed tracks from discretized HHL solution
        #------------------------------------------------------------
        if display_tracks:
            self.display_all_tracks(hhl_rec_tracks, text=f" Reconstructed event tracks from discretized HHL solution")

        #---------------------------------------------------------
        # Plot reconstructed tracks from discretized HHL solution
        #---------------------------------------------------------
        if do_plot_tracks:
            self.plot_event(event,
                            text=f" Plot of reconstructed event tracks from discretized HHL solution",
                            resolution=resolution
                           )

        return
    
    #----------------------------------
    # Define function run_simulation()
    #----------------------------------
    def run_simulation(self):
        if self.param is None:
            print("run_simulation: missing parameter param")
            return None
        param = self.param

        hits = param["hits"]
        do_solve_scipy = param["do_solve_scipy"]
        run_on_QPU = param['run_on_QPU']

        #---------------------------------------------
        # Find tracks with the function find_tracks()
        # Author: Alain Chancé
        #---------------------------------------------
        # Run find_tracks
        try:
            self.find_tracks(hits)
        except Exception as e:
            print(f"Error in function find_tracks(): {e}")

        #--------------------------------------
        # Fast construction of the Hamiltonian
        #--------------------------------------
        if do_solve_scipy or run_on_QPU:
            # Setup Hamiltonian
            try:
                self.setup_Hamiltonian()
            except Exception as e:
                print(f"Error in function setup_Hamiltonian(): {e}")
        
        #----------------------
        # Classical simulation
        #----------------------
        if do_solve_scipy:
            # Run classical simulation
            try:
                self.classical_simulation()
            except Exception as e:
                print(f"Error in function classical_simulation(): {e}")

        #------------------------------
        # 1-Bit HHL quantum simulation
        #------------------------------
        OK = True
        if run_on_QPU:
            # Run 1-Bit HHL quantum simulation
            try:
                self.HHL_simulation()
            except Exception as e:
                print(f"Error in function HHL_simulation(): {e}")
                OK = False

            #------------------------------------------------------------------------------------
            # Print a rough estimate of the energy consumption of the quantum device
            # **Assumption**
            # A ballpark figure for a typical modern IBM-class superconducting quantum computer 
            # (including cryogenics + support, while idle or lightly used): ~ 15–25 kW. 
            # Source: [Green quantum computing, Capgemini, 8 May 2023]
            # (https://www.capgemini.com/insights/expert-perspectives/green-quantum-computing/).
            #------------------------------------------------------------------------------------
            if OK:
                QPU_usage, QPU_power_consumption = self.get_QPU_usage()

        #-------------------------
        # Stop the eco2AI tracker
        #-------------------------
        tracker = self.param["eco2ai_tracker"]
        if tracker is not None:
            tracker.stop()

        #----------------------------------------------------------------------------------------
        # Read the CSV file and print the duration and power consumption of classical processing
        #----------------------------------------------------------------------------------------
        duration, classical_power_usage = self.get_classical_power_usage()
        
        return