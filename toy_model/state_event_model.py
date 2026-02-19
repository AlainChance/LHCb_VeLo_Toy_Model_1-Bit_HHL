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

#-----------------------------------------------------------------------------------------
## Credit
# This is a modified version of the Python file state_event_model.py, 
# https://github.com/Xenofon-Chiotopoulos/OneBQF/blob/main/toy_model/state_event_model.py
#-----------------------------------------------------------------------------------------

#-------------------------------------------------------------------------------------------------------------------------
# Modifications made by Alain Chancé
#
# class Hit
# Added:
#    theta: float = field(init=False)  # Phase in polar coordinates when projected onto the XY plane
#    index: int = field(init=False)    # Index of the hit in an array of hits
#
#    def __post_init__(self): 
#        self.theta = math.atan2(self.y, self.x)
#        self.index = 0
#
# class Segment
# Added:
#    module_id: int = field(init=False)  # Module id of the hit in the outer module
#    track_id: int = field(init=False)   # Track id of the hit in the outer module
#    theta: float = field(init=False)    # Phase in polar coordinates when projected onto the XY plane
#
#    def __post_init__(self):
#        self.module_id = self.hits[1].module_id
#        self.track_id = self.hits[1].track_id
#        self.theta = math.atan2(self.hits[1].y - self.hits[0].y, self.hits[1].x - self.hits[0].x)
#
#     def p0(self):
#         return [self.hits[0].x, self.hits[0].y, self.hits[0].z]
#
#     def p1(self):
#         return [self.hits[1].x, self.hits[1].y, self.hits[1].z]
#
# class Event
# Added:
#    ghost_hits: []
#-------------------------------------------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------------------
## References
# Xenofon Chiotopoulos, TrackHHL: A Quantum Computing Algorithm for Track Reconstruction at the LHCb,
# CHEP 2024, 21 Oct 2024, 
# https://indico.cern.ch/event/1338689/contributions/6010017/
#-----------------------------------------------------------------------------------------------------

'''
The goal of this module is to provide a state event model for for tracks parameterised by the standard LHCb state (x,y,tx,ty,p/q)
'''
from itertools import count
from abc import ABC, abstractmethod
import matplotlib.animation as animation
import dataclasses
from mpl_toolkits.mplot3d import Axes3D, art3d
from matplotlib.patches import Rectangle
from matplotlib.animation import FuncAnimation
import numpy as np
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

# Added by Alain Chancé
from dataclasses import dataclass, field
import math

# -------------------------------------------------------------------------
# Abstract base class for detector geometry definitions
# -------------------------------------------------------------------------

@dataclasses.dataclass(frozen=False)
class Hit:
    hit_id: int
    x: float
    y: float
    z: float
    module_id: int
    track_id: int

    #-----------------------------------------------------------------------------------------------
    # Added by Alain Chancé
    # Computed fields (must come AFTER all init=True fields)
    theta: float = field(init=False)  # Phase in polar coordinates when projected onto the XY plane
    index: int = field(init=False)    # Index of the hit in an array of hits
    #-----------------------------------------------------------------------------------------------

    def __getitem__(self, index):
        return (self.x, self.y, self.z)[index]
    
    def __eq__(self, __value: object) -> bool:
        return self is __value

    #----------------------------------------------------------------
    # Added by Alain chancé
    def __post_init__(self): 
        self.theta = math.atan2(self.y, self.x)
        self.index = 0
    #----------------------------------------------------------------
    
@dataclasses.dataclass(frozen=False)
class Module:
    module_id: int
    z: float
    lx: float
    ly: float
    hits: list[Hit]

    def __eq__(self, __value: object) -> bool:
        if self.module_id == __value.module_id:
            return True
        else:
            return False
        
