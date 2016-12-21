#!/usr/bin/env python3

###############################
# "1D" diffusion in a thin tube
###############################

import pymcell as m


def main():
    a = m.Species("a", dc=1e-6)
    plane_top = m.create_plane("top", 1.0, (0, 0, 0.1))
    plane_bottom = m.create_plane("bottom", 1.0,  (0, 0, -0.1))
    mesh_objs = [plane_top, plane_bottom]
    sim = m.Simulation(dt=1e-6, meshes=mesh_objs)
    for i in range(-10, 11):
        sim.create_molecule(a, (i*0.1, 0, 0))
    sim.run_iterations(100)


if __name__ == "__main__":
    main()
