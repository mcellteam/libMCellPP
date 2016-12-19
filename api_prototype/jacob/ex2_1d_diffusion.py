#!/usr/bin/env python3

###############################
# "1D" diffusion in a thin tube
###############################

import pymcell
import tube

def main():
    a = pymcell.Species("a", dc=1e-6)
    reg = pymcell.Region("reg", tube.reg_indices)
    tube_obj = pymcell.MeshObject("tube", tube.verts, tube.faces, [reg])
    mesh_objs = [tube_obj]
    sim = pymcell.Simulation(dt=1e-6, meshes=mesh_objs)
    sim.create_molecules_obj(a, 100, (0, 0, 0))
    sim.run_iterations(100)

if __name__ == "__main__":
    main()
