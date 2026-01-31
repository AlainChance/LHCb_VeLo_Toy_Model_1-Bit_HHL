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

#----------------------------------------------------------------------------------------------------------------
# Credits
#
# This Python file is derived from the following sources:
#
# GitHub repository OneBQF, https://github.com/Xenofon-Chiotopoulos/OneBQF/tree/main 
# owned by Xenofon Chiotopoulos and more specifically:
#   - Module OneBQF.py, (https://github.com/Xenofon-Chiotopoulos/OneBQF/blob/main/quantum_algorithms/OneBQF.py
#   - Jupyter notebook example.ipynb, https://github.com/Xenofon-Chiotopoulos/OneBQF/blob/main/example.ipynb
#
# Jupyter notebook George_Sandbox.ipynb,
# https://github.com/GeorgeWilliam1999/LHCb_VeLo_Toy_Model/blob/main/George_Sandbox.ipynb 
# owned by George William Scriven, [GeorgeWilliam1999](https://orcid.org/0009-0004-9997-1647).
#
# Relevant documentation can be found in the Jupyter notebook example_notebook.ipynb,
# https://github.com/Xenofon-Chiotopoulos/Tracking_Toy_model/blob/main/example_notebook.ipynb.
# owned by Xenofon Chiotopoulos.
#----------------------------------------------------------------------------------------------------------------

#-------------------------------------------------------------------------------------------------------------------------------
# LHCb_VeLo_Toy_Model_1-Bit_HHL

## The Large Hadron Collider beauty (LHCb) experiment at CERN
# The LHCb Experiment at CERN is a general-purpose detector at the Large Hadron Collider (LHC) and specializes in
# investigating the slight differences between matter and antimatter by studying a type of particle called 
# the "beauty quark", or "b quark".

# It uses a series of subdetectors to detect mainly forward particles – those thrown forwards by the collision in one 
# direction. The first subdetector is mounted close to the collision point, with the others following one behind the other
# over a length # of 20 meters.
# The 5600-tonne LHCb detector is made up of a forward spectrometer and planar detectors. It is 21 meters long, 
# 10 meters high and 13 meters wide, # and sits 100 meters below ground near the town of Ferney-Voltaire, France. 

# As of 2024, more than 1600 members from 98 institutes in 22 countries, including 1100 authors.
# Source: https://home.cern/science/experiments/lhcb 

## Particle track reconstruction in the LHCb Vertex Locator (VELO)
# In the High Luminosity phase of the Large Hadron Collider (HL-LHC), thousands of particles are produced simultaneously. 
# Particles leave energy hits in detector layers. Hits are reconstructed into particle tracks. Tracks reveal Primary Vertices 
# (collision points). Tracks in the LHCb Vertex Locator (VELO) can be modeled as straight lines intersecting the z-axis 
# because it is the sub-detector closest to the LHCb collision point and it contains a negligible magnetic field.

## Classical sort-by-angle θ particle track reconstruction
# In the XY projection, these straight lines pass through the origin. As a result, energy hits are likely to have a constant
# phase in polar coordinates when projected onto the XY plane (see Section 3, *Search by triplet — Sort by φ*, in 
# [ALGO10](https://arxiv.org/pdf/2207.03936)).
#
# We have developed the following functions:
# - `cluster_by_last_column()`, which clusters hits by the last-column polar angle `theta` of an array of hits.
# - `segment_intersects_z_axis()`, which checks whether a line intersects the z-axis and finds the corresponding primary vertex.  
# - `find_tracks()`, which reconstructs tracks from these clusters and finds all primary vertices.

# Efficient Implementation
# This implementation uses only hits from the first three layers for both classical and 1-bit HHL simulations.

## Fast construction of the Hamiltonian H(S)
# The function `construct_segments` is enhanced to identify segments with matching values of `theta` during their creation
# and to append them to the list `segment_in_indices`, along with their corresponding segment IDs in the list `segment_indices`.
# The function `construct_hamiltonian` then considers only doublets S_i and S_j of segments in `segment_in_indices` 
# whose angular difference in `theta` is within epsilon. This modification significantly improves the performance 
# of the preprocessing step.

## Smart error detection and recovery
# The function `get_tracks_smart()` performs the following steps:
# - Identifies active segments in the first three layers from both the classical solution and the 1-bit HHL quantum solution.  
# - Reconstructs tracks using only segments that intersect the z-axis; their intersection points define the reconstructed 
# primary vertices.  
# - Adds missed segments intersecting the z-axis and extends active segments to all outer layers.
#-------------------------------------------------------------------------------------------------------------------------------

