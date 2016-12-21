#!/usr/bin/env python3

###############################
# "1D" diffusion in a thin tube
###############################

import pymcell as m
import tube


def main():
    a = m.Species("a", dc=1e-6)
    reg = m.Region("tube_reg", tube.reg_indices)
    tube_obj = m.MeshObject("tube", tube.verts, tube.faces, [reg])
    mesh_objs = [tube_obj]
    sim = m.Simulation(dt=1e-6, meshes=mesh_objs)
    sim.create_molecules_reg(a, reg, 100)
    sim.run_iterations(100)

if __name__ == "__main__":
    main()
