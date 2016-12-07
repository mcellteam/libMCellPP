#!/usr/bin/env python

import pyMCell as pymc

world = pymc.mcell_world()

world.add_species(name = "a", diffusion_constant = 1e-6, type = "SURFACE")

world.instance_geom_object({"name":"my_obj", "shape":"BOX", "vertices":[[-0.5,-0.5,-0.001],[0.5,0.5,0.001]]})

world.geometry.my_obj.add_region({"name":"bottom", "faces":['BOTTOM']})

world.add_release_site({"species":"a", "shape":world.geometry.my_obj.regions.bottom, "number":1000}) 

world.run({})


