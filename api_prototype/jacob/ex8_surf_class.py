#!/usr/bin/env python3

#####################
# Surace classes
#####################

import pymcell as m
from pathlib import Path


def main():
    a = m.Species("a", dc=1e-6)
    a_mix = (a, m.Orient.mix)
    box = m.create_box("box")
    sim = m.Simulation(dt=1e-6, meshes=[box])
    sim.create_molecules_obj(a, box, 100)
    sim.run_iterations(100)

if __name__ == "__main__":
    main()