#----------------------------------------------------------------------------------------------------------------------------
## Energetics Analysis
# **Assumption:**
#  A ballpark estimate for a typical modern IBM-class superconducting quantum computer (including cryogenics and supporting
# infrastructure, while idle or lightly used) is approximately **15–25 kW**.
#  Source: Green Quantum Computing, Capgemini, 8 May 2023,
# https://www.capgemini.com/insights/expert-perspectives/green-quantum-computing/.

# The `One_Bit_HHL` class integrates the eco2AI,
# https://github.com/sb-ai-lab/Eco2AI tracking feature, a python library which
# accumulates statistics about power consumption and CO2 emission during running code. 
# The Eco2AI is licensed under a Apache licence #2.0, https://www.apache.org/licenses/LICENSE-2.0.
#----------------------------------------------------------------------------------------------------------------------------

#---------------------------------------------------------------------------------------------
# Additions by Alain Chancé
#
## This module defines a new class `One_Bit_HHL`.
#
# The following methods are copied from class SQD in SQD_Alain.py,
# https://github.com/AlainChance/SQD_Alain/blob/main/SQD_Alain.py:
# - setup_backend()
# - check_size()
# - get_QPU_usage()
# - get_classical_power_usage()

# The following method is derived from the module OneBQF/toy_model/simple_hamiltonian.py,
# https://github.com/Xenofon-Chiotopoulos/OneBQF/blob/main/toy_model/simple_hamiltonian.py:
#  - find_segments() derived from function find_segments()

# New methods:
# - cluster_by_last_column()
# - find_tracks()
# - gen_indices()
# - check_intersection()
# - intersects_origin()
# - intersects_z_axis()
# - segment_intersects_z_axis()
# - get_tracks_smart()
# - display_tracks()
# - display_p_vertices()
# - plot_event()
# - setup_Hamiltonian()
# - classical_simulation()
# - run_qc()
# - HHL_simulation()
# - run_simulation()
#---------------------------------------------------------------------------------------------

# Import common packages first
import psutil
import sys
import os
import time
import pandas as pd

