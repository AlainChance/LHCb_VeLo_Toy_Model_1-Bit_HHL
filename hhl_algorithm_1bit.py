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
# This is a modified version of the Python file hhl_algorithm_1bit.py, 
# https://github.com/GeorgeWilliam1999/LHCb_VeLo_Toy_Model/blob/main/hhl_algorithm_1bit.py 
# owned by George William Scriven, GeorgeWilliam1999, https://orcid.org/0009-0004-9997-1647
#-------------------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
# Modifications by Alain Chancé in class HHLAlgorithm
#
# In __init()__ 
# Added:
#   keywords: gain=0.3, lam_s=6, angle_pi=True, max_abs_eigen=4, do_draw=False
#
#   self.gain = gain
#   self.lam_s = lam_s
#   self.angle_pi = angle_pi
#   self.max_abs_eigen = max_abs_eigen
#   self.t = np.pi / self.max_abs_eigen

# Commented out:
#   self.eigenvalues = np.linalg.eigvals(self.A_orig)
#   self.eigenvalues_scaled = np.linalg.eigvals(self.A)
#
# In build_circuit(), 
# added:
#   lam = round(lam)
# modified:
#   if abs(lam) > self.lam_s or abs(lam) < self.lam_s
# 
# In run_with_noise_simulation(), removed credentials
#-------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------------------
## References
# Xenofon Chiotopoulos, TrackHHL: A Quantum Computing Algorithm for Track Reconstruction at the LHCb,
# CHEP 2024, 21 Oct 2024, 
# https://indico.cern.ch/event/1338689/contributions/6010017/
#-----------------------------------------------------------------------------------------------------
import numpy as np
import math
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile
from qiskit.visualization import plot_histogram
from qiskit_aer import AerSimulator
from qiskit.circuit.library import QFT, RYGate, UnitaryGate
from scipy.linalg import expm

from qiskit.quantum_info import SparsePauliOp
from qiskit.circuit.library import PauliEvolutionGate
from qiskit.synthesis import QDrift, LieTrotter, SuzukiTrotter

def add_suzuki_trotter_to_class(HHLAlgorithmClass):
    
    def _create_trotter_gate(self, evolution_time, trotter_steps=1, order=0):
        if not hasattr(self, '_pauli_A'):
            self._pauli_A = SparsePauliOp.from_operator(self.A)

        if order == 1:
            synthesis_method = LieTrotter(reps=trotter_steps)
        if order == 0:
            synthesis_method = QDrift(reps=trotter_steps)
        else:
            synthesis_method = SuzukiTrotter(reps=trotter_steps, order=2)

        trotter_gate = PauliEvolutionGate(self._pauli_A, 
                                          time=evolution_time, 
                                          synthesis=synthesis_method)
        return trotter_gate

    def _apply_trotter_controlled_u(self, qc, control_qubit, target_qubits, power, trotter_steps=1, order=2):
        evolution_time = self.t * power
        trotter_gate = self._create_trotter_gate(evolution_time, trotter_steps, order)
        controlled_trotter = trotter_gate.control(1, label=f"C-Trot(t={evolution_time:.1f})")
        qc.append(controlled_trotter, [control_qubit] + target_qubits)

    # Replace the class's original apply_controlled_u with our new one
    print("Patching HHLAlgorithm with Suzuki-Trotter methods...")
    HHLAlgorithmClass._create_trotter_gate = _create_trotter_gate
    HHLAlgorithmClass.apply_controlled_u = _apply_trotter_controlled_u
    
    return HHLAlgorithmClass