@dataclasses.dataclass
class Segment:
    hits: list[Hit]
    segment_id: int
    #-------------------------------------------------------------------------------------------------
    # Added by Alain Chancé
    module_id: int = field(init=False)  # Module id of the hit in the outer module
    track_id: int = field(init=False)   # Track id of the hit in the outer module
    theta: float = field(init=False)    # Phase in polar coordinates when projected onto the XY plane
    #-------------------------------------------------------------------------------------------------
    
    def __eq__(self, __value: object) -> bool:
        return self is __value
    
    def to_vect(self):
        return (self.hits[1].x - self.hits[0].x, 
                self.hits[1].y - self.hits[0].y, 
                self.hits[1].z - self.hits[0].z)
    
    def __mul__(self, __value):
        v_1 = self.to_vect()
        v_2 = __value.to_vect()
        n_1 = (v_1[0]**2 + v_1[1]**2 + v_1[2]**2)**0.5
        n_2 = (v_2[0]**2 + v_2[1]**2 + v_2[2]**2)**0.5
        
        return (v_1[0]*v_2[0] + v_1[1]*v_2[1] + v_1[2]*v_2[2])/(n_1*n_2)

    #-----------------------
    # Added by Alain Chancé
    #-----------------------
    def __post_init__(self):
        self.module_id = self.hits[1].module_id
        self.track_id = self.hits[1].track_id
        self.theta = math.atan2(self.hits[1].y - self.hits[0].y, self.hits[1].x - self.hits[0].x)

    def p0(self):
        return [self.hits[0].x, self.hits[0].y, self.hits[0].z]

    def p1(self):
        return [self.hits[1].x, self.hits[1].y, self.hits[1].z]
        
@dataclasses.dataclass
class Track:
    track_id    : int
    hits        : list[Hit]
    segments    : list[Segment]
    
    def __eq__(self, __value: object) -> bool:
        return self is __value

@dataclasses.dataclass
class module:
    module_id: int
    z: float
    lx: float
    ly: float
    hits: list[Hit]
    
    def __eq__(self, __value: object) -> bool:
        if self.module_id == __value.module_id:
            return True
        else:
            return False
        
# -------------------------------------------------------------------------
# Abstract geometry specification
# -------------------------------------------------------------------------

@dataclasses.dataclass(frozen=True)
class Geometry(ABC):
    module_id: list[int]  # List of module identifiers

    @abstractmethod
    def __getitem__(self, index):
        """
        Returns geometry item data at specific index.
        """
        pass

    @abstractmethod
    def point_on_bulk(self, state: dict):
        """
        Checks if the (x, y) point from a particle state is within the geometry.
        """
        pass

    def __len__(self):
        """
        Returns the number of modules.
        """
        return len(self.module_id)


# -------------------------------------------------------------------------
# Plane geometry specification
# -------------------------------------------------------------------------
@dataclasses.dataclass(frozen=True)
class PlaneGeometry(Geometry):
    lx: list[float]  # Half-sizes in the x-direction
    ly: list[float]  # Half-sizes in the y-direction
    z: list[float]   # z positions of planes

    def __getitem__(self, index):
        """
        Returns tuple (module_id, lx, ly, z) for a specific index.
        """
        return (self.module_id[index], 
                self.lx[index], 
                self.ly[index], 
                self.z[index])

    def point_on_bulk(self, state: dict):
        """
        Checks if a given state (x, y) is within plane boundaries.
        """
        x, y = state['x'], state['y']  # Extract x, y from particle state
        for i in range(len(self.module_id)):
            # Check if x, y are within the lx, ly boundaries
            if (x < self.lx[i] and x > -self.lx[i] and
                y < self.ly[i] and y > -self.ly[i]):
                return True
        return False


# -------------------------------------------------------------------------
# Detector geometry with a rectangular void in the middle
# -------------------------------------------------------------------------
@dataclasses.dataclass(frozen=True)
class RectangularVoidGeometry(Geometry):
    """
    Detector geometry that contains a rectangular void region in the center.
    """
    z: list[float]         # z positions
    void_x_boundary: list[float]  # +/- x boundary of the void
    void_y_boundary: list[float]  # +/- y boundary of the void
    lx: list[float]       # +/- x boundary of the entire detector
    ly: list[float]       # +/- y boundary of the entire detector

    def __getitem__(self, index):
        """
        Returns tuple with module_id, void, and boundary definitions.
        """
        return (
            self.module_id[index],
            self.lx[index],
            self.ly[index],
            self.z[index]
        )

    def point_on_bulk(self, state: dict):
        """
        Checks if (x, y) point is outside the void region, indicating it is on the bulk material.
        """
        x, y = state['x'], state['y']  # Extract x, y
        if (x < self.void_x_boundary and x > -self.void_x_boundary and
            y < self.void_y_boundary and y > -self.void_y_boundary) or (x > self.lx[0] or x < -self.lx[0] or y > self.ly[0] or y < -self.ly[0]):
            return False
        else:
            return True

