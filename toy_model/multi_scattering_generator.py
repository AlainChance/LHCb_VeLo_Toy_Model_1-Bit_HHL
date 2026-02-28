import numpy as np
import toy_model.state_event_model as em
import dataclasses
from itertools import count

@dataclasses.dataclass(frozen=True)
class SimpleDetectorGeometry:
    module_id   : list[int]
    lx          : list[float]
    ly          : list[float]
    z           : list[float]
    
    def __getitem__(self, index):
        return (self.module_id[index], self.lx[index], self.ly[index], self.z[index])
    
    def __len__(self):
        return len(self.module_id)

@dataclasses.dataclass()
class MultiScatteringGenerator:
    detector_geometry   : SimpleDetectorGeometry
    primary_vertices    : list = dataclasses.field(default_factory=list)
    phi_min             : float = 0.0
    phi_max             : float = 2*np.pi
    theta_min           : float = 0.0
    theta_max           : float = np.pi/10
    rng                 : np.random.Generator = np.random.default_rng()
    #ToDo : Fix the divergence angles
    theta_divergence = np.pi/20
    phi_divergence = np.pi/20

    def generate_random_primary_vertices(self, n_events, sigma):
        primary_vertices = []
        for _ in range(n_events):
            x = self.rng.normal(0, sigma[0])
            y = self.rng.normal(0, sigma[1])
            z = self.rng.normal(0, sigma[2])
            primary_vertices.append((x, y, z))
        return primary_vertices

    def find_vs(self, theta, phi):
        return np.sin(theta) * np.cos(phi), np.sin(theta) * np.sin(phi), np.cos(theta)
    
    #ToDo: Fix events naming
    def generate_event(self, n_particles, n_events=1, sigma=(0,0,0), defined_primary_vertex=None):
        hit_id_counter = count()
        all_events = []

        for event_index in range(n_events):
            
            if defined_primary_vertex is not None:
                primary_vertex = defined_primary_vertex[event_index]
            elif defined_primary_vertex is None:
                primary_vertex = (0,0,0)
            else:
                primary_vertex = self.generate_random_primary_vertices(1,sigma)[0]

            mc_info = []

            hits_per_module = [[] for _ in range(len(self.detector_geometry.module_id))]
            hits_per_track = []

            pvx, pvy, pvz = primary_vertex
            self.primary_vertices.append((pvx, pvy, pvz))

            for track_id in range(n_particles):
                phi = self.rng.uniform(self.phi_min, self.phi_max)
                cos_theta = self.rng.uniform(np.cos(self.theta_max), np.cos(self.theta_min))
                theta = np.arccos(cos_theta)
                sin_theta = np.sin(theta)

                vx, vy, vz = self.find_vs(theta, phi)

                track_hits = []
                zs = [pvz]
                x_hits = [pvx]
                y_hits = [pvy]
                vxs = [vx]
                vys = [vy]
                vzs = [vz]
                ts = [0]
                thetas = [theta]
                phis = [phi]
                ts = []

                for idx, (module_id, zm, lx, ly) in enumerate(
                        zip(self.detector_geometry.module_id, self.detector_geometry.z, self.detector_geometry.lx,
                            self.detector_geometry.ly)):
                    
                    t = (zm - zs[idx]) / vz
                    ts.append(t)
                    zs.append(zm)

                    x_hits.append(x_hits[idx] + vxs[idx] * t)
                    y_hits.append(y_hits[idx] + vys[idx] * t)
                    # ToDo: Name resolution noise a parameter of order 10 microns

                    #ToDo: Impliment as x,y scattering - Marcel to send specification
                    additional_cos_phi = self.rng.normal(0, self.phi_divergence)
                    additional_cos_theta = self.rng.normal(0, self.theta_divergence)
                    additional_phi = np.arccos(additional_cos_phi)
                    additional_theta = np.arccos(additional_cos_theta)

                    phis.append(phi + additional_phi)
                    thetas.append(theta + additional_theta)

                    vx, vy, vz = self.find_vs(thetas[idx+1], phis[idx+1])
                    vxs.append(vx)
                    vys.append(vy)
                    vzs.append(vz)

            
                   
                    if np.abs(x_hits[idx+1]) < lx / 2 and np.abs(y_hits[idx+1]) < ly / 2: 
                        hit = em.Hit(next(hit_id_counter), x_hits[idx+1] + self.rng.normal(0, 1e-5), y_hits[idx+1] + self.rng.normal(0, 1e-5), zm, module_id, track_id)
                        hits_per_module[idx].append(hit)
                        track_hits = [em.Hit(next(hit_id_counter),x + self.rng.normal(0, 1e-5), y + self.rng.normal(0, 1e-5), z, module_id, track_id) for x, y, z in zip(x_hits[1:], y_hits[1:], zs[1:])]
                hits_per_track.append(track_hits)

            mc_info.append((track_id, em.MCInfo(
                    primary_vertex,
                    phis,
                    thetas,
                    ts)))

            modules = [em.Module(module_id, z, lx, ly, hits_per_module[idx]) for idx, (module_id, z, lx, ly) in
                       enumerate(
                           zip(self.detector_geometry.module_id, self.detector_geometry.z, self.detector_geometry.lx,
                                self.detector_geometry.ly))]
            tracks = []

            for idx, (track_id, mc_info) in enumerate(mc_info):
                tracks.append(em.Track(track_id, mc_info, hits_per_track[idx]))
            global_hits = [hit for sublist in hits_per_module for hit in sublist]

            all_events.append(em.Event(modules, tracks, global_hits))
        if n_events == 1:
            all_events = all_events[0]
        return all_events
                