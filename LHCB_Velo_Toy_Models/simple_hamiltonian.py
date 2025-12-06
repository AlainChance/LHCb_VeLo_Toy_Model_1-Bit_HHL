
from LHCB_Velo_Toy_Models.state_event_generator import StateEventGenerator
from LHCB_Velo_Toy_Models.state_event_model import Segment
from LHCB_Velo_Toy_Models.hamiltonian import Hamiltonian

from itertools import product, count
from scipy.special import erf 
import scipy as sci
import numpy as np


class SimpleHamiltonian(Hamiltonian):
    
    def __init__(self, epsilon, gamma, delta):
        self.epsilon                                    = epsilon
        self.gamma                                      = gamma
        self.delta                                      = delta
        self.Z                                          = None
        self.A                                          = None
        self.b                                          = None
        self.segments                                   = None
        self.segments_grouped                           = None
        self.n_segments                                 = None
    
    def construct_segments(self, event: StateEventGenerator):
        
        segments_grouped = []
        segments = []
        n_segments = 0
        segment_id = count()

        for idx in range(len(event.modules)-1):
            from_hits = event.modules[idx].hits
            to_hits = event.modules[idx+1].hits

            segments_group = []
            for from_hit, to_hit in product(from_hits, to_hits):
                seg = Segment([from_hit, to_hit],next(segment_id))
                segments_group.append(seg)
                segments.append(seg)
                n_segments = n_segments + 1
        
            segments_grouped.append(segments_group)
            
        self.segments_grouped = segments_grouped
        self.segments = segments
        self.n_segments = n_segments
        
    def construct_hamiltonian(self, event: StateEventGenerator, convolution: bool= False):
        # Check to see if EFR < thresh then map to 0.
        Segment.id_counter = 0
        if self.segments_grouped is None:
            self.construct_segments(event)
        A = sci.sparse.eye(self.n_segments,format='lil')*(-(self.delta+self.gamma))
        b = np.ones(self.n_segments)*self.delta
        for group_idx in range(len(self.segments_grouped) - 1):
            for seg_i, seg_j in product(self.segments_grouped[group_idx], self.segments_grouped[group_idx+1]):
                if seg_i.hits[1] == seg_j.hits[0]:
                    cosine = seg_i * seg_j - 1e-9
                    if convolution:
                        convolved_step = (1 + erf((self.epsilon - abs(np.arccos(cosine))) / (0.001 * np.sqrt(2)))) # ASK XENO/DAVIDE
                        # if convolved_step < 1e-3:
                        #     convolved_step = 0
                        A[seg_i.segment_id, seg_j.segment_id] = A[seg_j.segment_id, seg_i.segment_id] =  convolved_step
                    else: 
                        if abs(cosine - 1) < self.epsilon:
                            A[seg_i.segment_id, seg_j.segment_id] = A[seg_j.segment_id, seg_i.segment_id] =  1
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
    
from copy import deepcopy
from LHCB_Velo_Toy_Models.state_event_model import Track

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
        #print([list(filter(lambda b: b.hit_id == a, event.hits))[0] for a in track])
        #tracks_processed.append(Track(track_ind,[list(filter(lambda b: b.hit_id == a, event.hits))[0] for a in track],1))
        track_hits = []
        for hit_id in track:
            matching_hits = list(filter(lambda b: b.hit_id == hit_id, event.hits))
            if matching_hits:  
                track_hits.append(matching_hits[0])
        if track_hits:
            tracks_processed.append(Track(track_ind, track_hits, 1))
    return tracks_processed