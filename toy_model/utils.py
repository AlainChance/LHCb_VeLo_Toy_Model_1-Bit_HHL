"""
Utility functions for the tracking toy model.
"""
import os
import numpy as np
import dataclasses
from itertools import pairwise
import matplotlib.pyplot as plt

def plot_solution_comparison(classical_solution, discretized_solution, threshold=None, title = "Classical Solution", figsize=(12, 5)):
    """
    Plot classical and discretized Hamiltonian solutions side by side as bar charts.
    
    Parameters:
    -----------
    classical_solution : array-like
        Continuous solution from Hamiltonian optimization
    discretized_solution : array-like
        Binary solution after thresholding
    threshold : float, optional
        Threshold value used for discretization (for reference line)
    figsize : tuple, optional
        Figure size (width, height)
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=figsize)
    
    indices = np.arange(len(classical_solution))
    
    # Plot classical solution as bar chart
    ax1.bar(indices, classical_solution, color='skyblue', alpha=0.7, edgecolor='black', linewidth=0.5)
    ax1.set_title(title, fontsize=14)
    ax1.set_xlabel('Solution Index')
    ax1.set_ylabel('Solution Value')
    ax1.grid(True, alpha=0.3, axis='y')
    
    # Add threshold line if provided
    if threshold is not None:
        ax1.axhline(y=threshold, color='r', linestyle='--', linewidth=2,
                   label=f'Threshold = {threshold}')
        ax1.legend()
    
    # Plot discretized solution as bar chart
    colors = ['lightcoral' if x == 1 else 'lightgray' for x in discretized_solution]
    ax2.bar(indices, discretized_solution, color=colors, edgecolor='black', linewidth=0.5)
    ax2.set_title('Ground Truth', fontsize=14)
    ax2.set_xlabel('Solution Index')
    ax2.set_ylabel('Binary Value')
    ax2.set_ylim(-0.1, 1.1)
    ax2.grid(True, alpha=0.3, axis='y')
    
    # Add statistics
    n_active = np.sum(discretized_solution)
    total = len(discretized_solution)
    ax2.text(0.02, 0.98, f'Active elements: {n_active}/{total}', 
             transform=ax2.transAxes, verticalalignment='top',
             bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
    
    plt.tight_layout()
    plt.show()


def plot_solution_histogram(classical_solution, threshold=None, bins=50, figsize=(8, 6)):
    """
    Plot histogram of classical solution values with optional threshold line.
    
    Parameters:
    -----------
    classical_solution : array-like
        Continuous solution from Hamiltonian optimization
    threshold : float, optional
        Threshold value used for discretization
    bins : int, optional
        Number of histogram bins
    figsize : tuple, optional
        Figure size (width, height)
    """
    plt.figure(figsize=figsize)
    
    plt.hist(classical_solution, bins=bins, alpha=0.7, color='skyblue', 
             edgecolor='black', linewidth=0.5)
    
    if threshold is not None:
        plt.axvline(x=threshold, color='red', linestyle='--', linewidth=2,
                   label=f'Threshold = {threshold}')
        
        # Count elements above/below threshold
        above = np.sum(classical_solution > threshold)
        below = np.sum(classical_solution <= threshold)
        
        plt.text(0.02, 0.98, f'Above threshold: {above}\nBelow threshold: {below}', 
                transform=plt.gca().transAxes, verticalalignment='top',
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
        
        plt.legend()
    
    plt.title('Distribution of Classical Solution Values', fontsize=14)
    plt.xlabel('Solution Value')
    plt.ylabel('Frequency')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()


def solution_statistics(classical_solution, discretized_solution, threshold):
    """
    Print statistics about the classical and discretized solutions.
    
    Parameters:
    -----------
    classical_solution : array-like
        Continuous solution from Hamiltonian optimization
    discretized_solution : array-like
        Binary solution after thresholding
    threshold : float
        Threshold value used for discretization
    """
    print("=" * 50)
    print("SOLUTION STATISTICS")
    print("=" * 50)
    
    print(f"Classical Solution:")
    print(f"  Min value: {np.min(classical_solution):.6f}")
    print(f"  Max value: {np.max(classical_solution):.6f}")
    print(f"  Mean value: {np.mean(classical_solution):.6f}")
    print(f"  Std deviation: {np.std(classical_solution):.6f}")
    
    print(f"\nDiscretization:")
    print(f"  Threshold: {threshold}")
    print(f"  Elements above threshold: {np.sum(classical_solution > threshold)}")
    print(f"  Elements below threshold: {np.sum(classical_solution <= threshold)}")
    
    print(f"\nBinary Solution:")
    print(f"  Active elements (1s): {np.sum(discretized_solution)}")
    print(f"  Inactive elements (0s): {np.sum(discretized_solution == 0)}")
    print(f"  Total elements: {len(discretized_solution)}")
    print(f"  Activation rate: {np.mean(discretized_solution):.2%}")


@dataclasses.dataclass
class EventCollection:
    events: list
    
    def __post_init__(self):
        self.combined_modules = [module for event in self.events for module in event.modules]    
        self.combined_tracks = [track for event in self.events for track in event.tracks]
        self.combined_hits = [hit for event in self.events for hit in event.hits]
        self.relabel_track_ids()
    
    def relabel_track_ids(self):
        track_sum = 0
        for event_index, event in enumerate(self.events):
            if event_index == 0:
                track_sum += len(event.tracks)
                continue
            for hit in event.hits:
                if hit.track_id < track_sum:
                    hit.track_id += track_sum 

    def get_combined_event(self):
        from toy_model import state_event_model as em
        combined_segments = [segment for event in self.events for segment in event.segments]
        return em.Event(
            detector_geometry=self.events[0].detector_geometry,
            tracks=self.combined_tracks,
            hits=self.combined_hits,
            segments=combined_segments,
            modules=self.combined_modules
        )

def plot_event_2d(event_tracks, detector, x=2, y=1, figsize=(20, 11), dpi=200, 
                  filename="event_visualization.png", save_to_file=False,
                  show_pv=True, show_wrong_segments=True, uniform_segment_color=False,
                  segment_color='forestgreen'):
    """
    Plot a 2D visualization of the tracking event showing hits, true tracks, and detector modules.
    
    Parameters:
    -----------
    event_tracks : Event object or list of Event objects
        The generated event(s) containing tracks and hits
    detector : PlaneGeometry
        The detector geometry
    x, y : int
        Coordinate indices to plot (0=x, 1=y, 2=z)
    figsize : tuple
        Figure size in inches
    dpi : int
        Figure resolution
    filename : str
        Output filename if save_to_file=True
    save_to_file : bool
        Whether to save the figure
    show_pv : bool
        Whether to display primary vertices
    show_wrong_segments : bool
        Whether to display incorrect track segments (ghost connections)
    uniform_segment_color : bool
        If True, all segments use the same color. If False, true tracks are green, wrong are grey
    segment_color : str
        Color to use when uniform_segment_color=True
    """
    fig, ax = plt.subplots(figsize=figsize, dpi=dpi)
    
    if not isinstance(event_tracks, list):
        events = [event_tracks]
    else:
        events = event_tracks
    
    event_collection = EventCollection(events)
    combined_event = event_collection.get_combined_event()
    
    primary_vertices = []
    for event in events:
        if event.tracks:
            first_track = event.tracks[0]
            if first_track.hits:
                primary_vertices.append((0, 0, 0))
            else:
                primary_vertices.append((0, 0, 0))
        else:
            primary_vertices.append((0, 0, 0))
    
    modules = []
    n_modules = len(combined_event.modules)
    for i in range(n_modules):
        combined_hits = []
        for e in events:
            combined_hits.extend(e.modules[i].hits)
        modules.append(combined_hits)
    
    all_y_values = [hit[y] for hit in combined_event.hits]
    if all_y_values:
        y_min, y_max = min(all_y_values), max(all_y_values)
        y_range = y_max - y_min
        if y_range == 0:
            y_range = 1  
    else:
        y_min, y_max, y_range = -10, 10, 20
    
    for module in combined_event.modules:
        z = module.z
        ax.axvline(x=z, color='black', linewidth=6)
    
    segments = []
    
    if show_pv:
        for pv, event in zip(primary_vertices, events):
            if event.modules and event.modules[0].hits:
                for hit in event.modules[0].hits:
                    segments.append((pv, hit))
    
    for module1, module2 in pairwise(modules):
        for hit1 in module1:
            for hit2 in module2:
                segments.append((hit1, hit2))
    
    for hit1, hit2 in segments:
        if isinstance(hit1, tuple):  
            if not show_pv:
                continue
            color = 'blue'
            linewidth = 1
            alpha = 0
        elif uniform_segment_color:
            color = segment_color
            linewidth = 3
            alpha = 1
        elif hit1.track_id == hit2.track_id:
            color = 'forestgreen'
            linewidth = 3
            alpha = 1
        else:
            if not show_wrong_segments:
                continue
            color = 'black'
            linewidth = 1
            alpha = 0.1
        
        ax.plot([hit1[x], hit2[x]], [hit1[y], hit2[y]], 
                color=color, linewidth=linewidth, alpha=alpha, zorder=2)
    
    for hit in combined_event.hits:
        ax.scatter(hit[x], hit[y], color='black', s=50, zorder=3, linewidth=0)
        ax.scatter(hit[x], hit[y], color='white', s=20, zorder=4, linewidth=0)
    
    if show_pv:
        for i, pv in enumerate(primary_vertices):
            ax.scatter(pv[x], pv[y], color='black', s=400, marker='*', zorder=10)
            ax.text(pv[x], pv[y], f'PV{i+1}', fontsize=20, color='black',
                    verticalalignment='bottom', horizontalalignment='right')
    
    ax.set_xlabel('Z (mm)' if x == 2 else ('X (mm)' if x == 0 else 'Y (mm)'), fontsize=16)
    ax.set_ylabel('Y (mm)' if y == 1 else ('X (mm)' if y == 0 else 'Z (mm)'), fontsize=16)
    
    z_min = -5 if show_pv else 0  
    z_max = max(module.z for module in combined_event.modules) + 5
    ax.set_xlim(z_min, z_max)
    ax.set_ylim(y_min - 0.2 * y_range, y_max + 0.2 * y_range)
    
    ax.set_axis_off()
    
    if save_to_file:
        plt.savefig(f'figures/{filename}', bbox_inches='tight', transparent=True)
    
    plt.tight_layout()
    plt.show()