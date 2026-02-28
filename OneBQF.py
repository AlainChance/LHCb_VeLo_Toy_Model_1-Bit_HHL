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

#---------------------------------------------------------------------------------------
# Credit
# This is a modified version of the Python file OneBQF.py published here: 
# https://github.com/Xenofon-Chiotopoulos/OneBQF/blob/main/quantum_algorithms/OneBQF.py
#---------------------------------------------------------------------------------------

#--------------------------------------------------------------------------------
# Modifications by Alain Chancé in class OneBQF
# In Qiskit v2.2.2, there is a known bug with qpy that causes 
# an `IndexError: index out of range` if a register starts with the name ancilla
# Changed the register name "ancilla" to "qr_ancilla" as follows:
#self.ancilla_qr = QuantumRegister(1, "ancilla")
# self.ancilla_qr = QuantumRegister(1, "qr_ancilla")
#-------------------------------------------------------------------------------

import numpy as np
import math
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile
from qiskit_aer import AerSimulator
from qiskit.circuit.library import QFT, RXGate
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel
from qiskit_ibm_runtime import QiskitRuntimeService
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager

class OneBQF:
    def __init__(self, matrix_A, vector_b, num_time_qubits=1, shots=1024, debug=False):
        A = matrix_A
        self.original_dim = A.shape[0]
        self.debug = debug

        d = self.original_dim
        n_needed = math.ceil(np.log2(d))
        padded_dim = 2 ** n_needed
        if padded_dim != d:
            A_padded = np.zeros((padded_dim, padded_dim))
            A_padded[:d, :d] = A
            for i in range(d, padded_dim):
                diagonal_value = np.diag(A)[0]
                A_padded[i, i] = diagonal_value
            A = (A_padded + A_padded.conj().T) / 2

            b_padded = np.ones(padded_dim)
            b_padded[:d] = vector_b
            vector_b = b_padded

        b_normalized = vector_b / np.linalg.norm(vector_b)

        self.A = A
        self.vector_b = b_normalized
        self.num_time_qubits = num_time_qubits
        self.shots = shots

        self.system_dim = A.shape[0]
        self.num_system_qubits = int(np.log2(self.system_dim))

        self.time_qr = QuantumRegister(self.num_time_qubits, "time")
        self.b_qr = QuantumRegister(self.num_system_qubits, "b")
        #--------------------------------------------------------------------------------
        # Modified by Alain Chancé
        # In Qiskit v2.2.2, there is a known bug with qpy that causes 
        # an `IndexError: index out of range` if a register starts with the name ancilla
        # Changed the register name "ancilla" to "qr_ancilla" as follows:
        #self.ancilla_qr = QuantumRegister(1, "ancilla")
        self.ancilla_qr = QuantumRegister(1, "qr_ancilla")
        #--------------------------------------------------------------------------------
        self.classical_reg = ClassicalRegister(1 + self.num_system_qubits, "c")

        self.circuit = None
        self.counts = None

        diagonal = np.diag(self.A)
        off_diagonal_sums = np.sum(np.abs(self.A), axis=1) - np.abs(diagonal)
        
        #lambda_min_estimate = np.min(diagonal - off_diagonal_sums)
        #lambda_max_estimate = np.max(diagonal + off_diagonal_sums)
        #self.t = np.pi / ((lambda_min_estimate + lambda_max_estimate)/2)
        self.t = np.pi / A[0,0]  # Using the diagonal value for time scaling

        if not np.all(np.diag(A) == np.diag(A)[0]):
            raise ValueError("Matrix A must have a constant diagonal for this scheme.")
        
        self.diagonal_val = np.diag(A)[0]
        B = self.diagonal_val * np.identity(self.system_dim) - self.A
        
        rows, cols = np.where(np.triu(B) != 0)
        self.interaction_pairs = list(zip(rows, cols))
        
        if self.debug:
            print("--- Automated Matrix Analysis ---")
            print(f"Diagonal Value (c): {self.diagonal_val}")
            print(f"Found {len(self.interaction_pairs)} interaction pair(s): {self.interaction_pairs}")
            print("---------------------------------")
    
    def _apply_direct_controlled_u(self, qc, control_qubit, target_qubits, power, inverse=False):
        """
        Implements e^{-i H_{ij} t} exactly using Two-Level Unitary decomposition (Givens Rotation).
        This works for ANY Hamming distance and prevents spectral leakage (Ghost Couplings).
        """
        evolution_time = self.t * power
        theta = 2 * evolution_time
        
        if inverse:
            theta = -theta

        for i, j in self.interaction_pairs:
            xor_val = i ^ j
            differing_indices = [k for k in range(self.num_system_qubits) if (xor_val >> k) & 1]
            if not differing_indices: continue
            pivot = differing_indices[0]
            rest_diff = differing_indices[1:]

            for k in rest_diff:
                qc.cx(target_qubits[pivot], target_qubits[k])

            i_transformed = i
            for k in rest_diff:
                if (i_transformed >> pivot) & 1:
                    i_transformed ^= (1 << k)

            qubits_to_flip = []
            full_control_list = [control_qubit]
            
            for k in range(self.num_system_qubits):
                if k == pivot: continue 
                
                bit_val = (i_transformed >> k) & 1
                
                full_control_list.append(target_qubits[k])
                
                if bit_val == 0:
                    qubits_to_flip.append(target_qubits[k])

            if qubits_to_flip: qc.x(qubits_to_flip)
            mcrx = RXGate(theta).control(len(full_control_list))
            qc.append(mcrx, full_control_list + [target_qubits[pivot]])
            if qubits_to_flip: qc.x(qubits_to_flip)
            for k in reversed(rest_diff):
                qc.cx(target_qubits[pivot], target_qubits[k])
        phase = -self.diagonal_val * evolution_time
        if inverse: phase = -phase
        qc.p(phase, control_qubit)

    def apply_controlled_u(self, qc, control_qubit, target_qubits, power, inverse=False):
        self._apply_direct_controlled_u(qc, control_qubit, target_qubits, power, inverse=inverse)

    def inverse_qft(self, n_qubits):
        return QFT(n_qubits, do_swaps=True).inverse()

    def phase_estimation(self, qc):
        qc.h(self.time_qr)
        for i in range(self.num_time_qubits):
            power = 2**i
            self.apply_controlled_u(self.circuit, self.time_qr[self.num_time_qubits - 1 - i], list(self.b_qr), power)
        qc.append(self.inverse_qft(self.num_time_qubits).to_gate(label="IQFT"), self.time_qr)

    def uncompute_phase_estimation(self, qc):
        qc.append(QFT(self.num_time_qubits, do_swaps=True).to_gate(label="QFT"), self.time_qr)
        for i in reversed(range(self.num_time_qubits)):
            power = 2**i
            self.apply_controlled_u(self.circuit, self.time_qr[self.num_time_qubits - 1 - i], list(self.b_qr), power, inverse=True)
        qc.h(self.time_qr)

    def build_circuit(self):
        self.circuit = QuantumCircuit(self.time_qr, self.b_qr, self.ancilla_qr, self.classical_reg)
        self.circuit.h(self.b_qr)
        self.phase_estimation(self.circuit) 
        self.circuit.x(self.time_qr[0])
        self.circuit.cx(self.time_qr[0], self.ancilla_qr[0])
        self.circuit.x(self.time_qr[0])
        self.uncompute_phase_estimation(self.circuit)
        self.circuit.measure(self.ancilla_qr[0], self.classical_reg[0])
        self.circuit.measure(self.b_qr, self.classical_reg[1:])
        return self.circuit

    def run(self, use_noise_model=False, backend_name='ibm_torino'):
        """
        Run the circuit with optional noise model.
        
        Args:
            use_noise_model (bool): If True, uses the noise model from the specified backend
            backend_name (str): Name of the IBM backend to get noise model from
        """
        simulator = AerSimulator()
        
        if use_noise_model:
            # Load your IBM account (make sure you've saved your API token)
            
            service = QiskitRuntimeService()
            backend = service.backend(backend_name)
            noise_model = NoiseModel.from_backend(backend)
            basis_gates = noise_model.basis_gates
            
            print(f"\n--- Using {backend_name} Noise Model ---")
            print(f"Basis gates: {basis_gates}")
            print(f"Number of qubits: {backend.num_qubits}")
            
            pm = generate_preset_pass_manager(
                optimization_level=3,
                backend=backend
            )
            transpiled_circuit = pm.run(self.circuit)
            
            simulator = AerSimulator(noise_model=noise_model)
            job = simulator.run(transpiled_circuit, shots=self.shots)
                
        else:
            transpiled_circuit = transpile(self.circuit, simulator, optimization_level=3)
            job = simulator.run(transpiled_circuit, shots=self.shots)
        
        result = job.result()
        self.counts = result.get_counts()
        return self.counts

    def get_solution(self, counts=None):
        if counts: self.counts = counts
        if not self.counts: raise ValueError("No measurement results available.")
        total_success, prob_dist = 0, np.zeros(2**self.num_system_qubits)

        for outcome, count in self.counts.items():
            if outcome[-1] == '1':
                system_bits = outcome[:-1]#[::-1]
                index = int(system_bits, 2)
                prob_dist[index] += count
                total_success += count

        if total_success == 0: return np.zeros(self.original_dim)
        prob_dist /= np.sum(prob_dist)
        solution_padded = np.sqrt(prob_dist)
        solution_padded /= np.linalg.norm(solution_padded)
        return solution_padded[:self.original_dim], total_success