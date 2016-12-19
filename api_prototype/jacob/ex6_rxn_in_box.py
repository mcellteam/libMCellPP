#!/usr/bin/env python3

#####################
# Reactions in box
#####################

import pymcell
from pathlib import Path


def main():
    a = pymcell.Species("a", dc=1e-6)
    b = pymcell.Species("b", dc=1e-6)
    c = pymcell.Species("c", dc=1e-6)
    unimol1 = pymcell.Reaction([a], [b], rate=1e4)
    unimol2 = pymcell.Reaction([a], rate=1e4)
    bimol_irrev = pymcell.Reaction([a, b], [c], rate=1e4)
    bimol_rev = pymcell.Reaction([a, b], [c], reversible=True, rate=1e4)
    box = pymcell.import_obj(Path("./box.obj"))
    sim = pymcell.Simulation(dt=1e-6, meshes=[box])
    sim.create_molecules_obj(a, box, 100)
    sim.create_molecules_obj(b, box, 100)
    sim.run_iterations(100)

if __name__ == "__main__":
    main()
