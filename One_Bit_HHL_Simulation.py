# 1-Bit HHL track simulation toy model by George William Scriven and Alain Chancé

## MIT License

# MIT_License Copyright (c) 2025 George William Scriven and Alain Chancé
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

#-------------------------------------------------------------------------------------------
## Credit
# This Python code is derived from the Jupyter notebook test.ipynb, 
# https://github.com/GeorgeWilliam1999/LHCb_VeLo_Toy_Model/blob/main/test.ipynb 
# owned by George William Scriven, GeorgeWilliam1999, https://orcid.org/0009-0004-9997-1647
#
# Relevant documentation can be found in the Jupyter notebook example_notebook.ipynb,
# https://github.com/Xenofon-Chiotopoulos/Tracking_Toy_model/blob/main/example_notebook.ipynb.
# owned by Xenofon Chiotopoulos.
#
## Contributions by Alain Chancé
# Added the following functions:
# - setup_backend() derived from class SQD in SQD_Alain.py
# - check_size() derived from class SQD in SQD_Alain.py
# - gen_indices()
# - check_intersection()
# - intersects_origin()
# - intersects_z_axis()
# - segment_intersects_z_axis()
# - find_segments() derived from function find_segments() in simple_hamiltonian.py
# - get_tracks_smart() derived from function get_tracks() in simple_hamiltonian.py
# - display_tracks()
# - display_p_vertices()
# - plot_event() 
# - classical_simulation()
# - HHL_simulation() derived from class SQD in SQD_Alain.py
# - run_simulation()
#
# https://github.com/AlainChance/SQD_Alain/blob/main/SQD_Alain.py is owned by Alain Chancé
#-------------------------------------------------------------------------------------------

#---------------------------------------------------------------------------------------------------------------------------------------------
## References
### LHCb Velo Toy Model
# [LHCb_VeLo_Toy_Model](https://github.com/GeorgeWilliam1999/LHCb_VeLo_Toy_Model/tree/main)

# [test.ipynb](https://github.com/GeorgeWilliam1999/LHCb_VeLo_Toy_Model/blob/main/test.ipynb)

# [George_Sandbox.ipynb](https://github.com/GeorgeWilliam1999/LHCb_VeLo_Toy_Model/blob/main/George_Sandbox.ipynb)

# [Xenofon Chiotopoulos, TrackHHL: A Quantum Computing Algorithm for Track Reconstruction at the LHCb,CHEP 2024, 21 Oct 2024,]
#(https://indico.cern.ch/event/1338689/contributions/6010017/attachments/2951297/5188722/CHEP_ppt.pdf)

# [Tracking Toy Model Demo](https://github.com/Xenofon-Chiotopoulos/Tracking_Toy_model/blob/main/example_notebook.ipynb)

# [D. Nicotra et al., arXiv:2308.00619v2, 7 Oct 2023, A quantum algorithm for track reconstruction in the LHCb vertex detector]
# (https://arxiv.org/pdf/2308.00619

# Primary Vertex Reconstruction at LHCb, LHCb-PUB-2014-044, October 21, 2014
# https://cds.cern.ch/record/1756296/files/LHCb-PUB-2014-044.pdf

### Quantum Algorithms for Track Reconstruction
# [Okawa, Hideki, Quantum Algorithms for Track Reconstruction at High Energy Colliders, Workshop of Tracking in Particle Physics Experiments,
# May 17-19, 2024](https://indico.ihep.ac.cn/event/21775/contributions/155907/attachments/78247/97329/okawa_QTrack_20240517.pdf)

# Quantum pathways for charged track finding in high-energy collisions, Front. Artif. Intell., 30 May 2024, Sec. Big Data and AI in High Energy Physics,
# Volume 7 - 2024, https://doi.org/10.3389/frai.2024.1339785
 
### Quantum Machine Learning in High Energy Physics
# Wen Guan et al, Quantum machine learning in high energy physics, 2021 Mach. Learn.: Sci. Technol. 2 011003
# https://quantum.web.cern.ch/sites/default/files/2021-07/Quantum%20Machine%20Learning%20in%20High%20Energy%20Physics.pdf

# Gray HM. Quantum pattern recognition algorithms for charged particle tracking. Philos Trans A Math Phys Eng Sci. 2022 Feb 7;380(2216):20210103. 
# doi: 10.1098/rsta.2021.0103. Epub 2021 Dec 20. PMID: 34923843; PMCID: PMC8685607.
# https://pmc.ncbi.nlm.nih.gov/articles/PMC8685607/

### Hough transform
# Straight line Hough transform, https://scikit-image.org/docs/stable/auto_examples/edges/plot_line_hough_transform.html

# Frank Klefenz, Nico Wittrock, Frank Feldhoff, Parallel Quantum Hough Transform, 15 Nov 2023, arXiv:2311.09002 eess.IV
# https://doi.org/10.48550/arXiv.2311.09002

# F. Klefenz, K.-H. Noffz, W. Conen, R. Zoz, A. Kugel, and R. Manner. “Track recognition in 4 µs by a systolic trigger processor 
# using a parallel Hough transform”. IEEE Transactions on Nuclear Science 40, 688–691 (1993)
# https://ieeexplore.ieee.org/document/256642

