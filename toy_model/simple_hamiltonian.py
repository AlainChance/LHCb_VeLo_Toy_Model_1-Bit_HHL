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

#------------------------------------------------------------------------------------------
# Credit
# This is a modified version of the Python file simple_hamiltonian.py published here: 
# https://github.com/Xenofon-Chiotopoulos/OneBQF/blob/main/toy_model/simple_hamiltonian.py
#------------------------------------------------------------------------------------------

#--------------------------------------------------------------------------------------------------------------
# Additions by Alain Chancé
#
## Fast construction of the Hamiltonian H(S)
# The function `construct_segments` is enhanced to identify segments with matching values of `theta` 
# during their creation and to append them to the list `segment_in_indices`, along with their corresponding 
# segment IDs in the list `segment_indices`. The function `construct_hamiltonian` then considers only doublets
# S_i and S_j of segments in `segment_in_indices`.
# This modification significantly improves the performance of the preprocessing step.
#
### Class SimpleHamiltonian
# Additional properties: 
# - self.segment_indices
# - self.segment_in_indices
#--------------------------------------------------------------------------------------------------------------

from toy_model.state_event_generator import StateEventGenerator
from toy_model.state_event_model import Segment, Hit, Track, Event
from toy_model.hamiltonian import Hamiltonian
from toy_model.state_event_model import Track

from itertools import product, count
from scipy.special import erf 
from copy import deepcopy
import scipy as sci
import numpy as np
import scipy.sparse as sp


class SimpleHamiltonian(Hamiltonian):
    
    def __init__(self, epsilon, alpha, beta, theta_d = 1e-4):
        self.epsilon                                    = epsilon
        self.gamma                                      = alpha
        self.delta                                      = beta
        self.theta_d                                   = theta_d
        self.Z                                          = None
        self.A                                          = None
        self.b                                          = None
        self.segments                                   = None
        self.segments_grouped                           = None
        self.n_segments                                 = None
        #---------------------------------------------------
        # Added by Alain Chancé
        self.segment_indices                            = []
        self.segment_in_indices                         = []
        #---------------------------------------------------
    
    def construct_segments(self, event: StateEventGenerator):    
        segments_grouped = []
        segments = []
        n_segments = 0
        segment_id = count()

        #-------------------------
        # Added by Alain Chancé
        first = True
        #------------------------

        for idx in range(len(event.modules)-1):
            from_hits = event.modules[idx].hits
            to_hits = event.modules[idx+1].hits

            segments_group = []
            for from_hit, to_hit in product(from_hits, to_hits):
                seg = Segment([from_hit, to_hit],next(segment_id))
                segments_group.append(seg)
                segments.append(seg)
                n_segments = n_segments + 1

                #------------------------------------------------------------------------------
                # Added by Alain Chancé
                #
                # Identify segments with matching values of `theta` during their creation and
                # append them to the list `segment_in_indices`, along with their corresponding
                # segment IDs in the list `segment_indices`.
                #------------------------------------------------------------------------------
                if np.allclose(from_hit.theta, to_hit.theta, atol=self.theta_d):

                    if first:
                        print(f"\nFunction construct_segments() - Adding segments with matching theta to segment_in_indices")
                        print(f"\n    Segment ID        Hits           Theta         Module ID     Track ID")
                        first = False
                    
                    print(f"    {seg.segment_id:4d}       {seg.hits[0].hit_id:6d}   {seg.hits[1].hit_id:4d}        {seg.theta:6.3f}         {seg.module_id:4d}           {seg.track_id:4d}")

                    self.segment_in_indices.append(seg)
                #---------------------------------------
        
            segments_grouped.append(segments_group)

        #-----------------------
        # Added by Alain Chancé
        #-----------------------
        self.segment_indices = [segment.segment_id for segment in self.segment_in_indices]
        print("\nconstruct_segments() - list segment_indices")
        print(f"\n{self.segment_indices}")
        #----------------------------------------------------------------------------------
            
        self.segments_grouped = segments_grouped
        self.segments = segments
        self.n_segments = n_segments

        return
        
    def construct_hamiltonian(self, event: StateEventGenerator, convolution: bool= False):
        Segment.id_counter = 0
        if self.segments_grouped is None:
            self.construct_segments(event)
        A = sci.sparse.eye(self.n_segments,format='lil')*(-(self.delta+self.gamma))
        b = np.ones(self.n_segments)*self.delta

        #-----------------------
        # Added by Alain Chancé
        #-----------------------
        if self.segment_in_indices != []:
            #--------------------------------------------------------------------------------------------
            # Consider only segments in segment_in_indices returned by the function construct_segments()
            #--------------------------------------------------------------------------------------------
            for group_idx in range(len(self.segments_grouped) - 1):
                for seg_i, seg_j in product(self.segment_in_indices, self.segment_in_indices):
                    if seg_i.hits[1] == seg_j.hits[0]:
                        A[seg_i.segment_id, seg_j.segment_id] = A[seg_j.segment_id, seg_i.segment_id] =  1
        else:
            #---------------------------------
            # Search in all possible segments
            #---------------------------------
            for group_idx in range(len(self.segments_grouped) - 1):
                for seg_i, seg_j in product(self.segments_grouped[group_idx], self.segments_grouped[group_idx+1]):
                    
                    # Modified by Alain Chancé
                    #if seg_i.hits[1] == seg_j.hits[0]:
                        #cosine = (seg_i * seg_j) 
                        #if convolution:
                            #convolved_step = (1 + erf((self.epsilon - abs(np.arccos(cosine))) / (self.theta_d * np.sqrt(2))))
                            #A[seg_i.segment_id, seg_j.segment_id] = A[seg_j.segment_id, seg_i.segment_id] =  convolved_step
                        #else: 
                            #if abs(cosine - 1) < self.epsilon:
                                #A[seg_i.segment_id, seg_j.segment_id] = A[seg_j.segment_id, seg_i.segment_id] =  1
                    
                    if seg_i.hits[1] == seg_j.hits[0] and np.allclose(seg_i.theta, seg_j.theta, atol=self.theta_d):
                        A[seg_i.segment_id, seg_j.segment_id] = A[seg_j.segment_id, seg_i.segment_id] =  1
        
        #------------------------------------------------------------------
        # Get a new sparse matrix in CSC format for fast column operations
        #------------------------------------------------------------------
        A = A.tocsc()
        
        self.A, self.b = -A, b
        return -A, b
    
    def solve_classicaly(self):

        if self.A is None:
            raise Exception("Not initialised")
        
        solution, _ = sci.sparse.linalg.cg(self.A, self.b, atol=0)
        return solution
    
    def evaluate(self, solution: list):

        if self.A is None:
            raise Exception("Not initialised")
        
        if isinstance(solution, list):
            sol = np.array([solution, None])
        elif isinstance(solution, np.ndarray):
            if solution.ndim == 1:
                sol = solution[..., None]
            else: sol = solution
            
            
        return -0.5 * sol.T @ self.A @ sol + self.b.dot(sol)

