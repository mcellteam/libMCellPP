#!/usr/bin/env python3

#####################
# Counting
#####################

import pymcell as m
from pathlib import Path


def main():
    a = m.Species("a", dc=1e-6)
    b = m.Species("b", dc=1e-6)
    c = m.Species("c", dc=1e-6)
    a_mix = (a, m.Orient.mix)
    b_mix = (b, m.Orient.mix)
    c_mix = (c, m.Orient.mix)
    bimol_irrev = m.Reaction([a_mix, b_mix], [c_mix], rate=1e4, name="rxn")
    box = m.create_box("box", 1.0)
    count_a_box = m.CountMolecules(a, box)
    count_a_rxn = m.CountReaction(bimol_irrev, box)
    sim_counts = [count_a_box, count_a_rxn]
    sim = m.Simulation(
        dt=1e-6, meshes=[box], reactions=[bimol_irrev], counts=sim_counts)
    sim.create_molecules_obj(a, box, 100)
    sim.create_molecules_obj(b, box, 100)
    sim.run_iterations(100)

if __name__ == "__main__":
    main()