### SQD_Alain
# SQD_Alain, https://github.com/AlainChance/SQD_Alain
#---------------------------------------------------------------------------------------------------------------------------------------------

# Import common packages first
import psutil
import sys
import os
import time

from copy import deepcopy

import numpy as np
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

# Import qiskit ecosystems
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler
from qiskit_ibm_runtime import SamplerOptions

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

from LHCB_Velo_Toy_Models.state_event_generator import *
from LHCB_Velo_Toy_Models import state_event_model
from LHCB_Velo_Toy_Models.simple_hamiltonian import SimpleHamiltonian
from LHCB_Velo_Toy_Models.simple_hamiltonian import get_tracks
from LHCB_Velo_Toy_Models.toy_validator import EventValidator as evl
from LHCB_Velo_Toy_Models.state_event_model import module, Event

# HHL algorithm
from hhl_algorithm import HHLAlgorithm as hhl

# 1-Bit HHL algorithm
from hhl_algorithm_1bit import HHLAlgorithm as hhl_1
from hhl_algorithm_1bit import add_suzuki_trotter_to_class

# Patching HHLAlgorithm with Suzuki-Trotter methods...
hhl_1 = add_suzuki_trotter_to_class(hhl_1)

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

#--------------------------
# Define class One_Bit_HHL
# Author: Alain Chancé
#--------------------------
class One_Bit_HHL:
    def __init__(self,
                 dz = 20,                           # layer spacing (mm)
                 layers = 3,                        # Number of layers
                 n_particles = [32],                # Number of particles
                 p_vertices = [(0,0,10)],           # Primary vertices
                 do_draw = False,                   # Whether to draw the HHL circuit
                 num_time_qubits = 2,               # Number of time qubits
                 measurement_error = 0.0,           # HIT RESOLUTION (sigma on measurement) (sigma)
                 collision_noise = 0.0,             # MULTIPLE SCATTERING (angular noise proxy)
                 ghost_rate = 1e-2,                 # ghost (fake) track rate
                 drop_rate = 0.0,                   # hit drop (inefficiency) rate
                 display_hits = False,              # Whether to display hits
                 display_tracks = True,             # Whether to display events and ghost tracks
                 plot_tracks = True,                # Whether to plot events and ghost tracks
                 T_classical = 0.45,                # Threshold for discretizing classical solutions
                 T_hhl = None,                      # Threshold for discretizing 1-Bit HHL solutions - None: to be computed
                 do_spectrum = False,               # Whether to analyze the classical solution spectrum
                 do_print_counts = False,           # Whether to print raw measurement counts
                 resolution = 25,                   # Resolution for plots of tracks - Increase for finer mesh
                 gain = 0.3,                        # Used by function build_circuit in hhl_algorithm_1bit.py
                 lam_s = 6,                         # Used by function build_circuit in hhl_algorithm_1bit.py
                 angle_pi = True,                   # Used by function build_circuit in hhl_algorithm_1bit.py
                 max_abs_eigen = 4,                 # Used by function build_circuit in hhl_algorithm_1bit.py
                 #------------------------------------------
                 # Files containing token (API key) and CRN
                 #------------------------------------------
                 token_file = "Token.txt",           # Token file
                 CRN_file = "CRN.txt",               # CRN file
                 #-------------
                 # Run options
                 #-------------
                 backend_name = None,                # IBM cloud backend name
                 job_id = None,                      # job_id of a previously run job
                 run_on_QPU = False,                 # Whether to run the quantum circuit on the target hardware
                 nshots = 100000,                    # Number of shots
                 opt_level = 3,                      # Optimization level
                 poll_interval = 5,                  # Poll interval in seconds for job monitor
                 timeout = 600,                      # Time out for job monitor
                ):

        # Initialize self.backend to None
        self.backend = None

        #--------------------------
        # Print simulation options
        #--------------------------
        print("\nSimulation options")
        print("layer spacing (mm), dz:", dz)
        print("layers:", layers)
        print("n_particles:", n_particles)
        print("primary_vertices:", p_vertices)
        print("do_draw:", do_draw)
        print("num_time_qubits:", num_time_qubits)
        print("measurement hit resolution:", measurement_error)
        print("multiple scattering collision noise:", collision_noise)
        print("ghost (fake) track rate:", ghost_rate)
        print("hit drop (inefficiency) rate:", drop_rate)
        print("display_hits:", display_hits)
        print("display_tracks:", display_tracks)
        print("plot_tracks:", plot_tracks)
        print("T_classical:", T_classical)                  # Threshold for discretizing classical solutions
        print("T_hhl:", T_hhl)                              # Threshold for discretizing 1-Bit HHL solutions
        print("do_spectrum:", do_spectrum)
        print("do_print_counts:", do_print_counts)
        print("resolution:", resolution)
        print("gain:", gain)
        print("lam_s:", lam_s)
        print("angle_pi:", angle_pi)
        print("max_abs_eigen:", max_abs_eigen)

        #-------------------
        # Print run options
        #-------------------
        print("Backend name:", backend_name)
        
        if job_id is not None:
            print("job_id:", job_id)
        
        print("Run on QPU:", run_on_QPU)
        print("Number of shots:", nshots)
        print("Optimization level:", opt_level)

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
            "num_time_qubits": num_time_qubits,              # Number of time qubits
            "measurement_error": measurement_error,          # HIT RESOLUTION (sigma on measurement) (sigma)
            "collision_noise": collision_noise,              # MULTIPLE SCATTERING (angular noise proxy)
            "ghost_rate": ghost_rate,                        # ghost (fake) track rate
            "drop_rate": drop_rate,                          # hit drop (inefficiency) rate
            "display_hits": display_hits,                    # Whether to display hits
            "display_tracks": display_tracks,                # Whether to display events and ghost tracks
            "plot_tracks": plot_tracks,                      # Whether to plot events and ghost tracks
            "T_classical": T_classical,                      # Threshold for discretizing classical solutions
            "T_hhl": T_hhl,                                  # Threshold for discretizing 1-Bit HHL solutions
            "do_spectrum": do_spectrum,                      # Whether to analyze the classical solution spectrum
            "do_print_counts": do_print_counts,              # Whether to print raw measurement counts
            "resolution": resolution,                        # Resolution for plots of tracks - Increase for finer mesh
            "gain": gain,                                    # Used by function build_circuit in hhl_algorithm_1bit.py
            "lam_s": lam_s,                                  # Used by function build_circuit in hhl_algorithm_1bit.py
            "angle_pi": angle_pi,                            # Used by function build_circuit in hhl_algorithm_1bit.py
            "max_abs_eigen": max_abs_eigen,                  # Used by function build_circuit in hhl_algorithm_1bit.py
            #------------------------------------------
            # Files containing token (API key) and CRN
            #------------------------------------------
            "token_file": token_file,                        # Token file
            "CRN_file": CRN_file,                            # CRN file
            #-------------
            # Run options
            #-------------
            "backend_name": backend_name,                    # IBM cloud backend name
            "job_id": job_id,                                # job_id
            "run_on_QPU": run_on_QPU,                        # Whether to run the quantum circuit on the target hardware
            "nshots": nshots,                                # Number of shots
            "opt_level":opt_level,                           # Optimization level
            "poll_interval": poll_interval,                  # Poll interval in seconds for job monitor
            "timeout": timeout,                              # Time out in seconds for gob monitor
            #------------------
            # Shared variables
            #------------------
            "n_qubits": 2,                                   # Number of qubits in the HHL circuit, set by function run_HHL()
            "init_particles": [],                            # List of initial particle state dictionaries for each event based on the primary vertices
            "event_tracks": None,                            # Full event created by setup_events() of class Event (state_event_model.py)
            "false_tracks": None,                            # Event with ghost hits
            "modules": [],                                   # List of modules
            "rec_event": None,                               # Reconstructed event from discretized classical solution
            "hhl_rec_event": None,                           # Reconstructed event from discretized HHL solution
            "ham": None,                                     # Hamiltonian operator
            "A": None,                                       # Hamiltonian matrix       
            "circuit": None,                                 # HHL Quantum circuit returned by function HHL_simulation()
            "detector_geometry": None,                       # Geometry of the detector
            "found_p_vertices":None,                         # List of found primary vertices
            "true_hits": None,                               # List of true hits computed by the function generate_complete_events()
            "hits": None,                                    # List of all true and ghost hits computed by the function make_noisy_event()
            "counts": None,                                  # Raw measurement counts set by function HHL_simulation()
            "correct_indices": None,                         # Correct indices set by function classical_simulation()
            "hhl_correct_indices": None                      # HHL correct indices set by function HHL_simulation
        }

        #--------------------------------------------------------------------
        # If token_file and CRN_file are provided, then retrieve credentials
        # Author: Alain Chancé 
        #--------------------------------------------------------------------
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
        
        #-------------------------------------------------------------------------------------------
        # Instantiate the service
        # Once the account is saved on disk, you can instantiate the service without any arguments:
        # https://docs.quantum.ibm.com/api/migration-guides/qiskit-runtime
        #-------------------------------------------------------------------------------------------
        try:
            service = QiskitRuntimeService()
        except:
            service = None

        self.service = service

        param = self.param
        opt_level = param['opt_level']
        backend_name = self.param['backend_name']
        n_qubits = self.param['n_qubits']
        
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
                    self.param['backend_name'] = self.backend.name

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
                        self.param['backend_name'] = self.backend.name
                        self.sampler = Sampler(mode=self.backend)
                    except Exception as e:
                        print(f"No suitable backend found with name {backend_name} and minimum: {n_qubits} qubits - Default to 'fake_torino'")
                        backend_name = "fake_torino"

            if backend_name[:4] == "fake":
                # https://quantum.cloud.ibm.com/docs/en/api/qiskit-ibm-runtime/fake-provider
                # https://quantum.cloud.ibm.com/docs/en/api/qiskit-ibm-runtime/fake-provider-fake-provider-for-backend-v2
                fake_provider = FakeProviderForBackendV2()
                try:
                    backend = fake_provider.backend(backend_name)
                except Exception as e:
                    print(f"Unknown fake backend name: {backend_name} - Default to 'fake_torino'")
                    backend_name = "fake_torino"
                    backend = FakeTorino()
                
                noise_model = NoiseModel.from_backend(backend)
                self.backend = AerSimulator(method='statevector', noise_model=noise_model)
                self.param['backend_name'] = self.backend.name
                self.sampler = StatevectorSampler()
                print("\nUsing AerSimulator with method statevector and noise model from", backend_name)

        #-------------------------------------------------------------------------------------------
        # Generate preset pass manager
        # https://docs.quantum.ibm.com/migration-guides/local-simulators#aersimulator
        self.pm = generate_preset_pass_manager(backend=self.backend, optimization_level=opt_level)
        #-------------------------------------------------------------------------------------------
        if isinstance(self.backend, AerSimulator):
            # Check that there is enough memory to perform a simulation with AerSimulator
            self.check_size()
            
        else:
            print(f"Backend name: {self.backend.name}\n"
                  f"Version: {self.backend.version}\n"
                  f"Number of qubits: {self.backend.num_qubits}"
                 )

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

    #-----------------------------------------------------------------------------------
    # Define function gen_indices()
    # 
    # Input parameters:
    #  - param["n_particles"][0] 
    #  - param["layers"]
    #
    # Returns
    #  - a list of indices ordered as shown on page 9 of the presentation
    #    TrackHHL: A Quantum Computing Algorithm for Track Reconstruction at the LHCb
    #    https://indico.cern.ch/event/1338689/contributions/6010017/
    #
    # Author: Alain Chancé
    #-----------------------------------------------------------------------------------
    def gen_indices(self):
        param = self.param
        
        npart = param["n_particles"][0]
        layers = param["layers"]
        
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

    #-------------------------------------------------------------------
    # Define function segment_intersects_z_axis()
    # Input parameter:
    #  - a segment of the class segment defined in state_event_model.py
    # Returns:
    #  - intersects: boolean True if the segment intersects the z-axis
    # Author: Alain Chancé
    #-------------------------------------------------------------------
    def segment_intersects_z_axis(self, s: Segment, tol=1e-6):
        param = self.param
        
        p0 = s.p0()
        p1 = s.p1()
        d = s.to_vect()

        intersects, xyz = self.intersects_z_axis(p0[0], p0[1], p0[2], d[0], d[1], d[2])
        if not intersects:
            return False
            
        intersects, xyz = self.intersects_z_axis(p1[0], p1[1], p1[2], d[0], d[1], d[2])
        if not intersects:
            return False
        
        if param["found_p_vertices"] is None:
            param["found_p_vertices"] = [xyz]
        else:
            found = True
            for p_vertex in param["found_p_vertices"]:
                if np.allclose(p_vertex, xyz, atol=tol):
                    found = False
            if found:
                param["found_p_vertices"].append(xyz)
        
        return True
    
    #---------------------------------------------------------------------------------------------------------------
    # Define function find_segments()
    # Derived from function find_segments() in simple_hamiltonian.py
    # https://github.com/GeorgeWilliam1999/LHCb_VeLo_Toy_Model/blob/main/LHCB_Velo_Toy_Models/simple_hamiltonian.py
    #---------------------------------------------------------------------------------------------------------------
    def find_segments(self, s0: Segment, active: Segment):
        found_s = []
        for s1 in active:
            if s0.hits[0].hit_id == s1.hits[1].hit_id or \
            s1.hits[0].hit_id == s0.hits[1].hit_id:             
                found_s.append(s1)
        return found_s

    #---------------------------------------------------------------------------------------------------------------
    # Define function get_tracks_smart()
    #
    # This function is derived from function get_tracks() in simple_hamiltonian.py
    # https://github.com/GeorgeWilliam1999/LHCb_VeLo_Toy_Model/blob/main/LHCB_Velo_Toy_Models/simple_hamiltonian.py
    #
    # Input parameters:
    #  - ham: simple Hamiltonian
    #  - solution: list of active segments
    #
    # Input from param data structure
    # - param["modules"]
    # - param["detector_geometry"]
    # - param[hits]
    #
    # Returns
    #  - event: an instance of the class Event defined in state_event_model.py
    #  - tracks_processed
    #  - good_indices: list of indices of active segments that intersects the z-axis
    #
    # Author: Alain Chancé
    #---------------------------------------------------------------------------------------------------------------
    def get_tracks_smart(self, ham: SimpleHamiltonian, solution: list[int], atol=1e-6):
        param = self.param
        
        #------------ Modified by Alain Chancé ---------------------------------------------------------------------------------
        #active_segments = [segment for segment,pseudo_state in zip(ham.segments,solution) if pseudo_state > np.min(solution)]
        # Only segments that intersect the z-axis are included in the list of active segments
        active_segments = [segment for segment,pseudo_state in zip(ham.segments,solution) if pseudo_state > np.min(solution) and self.segment_intersects_z_axis(segment)]
        #------------------------------------------------------------------------------------------------------------------------
        
        #--------------------------------------------------------------------------------------------------------------
        # Create an instance of the class Event defined in state_event_model.py
        # https://github.com/GeorgeWilliam1999/LHCb_VeLo_Toy_Model/blob/main/LHCB_Velo_Toy_Models/state_event_model.py
        # Author: Alain Chancé
        #--------------------------------------------------------------------------------------------------------------
        event = Event(
            detector_geometry = param["detector_geometry"],
            tracks = [],
            hits = param["hits"],
            segments = active_segments,
            modules = param["modules"]
        )
        
        good_indices = [segment.segment_id for segment in active_segments]

        #-------------------------------------------------------------------
        # Complete the list of active segments with hits in the modules > 3
        # Author: Alain Chancé
        #-------------------------------------------------------------------
        if active_segments == []:
            return event, [], good_indices
  
        k = max(segment.segment_id for segment in active_segments) + 1

        for module in [module for module in param["modules"] if module.module_id > 3]:
            for hit in module.hits:
                active = deepcopy(active_segments)
                for s in active:
                    p1 = s.p1()
                    d1 = s.to_vect()
                    d2 = (hit.x - p1[0], hit.y - p1[1], hit.z - p1[2])

                    # Check whether directions are close enough to be considered the same
                    if np.allclose(d1, d2, atol=atol):
                    
                        seg = Segment(
                            segment_id = k,
                            hits = [s.hits[1], hit]
                        )
                        
                        active_segments.append(seg)
                        k += 1

        #---------------
        # Create tracks
        #---------------
        active = deepcopy(active_segments)
        tracks = []
        while len(active):
            s = active.pop()
            
            nextt = self.find_segments(s, active) 
            track = set([s.hits[0].hit_id, s.hits[1].hit_id])
                
            while len(nextt):
                s = nextt.pop()
                try:
                    active.remove(s)
                except:
                    pass
                nextt += self.find_segments(s, active)
                track = track.union(set([s.hits[0].hit_id, s.hits[1].hit_id]))
            tracks.append(track)

        tracks_processed = []
        for track_ind, track in enumerate(tracks):
            track_hits = []
            for hit_id in track:
                matching_hits = list(filter(lambda b: b.hit_id == hit_id, param["hits"]))
                if matching_hits:  
                    track_hits.append(matching_hits[0])
            if track_hits:
                tracks_processed.append(Track(track_ind, track_hits, 1))

        event.tracks = tracks_processed,
        
        return event, tracks_processed, good_indices

    #----------------------------------
    # Define function display_tracks()
    # Author: Alain Chancé
    #----------------------------------
    def display_tracks(self, tracks):
        for track in tracks:
            print(f"\nTrack ID: {track.track_id}")

            for hit in track.hits:
                print(f"  Hit ID: {hit.hit_id}, x: {hit.x}, y: {hit.y}, z: {hit.z}, Module ID: {hit.module_id}")
        return

    #--------------------------------------
    # Define function display_p_vertices()
    # Author: Alain Chancé
    #--------------------------------------
    def display_p_vertices(self):
        if self.param["found_p_vertices"] is not None:
            print(f"\nFound primary vertices:")
            for p in self.param["found_p_vertices"]:
                print(f"({p[0]:.1f}, {p[1]:.1f}, {p[2]:.1f})")
        return

    #--------------------------------------------------------------------------------------------------------------
    # Define function plot_event()
    # Input parameters:
    #  - an event of the class Event defined in state_event_model.py
    #  - resolution
    # Returns
    #  - a plot
    # This function is derived from function plot_segments in module state_event_model.py
    # https://github.com/GeorgeWilliam1999/LHCb_VeLo_Toy_Model/blob/main/LHCB_Velo_Toy_Models/state_event_model.py
    # Author: Alain Chancé
    #--------------------------------------------------------------------------------------------------------------
    def plot_event(self, event, resolution):
        
        detector_geometry = event.detector_geometry
        tracks = event.tracks
        hits = event.hits
        segments = event.segments
        
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        # Re-map: X-axis <- Z, Y-axis <- Y, Z-axis <- X
        X = [h.z for h in hits]
        Y = [h.y for h in hits]
        Z = [h.x for h in hits]
        ax.scatter(X, Y, Z, c='r', marker='o')
            
        # Plot lines
        for segment in segments:
            x = [h.z for h in segment.hits]
            y = [h.y for h in segment.hits]
            z = [h.x for h in segment.hits]
            ax.plot(x, y, z, c='b')

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

        # plot ghost_hits (hits that are not part of a segment)
        ghost_hits = [h for h in hits if not any(h in s.hits for s in segments)]
        X = [h.z for h in ghost_hits]
        Y = [h.y for h in ghost_hits]
        Z = [h.x for h in ghost_hits]
        ax.scatter(X, Y, Z, c='g', marker='x')
        
        ax.set_xlabel('Z (horizontal)')
        ax.set_ylabel('Y')
        ax.set_zlabel('X')
        plt.tight_layout()
        plt.show()
            
    #---------------------------------------------------------------
    # Define function setup_events()
    # This function is derived from the Jupyter notebook test.ipynb
    #---------------------------------------------------------------
    def setup_events(self):
        param = self.param
        dz = param["dz"]
        layers = param["layers"]
        n_particles = param["n_particles"]
        p_vertices = param["p_vertices"]
        measurement_error = param["measurement_error"]
        collision_noise = param["collision_noise"]
        drop_rate = param["drop_rate"]
        ghost_rate = param["ghost_rate"]
        display_hits = param["display_hits"]
        display_tracks = param["display_tracks"]
        plot_tracks = param["plot_tracks"]
        
        events_num = len(n_particles) # Number of events to generate
        n = np.sum(n_particles)

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

        #------------------------------------------------------------------------------------------------------------------
        # Generate a list of initial particle state dictionaries for each event based on the primary vertices 
        # Calls the function generate_particles() in module state_event_generator.py
        # https://github.com/GeorgeWilliam1999/LHCb_VeLo_Toy_Model/blob/main/LHCB_Velo_Toy_Models/state_event_generator.py
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
        #------------------------------------------------------------------------------------------------------------------
        init_particles = state_event_gen.generate_particles(event_particles)
        param["init_particles"] = init_particles

        print("\nInitial particle states")
        for event_particles in init_particles:
            print("\nEvent particles")
            for p in event_particles:
                print(f"Type: {p['type']}, Position: ({p['x']}, {p['y']}, {p['z']}), Direction: ({p['tx']}, {p['ty']}), p/q: {p['p/q']}")
        
        #-------------------------------------------
        # Generate full event (hits + associations)
        #-------------------------------------------
        event_tracks = state_event_gen.generate_complete_events()
        param["event_tracks"] = event_tracks 

        #-------------------
        # Display true hits
        #-------------------
        if display_hits:
            if event_tracks.hits != []:
                print("\nTrue hits")
                for hit in event_tracks.hits:
                    print(f"  Hit ID: {hit.hit_id}, x: {hit.x}, y: {hit.y}, z: {hit.z}, Module ID: {hit.module_id}")

        #---------------------------------------------------------------------------------
        # Create a more realistic false_tracks event by adding realistic detector effects
        # Real detectors have imperfections. We can simulate:
        # - Drop rate: Probability of missing a hit (detector inefficiency)
        # - Ghost rate: Probability of fake hits (noise, electronic artifacts)
        #---------------------------------------------------------------------------------
        false_tracks = state_event_gen.make_noisy_event(drop_rate=drop_rate, ghost_rate=ghost_rate)
        param["false_tracks"] = false_tracks
        param["hits"] = false_tracks.hits

        #---------------------------------
        # Display all true and ghost hits
        #---------------------------------
        if display_hits:
            if false_tracks.hits != []:
                print("\nAll true and ghost hits")
                for hit in false_tracks.hits:
                    print(f"  Hit ID: {hit.hit_id}, x: {hit.x}, y: {hit.y}, z: {hit.z}, Module ID: {hit.module_id}")

        #-------------------------------------
        # Display full event and false tracks
        #-------------------------------------
        if display_tracks:
            print("\nEvent tracks")
            self.display_tracks(event_tracks.tracks)
            print("\nEvent tracks hits:", len(event_tracks.modules[0].hits))

            print("\nEvent tracks with ghost hits (false tracks)")
            self.display_tracks(false_tracks.tracks)
            print("\nFalse tracks hits:", len(false_tracks.modules[0].hits))

        #----------------------------------
        # Plot full event and false tracks
        #----------------------------------
        if plot_tracks:
            print("\nPlotting event tracks")
            event_tracks.plot_segments()

            print("\nPlotting event tracks with ghost hits (false tracks)")
            false_tracks.plot_segments()
        
        return
    
    #--------------------------------------------------------
    # Define function plot_heat_map()
    # Heat map of sparse matrix A (value‑coded non‑zeros)
    # Adapted from the jupyter notebook George_Sandbox.ipynb
    #--------------------------------------------------------
    def plot_heat_map(self, A):
        param = self.param
        ham = param["ham"]

        sparse_A = ham.A if hasattr(ham, "A") else A
        if not ss.issparse(sparse_A):
            sparse_A = ss.csr_matrix(sparse_A)

        m, n = sparse_A.shape
        nnz = sparse_A.nnz
        density = nnz / (m * n)

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

    #------------------------------------------------------------------------------------
    # Define function setup_Hamiltonian()
    # Adapted from the Jupyter notebook test.ipynb
    # The Hamiltonian is set up using only the list of modules in the first three layers
    # Parameters:
    # - epsilon: Regularization parameter
    # - gamma: Track continuation penalty
    # - delta: Hit association strength
    # - T: Decision threshold for track selection
    #------------------------------------------------------------------------------------
    def setup_Hamiltonian(self):
        param = self.param
        event_tracks = param["event_tracks"]
        
        ham = SimpleHamiltonian(epsilon=1e-7, gamma=2.0, delta=1.0)
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

        ham.construct_hamiltonian(event=event_tracks, convolution=False)
        
        A = ham.A.todense()
        param["A"] = A

        print("Shape of Hamiltonian matrix A:", np.shape(A))
        
        self.plot_heat_map(A)

        print("Eigenvalues of Hamiltonian matrix A:")
        print(np.abs(np.linalg.eigvals(A)))

        #-------------------------------------------------------
        # Restore the list of modules from param data structure
        #-------------------------------------------------------
        param["event_tracks"].modules = param["modules"]

        return

    #-----------------------------------------------------------------------------
    # Define function analyze_solution_spectrum()
    # Adapted from the Jupyter notebook test.ipynb
    # Classically computes the exact solution to Ax=b and decomposes it
    # into components based on the eigenvalues of A, with added debugging prints.
    #-----------------------------------------------------------------------------
    def analyze_solution_spectrum(self, matrix_A, vector_b):
        print("\n--- INSIDE analyze_solution_spectrum ---")
        print(f"Initial shape of matrix_A: {matrix_A.shape}")
        print(f"Initial shape of vector_b: {vector_b.shape}")

        # --- ROBUSTNESS FIX ---
        # Ensure the input vector is a 1D array ('flattened').
        vector_b = vector_b.flatten()
        print(f"Shape of vector_b after flattening: {vector_b.shape}")
        print("-------------------------------------\n")

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

    #----------------------------------------
    # Define function classical_simulation()
    # Author: Alain Chancé
    #----------------------------------------
    def classical_simulation(self):
        param = self.param
        A = param["A"]
        do_draw = param["do_draw"]
        false_tracks = param["false_tracks"]
        ham = param["ham"]
        T_classical = param["T_classical"]
        do_spectrum = param["do_spectrum"]
        do_print_counts = param["do_print_counts"]
        display_tracks = param["display_tracks"]
        plot_tracks = param["plot_tracks"]
        detector_geometry = param["detector_geometry"]
        resolution = param["resolution"]

        vector_b = np.ones(len(A))

        #----------------------------------------------------------------------------------------
        # Solve classically using scipy.sparse.linalg.cg
        # https://docs.scipy.org/doc/scipy-1.12.0/reference/generated/scipy.sparse.linalg.cg.html
        #-----------------------------------------------------------------------------------------
        print("\n-----------------------------------------------------------------------------------")
        print(" Solving classically with only the first three layers using scipy.sparse.linalg.cg")
        print("-----------------------------------------------------------------------------------")
        #sol = ham.solve_classicaly()
        sol, _ = sci.sparse.linalg.cg(A, vector_b, atol=0)
        
        print("\nClassical solution:")
        print(sol)

        # Compute discretized solution
        # Modified by Alain Chancé
        #T = .45
        disc_sol = (sol > T_classical).astype(int)

        print("\nDiscretized classical solution:")
        print(disc_sol)

        print("\nCorrect indices of classical solution:")
        correct_indices = [i for i, val in enumerate(disc_sol) if val == 1]
        print(correct_indices)
        param["correct_indices"] = correct_indices

        #---------------------------
        # Analyze solution spectrum
        #---------------------------
        if do_spectrum:
            self.analyze_solution_spectrum(np.array(A), np.array(vector_b))

        #------------------------------------------------------------------------
        # Reconstruct tracks from Hamiltonian and discretized classical solution
        #------------------------------------------------------------------------
        #rec_tracks = get_tracks(ham, disc_sol, false_tracks)
        event, rec_tracks, good_indices = self.get_tracks_smart(ham, disc_sol)
        param["rec_event"] = event

        #--------------------------------
        # Display found primary vertices
        #--------------------------------
        self.display_p_vertices()

        #------------------------------------------------------------------------
        # Display reconstructed event tracks from discretized classical solution
        #------------------------------------------------------------------------
        if display_tracks:
            print("\nReconstructed event tracks from discretized classical solution")
            self.display_tracks(rec_tracks)

        #---------------------------------------------------------------------
        # Plot reconstructed event tracks from discretized classical solution
        #---------------------------------------------------------------------
        if plot_tracks:
            print("\nReconstructed event tracks from discretized classical solution")
            self.plot_event(event, resolution)

        #-------------------------------------------------
        # Compute and print event validation matrix table
        #-------------------------------------------------
        validator = evl(false_tracks, rec_tracks)
        print("")
        validator.print_metrics()
        print("")

        return

    #-----------------------------------------------------------------
    # Define function HHL_simulation()
    # Derived from class SQD in SQD_Alain.py
    # https://github.com/AlainChance/SQD_Alain/blob/main/SQD_Alain.py
    # Author: Alain Chancé
    #-----------------------------------------------------------------
    def HHL_simulation(self):
        param = self.param
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
        plot_tracks = param["plot_tracks"]
        gain = param["gain"]                             # Used by function build_circuit in hhl_algorithm_1bit.py
        lam_s = param["lam_s"]                           # Used by function build_circuit in hhl_algorithm_1bit.py
        angle_pi = param["angle_pi"]                     # Used by function build_circuit in hhl_algorithm_1bit.py
        max_abs_eigen = param["max_abs_eigen"]           # Used by function build_circuit in hhl_algorithm_1bit.py
        resolution = param["resolution"]
        detector_geometry = param["detector_geometry"]
        correct_indices = param["correct_indices"]
        hhl_correct_indices = param["hhl_correct_indices"]

        vector_b = np.ones(len(A))

        #--------------------------------------
        # Reset list of found primary vertices
        #--------------------------------------
        param["found_p_vertices"] = None
        found_p_vertices = param["found_p_vertices"]

        #-------------------------------
        # Return if run_on_QPU is False
        #-------------------------------
        if not param['run_on_QPU']:
            return None

        print("\n-------------------------------------------------------")
        print(" 1-Bit HHL simulation with only the first three layers")
        print("-------------------------------------------------------")

        #------------------------------------------------------------------
        # Compute max_abs_eigen classically if not provided as a parameter
        #------------------------------------------------------------------
        if max_abs_eigen is None:
            max_abs_eigen = round(np.max(np.abs(np.linalg.eigvals(A))))
            print("\nComputed max_abs_eigen = round(np.max(np.abs(np.linalg.eigvals(A)))):", max_abs_eigen)
            param["max_abs_eigen"] = max_abs_eigen
        
        #---------------------------------------------------------
        # 1-Bit HHL simulation with only the first three layers
        # Create an instance of the HHL algorithm.
        # Use parameters for simulation with only first 3 layers:
        # - num_time_qubits=2
        # - lam_s=6
        # - angle_pi=True
        # - shots=nshots
        #---------------------------------------------------------
        hhl_solver = hhl_1(A, vector_b, num_time_qubits=2, gain=gain, lam_s=6, angle_pi=True, max_abs_eigen=max_abs_eigen, shots=nshots)
        print("\nCreating hhl_solver instance of the HHLAlgorithm as follows:")
        print("Number of time qubits:", hhl_solver.num_time_qubits)
        print("lam_s:", hhl_solver.lam_s)
        print("max_abs_eigen:", hhl_solver.max_abs_eigen)

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

        self.param["n_qubits"] = circuit.num_qubits
        print("\nNumber of qubits in HHL circuit: ", circuit.num_qubits)

        #---------------
        # Setup backend
        #---------------
        self.setup_backend()
        
        if not param['run_on_QPU']:
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

        counts = None
            
        if isinstance(self.backend, AerSimulator):
            #------------------------------
            # Simulating with AerSimulator
            #------------------------------
            print("\nSimulating with AerSimulator")
            job = self.backend.run([isa_circuit], shots=param['nshots'])
            result = job.result()
            counts = result.get_counts(isa_circuit)
            
        else:
            job_id = param["job_id"]

            if job_id is not None:
                #-------------------------------
                # Retrieve the job using its ID
                #-------------------------------
                job = self.service.job(job_id)

                try:
                    result = job.result()
                except Exception as e:
                    print(f"Error retrieving job result: {e}")
                    return
            else:
                #----------------------------------------------------
                # Running the quantum circuit on the target hardware
                #----------------------------------------------------
                print("Running the quantum circuit on the target hardware: ", self.backend.name)

                # Migrate from backend.run to Qiskit Runtime primitives
                # https://docs.quantum.ibm.com/migration-guides/qiskit-runtime
                job = self.sampler.run([isa_circuit], shots=param['nshots'])
                print("\njob id:", job.job_id())

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
                print("\nHHL solver job failed")
                return
            else:
                # Get results for the first (and only) PUB
                pub_result = result[0]

                #--------------------------------------------------------------------------------------------
                # Get counts for the classical register with name "c"
                #
                # The class HHLAlgorithm in hhl_algorithm_1bit.py sets-up a classical register with name "c"
                #   self.time_qr = QuantumRegister(self.num_time_qubits, "time")
                #   self.b_qr = QuantumRegister(self.num_system_qubits, "b")
                #   self.ancilla_qr = QuantumRegister(1, "ancilla")
                #   self.classical_reg = ClassicalRegister(1 + self.num_system_qubits, "c")
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
                #--------------------------------------------------------------------------------------------
                try:
                    counts = pub_result.data.c.get_counts()
                except:
                    print("Unable to get counts")
                    return

        # Exit if counts is None
        if counts is None:
            print("HHL solver job did not find a solution")
            return
            
        if do_print_counts:
            print("\nRaw Measurement Counts:")
            print(counts)
            print("")

        param["counts"] = counts

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

        # Extract the HHL solution (trimmed to the original dimension).
        x_hhl = hhl_solver.get_solution(counts=counts)

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

        #--------------------------------
        # Display found primary vertices
        #--------------------------------
        self.display_p_vertices()

        #-----------------------------------------------------------------------------------
        # Compare correct indices of HHL solution and correct indices of classical solution
        #-----------------------------------------------------------------------------------
        if correct_indices is not None and hhl_correct_indices is not None: 
            ok1 = (hhl_correct_indices == correct_indices)
            print("\nCorrect indices of HHL solution is equal to correct indices of classical solution:", ok1)

            #--------------------------------------------------------------------------------
            # Compare good indices of HHL solution and correct indices of classical solution
            #--------------------------------------------------------------------------------
            if not ok1 and hhl_good_indices is not None:
                print("\nGood indices of HHL solution:")
                print(hhl_good_indices)
                print("Good indices of HHL solution is equal to correct indices of classical solution:", hhl_good_indices == correct_indices)

        #------------------------------------------------------------
        # Display reconstructed tracks from discretized HHL solution
        #------------------------------------------------------------
        if display_tracks:
            print("\nReconstructed event tracks from discretized HHL solution")
            self.display_tracks(hhl_rec_tracks)

        #---------------------------------------------------------
        # Plot reconstructed tracks from discretized HHL solution
        #---------------------------------------------------------
        if plot_tracks:
            print("\nPlotting reconstructed event tracks from discretized HHL solution")
            self.plot_event(event, resolution)

        return
    
    #----------------------------------
    # Define function run_simulation()
    #----------------------------------
    def run_simulation(self):
        param = self.param

        self.classical_simulation()
        self.HHL_simulation()
        
        return