def find_segments(s0: Segment, active: Segment):
        found_s = []
        for s1 in active:
            if s0.hits[0].hit_id == s1.hits[1].hit_id or \
            s1.hits[0].hit_id == s0.hits[1].hit_id:
                found_s.append(s1)
        return found_s

def get_tracks(ham: SimpleHamiltonian, classical_solution: list[int], event: StateEventGenerator):
    active_segments = [segment for segment,pseudo_state in zip(ham.segments,classical_solution) if pseudo_state > np.min(classical_solution)]
    active = deepcopy(active_segments)
    tracks = []
    while len(active):
        s = active.pop()
        nextt = find_segments(s, active)
        track = set([s.hits[0].hit_id, s.hits[1].hit_id])
        while len(nextt):
            s = nextt.pop()
            try:
                active.remove(s)
            except:
                pass
            nextt += find_segments(s, active)
            track = track.union(set([s.hits[0].hit_id, s.hits[1].hit_id]))
        tracks.append(track)

    tracks_processed = []
    for track_ind, track in enumerate(tracks):
        track_hits = []
        for hit_id in track:
            matching_hits = list(filter(lambda b: b.hit_id == hit_id, event.hits))
            if matching_hits:  
                track_hits.append(matching_hits[0])
        if track_hits:
            tracks_processed.append(Track(track_ind, track_hits, 1))
    return tracks_processed





