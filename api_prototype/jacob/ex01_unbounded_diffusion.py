#!/usr/bin/env python3

#####################
# Unbounded diffusion
#####################

import pymcell as m


def main():
    a = m.Species("a", dc=1e-6)
    sim = m.Simulation(dt=1e-6)
    sim.create_molecules_shape(a, 100, (0, 0, 0))
    sim.run_iterations(100)


if __name__ == "__main__":
    main()
