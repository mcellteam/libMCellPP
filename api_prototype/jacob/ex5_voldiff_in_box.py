#!/usr/bin/env python3

#############################
# Volumetric diffusion in box
#############################

import pymcell as m


def main():
    a = m.Species("a", dc=1e-6)
    box = m.create_box("box", 1.0)
    sim = m.Simulation(dt=1e-6)
    sim.create_molecules_obj(a, box, 100)
    sim.run_iterations(100)

if __name__ == "__main__":
    main()
