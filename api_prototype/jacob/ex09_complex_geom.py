#!/usr/bin/env python3

########################
# Complex geometry
########################

import cellblender.pymcell as m
import bpy


def main():
    bl_obj = bpy.data.objects["Cube"]
    obj = m.import_blender_mesh(bl_obj)
    sim = m.Simulation(dt=1e-6, meshes=[obj])
    sim.run_iterations(100)


if __name__ == "__main__":
    main()
