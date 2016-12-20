#!/usr/bin/env python3

#####################
# Reactions in box
#####################

import pymcell as m
from pathlib import Path


def main():
    a = m.Species("a", dc=1e-6)
    b = m.Species("b", dc=1e-6)
    c = m.Species("c", dc=1e-6)
    a_mix = (a, m.Orient.mix)
    b_mix = (b, m.Orient.mix)
    c_mix = (b, m.Orient.mix)
    unimol1 = m.Reaction([a_mix], [b_mix], rate=1e4)
    unimol2 = m.Reaction([a_mix], rate=1e4)
    bimol_irrev = m.Reaction([a_mix, b_mix], [c_mix], rate=1e4)
    bimol_rev = m.Reaction([a_mix, b_mix], [c_mix], reversible=True, rate=1e4)
    box = m.import_obj(Path("./box.obj"))
    sim = m.Simulation(dt=1e-6, meshes=[box])
    sim.create_molecules_obj(a, box, 100)
    sim.create_molecules_obj(b, box, 100)
    sim.run_iterations(100)

if __name__ == "__main__":
    main()
