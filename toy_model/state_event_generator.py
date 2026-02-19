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

#---------------------------------------------------------------------------------------------
# Credit
# This is a modified version of the Python file state_event_generator.py published here: 
# https://github.com/Xenofon-Chiotopoulos/OneBQF/blob/main/toy_model/state_event_generator.py
#---------------------------------------------------------------------------------------------

#--------------------------------------------------------------------------------------------------------------------------------------------------
# Modifications by Alain Chancé
# 
# class StateEventGenerator
# Added property: ghost_hits
#    self.ghost_hits = []
#
# Function generate_particles()
# Added:
#
# if event == len(self.primary_vertices):
#    print(f"\nError: the list of particles is larger than the list of primary vertices.")
#    return 0
#
# try:
#    x, y, z = self.primary_vertices[event]
# except Exception as e:
#    print(f"StateEventGenerator - Error generating particles: {e}")
#    return 0
#
# Function make_noisy_event()
# Added:
#    self.ghost_hits = ghost_hits
#
# Function generate_complete_events()
# Modified
#    self.true_event = em.Event(self.detector_geometry, self.true_tracks, self.true_hits, self.true_segments, self.true_modules, self.ghost_hits)
#
# Function make_noisy_event()
# Modified
#    self.false_event = em.Event(
#        self.detector_geometry, self.tracks, self.hits, self.segments, self.modules, self.ghost_hits)
#--------------------------------------------------------------------------------------------------------------------------------------------------

"""
This file contains the class StateEventGenerator, which is used to generate one or multiple
collision events parameterized by the LHCb state vector (x, y, tx, ty, p/q).
"""

import numpy as np
import toy_model.state_event_model as em
import dataclasses
from itertools import count
from abc import ABC, abstractmethod
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from toy_model.state_event_model import *