class HHLAlgorithm:
    # Modified by Alain Chancé
    #def __init__(self, matrix_A, vector_b, num_time_qubits=5, shots=1024, debug=False):
    def __init__(self, matrix_A, vector_b, num_time_qubits=5, gain=0.3, lam_s=6, angle_pi=True, max_abs_eigen=4, shots=1024, debug=False, do_draw=False):
        A = matrix_A
        self.original_dim = A.shape[0]
        self.debug = debug
        #----------------------------------
        # Added by Alain Chancé
        self.gain = gain
        self.lam_s = lam_s
        self.angle_pi = angle_pi
        self.max_abs_eigen = max_abs_eigen
        #----------------------------------

        d = self.original_dim
        n_needed = math.ceil(np.log2(d))
        padded_dim = 2 ** n_needed

        if padded_dim != d:
            A_padded = np.zeros((padded_dim, padded_dim), dtype=complex)
            A_padded[:d, :d] = A
            A = (A_padded + A_padded.conj().T) / 2

            b_padded = np.zeros(padded_dim, dtype=complex)
            b_padded[:d] = vector_b
            vector_b = b_padded

        b_normalized = vector_b / np.linalg.norm(vector_b)

        self.A_orig = A.copy()
        self.A_norm = np.linalg.norm(A)
        #A = A / self.A_norm

        self.A = A
        self.vector_b = b_normalized
        self.num_time_qubits = num_time_qubits
        self.shots = shots

        self.system_dim = A.shape[0]
        self.num_system_qubits = int(np.log2(self.system_dim))

        self.time_qr = QuantumRegister(self.num_time_qubits, "time")
        self.b_qr = QuantumRegister(self.num_system_qubits, "b")
        self.ancilla_qr = QuantumRegister(1, "ancilla")
        self.classical_reg = ClassicalRegister(1 + self.num_system_qubits, "c")

        self.circuit = None
        self.counts = None

        # Modified by Alain Chancé
        #self.t = np.pi / np.max(np.abs(np.linalg.eigvals(A)))
        self.t = np.pi / self.max_abs_eigen

        # Commented out by Alain Chancé
        #self.eigenvalues = np.linalg.eigvals(self.A_orig)
        #self.eigenvalues_scaled = np.linalg.eigvals(self.A)

    def create_input_state(self):
        qc_b = QuantumCircuit(self.num_system_qubits)
        qc_b.initialize(self.vector_b, list(range(self.num_system_qubits)))
        return qc_b

    def apply_controlled_u(self, qc, matrix, control, target, power):
        U = expm(1j * matrix * self.t * power)
        controlled_U = UnitaryGate(U).control(1)
        qc.append(controlled_U, [control] + target)
        return qc

    def inverse_qft(self, n_qubits):
        return QFT(n_qubits, do_swaps=True).inverse()

    def phase_estimation(self, qc):
        for qubit in self.time_qr:
            qc.h(qubit)

        for i in range(self.num_time_qubits):
            power = 2 ** i
            self.apply_controlled_u(qc, self.time_qr[self.num_time_qubits - i - 1], list(self.b_qr), power)

        iqft = self.inverse_qft(self.num_time_qubits).to_gate(label="IQFT")
        qc.append(iqft, self.time_qr[:])

    def uncompute_phase_estimation(self, qc):
        qft = QFT(self.num_time_qubits, do_swaps=True).to_gate(label="QFT")
        qc.append(qft, self.time_qr[:])

        for i in reversed(range(self.num_time_qubits)):
            power = 2 ** i
            self.apply_controlled_u(qc, self.time_qr[self.num_time_qubits - i - 1], list(self.b_qr), power)

        for qubit in self.time_qr:
            qc.h(qubit)

    def build_circuit(self):
        qc = QuantumCircuit(self.time_qr, self.b_qr, self.ancilla_qr, self.classical_reg)

        #qc.compose(self.create_input_state(), qubits=list(self.b_qr), inplace=True)
        for qubit in self.b_qr:
            qc.h(qubit)
            
        self.phase_estimation(qc)

        #--------------------------
        # Modified by Alain Chancé
        #gain = 0.3
        gain = self.gain
        #--------------------------
        
        #n_time = self.num_time_qubits
        
        for i in range(2 ** self.num_time_qubits):
            #phase = i / (2 ** n_time)
            #if phase >= 0.5:
            #    phase = phase - 1.0
            #print(self.t)
            #print(np.max(np.linalg.eigvals(self.A)))

            phase = i / (2 ** self.num_time_qubits)
            lam = 2 * np.pi * phase / self.t

            #-----------------------
            # Added by Alain Chancé
            lam = round(lam)
            #-----------------------
            
            #------------------------------------------------------------
            # Modified by Alain Chancé
            #if abs(lam) > 6 or abs(lam) < 6:#1e-9:# or abs(lam) > 10.0:
            if abs(lam) > self.lam_s or abs(lam) < self.lam_s:
                continue
            #------------------------------------------------------------

            inv_lam = 1.0 / lam

            if self.angle_pi:
                angle = np.pi
            else:
                angle = 2 * np.arcsin(min(1, gain * inv_lam / 2))
                print("gain:", gain, " angle:", angle)
                
            controls = list(self.time_qr)

            bits = format(i, f"0{self.num_time_qubits}b")
            for j, bit in enumerate(bits):
                if bit == '0':
                    qc.x(self.time_qr[j])

            cry = RYGate(angle).control(num_ctrl_qubits=self.num_time_qubits)
            qc.append(cry, [*controls, self.ancilla_qr[0]])

            for j, bit in enumerate(bits):
                if bit == '0':
                    qc.x(self.time_qr[j])

        self.uncompute_phase_estimation(qc)

        # https://quantum.cloud.ibm.com/docs/en/guides/measure-qubits
        qc.measure(self.ancilla_qr[0], self.classical_reg[0])
        qc.measure(self.b_qr, self.classical_reg[1:])

        self.circuit = qc
        return qc

    def run(self):
        simulator = AerSimulator()
        transpiled_circuit = transpile(self.circuit, simulator, optimization_level=3)
        job = simulator.run(transpiled_circuit, shots=self.shots)
        result = job.result()
        self.counts = result.get_counts()
        return self.counts
    
    def run_with_noise_simulation(self, backend_name="ibm_brisbane"):
        print(f"\n--- Starting Noisy Simulation based on '{backend_name}' ---")

        try:
            # Step 1: Connect to the service and get the real backend object
            print("Connecting to IBM Quantum to fetch backend properties...")
            # This uses your saved IBM Cloud credentials
            from qiskit_ibm_runtime import QiskitRuntimeService
            #-------------------------------------------------------------------------------------------
            # Modified by Alain Chancé
            # Instantiate the service
            # Once the account is saved on disk, you can instantiate the service without any arguments:
            # https://docs.quantum.ibm.com/api/migration-guides/qiskit-runtime
            #-------------------------------------------------------------------------------------------
            service = QiskitRuntimeService()
            
            real_backend = service.backend(backend_name)
            print(f"Successfully fetched properties for '{backend_name}'.")

            # Step 2: Create a simulator from the real backend's properties
            # This automatically configures the simulator with the noise model,
            # coupling map, and basis gates of the real device.
            print("Creating noise model and configured simulator...")
            from qiskit_aer import AerSimulator
            noisy_simulator = AerSimulator.from_backend(real_backend)
            
            # Step 3: Transpile the circuit for the real backend
            # This is crucial. It rewrites the circuit to use the correct gates
            # and adds SWAP gates to handle qubit connectivity.
            print(f"Transpiling circuit for '{backend_name}' architecture...")
            # Using optimization_level=3 is recommended for performance
            transpiled_circuit = transpile(self.circuit, backend=real_backend, optimization_level=3)
            
            print(f"Ideal depth: {self.circuit.depth()} -> Transpiled depth: {transpiled_circuit.depth()}")

            # Step 4: Run the simulation on the configured noisy simulator
            print(f"Running simulation with {self.shots} shots...")
            job = noisy_simulator.run(transpiled_circuit, shots=self.shots)
            result = job.result()
            self.counts = result.get_counts()
            
            print("Noisy simulation finished.")
            return self.counts

        except Exception as e:
            print(f"\nAn error occurred during the noisy simulation: {e}")
            print("Please ensure your IBM Cloud credentials are saved and you have the necessary packages installed.")
            return None

    def get_solution(self, counts = None):
        if self.counts is None and counts is None:
            raise ValueError("No measurement results available. Run run() first.")
        if counts is not None:
            self.counts = counts
        total_success = 0
        padded_dim = 2 ** self.num_system_qubits
        prob_dist = np.zeros(padded_dim)

        for outcome, count in self.counts.items():
            if outcome[-1] == '1':
                print(f"Outcome: {outcome}, Count: {count}")
                #print(outcome[:-1])
                system_bits = outcome[:-1]#[::-1]
                #print(f"System bits: {system_bits}")
                index = int(system_bits, 2)
                prob_dist[index] += count
                total_success += count

        if total_success == 0:
            print("No valid solution: ancilla was never measured as |1⟩.")
            return None

        print('Total success:', total_success/len(self.counts))
        prob_dist = prob_dist / total_success
        solution_padded = np.sqrt(prob_dist)
        solution_padded = solution_padded / np.linalg.norm(solution_padded)

        solution_vector = solution_padded[:self.original_dim]
        solution_vector = solution_vector #/ np.linalg.norm(solution_vector)
        #solution_vector = solution_vector / self.A_norm
        return solution_vector

    def plot_results(self, filename="hhl_results.png"):
        if self.counts is None:
            raise ValueError("No measurement results available. Run run() first.")
        plot_histogram(self.counts)
        plt.title("HHL Algorithm Results")
        plt.savefig(filename)
        print(f"Results histogram saved as '{filename}'.")

    def simulate_statevector(self):
        from qiskit_aer import Aer
        backend = Aer.get_backend("statevector_simulator")
        job = backend.run(transpile(self.circuit, backend))
        statevector = job.result().get_statevector()
        return statevector

    def extract_postselected_solution(self, statevector):
        dim = 2 ** (self.num_time_qubits + self.num_system_qubits + 1)
        total_qubits = self.num_time_qubits + self.num_system_qubits + 1
        system_qubits = self.num_system_qubits
        ancilla_index = self.num_time_qubits + self.num_system_qubits

        probs = np.abs(statevector.data) ** 2
        sol = np.zeros(2 ** system_qubits)

        for i, amp in enumerate(statevector.data):
            if ((i >> ancilla_index) & 1) == 1:
                system_state = (i >> 0) & ((1 << system_qubits) - 1)
                sol[system_state] += np.abs(amp) ** 2

        sol = np.sqrt(sol)
        sol = sol / np.linalg.norm(sol)
        return sol


