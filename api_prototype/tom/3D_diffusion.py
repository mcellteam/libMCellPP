#!/usr/bin/env python

import pyMCell as pymc

world = pymc.mcell_world()

world.add_species(name = "a", diffusion_constant = 1e-6, type = "VOLUME")

world.instance_geom_object({"name":"my_obj", "shape":"BOX", "vertices":[[-0.5,-0.5,-0.001],[0.5,0.5,0.001]]})

world.add_release_site({"species":"a", "shape":world.geometry.my_obj, "number":1000}) 

world.run({})


