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
# Alain Chancé has contributed the functions setup_backend() and check_size() and the 
# code "Run the 1-Bit HHL simulation circuit" in the function run_simulation()
#-------------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------------------
## References
# Xenofon Chiotopoulos, TrackHHL: A Quantum Computing Algorithm for Track Reconstruction at the LHCb,
# CHEP 2024, 21 Oct 2024, 
# https://indico.cern.ch/event/1338689/contributions/6010017/
#-----------------------------------------------------------------------------------------------------

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

# HHL algorithm
from hhl_algorithm import HHLAlgorithm as hhl

# 1-Bit HHL algorithm
from hhl_algorithm_1bit import HHLAlgorithm as hhl_1
from hhl_algorithm_1bit import add_suzuki_trotter_to_class

# Patching HHLAlgorithm with Suzuki-Trotter methods...
hhl_1 = add_suzuki_trotter_to_class(hhl_1)

import psutil
import os

import numpy as np
import matplotlib.pyplot as plt

import scipy as sci
import scipy.sparse as ss

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
                 do_draw = False,                   # Whether to draw the HHL circuit
                 num_time_qubits = 2,               # Number of time qubits
                 measurement_error = 0.0,           # HIT RESOLUTION (sigma on measurement) (sigma)
                 collision_noise = 0.0,             # MULTIPLE SCATTERING (angular noise proxy)
                 ghost_rate = 1e-2,                 # ghost (fake) track rate
                 drop_rate = 0.0,                   # hit drop (inefficiency) rate
                 display_tracks = True,             # Whether to display events and ghost tracks
                 #------------------------------------------
                 # Files containing token (API key) and CRN
                 #------------------------------------------
                 token_file = "Token.txt",           # Token file
                 CRN_file = "CRN.txt",               # CRN file
                 #-------------
                 # Run options
                 #-------------
                 backend_name = None,                # IBM cloud backend name
                 run_on_QPU = False,                 # Whether to run the quantum circuit on the target hardware
                 nshots = 1e7,                       # Number of shots
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
        print("do_draw:", do_draw)
        print("num_time_qubits:", num_time_qubits)
        print("measurement hit resolution:", measurement_error)
        print("multiple scattering collision noise:", collision_noise)
        print("ghost (fake) track rate:", ghost_rate)
        print("hit drop (inefficiency) rate:", drop_rate)
        print("display_tracks:", display_tracks)

        #-------------------
        # Print run options
        #-------------------
        print("Backend name:", backend_name)
        print("Run on QPU:", run_on_QPU)
        print("Number of shots:", nshots)

        #-------------------------
        # Set up param dictionary
        #-------------------------
        self.param = {
            #--------------------
            # Simulation options
            #--------------------
            "dz": dz,                                        # layer spacing (mm)
            "layers": layers,                                # Number of layers
            "n_particles": n_particles,                      # Number of particles
            "do_draw": do_draw,                              # Whether to draw the HHL circuit
            "num_time_qubits": num_time_qubits,              # Number of time qubits
            "measurement_error": measurement_error,          # HIT RESOLUTION (sigma on measurement) (sigma)
            "collision_noise": collision_noise,              # MULTIPLE SCATTERING (angular noise proxy)
            "ghost_rate": ghost_rate,                        # ghost (fake) track rate
            "drop_rate": drop_rate,                          # hit drop (inefficiency) rate
            "display_tracks": display_tracks,                # Whether to display events and ghost tracks
            #------------------------------------------
            # Files containing token (API key) and CRN
            #------------------------------------------
            "token_file": token_file,                        # Token file
            "CRN_file": CRN_file,                            # CRN file
            #-------------
            # Run options
            #-------------
            "backend_name": backend_name,                    # IBM cloud backend name
            "run_on_QPU": run_on_QPU,                        # Whether to run the quantum circuit on the target hardware
            "nshots": nshots,                                # Number of shots
            "opt_level":opt_level,                           # Optimization level
            "poll_interval": poll_interval,                  # Poll interval in seconds for job monitor
            "timeout": timeout,                              # Time out in seconds for gob monitor
            #------------------
            # Shared variables
            #------------------
            "n_qubits": 2,                                   # Number of qubits in the HHL circuit, set by function run_HHL()
            "event_tracks": None,
            "false_tracks": None,
            "ham": None,
            "A": None,                                       # Hamiltonian matrix       
            "circuit": None,                                 # HHL Quantum circuit returned by function run_HHL()
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

    def setup_backend(self):
        #-------------------------------------
        # Define the function setup_backend()
        # Author: Alain Chancé
        #-------------------------------------
        
        #-------------------------------------------------------------------------------------------
        # Instantiate the service
        # Once the account is saved on disk, you can instantiate the service without any arguments:
        # https://docs.quantum.ibm.com/api/migration-guides/qiskit-runtime
        #-------------------------------------------------------------------------------------------
        try:
            service = QiskitRuntimeService()
        except:
            service = None

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
            
    #----------------------------------------------
    # Define function setup_events()
    # Adapted from the Jupyter notebook test.ipynb
    #----------------------------------------------
    def setup_events(self):
        param = self.param
        dz = param["dz"]
        layers = param["layers"]
        n_particles = param["n_particles"]
        measurement_error = param["measurement_error"]
        collision_noise = param["collision_noise"]
        drop_rate = param["drop_rate"]
        ghost_rate = param["ghost_rate"]
        display_tracks = param["display_tracks"]
        
        events = len(n_particles)
        n = np.sum(n_particles)

        module_id = [l for l in range(1, layers+1)]
        lx = [33 for x in range(1, layers+1)]
        ly = [33 for x in range(1, layers+1)]
        zs = [dz*l for l in range(1, layers+1)]

        Detector = state_event_model.PlaneGeometry(module_id=module_id,lx = lx,ly = ly,z = zs)
        # Detector = state_event_model.RectangularVoidGeometry(module_id=module_id,lx = lx,ly = ly,z=zs, void_x_boundary=5, void_y_boundary=5)

        # --- State event generator setup ---
        state_event_gen = StateEventGenerator(Detector, 
                                              events = events,
                                              n_particles = n_particles,
                                              measurement_error = measurement_error,
                                              collision_noise = collision_noise
                                             )

        # Random primary vertices (unit box extents in x,y,z)
        state_event_gen.generate_random_primary_vertices({'x': 0, 'y': 0, 'z': 0})

        # Particle species definition (all identical MIPs here)
        event_particles = []
        for event in range(events):
            particles_list = []
            for particle in range(n):
                particle_dict = {
                    'type' : 'MIP',
                    'mass': 0.511,
                    'q': 1
                }
                particles_list.append(particle_dict)
            event_particles.append(particles_list)

        # Generate truth particles and full event (hits + associations)
        state_event_gen.generate_particles(event_particles)
        event_tracks = state_event_gen.generate_complete_events()
        param["event_tracks"] = event_tracks 

        # --- Inject noise into events (ghost hits/tracks & dropped hits) ---
        false_tracks = state_event_gen.make_noisy_event(drop_rate=drop_rate, ghost_rate=ghost_rate)
        param["false_tracks"] = false_tracks

        if display_tracks:
            event_tracks.plot_segments()
            false_tracks.plot_segments()

        print("Event tracks hits:", len(event_tracks.modules[0].hits))
        print("False tracks hits:", len(false_tracks.modules[0].hits))
        
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

    #----------------------------------------------
    # Define function setup_Hamiltonian()
    # Adapted from the Jupyter notebook test.ipynb
    #----------------------------------------------
    def setup_Hamiltonian(self):
        param = self.param
        event_tracks = param["event_tracks"]
        
        ham = SimpleHamiltonian(epsilon=1e-7, gamma=2.0, delta=1.0)
        param["ham"] = ham

        ham.construct_hamiltonian(event=event_tracks, convolution=False)
        
        classical_solution = ham.solve_classicaly()
        T = .45
        discretized_classical_solution = (classical_solution > T).astype(int)
        param["discretized_classical_solution"] = discretized_classical_solution
        
        A = ham.A.todense()
        param["A"] = A

        print("Shape of Hamiltonian matrix A:", np.shape(A))
        
        self.plot_heat_map(A)

        print("Eigenvalues of Hamiltonian matrix A:")
        print(np.abs(np.linalg.eigvals(A)))

        return

    #----------------------------------------------
    # Define function analyze_solution_spectrum()
    # Adapted from the Jupyter notebook test.ipynb
    # Classically computes the exact solution to Ax=b and decomposes it
    # into components based on the eigenvalues of A, with added debugging prints.
    #----------------------------------------------
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
    
    #----------------------------------
    # Define function run_simulation()
    #----------------------------------
    def run_simulation(self):
        param = self.param
        A = param["A"]
        num_time_qubits = param["num_time_qubits"]
        nshots = param["nshots"]
        do_draw = param["do_draw"]
        false_tracks = param["false_tracks"]
        discretized_classical_solution = param["discretized_classical_solution"]
        ham = param["ham"]
        
        matrix_A = A
        vector_b = np.ones(len(A))

        #--------------------------------------------
        # Solve classically using Numpy linalg.solve
        #--------------------------------------------
        print("\n----------------------------------")
        print(" Solving classical Hamiltonian...")
        print("----------------------------------")
        print("Solving Ax = b with:")
        print("A =")
        print(matrix_A)
        print("b =")
        print(vector_b)

        # Compute the theoretical solution for comparison (using the original system, not the padded one).
        x_exact = np.linalg.solve(matrix_A, vector_b)
        print("\nExact solution:")
        print(x_exact)

        x_exact_disc = (x_exact > 0.4).astype(int)
        correct_indices = set(np.nonzero(x_exact_disc)[0])
        print("\nCorrect indices (items exact solution > 0.4):")
        print(np.array2string(np.nonzero(x_exact_disc)[0], separator=', ', formatter={'int': lambda x: f"{x:2d}"}))

        #---------------------------
        # Analyze solution spectrum
        #---------------------------
        self.analyze_solution_spectrum(np.array(matrix_A), np.array(vector_b))

        #-------------------------------------------------
        # Compute and print event validation matrix table
        #-------------------------------------------------
        truth_event = false_tracks
        rec_tracks = get_tracks(ham, discretized_classical_solution, false_tracks) 
        validator = evl(truth_event, rec_tracks)
        print("")
        validator.print_metrics()
        print("")

        #-------------------------------
        # Return if run_on_QPU is False
        #-------------------------------
        if not param['run_on_QPU']:
            return None

        print("\n----------------------")
        print(" 1-Bit HHL simulation")
        print("----------------------")
        
        #------------------------------------------
        # 1-Bit HHL simulation
        # Create an instance of the HHL algorithm.
        #------------------------------------------
        hhl_solver = hhl_1(matrix_A, vector_b, num_time_qubits=num_time_qubits, shots=nshots)

        # Build the HHL circuit
        circuit = hhl_solver.build_circuit()
        self.param['circuit'] = circuit

        if do_draw:
            # Draw the circuit using matplotlib
            fig = circuit.draw(output="mpl")

            # Display the figure
            display(fig)

            # Save the figure to a file
            fig.savefig("HHL_circuit.png", bbox_inches='tight')

        self.param["n_qubits"] = circuit.num_qubits
        print("\nNumber of qubits in HHL circuit: ", circuit.num_qubits)

        #-------------------------------------------
        # Run the 1-Bit HHL simulation circuit.
        # Commented out by Alain Chancé
        # counts = hhl_solver.run()
        # Below code is contributed by Alain Chancé
        #-------------------------------------------

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

            if result is not None:
                # Get results for the first (and only) PUB
                pub_result = result[0]
                                
                # Get counts from the result
                # https://docs.quantum.ibm.com/migration-guides/qiskit-runtime-examples#2-get-counts-from-the-result
                counts = pub_result.data.meas.get_counts()

            else:
                print("\nHHL solver job failed")
                return
        
        print("\nRaw Measurement Counts:")
        print(counts)
        print("")

        # Update hhl_solver property counts
        hhl_solver.counts = counts

        # Extract the HHL solution (trimmed to the original dimension).
        x_hhl = hhl_solver.get_solution(counts=counts)

        if x_hhl is None:
            print("HHL solver did not find a solution")
            return
            
        print("\nExtracted HHL solution (normalized):")
        print(x_hhl)

        #----------------------------------
        # Analyze measurement counts
        # Copied from George_Sandbox.ipynb
        #----------------------------------
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

        #---------------------------------------------
        # List of correct indices of the HHL solution
        # Author: Alain Chancé
        #---------------------------------------------
        x_hhl_disc = (x_hhl > 0).astype(int)
        hhl_correct_indices = set(np.nonzero(x_hhl_disc)[0])
        print("\nHHL solution correct indices (items > 0):")
        print(np.array2string(np.nonzero(x_hhl_disc)[0], separator=', ', formatter={'int': lambda x: f"{x:2d}"}))

        #-------------------------------------------------------------------------------------------
        # Check that list of correct indices of the HHL solution and of the exact solution are equal
        # Author: Alain Chancé
        #-------------------------------------------------------------------------------------------
        print("\ncorrect_indices == hhl_correct_indices:", correct_indices == hhl_correct_indices)

        return