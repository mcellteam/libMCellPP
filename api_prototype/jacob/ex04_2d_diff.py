#!/usr/bin/env python3

###############################
# 2D diffusion on surface
###############################

import pymcell as m


def main():
    a = m.Species("a", volume=False, dc=1e-6)
    box = m.create_box("box", 1.0, (0, 0, 0))
    sim = m.Simulation(dt=1e-6, meshes=[box])
    sim.create_molecules_reg(
        a, box.regions["top"], 100, conc_dens=True, orient=m.Orient.up)
    sim.run_iterations(100)


if __name__ == "__main__":
    main()