if __name__ == "__main__":
    matrix_A = np.array([[ 3.        ,  0.        ,  0.        ,  0.        , -1,
                            0.        ,  0.        ,  0.        ],
                            [ 0.        ,  3.        ,  0.        ,  0.        ,  0.        ,
                            0.        ,  0.        ,  0.        ],
                            [ 0.        ,  0.        ,  3.        ,  0.        ,  0.        ,
                            0.        ,  0.        ,  0.        ],
                            [ 0.        ,  0.        ,  0.        ,  3.        ,  0.        ,
                            0.        ,  0.        , -1],
                            [-1,  0.        ,  0.        ,  0.        ,  3.        ,
                            0.        ,  0.        ,  0.        ],
                            [ 0.        ,  0.        ,  0.        ,  0.        ,  0.        ,
                            3.        ,  0.        ,  0.        ],
                            [ 0.        ,  0.        ,  0.        ,  0.        ,  0.        ,
                            0.        ,  3.        ,  0.        ],
                            [ 0.        ,  0.        ,  0.        , -1,  0.        ,
                            0.        ,  0.        ,  3.        ]])

    vector_b = np.array([1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]) 

    HHLAlgorithm = add_suzuki_trotter_to_class(HHLAlgorithm)

    hhl_solver = HHLAlgorithm(matrix_A, vector_b, num_time_qubits=2, shots=16000, debug=True)
    circuit = hhl_solver.build_circuit()
    
    #--------------------------------------------------------------
    # Modified by Alain Chancé
    #print(circuit.draw(output="text"))

    if do_draw:
        # Draw the circuit using matplotlib
        fig = circuit.draw(output="mpl")

        # Save the figure to a file
        fig.savefig("HHL_solver_circuit.png", bbox_inches='tight')
    #--------------------------------------------------------------

    #counts = hhl_solver.run_with_noise_simulation()
    counts = hhl_solver.run()

    #from pytket.utils import gate_counts
    #from pytket.extensions.qiskit import qiskit_to_tk

    #circuit_tk = qiskit_to_tk(circuit)
    #gate_counts(circuit_tk)

    print('counts:', counts)
    hhl_solver.plot_results("hhl_results.png")
    x_hhl = hhl_solver.get_solution()
    print("\nHHL Solution:", x_hhl)

    x_exact = np.linalg.solve(matrix_A, vector_b)
    x_exact_normalized = x_exact / np.linalg.norm(x_exact)
    print("\nExact Solution:", x_exact_normalized)

    if x_hhl is not None:
        fidelity = np.abs(np.vdot(x_hhl, x_exact_normalized))
        print(f"\nFidelity with exact solution: {fidelity:.4f}")
    
    circuit_depth = circuit.decompose().decompose().decompose().decompose().decompose().decompose().depth()
    gate_statistics = circuit.decompose().decompose().decompose().decompose().decompose().decompose().count_ops()
    print(f"The depth of the quantum circuit is: {circuit_depth}")
    print("Gate statistics for the circuit:")
    print(gate_statistics)

    #print("\nEigenvalues of original A:", np.round(hhl_solver.eigenvalues, 4))
    #print("Eigenvalues of scaled A (used in phase estimation):", np.round(hhl_solver.eigenvalues_scaled, 4))

    #print("\n[Debug] Running ideal statevector simulation...")
    #statevector = hhl_solver.simulate_statevector()
    #print("Final statevector (truncated):", statevector.data[:8])

    #post_selected = hhl_solver.extract_postselected_solution(statevector)
    #print("\nPostselected solution from statevector:", post_selected)
    #fidelity_post = np.abs(np.vdot(post_selected, x_exact_normalized))
    #print(f"Fidelity (postselected vs exact): {fidelity_post:.4f}")

    