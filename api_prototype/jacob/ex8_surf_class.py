#!/usr/bin/env python3

#####################
# Surace classes
#####################

import pymcell as m


def main():
    a = m.Species("a", dc=1e-6)
    a_up = (a, m.Orient.up)
    a_down = (a, m.Orient.down)
    transp_a = m.SurfaceProperty("transp_a", m.SP.transp, a_down)
    absorb_a = m.SurfaceProperty("absorb_a", m.SP.absorb, a_down)
    clamp_a = m.SurfaceProperty("clamp_a", m.SP.clamp, a_up, clamp_val=1e-8)
    box = m.create_box("box", 1.0)
    box.add_surface_property(transp_a, box.regions["left"])
    box.add_surface_property(absorb_a, box.regions["right"])
    box.add_surface_property(clamp_a, box.regions["top"])
    box.add_surface_property(absorb_a, box.regions["top"])
    sim = m.Simulation(dt=1e-6, meshes=[box])
    sim.create_molecules_obj(a, box, 100)
    sim.run_iterations(100)

if __name__ == "__main__":
    main()