# -------------------------------------------------------------------------
# StateEventGenerator class
# -------------------------------------------------------------------------
class StateEventGenerator:
    """
    A class to generate state events for a particle detector simulation.
    """
    def __init__(
        self,
        detector_geometry: Geometry,
        primary_vertices: list[tuple[float, float, float]] = None,
        phi_min: float = - 0.2,
        phi_max: float =   0.2,
        theta_min: float = -0.2,
        theta_max: float =  0.2,
        events: int = 3,
        n_particles: list[int] = None,
        particles: list[dict] = None,
        measurement_error: float = 0.,
        collision_noise: float = 0.1e-3
    ) -> None:
        """
        Initializes the StateEventGenerator with geometry, angle limits, event counts, etc.
        """
        self.detector_geometry = detector_geometry  # Geometry of the detector
        self.primary_vertices = primary_vertices if primary_vertices is not None else []
        self.phi_min = phi_min                      # Minimum tx angle
        self.phi_max = phi_max                      # Maximum tx angle
        self.theta_min = theta_min                  # Minimum ty angle
        self.theta_max = theta_max                  # Maximum ty angle
        self.events_num = events                        # Number of events to generate
        self.n_particles = n_particles if n_particles is not None else []
        self.particles = particles if particles is not None else []
        self.rng = np.random.default_rng()          # Random number generator
        self.measurment_error_flag = True           # Flag for measurment error
        self.measurement_error = measurement_error       # Measurment error
        self.collision_noise = collision_noise
        #-----------------------
        # Added by Alain Chancé
        self.ghost_hits = []
        #-----------------------

    def generate_random_primary_vertices(
        self,
        physical_variance: dict[str, float]
    ) -> list[tuple[float, float, float]]:
        """
        Generates random primary vertices (x, y, z) for events based on provided variances.
        """
        primary_vertices = []  # Accumulate generated vertices
        # Ensure variances are small
        for _ in range(self.events_num):
            # Generate each primary vertex with normal distribution
            x = 0
            y = 0
            z = self.rng.normal(0, physical_variance['z'])
            primary_vertices.append((x, y, z))
        # Store back in the instance
        self.primary_vertices = primary_vertices
        return primary_vertices

    def set_primary_vertices(self, primary_vertices: list[tuple[float, float, float]]) -> None:
        """
        Sets the list of primary vertices for the events.
        """
        self.primary_vertices = primary_vertices
        # Validate length
        assert len(primary_vertices) == self.events_num, (
            'Number of primary vertices must be equal to the number of events'
        )
        # Validate structure
        assert all([len(vertex) == 3 for vertex in primary_vertices]), (
            'Primary vertices must be a list of 3-tuples'
        )
        # Validate closeness to origin
        assert all([np.linalg.norm(np.array(vertex)) < 1e3 for vertex in primary_vertices]), (
            'Primary vertices must be close to the origin'
        )

    def generate_particles(self, particles: list[list[dict]] = None) -> list[dict]:
        """
        Generates particle state dictionaries for each event based on the primary vertices.
        """
        init_particles = []  # Overwrite local particles list
        for event in range(self.events_num):
            # For each event, retrieve the stored primary vertex
            
            #------------------------------------------------------------------------------------------
            # Modified by Alain Chancé
            if event == len(self.primary_vertices):
                print(f"\nError: the list of particles is larger than the list of primary vertices.")
                return 0
            
            try:
                x, y, z = self.primary_vertices[event]
            except Exception as e:
                print(f"StateEventGenerator - Error generating particles: {e}")
                return 0
            #------------------------------------------------------------------------------------------
            
            event_particles = []  # Accumulate particles for this event
            for n in range(self.n_particles[event]):
                # Sample azimuthal angle (phi) in [phi_min, phi_max]
                phi = self.rng.uniform(self.phi_min, self.phi_max)
                # Sample cos(theta) to get uniform distribution in cos(theta)
                theta = self.rng.uniform(self.theta_min,self.theta_max)

                # Transverse slopes
                tx = np.tan(phi)
                ty = np.tan(theta)
             

                # Retrieve charge from input (example usage)
                # If "q" or other keys are needed, adapt code accordingly
                # Assumes 'q' is in the input dictionary per particle specification
                q = 1 if not particles else particles[event][n].get('q', 1)

                # Compute momentum (dummy usage, must adapt to actual model)
                p = np.linalg.norm([tx, ty, 1]) * particles[event][n]['mass']*0.89

                # Append new particle state
                event_particles.append(
                    {
                        'type' : particles[event][n]['type'],
                        'x': x,
                        'y': y,
                        'z': z,
                        'tx': tx,
                        'ty': ty,
                        'p/q': p/q  
                    }
                )
                # Store final list in the instance
            init_particles.append(event_particles)
            self.particles = init_particles
            # print(f'init_particles : {init_particles}')
        return init_particles

    def collision_update(self, particle: dict) -> dict:
        """
        Updates a particle's direction to simulate a collision.
        """
        # Update slopes
        update_x = np.tan(np.random.normal(0, self.collision_noise))
        update_y = np.tan(np.random.normal(0, self.collision_noise))

        particle['tx'] += update_x 
        particle['ty'] += update_y

        # print(f'x : {update_x}, y : {update_y}')
        return particle
    
    def measurment_error(self, particle: dict) -> dict:
        """
        Updates a particle's position to simlate a measurenemnt error
        """
        # Random slight shifts in x, y
        particle['x'] += np.random.normal(0, self.measurement_error)
        particle['y'] += np.random.normal(0, self.measurement_error)
    
        return particle

    def propagate(self, particle: dict, dz: float) -> dict:
        """
        Moves a particle forward by dz in the z-direction, updating x and y.
        """
        # Position updates based on slopes
        particle['x'] += particle['tx'] * dz
        particle['y'] += particle['ty'] * dz
        particle['z'] += dz

        # print(f'particle state : {particle}, dz : {dz}')

        return particle

    def generate_complete_events(self):
        """
        Generates fully propagated events, from the primary vertices through each detector layer,
        recording hits and segments along the way.
        Returns a list of lists (one list per event), where each sublist contains tracks.
        """
        #init hit counter
        hit_counter = count()
        #init track counter
        track_counter = count()
        # Prepare container for all events
        all_event_tracks = []
        # Loop over the number of events
        for evt_idx in range(self.events_num):
            # Container for tracks in this event
            event_tracks = []
            # Retrieve the primary vertex for this event
            vx, vy, vz = self.primary_vertices[evt_idx]
            for p_idx in range(self.n_particles[evt_idx]):
                track_id = next(track_counter)
                # Create a new track with empty collections of hits and segments
                track = em.Track(track_id, hits=[], segments=[])
                # Initialize the particle's state at the primary vertex
                state = self.particles[evt_idx][p_idx]
                # Propagate through each layer of the detector geometry
                for mod_id, lx, ly, zpos in self.detector_geometry:
                    # Calculate distance to the next layer along z
                    dz = zpos - state['z']
                    # Update particle state by propagating in z
                    state = self.propagate(state, dz)
                    # print(f'state : {state}')
                    if not self.detector_geometry.point_on_bulk(state):
                        continue
                    # Create and record a new hit at this layer
                    if self.measurment_error_flag:
                        errot_state = self.measurment_error(state)
                        hit = em.Hit(
                            hit_id = next(hit_counter),
                            track_id = track_id,         
                            x=errot_state['x'],
                            y=errot_state['y'],
                            z=zpos,
                            module_id=mod_id
                        )
                    else:
                        hit = em.Hit(
                            hit_id = next(hit_counter),
                            track_id = track_id,  
                            x=state['x'],
                            y=state['y'],
                            z=zpos,
                            module_id=mod_id
                        )
                    state = self.collision_update(state)
                    track.hits.append(hit)
                #find the segments
                for i in range(len(track.hits)-1):
                    seg = em.Segment(
                        segment_id = i,
                        hits = [track.hits[i], track.hits[i+1]]
                    )
                    track.segments.append(seg)
                # Store this track in the event collection
                event_tracks.append(track)
            # Store all tracks for this event
            all_event_tracks.append(event_tracks)
            
        # Return all events, each containing its tracks
        self.events = all_event_tracks
        self.tracks = []
        for event in all_event_tracks:
            for track in event:
                self.tracks.append(track)
        self.hits = []
        for event in all_event_tracks:
            for track in event:
                for hit in track.hits:
                    self.hits.append(hit)
        self.segments = []
        for event in all_event_tracks:
            for track in event:
                for seg in track.segments:
                    self.segments.append(seg)

        self.true_hits = self.hits
        self.true_segments = self.segments
        self.true_tracks = self.tracks
    
        # Generate modules (layer wise hits)
        self.modules = []
        for mod_id, lx, ly, zpos in self.detector_geometry:
            # print(mod_id, lx, ly, zpos)
            hits = [hit for hit in self.hits if hit.module_id == mod_id]
            # print(hits)
            self.modules.append(em.Module(mod_id, zpos, lx, ly, hits))
        self.true_modules = self.modules

        # Modified by Alain Chancé
        #self.true_event = em.Event(self.detector_geometry, self.true_tracks, self.true_hits, self.true_segments, self.true_modules)
        self.true_event = em.Event(self.detector_geometry, self.true_tracks, self.true_hits, self.true_segments, self.true_modules, self.ghost_hits)

        return self.true_event

    
    def make_noisy_event(self, drop_rate=0.1, ghost_rate=0.1):
        """
        Simulates hit dropout and adds ghost hits in the detector.
        """
        # Drop a fraction of hits
        total_hits = len(self.hits)
        to_drop = int(total_hits * drop_rate)
        drop_indices = self.rng.choice(total_hits, to_drop, replace=False)
        self.hits = [hit for i, hit in enumerate(self.hits) if i not in drop_indices]

        # Remove invalid segments and update each track
        valid_hits = self.hits
        self.segments = [
            seg 
            for seg in self.segments
            if seg.hits[0] in valid_hits and seg.hits[1] in valid_hits
        ]
        for track in self.tracks:
            track.hits = [hit for hit in track.hits if hit in valid_hits]
            track.segments = [
                seg 
                for seg in track.segments
                if seg.hits[0] in valid_hits and seg.hits[1] in valid_hits
            ]

        # Insert ghost hits
        ghost_count = int(total_hits * ghost_rate)
        ghost_hits = []
        for _ in range(ghost_count):
            mod_id, lx, ly, zpos = self.rng.choice(self.detector_geometry)
            x = self.rng.uniform(-lx / 2, lx / 2)
            y = self.rng.uniform(-ly / 2, ly / 2)
            ghost_hits.append(
                em.Hit(hit_id=next(count()), x=x, y=y, z=zpos, module_id=mod_id, track_id=-1)
            )
        self.hits += ghost_hits

        #----------------------------
        # Added by Alain Chancé
        self.ghost_hits = ghost_hits
        #----------------------------

        # Rebuild modules and store event
        self._rebuild_modules()
        #-------------------------------------------------------------------------------------------------
        # Modified by Alain Chancé
        #self.false_event = em.Event(
        #    self.detector_geometry, self.tracks, self.hits, self.segments, self.modules
        #)
        self.false_event = em.Event(
            self.detector_geometry, self.tracks, self.hits, self.segments, self.modules, self.ghost_hits)
        #-------------------------------------------------------------------------------------------------

        return self.false_event

    def _rebuild_modules(self):
        """Rebuilds the module list with current hits."""
        self.modules = []
        for mod_id, lx, ly, zpos in self.detector_geometry:
            hits = [h for h in self.hits if h.module_id == mod_id]
            self.modules.append(em.Module(mod_id, zpos, lx, ly, hits))
        