import warnings

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
                 measurement_error = 0.0,           # HIT RESOLUTION (sigma on measurement) (sigma)
                 collision_noise = 0.0,             # MULTIPLE SCATTERING (angular noise proxy)
                 ghost_rate = 1e-2,                 # ghost (fake) track rate
                 drop_rate = 0.0,                   # hit drop (inefficiency) rate
                 display_particles = True,          # Whether to display initial particle states
                 display_hits = False,              # Whether to display hits
                 display_ghost_hits = False,        # Whether to display ghost hits
                 display_tracks = True,             # Whether to display events and ghost tracks
                 display_clusters = False,          # Whether to display clusters found by find_tracks()
                 display_false_clusters = False,    # Whether to display clusters rejected by find_tracks()
                 do_plot_tracks = True,             # Whether to plot events and ghost tracks
                 do_plot_heat_map = True,           # Whether to plot the heat map
                 do_solve_scipy = True,             # Whether to solve classically using scipy.sparse.linalg.cg
                 T_classical = 0.45,                # Threshold for discretizing classical solutions
                 T_hhl = None,                      # Threshold for discretizing 1-Bit HHL solutions - None: to be computed
                 do_spectrum = False,               # Whether to analyze the classical solution spectrum
                 do_print_counts = False,           # Whether to print raw measurement counts
                 do_print_outer_segs = False,       # Whether to print segments in modules greater than 3       
                 resolution = 25,                   # Resolution for plots of tracks - Increase for finer mesh
                 tol = 1e-6,                        # Tolerance for floating point comparison
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
                 run_on_QPU = True,                  # Whether to run the quantum circuit on the target hardware
                 nshots = 1000,                      # Number of shots
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

        # Initialize self.backend to None
        self.backend = None

        #--------------------------
        # Print simulation options
        #--------------------------
        print("\nSimulation options")
        print("layer spacing (mm), dz:", dz)
        print("layers:", layers)
        print(f"n_particles: {n_particles}, Total number: {sum(n_particles)}")
        print("primary_vertices:", p_vertices) 
        print("do_draw:", do_draw)
        print("measurement hit resolution:", measurement_error)
        print("multiple scattering collision noise:", collision_noise)
        print("ghost (fake) track rate:", ghost_rate)
        print("hit drop (inefficiency) rate:", drop_rate)
        print("display_particles:", display_particles)        # Whether to display initial particle states
        print("display_hits:", display_hits)                  # Whether to display hits
        print("display_ghost_hits:", display_ghost_hits)      # Whether to display ghost hits
        print("display_tracks:", display_tracks)              # Whether to display tracks
        print("display_clusters:", display_clusters)          # Whether to display clusters found by find_tracks()
        print("display_false_clusters:", display_false_clusters)    # Whether to display clusters rejected by find_tracks()
        print("do_plot_tracks:", do_plot_tracks)              # Whether to plot events and ghost tracks
        print("do_plot_heat_map:", do_plot_heat_map)          # Whether to plot the heat map
        print("do_solve_scipy:", do_solve_scipy)              # Whether to solve classically using scipy.sparse.linalg.cg
        print("T_classical:", T_classical)                    # Threshold for discretizing classical solutions
        print("T_hhl:", T_hhl)                                # Threshold for discretizing 1-Bit HHL solutions
        print("do_spectrum:", do_spectrum)
        print("do_print_counts:", do_print_counts)
        print("do_print_outer_segs", do_print_outer_segs)     # Whether to print segments in modules greater than 3
        print("resolution:", resolution)

        tol = min(max(1e-7, tol), 1e-5)                       # Restrict range from 1e-7 to 1e-5
        print("tol:", tol)

        #-------------------
        # Print run options
        #-------------------
        print("\nRun options")
        print("Backend name:", backend_name)
        
        if job_id is not None:
            print("job_id:", job_id)
        
        print("Run on QPU:", run_on_QPU)

        if run_on_QPU:
            nshots = min(max(1e3, nshots), 1e7)        # Restrict range from one thousand to 10 million
            print("Number of shots:", nshots)
        
        print("Optimization level:", opt_level)

        #-------------------------------------
        # Print eco2AI Tracker options
        # https://github.com/sb-ai-lab/Eco2AI
        #-------------------------------------
        if do_eco2ai:
            print("\neco2AI Tracker options")
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
            "measurement_error": measurement_error,          # HIT RESOLUTION (sigma on measurement) (sigma)
            "collision_noise": collision_noise,              # MULTIPLE SCATTERING (angular noise proxy)
            "ghost_rate": ghost_rate,                        # ghost (fake) track rate
            "drop_rate": drop_rate,                          # hit drop (inefficiency) rate
            "display_particles": display_particles,          # Whether to display initial particle states
            "display_hits": display_hits,                    # Whether to display hits
            "display_ghost_hits": display_ghost_hits,        # Whether to display ghost hits
            "display_tracks": display_tracks,                # Whether to display events and ghost tracks
            "display_clusters": display_clusters,            # Whether to display clusters found by find_tracks()
            "display_false_clusters": display_false_clusters,    # Whether to display clusters rejected by find_tracks()
            "do_plot_tracks": do_plot_tracks,                # Whether to plot events and ghost tracks
            "do_plot_heat_map": do_plot_heat_map,            # Whether to plot the heat map
            "do_solve_scipy": do_solve_scipy if isinstance(do_solve_scipy, bool) else True, # Whether to use scipy.sparse.linalg.cg
            "T_classical": T_classical if T_classical is not None else 0.45,  # Threshold for discretizing classical solutions
            "T_hhl": T_hhl,                                  # Threshold for discretizing 1-Bit HHL solutions
            "do_spectrum": do_spectrum,                      # Whether to analyze the classical solution spectrum
            "do_print_counts": do_print_counts,              # Whether to print raw measurement counts
            "do_print_outer_segs": do_print_outer_segs,      # Whether to print segments in modules greater than 3
            "resolution": resolution,                        # Resolution for plots of tracks - Increase for finer mesh
            "tol": tol,                                      # Tolerance for floating point comparison
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
            "found_tracks": [],                              # Found tracks computed by function find_tracks()
            "found_segments": [],                            # Found segments computed by function find_tracks()
            "found_thetas": set(),                           # Polar coordinates theta of all found tracks computed by function find_tracks()
            "found_event": None,                             # Reconstructed event by the function find_tracks()
            "modules": [],                                   # List of modules
            "rec_event": None,                               # Reconstructed event from discretized classical solution
            "hhl_rec_event": None,                           # Reconstructed event from discretized HHL solution
            "ham": None,                                     # Hamiltonian operator
            "segment_indices": [],                           # List of segment indices computed by the modified function construct_segments()
            "segment_in_indices": [],                        # List of segment with an id in segment_indices
            "A": None,                                       # Hamiltonian matrix       
            "circuit": None,                                 # HHL Quantum circuit returned by function HHL_simulation()
            "detector_geometry": None,                       # Geometry of the detector
            "found_p_vertices": [],                          # List of found primary vertices
            "true_hits": [],                                 # List of true hits computed by the function generate_complete_events()
            "hits":[],                                       # List of all true and ghost hits computed by the function make_noisy_event()
            "ghost_hits": [],                                # List of ghost hits computed by the function make_noisy_event()
            "counts": None,                                  # Raw measurement counts set by function HHL_simulation()
            "correct_indices": None,                         # Correct indices set by function classical_simulation()
            "hhl_correct_indices": None,                     # HHL correct indices set by function HHL_simulation
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

       #---------------------------------------------------------------
        # If a valid job_id is provided, then get the corresponding job
        #---------------------------------------------------------------
        job_id = param['job_id']
        if job_id is not None:
            try:
                param['job'] = service.job(job_id)
                print(f"Successfully retrieved job with job_id: {job_id}")
            except Exception as e:
                print(f"Error retrieving job with job_id {job_id}: {e}")
        
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

    #------------------------------------------------------------------------------------------------
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
    # Author: Alain Chancé
    #------------------------------------------------------------------------------------------------
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
    # - layers: number of layers
    # - tol: tolerance
    # - do_plot_tracks
    # - resolution
    # - display_tracks
    # - display_clusters
    # - display_false_clusters
    # - ghost_hits (future use)
    #
    # Returns in the parameter list:
    #  - List of found tracks from rows of an array of hits clustered around the polar coordinate theta.
    #  - List of found segments.
    #  - List of polar coordinates theta of all found tracks
    #  - Reconstructed event.
    #
    # Displays:
    #  - Number of found tracks and false clusters
    #  - List of found clusters.
    #  - List of false clusters rejected by the function find_tracks().
    #  - list of found tracks.
    #  - List of primary vertices.
    #
    # Calls
    #  - cluster_by_last_column()
    #  - display_tracks()
    #  - display_p_vertices()
    #
    # Author: Alain Chancé
    #----------------------------------------------------------------------------------------------------
    def find_tracks(self, list_hits):

        if self.param is None:
            print("find_tracks: missing parameter param")
            return None
        param = self.param

        layers = param["layers"]
        tol = param["tol"]
        do_plot_tracks = param["do_plot_tracks"]
        resolution = param["resolution"]
        display_tracks = param["display_tracks"]
        display_clusters = param["display_clusters"]
        display_false_clusters = param["display_false_clusters"]
        ghost_hits = param["ghost_hits"]

        if list_hits is None or list_hits == []:
            print("find_tracks: input list of hits is None or empty - Exiting with no found track")
            return 0
        
        #--------------------------------------------------------
        # Create a NumPy array of hits with theta as last column
        #--------------------------------------------------------
        array_hits = np.array([[hit.hit_id, hit.x, hit.y, hit.z, hit.module_id, hit.theta] for hit in list_hits], dtype=float)

        #------------------------------------------
        # Cluster by last column the array of hits
        #------------------------------------------
        clusters = self.cluster_by_last_column(array_hits, tol=tol)

        # Sort each cluster internally
        sorted_clusters = [c[np.argsort(c[:, 0])] for c in clusters]
        
        # Sort the list of clusters by the first column of the first row
        sorted_clusters = sorted(sorted_clusters, key=lambda c: c[0, 0])

        clusters = sorted_clusters

        #-------------------------------------------
        # Create a list of tracks from the clusters
        #-------------------------------------------
        false_clusters = []
        found_clusters = []
        found_tracks = []
        found_segments = []

        threshold = max(1, int(layers/2))
        
        k = 0
        for cluster in clusters:

            # Discard clusters of length less than half the number of layers
            if len(cluster) < threshold:
                false_clusters.append(cluster)
                continue

            found_clusters.append(cluster)

            # Add in the set found_thetas the rounded polar coordinate theta of the first hit in the cluster
            param["found_thetas"].add(round(cluster[0][5] / tol) * tol)

            # Create a new track
            track_hits = [hit for hit in list_hits if hit.hit_id in [int(x[0]) for x in cluster]][:layers]
            track_segs = []
            
            for idx in range(len(track_hits) - 1):

                s = Segment(
                    hits=[track_hits[idx], track_hits[idx + 1]],
                    segment_id=idx
                )
                
                track_segs.append(s)
                found_segments.append(s)
                    
            track = Track(
                track_id = k,
                hits = track_hits,
                segments = track_segs
            )

            # Find primary vertice
            self.segment_intersects_z_axis(track.segments[0], tol=tol)

            found_tracks.append(track)
            k += 1

        #---------------------------------------------------
        # Display number of found tracks and false clusters
        #---------------------------------------------------
        text = f" find_tracks() found {len(found_tracks)} tracks"
        if len(false_clusters) > 0:
            text += f" and {len(false_clusters)} false clusters"
        line = "-" * (len(text) + 1)
        print(f"\n{line}\n{text}\n{line}")

        #------------------------
        # Display found clusters
        #------------------------
        if display_clusters and len(found_clusters) > 0:

            text = f" All {len(found_clusters)} clusters found by find_tracks()"
            line = "-" * (len(text) + 1)
            print(f"\n{line}\n{text}\n{line}")
            
            print(f"\n  Hit ID       x         y         z       Theta    Module ID")
            
            for cluster in found_clusters:
                for x in cluster:
                    print(f"    {x[0]:.0f}       {x[1]:6.2f}    {x[2]:6.2f}    {x[3]:6.2f}    {x[5]:6.3f}       {x[4]:.0f}")

        #------------------------
        # Display false clusters
        #------------------------
        if display_false_clusters and len(false_clusters) > 0:

            text = f" All {len(false_clusters)} false clusters rejected by the function find_tracks()"
            line = "-" * (len(text) + 1)
            print(f"\n{line}\n{text}\n{line}")
            
            print(f"\n  Hit ID       x         y         z       Theta    Module ID")

            for cluster in false_clusters:
                for x in cluster:
                    print(f"    {x[0]:.0f}       {x[1]:6.2f}    {x[2]:6.2f}    {x[3]:6.2f}    {x[5]:6.3f}       {x[4]:.0f}")

        #----------------------
        # Display found tracks
        #----------------------
        if display_tracks and len(found_tracks) > 0:                       
            self.display_tracks(found_tracks, text=f" All {len(found_tracks)} tracks found by the function find_tracks()")

        #--------------------------
        # Display primary vertices
        #--------------------------
        self.display_p_vertices()

        #-----------------------------------------------------------------------------------------
        # Create an instance of the class Event defined in state_event_model.py
        # https://github.com/Xenofon-Chiotopoulos/OneBQF/blob/main/toy_model/state_event_model.py
        # Author: Alain Chancé
        #-----------------------------------------------------------------------------------------
        found_event = Event(
            detector_geometry = param["detector_geometry"],
            tracks = found_tracks,
            hits = param["hits"],
            segments = found_segments,
            modules = param["modules"]
        )
        param["found_event"] = found_event

        #---------------------------
        # Plot reconstructed tracks
        #---------------------------
        if do_plot_tracks:          
            print("\nPlotting reconstructed event tracks found by the function find_tracks()")
            self.plot_event(found_event, resolution)

        #------------------------------------------------------
        # Save found tracks and segments in the parameter list
        #------------------------------------------------------
        param["found_tracks"] = found_tracks
        param["found_segments"] = found_segments
        
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
    #
    # Input parameter:
    #  - a segment of the class segment defined in state_event_model.py
    #
    # Returns:
    #  - intersects: boolean True if the segment intersects the z-axis
    #
    # Author: Alain Chancé
    #-------------------------------------------------------------------
    def segment_intersects_z_axis(self, s: Segment, tol=1e-6):
        param = self.param
        
        p0 = s.p0()
        p1 = s.p1()
        d = s.to_vect()

        intersects, xyz = self.intersects_z_axis(p0[0], p0[1], p0[2], d[0], d[1], d[2], tol=tol)
        if not intersects:
            return False
            
        intersects, xyz = self.intersects_z_axis(p1[0], p1[1], p1[2], d[0], d[1], d[2], tol=tol)
        if not intersects:
            return False

        # Reject intersection that is beyond the first layer
        if xyz[2] > param["dz"]:
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
        tol = param["tol"]

        #-------------------------------------------------------------------------------------------------------------------
        # List active segments from the solution returned by both the classical solution and the 1-bit HHL quantum solution
        #-------------------------------------------------------------------------------------------------------------------
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
            if self.segment_intersects_z_axis(s, tol=tol):
                filtered_solution[s.segment_id] = 1
            else:
                filtered_solution[s.segment_id] = 0
                filtered = True
                if first:
                    print("\nRemoved segments that do not intersect the z-axis:")
                    print(f"\n    Segment ID        Hits           Theta         Module ID     Track ID")
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
                if self.segment_intersects_z_axis(s, tol=tol):
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

        #-----------------------------------------------------------------------------------------
        # Create an instance of the class Event defined in state_event_model.py
        # https://github.com/Xenofon-Chiotopoulos/OneBQF/blob/main/toy_model/state_event_model.py
        # Author: Alain Chancé
        #-----------------------------------------------------------------------------------------
        event = Event(
            detector_geometry = param["detector_geometry"],
            tracks = found_tracks,
            hits = param["hits"],
            segments = found_segments,
            modules = param["modules"]
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
                print(f"\n    Segment ID        Hits           Theta         Module ID     Track ID")

            for s in [s for s in found_segments if s.module_id == module.module_id]:

                # Add new segment to the list of active segments
                active_segments.append(s)

                if do_print_outer_segs:
                    print(f"    {s.segment_id:4d}       {s.hits[0].hit_id:6d}   {s.hits[1].hit_id:4d}        {s.theta:6.3f}         {s.module_id:4d}           {s.track_id:4d}")

        event.tracks = found_tracks
        
        return event, found_tracks, good_indices

    #----------------------------------
    # Define function display_tracks()
    # Author: Alain Chancé
    #----------------------------------
    def display_tracks(self, tracks, text=None):

        if text: 
            line = "-" * (len(text) + 1) 
            print(f"\n{line}\n{text}\n{line}")
              
        for track in tracks:
            print(f"\nTrack ID: {track.track_id}")
            print(f"     Hit ID       x         y         z       Theta      Module ID")

            for hit in track.hits:
                print(f"    {hit.hit_id:4d}       {hit.x:6.2f}    {hit.y:6.2f}    {hit.z:6.2f}    {hit.theta:6.3f}       {hit.module_id:4d}")

            print(f"\n    Segment ID        Hits           Theta         Module ID     Track ID")
            for s in track.segments:
                print(f"    {s.segment_id:4d}       {s.hits[0].hit_id:6d}   {s.hits[1].hit_id:4d}        {s.theta:6.3f}         {s.module_id:4d}           {s.track_id:4d}")
        
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

    #----------------------------------------------------------------------------------------------
    # Define function plot_event()
    # Input parameters:
    #  - an event of the class Event defined in state_event_model.py
    #  - resolution
    # Returns
    #  - a plot
    # This function is derived from function plot_segments defined in module state_event_model.py
    # https://github.com/Xenofon-Chiotopoulos/OneBQF/blob/main/toy_model/state_event_model.py
    # Author: Alain Chancé
    #----------------------------------------------------------------------------------------------
    def plot_event(self, event, resolution, text=None):

        if text is not None:
            print(text)
        
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
        tol = param["tol"]
        
        events_num = len(n_particles) # Number of events to generate
        n = np.sum(n_particles)

        #----------------------------------------------------------------------------------------
        # Check that the list of particles and the list of primary vertices have the same length
        #----------------------------------------------------------------------------------------
        if len(n_particles) != len(p_vertices):
            print("setup_events - Error: The lists of particles and primary vertices must have the same length.")
            return None

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

        #-----------------------------------------------------------------------------------------------------
        # Generate a list of initial particle state dictionaries for each event based on the primary vertices 
        # Calls the function generate_particles() in module OneBQF/toy_model/state_event_generator.py
        # https://github.com/Xenofon-Chiotopoulos/OneBQF/blob/main/toy_model/state_event_generator.py
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
        #-----------------------------------------------------------------------------------------------------
        init_particles = state_event_gen.generate_particles(event_particles)
        
        param["init_particles"] = init_particles

        if init_particles == 0:
            return None

        if display_particles:
            print("\nInitial particle states")
            for event_particles in init_particles:
                print("\nEvent particles")
                print(f"Type        Position              Direction        p/q")
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
            line = "-" * (len(text) + 1)
            print(f"\n{line}\n{text}\n{line}")
            
            print(f"\n     Hit ID       x         y         z       Theta      Module ID")

            for hit in event_tracks.hits:
                print(f"    {hit.hit_id:4d}       {hit.x:6.2f}    {hit.y:6.2f}    {hit.z:6.2f}    {hit.theta:6.3f}       {hit.module_id:4d}")

        #---------------------------------------------------------------------------------
        # Create a more realistic false_tracks event by adding realistic detector effects
        # Real detectors have imperfections. We can simulate:
        # - Drop rate: Probability of missing a hit (detector inefficiency)
        # - Ghost rate: Probability of fake hits (noise, electronic artifacts)
        #---------------------------------------------------------------------------------
        false_tracks = state_event_gen.make_noisy_event(drop_rate=drop_rate, ghost_rate=ghost_rate)
        
        param["false_tracks"] = false_tracks
        param["hits"] = false_tracks.hits
        
        param["ghost_hits"] = state_event_gen.ghost_hits
        ghost_hits = param["ghost_hits"]

        #---------------------------------
        # Display all true and ghost hits
        #---------------------------------
        if display_ghost_hits and ghost_hits != []:

            text = f" All {len(ghost_hits)} ghost hits created by the function make_noisy_event()"
            line = "-" * (len(text) + 1)
            print(f"\n{line}\n{text}\n{line}")
            
            print(f"\n     Hit ID       x         y         z       Theta      Module ID")

            for hit in ghost_hits:
                print(f"    {hit.hit_id:4d}       {hit.x:6.2f}    {hit.y:6.2f}    {hit.z:6.2f}    {hit.theta:6.3f}       {hit.module_id:4d}")
        
        if display_hits and false_tracks.hits != []:

            text = f" All {len(false_tracks.hits)} true and ghost hits created by the function make_noisy_event()"
            line = "-" * (len(text) + 1)
            print(f"\n{line}\n{text}\n{line}")
            
            print(f"\n     Hit ID       x         y         z       Theta      Module ID")

            for hit in false_tracks.hits:
                print(f"    {hit.hit_id:4d}       {hit.x:6.2f}    {hit.y:6.2f}    {hit.z:6.2f}    {hit.theta:6.3f}       {hit.module_id:4d}")

        #-------------------------------------
        # Display full event and false tracks
        #-------------------------------------
        if display_tracks:

            self.display_tracks(event_tracks.tracks, text=f" Event tracks")
            print("\nEvent tracks hits:", len(event_tracks.modules[0].hits))

            self.display_tracks(false_tracks.tracks, text=f" Event tracks with ghost hits")
            print("\nFalse tracks hits:", len(false_tracks.modules[0].hits))

        #----------------------------------
        # Plot full event and false tracks
        #----------------------------------
        if do_plot_tracks:
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
        do_plot_heat_map = param["do_plot_heat_map"]

        if not do_plot_heat_map:
            return

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
        do_solve_scipy = param["do_solve_scipy"]
        event_tracks = param["event_tracks"]
        run_on_QPU = param["run_on_QPU"]
        do_spectrum = param["do_spectrum"]
        tol = param["tol"]

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

        #------------------------------------------------------------------------------
        # Call the modified construct_segments() method of the SimpleHamiltonian class
        #------------------------------------------------------------------------------
        print("\n------------------------------------------------------------")
        print(" construct_segments() method of the SimpleHamiltonian class")
        print("------------------------------------------------------------")
        ham.construct_segments(event=event_tracks)

        param["segment_indices"] = ham.segment_indices
        param["segment_in_indices"] = ham.segment_in_indices

        #----------------------------------------------------------------
        # Call construct_hamiltonian() method of class SimpleHamiltonian
        #----------------------------------------------------------------
        if do_solve_scipy or run_on_QPU:
            print("\n---------------------------------------------------------------")
            print(" construct_hamiltonian() method of the SimpleHamiltonian class")
            print("---------------------------------------------------------------")
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

        if do_solve_scipy:
            #----------------------------------------------------------------------------------------
            # Solve classically using scipy.sparse.linalg.cg
            # https://docs.scipy.org/doc/scipy-1.12.0/reference/generated/scipy.sparse.linalg.cg.html
            #-----------------------------------------------------------------------------------------
            print("\n-----------------------------------------------------------------------------------")
            print(" Solving classically with only the first three layers using scipy.sparse.linalg.cg")
            print("-----------------------------------------------------------------------------------")

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

        else:
            print("\n------------------------------------------------------------------------------------------------------------------------------")
            print("  Using tracks found by the function find_tracks() from the clusters by last column theta of the array of hits")
            print("  and the lists of active segments and their indices for the first three layers returned by the function construct_segments()")
            print("------------------------------------------------------------------------------------------------------------------------------")
            npart = sum(param["n_particles"])
            disc_sol = np.zeros(2*(npart**2), dtype=int)
            
            for i in segment_indices:
                disc_sol[i] = 1

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

        #--------------------------------
        # Display found primary vertices
        #--------------------------------
        self.display_p_vertices()

        #------------------------------------------------------------------------
        # Display reconstructed event tracks from discretized classical solution
        #------------------------------------------------------------------------
        if display_tracks:
            self.display_tracks(rec_tracks, text=f" Reconstructed event tracks from discretized classical solution")

        #---------------------------------------------------------------------
        # Plot reconstructed event tracks from discretized classical solution
        #---------------------------------------------------------------------
        if do_plot_tracks:
            self.plot_event(event, resolution, text=f" Reconstructed event tracks from discretized classical solution")

        #-------------------------------------------------
        # Compute and print event validation matrix table
        #-------------------------------------------------
        validator = evl(false_tracks, rec_tracks)
        print("")
        validator.print_metrics()
        print("")

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
    def run_qc(self):

        if self.param is None:
            print("run_qc: missing parameter param")
            return None
        param = self.param

        #-------------------------------------------
        # Retrieve parameters from param dictionary
        #-------------------------------------------
        do_print_counts = param['do_print_counts']
        isa_circuit = param['isa_circuit']
        
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
            job = param['job']

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
                job = self.sampler.run([isa_circuit], shots=param['nshots'])
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

        #--------------------------------------
        # Reset list of found primary vertices
        #--------------------------------------
        param["found_p_vertices"] = None
        found_p_vertices = param["found_p_vertices"]

        print("\n-------------------------------------------------------")
        print(" 1-Bit HHL simulation with only the first three layers")
        print("-------------------------------------------------------")
        
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

        #---------------------
        # Run quantum circuit
        #---------------------
        counts = self.run_qc()

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

        #--------------------------------
        # Display found primary vertices
        #--------------------------------
        self.display_p_vertices()

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

        #------------------------------------------------------------
        # Display reconstructed tracks from discretized HHL solution
        #------------------------------------------------------------
        if display_tracks:
            self.display_tracks(hhl_rec_tracks, text=f" Reconstructed event tracks from discretized HHL solution")

        #---------------------------------------------------------
        # Plot reconstructed tracks from discretized HHL solution
        #---------------------------------------------------------
        if do_plot_tracks:
            self.plot_event(event, resolution, text=f" Plotting reconstructed event tracks from discretized HHL solution")

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
        self.find_tracks(hits)

        if do_solve_scipy or run_on_QPU:
            # Setup Hamiltonian
            try:
                self.setup_Hamiltonian()
            except Exception as e:
                print(f"Error in function setup_Hamiltonian(): {e}")
        
        if do_solve_scipy:
            # Run classical simulation
            try:
                self.classical_simulation()
            except Exception as e:
                print(f"Error in function classical_simulation(): {e}")
            
        if run_on_QPU:
            # Run 1-Bit HHL quantum simulation
            try:
                self.HHL_simulation()
            except Exception as e:
                print(f"Error in function HHL_simulation(): {e}")

        #-------------------------
        # Stop the eco2AI tracker
        #-------------------------
        tracker = self.param["eco2ai_tracker"]
        if tracker is not None:
            tracker.stop()

        #------------------------------------------------------------------------------------
        # Print a rough estimate of the energy consumption of the quantum device
        # **Assumption**
        # A ballpark figure for a typical modern IBM-class superconducting quantum computer 
        # (including cryogenics + support, while idle or lightly used): ~ 15–25 kW. 
        # Source: [Green quantum computing, Capgemini, 8 May 2023]
        # (https://www.capgemini.com/insights/expert-perspectives/green-quantum-computing/).
        #------------------------------------------------------------------------------------
        QPU_usage, QPU_power_consumption = self.get_QPU_usage()

        #----------------------------------------------------------------------------------------
        # Read the CSV file and print the duration and power consumption of classical processing
        #----------------------------------------------------------------------------------------
        duration, classical_power_usage = self.get_classical_power_usage()
        
        return