@dataclasses.dataclass
class Event:
    detector_geometry: Geometry
    tracks: list[Track]
    hits: list[Hit]
    segments: list[Segment]
    modules: list[Module]
    #-----------------------
    # Added by Alain Chancé
    ghost_hits: []
    #-----------------------
    
    def __eq__(self, __value: object) -> bool:
        return self is __value

    def plot_segments(self):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        hits = []
        for segment in self.segments:
            hits.extend(segment.hits)

        X = [h.z for h in hits]
        Y = [h.y for h in hits]
        Z = [h.x for h in hits]
        ax.scatter(X, Y, Z, c='r', marker='o')

        for segment in self.segments:
            x = [h.z for h in segment.hits]
            y = [h.y for h in segment.hits]
            z = [h.x for h in segment.hits]
            ax.plot(x, y, z, c='b')

        resolution = 25  # Increase for finer mesh
        for mod_id, lx, ly, zpos in self.detector_geometry:
            xs = np.linspace(-lx, lx, resolution)
            ys = np.linspace(-ly, ly, resolution)
            X, Y = np.meshgrid(xs, ys)
            Z = np.full_like(X, zpos, dtype=float)

            for idx in np.ndindex(X.shape):
                x_val = X[idx]
                y_val = Y[idx]
                if not self.detector_geometry.point_on_bulk({'x': x_val, 'y': y_val, 'z': zpos}):
                    X[idx], Y[idx], Z[idx] = np.nan, np.nan, np.nan

            ax.plot_surface(Z, Y, X, alpha=0.3, color='gray')

        ghost_hits = [h for h in self.hits if not any(h in s.hits for s in self.segments)]
        X = [h.z for h in ghost_hits]
        Y = [h.y for h in ghost_hits]
        Z = [h.x for h in ghost_hits]
        ax.scatter(X, Y, Z, c='g', marker='x')

        ax.set_xlabel('Z (horizontal)')
        ax.set_ylabel('Y')
        ax.set_zlabel('X')
        plt.tight_layout()
        plt.show()

    def save_plot_segments(self, filename : str, params: dict = None):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        hits = []
        for segment in self.segments:
            hits.extend(segment.hits)

        X = [h.z for h in hits]
        Y = [h.y for h in hits]
        Z = [h.x for h in hits]
        ax.scatter(X, Y, Z, c='r', marker='o')

        # Plot lines
        for segment in self.segments:
            x = [h.z for h in segment.hits]
            y = [h.y for h in segment.hits]
            z = [h.x for h in segment.hits]
            ax.plot(x, y, z, c='b')

        # Draw planes from geometry, but only show regions that are in the bulk
        resolution = 25
        for mod_id, lx, ly, zpos in self.detector_geometry:
            xs = np.linspace(-lx, lx, resolution)
            ys = np.linspace(-ly, ly, resolution)
            X, Y = np.meshgrid(xs, ys)
            Z = np.full_like(X, zpos, dtype=float)

            for idx in np.ndindex(X.shape):
                x_val = X[idx]
                y_val = Y[idx]
                if not self.detector_geometry.point_on_bulk({'x': x_val, 'y': y_val, 'z': zpos}):
                    X[idx], Y[idx], Z[idx] = np.nan, np.nan, np.nan

            # Plot, using (Z, Y, X) to match the existing axis mappings
            ax.plot_surface(Z, Y, X, alpha=0.3, color='gray')

        # plot ghost_hits (hits that are not part of a segment)
        ghost_hits = [h for h in self.hits if not any(h in s.hits for s in self.segments)]
        X = [h.z for h in ghost_hits]
        Y = [h.y for h in ghost_hits]
        Z = [h.x for h in ghost_hits]
        ax.scatter(X, Y, Z, c='g', marker='x')

        ax.set_xlabel('Z (horizontal)')
        ax.set_ylabel('Y')
        ax.set_zlabel('X')
        if params:
            plt.title(f"Event Parameters: {params}")

        plt.tight_layout()
        plt.savefig(filename)
        plt.close()