class SimpleHamiltonianFast(Hamiltonian):
    """
    Optimized Hamiltonian construction for track finding.
    
    Uses vectorized numpy operations and efficient sparse matrix construction
    for significant speedup over the original implementation.
    """
    
    def __init__(self, epsilon, gamma, delta, theta_d=1e-4):
        self.epsilon = epsilon
        self.gamma = gamma
        self.delta = delta
        self.theta_d = theta_d
        self.Z = None
        self.A = None
        self.b = None
        self.segments = None
        self.segments_grouped = None
        self.n_segments = None
        
        # Cached data for fast Hamiltonian construction
        self._segment_vectors = None  # Normalized direction vectors
        self._segment_to_hit_ids = None  # (from_hit_id, to_hit_id) for each segment
        self._group_boundaries = None  # Start indices for each group
    
    def construct_segments(self, event: StateEventGenerator):
        """
        Construct segments and pre-compute direction vectors.
        """
        segments_grouped = []
        segments = []
        segment_vectors = []
        segment_hit_ids = []
        group_boundaries = [0]
        
        segment_id = 0
        
        for idx in range(len(event.modules) - 1):
            from_hits = event.modules[idx].hits
            to_hits = event.modules[idx + 1].hits
            
            segments_group = []
            for from_hit, to_hit in product(from_hits, to_hits):
                seg = Segment([from_hit, to_hit], segment_id)
                segments_group.append(seg)
                segments.append(seg)
                
                # Pre-compute normalized direction vector
                dx = to_hit.x - from_hit.x
                dy = to_hit.y - from_hit.y
                dz = to_hit.z - from_hit.z
                norm = np.sqrt(dx*dx + dy*dy + dz*dz)
                if norm > 0:
                    segment_vectors.append((dx/norm, dy/norm, dz/norm))
                else:
                    segment_vectors.append((0, 0, 1))
                
                # Store hit IDs for fast lookup
                segment_hit_ids.append((from_hit.hit_id, to_hit.hit_id))
                
                segment_id += 1
            
            segments_grouped.append(segments_group)
            group_boundaries.append(segment_id)
        
        self.segments_grouped = segments_grouped
        self.segments = segments
        self.n_segments = segment_id
        self._segment_vectors = np.array(segment_vectors)
        self._segment_to_hit_ids = segment_hit_ids
        self._group_boundaries = group_boundaries
    
    def construct_hamiltonian(self, event: StateEventGenerator, convolution: bool = False):
        """
        Construct the Hamiltonian matrix using optimized sparse construction.
        
        Uses COO format for efficient construction, then converts to CSC for solving.
        """
        Segment.id_counter = 0
        if self.segments_grouped is None:
            self.construct_segments(event)
        
        n = self.n_segments
        
        # Lists for COO sparse matrix construction
        row_indices = []
        col_indices = []
        data_values = []
        
        # Diagonal entries: -(delta + gamma)
        diag_value = -(self.delta + self.gamma)
        row_indices.extend(range(n))
        col_indices.extend(range(n))
        data_values.extend([diag_value] * n)
        
        # Off-diagonal entries: segment connections
        # Pre-compute for vectorized operations
        sqrt2_theta_d = self.theta_d * np.sqrt(2)
        
        for group_idx in range(len(self.segments_grouped) - 1):
            group_i = self.segments_grouped[group_idx]
            group_j = self.segments_grouped[group_idx + 1]
            
            # Get index offsets
            offset_i = self._group_boundaries[group_idx]
            offset_j = self._group_boundaries[group_idx + 1]
            
            for local_i, seg_i in enumerate(group_i):
                seg_i_id = offset_i + local_i
                seg_i_to_hit = self._segment_to_hit_ids[seg_i_id][1]
                vec_i = self._segment_vectors[seg_i_id]
                
                for local_j, seg_j in enumerate(group_j):
                    seg_j_id = offset_j + local_j
                    seg_j_from_hit = self._segment_to_hit_ids[seg_j_id][0]
                    
                    # Check if segments are connected (share middle hit)
                    if seg_i_to_hit == seg_j_from_hit:
                        vec_j = self._segment_vectors[seg_j_id]
                        
                        # Compute cosine of angle between segments
                        cosine = vec_i[0]*vec_j[0] + vec_i[1]*vec_j[1] + vec_i[2]*vec_j[2]
                        
                        # Clamp cosine to valid range to avoid numerical issues
                        cosine = np.clip(cosine, -1.0, 1.0)
                        
                        # Compute angle between segments
                        angle = np.arccos(cosine)
                        
                        if convolution:
                            # ERF-smoothed step function
                            value = 1 + erf((self.epsilon - angle) / sqrt2_theta_d)
                            # Symmetric matrix
                            row_indices.extend([seg_i_id, seg_j_id])
                            col_indices.extend([seg_j_id, seg_i_id])
                            data_values.extend([value, value])
                        else:
                            # Hard step function: accept if angle < epsilon
                            # This is consistent with the ERF version
                            if angle < self.epsilon:
                                row_indices.extend([seg_i_id, seg_j_id])
                                col_indices.extend([seg_j_id, seg_i_id])
                                data_values.extend([1.0, 1.0])
        
        #-------------------------------------------------------------------------
        # Setup a sparse matrix in COO format that is easy to build incrementally
        #-------------------------------------------------------------------------
        A = sp.coo_matrix((data_values, (row_indices, col_indices)), shape=(n, n))

        #------------------------------------------------------------------
        # Get a new sparse matrix in CSC format for fast column operations
        #------------------------------------------------------------------
        A = A.tocsc()
        
        b = np.ones(n) * self.delta
        
        self.A, self.b = -A, b
        return -A, b
    
    def solve_classicaly(self):
        """Solve the linear system using conjugate gradient."""
        if self.A is None:
            raise Exception("Not initialised")
        
        # Use sparse direct solver for small systems, iterative for large
        if self.n_segments < 5000:
            try:
                solution = sp.linalg.spsolve(self.A, self.b)
            except:
                solution, _ = sp.linalg.cg(self.A, self.b, atol=1e-10)
        else:
            solution, _ = sp.linalg.cg(self.A, self.b, atol=1e-10)
        
        return solution
    
    def evaluate(self, solution):
        """Evaluate the Hamiltonian energy for a given solution."""
        if self.A is None:
            raise Exception("Not initialised")
        
        if isinstance(solution, list):
            sol = np.array(solution).reshape(-1, 1)
        elif isinstance(solution, np.ndarray):
            if solution.ndim == 1:
                sol = solution.reshape(-1, 1)
            else:
                sol = solution
        
        return float(-0.5 * sol.T @ self.A @ sol + self.b.dot(sol.flatten()))


