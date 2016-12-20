#!/usr/bin/env python3

########################
# Reactions on a surface
########################

import pymcell as m
from pathlib import Path


def main():
    a = m.Species("a", dc=1e-6)
    b = m.Species("b", volume=False, dc=1e-6)
    c = m.Species("c", volume=False, dc=1e-6)
    a_mix = (a, m.Orient.mix)
    b_up = (b, m.Orient.up)
    c_up = (c, m.Orient.up)
    bimol_irrev = m.Reaction([a_mix, b_up], [c_up], rate=1e4)
    box = m.import_obj(Path("./box.obj"))
    sim = m.Simulation(dt=1e-6, meshes=[box], reactions=[bimol_irrev])
    sim.create_molecules_obj(a, box, 100)
    sim.create_molecules_obj(b, box, 100)
    sim.run_iterations(100)

if __name__ == "__main__":
    main()
