#!/usr/bin/env python3

#####################
# Reactions in box
#####################

import pymcell
import logging
from pathlib import Path


def main():
    logging.basicConfig(level=logging.INFO)
    a = pymcell.Species("a", dc=1e-6)
    b = pymcell.Species("b", dc=1e-6)
    c = pymcell.Species("c", dc=1e-6)
    unimol1 = pymcell.Reaction([a], [b], rate=1e4)
    unimol2 = pymcell.Reaction([a], rate=1e4)
    bimol_irrev = pymcell.Reaction([a, b], [c], rate=1e4)
    bimol_rev = pymcell.Reaction([a, b], [c], reversible=True, rate=1e4)
    box = pymcell.import_obj(Path("./box.obj"))
    sim = pymcell.Simulation(dt=1e-6, meshes=[box])
    sim.create_molecules_obj(a, 100, (0, 0, 0))
    sim.run_iterations(100)

if __name__ == "__main__":
    main()