def find_segments(s0: Segment, active: list):
    """Find segments connected to s0."""
    found_s = []
    s0_from_id = s0.hits[0].hit_id
    s0_to_id = s0.hits[1].hit_id
    for s1 in active:
        if s0_from_id == s1.hits[1].hit_id or s1.hits[0].hit_id == s0_to_id:
            found_s.append(s1)
    return found_s


def get_tracks_fast(ham: SimpleHamiltonianFast, classical_solution, event: StateEventGenerator):
    """
    Extract tracks from the Hamiltonian solution.
    
    Groups connected segments where the solution indicates activity.
    """
    min_val = np.min(classical_solution)
    active_segments = [
        segment for segment, pseudo_state in zip(ham.segments, classical_solution)
        if pseudo_state > min_val
    ]
    active = deepcopy(active_segments)
    tracks = []
    
    while len(active):
        s = active.pop()
        nextt = find_segments(s, active)
        track = set([s.hits[0].hit_id, s.hits[1].hit_id])
        
        while len(nextt):
            s = nextt.pop()
            try:
                active.remove(s)
            except:
                pass
            nextt += find_segments(s, active)
            track = track.union(set([s.hits[0].hit_id, s.hits[1].hit_id]))
        
        tracks.append(track)
    
    # Convert to Track objects
    tracks_processed = []
    for track_ind, track in enumerate(tracks):
        track_hits = []
        track_segs = []
        for hit_id in track:
            matching_hits = [h for h in event.hits if h.hit_id == hit_id]
            if matching_hits:
                track_hits.append(matching_hits[0])
        
        # Sort hits by z coordinate for proper segment construction
        track_hits.sort(key=lambda h: h.z)
        
        for idx in range(len(track_hits) - 1):
            track_segs.append(Segment(
                hits=[track_hits[idx], track_hits[idx + 1]], 
                segment_id=idx
            ))
        
        if track_hits and track_segs:
            tracks_processed.append(Track(track_ind, track_hits, track_segs))
    
    return tracks_processed


def construct_event(detector_geometry, tracks, hits, segments, modules):
    """Construct an Event object from components."""
    return Event(
        detector_geometry=detector_geometry,
        tracks=tracks,
        hits=hits,
        segments=segments,
        modules=modules
    )