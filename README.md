# LHCb_VeLo_Toy_Model_1-Bit_HHL
1-Bit HHL track simulation toy model derived from Xenofon Chiotopoulos, TrackHHL: A Quantum Computing Algorithm for Track Reconstruction at the LHCb.

## Credit
The below list of jupyter notebooks and the Python file [One_Bit_HHL_Simulation.py](https://github.com/AlainChance/LHCb_VeLo_Toy_Model_1-Bit_HHL/blob/main/One_Bit_HHL_Simulation.py) are derived from the Jupyter notebook [test.ipynb](https://github.com/GeorgeWilliam1999/LHCb_VeLo_Toy_Model/blob/main/test.ipynb) in the repository [LHCb_VeLo_Toy_Model](https://github.com/GeorgeWilliam1999/LHCb_VeLo_Toy_Model/tree/main) owned by George William Scriven, [GeorgeWilliam1999](https://orcid.org/0009-0004-9997-1647). Relevant documentation can be found in the Jupyter notebook [Tracking Toy Model Demo](https://github.com/Xenofon-Chiotopoulos/Tracking_Toy_model/blob/main/example_notebook.ipynb) in the public repository [Tracking_Toy_model](https://github.com/Xenofon-Chiotopoulos/Tracking_Toy_model/tree/main) owned by Xenofon Chiotopoulos.

## Contributions by Alain Chancé
### [One_Bit_HHL_Simulation.py](https://github.com/AlainChance/LHCb_VeLo_Toy_Model_1-Bit_HHL/blob/main/One_Bit_HHL_Simulation.py), new functions
- setup_backend() and check_size() derived from class SQD in [SQD_Alain.py](https://github.com/AlainChance/SQD_Alain/blob/main/SQD_Alain.py)
- gen_indices()
- event_from_tracks()
- display_tracks()
- plot_event()
- classical_simulation()
- HHL_simulation() derived from class SQD in [SQD_Alain.py](https://github.com/AlainChance/SQD_Alain/blob/main/SQD_Alain.py)
- run_simulation()

### [hhl_algorithm_1bit.py](https://github.com/AlainChance/LHCb_VeLo_Toy_Model_1-Bit_HHL/blob/main/hhl_algorithm_1bit.py), class HHLAlgorithm

#### init()
Added: 
- keywords gain=0.3, lam_s=6, angle_pi=True, do_draw=False
- print("class HHLAlgorithm modified by Alain Chancé")
- print("init round(np.max(np.abs(np.linalg.eigvals(A)))):", round(np.max(np.abs(np.linalg.eigvals(A)))))
- print("init self.t = np.pi / round(np.max(np.abs(np.linalg.eigvals(A)))):", self.t)

#### build_circuit()
Added:
- lam = round(lam)

Modified:
- gain = self.gain
- if abs(lam) > self.lam_s or abs(lam) < self.lam_s

#### run_with_noise_simulation()
Removed Qiskit runtime credentials.

The Python file [One_Bit_HHL_Simulation.py](https://github.com/AlainChance/LHCb_VeLo_Toy_Model_1-Bit_HHL/blob/main/One_Bit_HHL_Simulation.py) and the following list of Jupyter notebooks are compatible with Python 3.13, Qiskit v2.1, Qiskit runtime version: 0.40 and Qiskit Runtime V2 primitives:

## 3 layers
The 1-bit HHL simulation is in exact agreement with the classical simulation for 2, 4, 8, 16, 32, and 64 particles (the maximum that could be run with 32 Gb of RAM). For other number of particles, a check of the output of the HHL simulation may reveal inconsistencies, in which case a heuristic fix is applied. It uses a list created by the function gen_indices() which is ordered as illustrated on page 9 of the presentation [TrackHHL: A Quantum Computing Algorithm for Track Reconstruction at the LHCb](https://indico.cern.ch/event/1338689/contributions/6010017/): "𝑆1, 𝑆4, 𝑆5, 𝑆8 are good segments and 𝑆2, 𝑆3, 𝑆6, 𝑆7 are wrong combinations". 

- [HHL_2_particles_3_layers.ipynb](https://github.com/AlainChance/LHCb_VeLo_Toy_Model_1-Bit_HHL/blob/main/HHL_2_particles_3_layers.ipynb)
- [HHL_3_particles_3_layers.ipynb](https://github.com/AlainChance/LHCb_VeLo_Toy_Model_1-Bit_HHL/blob/main/HHL_3_particles_3_layers.ipynb)
- [HHL_4_particles_3_layers.ipynb](https://github.com/AlainChance/LHCb_VeLo_Toy_Model_1-Bit_HHL/blob/main/HHL_4_particles_3_layers.ipynb)
- [HHL_5_particles_3_layers.ipynb](https://github.com/AlainChance/LHCb_VeLo_Toy_Model_1-Bit_HHL/blob/main/HHL_5_particles_3_layers.ipynb)
- [HHL_8_particles_3_layers.ipynb](https://github.com/AlainChance/LHCb_VeLo_Toy_Model_1-Bit_HHL/blob/main/HHL_8_particles_3_layers.ipynb)
- [HHL_16_particles_3_layers.ipynb](https://github.com/AlainChance/LHCb_VeLo_Toy_Model_1-Bit_HHL/blob/main/HHL_16_particles_3_layers.ipynb)
- [HHL_32_particles_3_layers.ipynb](https://github.com/AlainChance/LHCb_VeLo_Toy_Model_1-Bit_HHL/blob/main/HHL_32_particles_3_layers.ipynb)
- [HHL_64_particles_3_layers.ipynb](https://github.com/AlainChance/LHCb_VeLo_Toy_Model_1-Bit_HHL/blob/main/HHL_64_particles_3_layers.ipynb)

## 4 layers
Same comment as above as for 3 layers.

- [HHL_2_particles_4_layers.ipynb](https://github.com/AlainChance/LHCb_VeLo_Toy_Model_1-Bit_HHL/blob/main/HHL_2_particles_4_layers.ipynb)
- [HHL_3_particles_4_layers.ipynb](https://github.com/AlainChance/LHCb_VeLo_Toy_Model_1-Bit_HHL/blob/main/HHL_3_particles_4_layers.ipynb)
- [HHL_4_particles_4_layers.ipynb](https://github.com/AlainChance/LHCb_VeLo_Toy_Model_1-Bit_HHL/blob/main/HHL_4_particles_4_layers.ipynb)
- [HHL_5_particles_4_layers.ipynb](https://github.com/AlainChance/LHCb_VeLo_Toy_Model_1-Bit_HHL/blob/main/HHL_5_particles_4_layers.ipynb)
- [HHL_8_particles_4_layers.ipynb](https://github.com/AlainChance/LHCb_VeLo_Toy_Model_1-Bit_HHL/blob/main/HHL_8_particles_4_layers.ipynb)
- [HHL_16_particles_4_layers.ipynb](https://github.com/AlainChance/LHCb_VeLo_Toy_Model_1-Bit_HHL/blob/main/HHL_16_particles_4_layers.ipynb) 
- [HHL_32_particles_4_layers.ipynb](https://github.com/AlainChance/LHCb_VeLo_Toy_Model_1-Bit_HHL/blob/main/HHL_32_particles_4_layers.ipynb)
- [HHL_64_particles_4_layers.ipynb](https://github.com/AlainChance/LHCb_VeLo_Toy_Model_1-Bit_HHL/blob/main/HHL_64_particles_4_layers.ipynb)

## 5 layers
This is work in progress.

- [HHL_2_particles_5_layers.ipynb](https://github.com/AlainChance/LHCb_VeLo_Toy_Model_1-Bit_HHL/blob/main/HHL_2_particles_5_layers.ipynb)
- [HHL_3_particles_5_layers.ipynb](https://github.com/AlainChance/LHCb_VeLo_Toy_Model_1-Bit_HHL/blob/main/HHL_3_particles_5_layers.ipynb)
- [HHL_4_particles_5_layers.ipynb](https://github.com/AlainChance/LHCb_VeLo_Toy_Model_1-Bit_HHL/blob/main/HHL_4_particles_5_layers.ipynb)
- [HHL_5_particles_5_layers.ipynb](https://github.com/AlainChance/LHCb_VeLo_Toy_Model_1-Bit_HHL/blob/main/HHL_5_particles_5_layers.ipynb)
- [HHL_8_particles_5_layers.ipynb](https://github.com/AlainChance/LHCb_VeLo_Toy_Model_1-Bit_HHL/blob/main/HHL_8_particles_5_layers.ipynb)

## References
- [LHCb_VeLo_Toy_Model](https://github.com/GeorgeWilliam1999/LHCb_VeLo_Toy_Model/tree/main)
- [test.ipynb](https://github.com/GeorgeWilliam1999/LHCb_VeLo_Toy_Model/blob/main/test.ipynb)
- [George_Sandbox.ipynb](https://github.com/GeorgeWilliam1999/LHCb_VeLo_Toy_Model/blob/main/George_Sandbox.ipynb)
- [Xenofon Chiotopoulos, TrackHHL: A Quantum Computing Algorithm for Track Reconstruction at the LHCb](https://indico.cern.ch/event/1338689/contributions/6010017/)
- [Tracking Toy Model Demo](https://github.com/Xenofon-Chiotopoulos/Tracking_Toy_model/blob/main/example_notebook.ipynb)
- [D. Nicotra et al., arXiv:2308.00619v2, 7 Oct 2023, A quantum algorithm for track reconstruction in the LHCb vertex detector](https://arxiv.org/pdf/2308.00619)
- [SQD_Alain](https://github.com/AlainChance/SQD_Alain)
- [TrackHHL: A Quantum Computing Algorithm for Track Reconstruction at the LHCb Experiment](https://indico.cern.ch/event/1338689/contributions/6010017/attachments/2951297/5188722/CHEP_ppt.pdf)
