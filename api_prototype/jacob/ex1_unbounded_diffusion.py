#!/usr/bin/env python3

#####################
# Unbounded diffusion
#####################

import pymcell


def main():
    a = pymcell.Species("a", dc=1e-6)
    sim = pymcell.Simulation(dt=1e-6)
    sim.create_molecules_shape(a, 100, (0, 0, 0))
    sim.run_iterations(100)

if __name__ == "__main__":
    main()
