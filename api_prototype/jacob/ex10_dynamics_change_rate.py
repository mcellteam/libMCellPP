#!/usr/bin/env python3

#####################
# Dynamic changes
#####################

import pymcell as m
import math


def main():
    a = m.Species("a", dc=1e-6)
    b = m.Species("b", dc=1e-6)
    c = m.Species("c", dc=1e-6)
    a_mix = (a, m.Orient.mix)
    b_mix = (b, m.Orient.mix)
    c_mix = (c, m.Orient.mix)
    bimol_irrev = m.Reaction([a_mix, b_mix], [c_mix], rate=0)
    box = m.create_box("box", 1.0, (0, 0, 0))
    sim = m.Simulation(dt=1e-6, meshes=[box], reactions=[bimol_irrev])
    sim.create_molecules_obj(a, box, 100)
    sim.create_molecules_obj(b, box, 100)
    for i in range(100):
        offs = 1e6
        bimol_irrev.rate = math.sin(i*0.1)*offs+offs
        sim.run_iteration()


if __name__ == "__main__":
    main()
