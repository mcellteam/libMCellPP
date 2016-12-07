#!/usr/bin/env python

import pyMCell as pymc

world = pymc.mcell_world()

world.add_species(name = "a", diffusion_constant = 1e-6, type = "VOLUME")
world.add_species(name = "b", diffusion_constant = 1e-6, type = "VOLUME")
world.add_species(name = "c", diffusion_constant = 1e-6, type = "VOLUME")

world.add_reaction({"name":"nil", "reaction":"a -> NULL", "forward_rate":1e3})
world.add_reaction({"reaction":"a -> b", "forward_rate":1e3})
world.add_reaction({"reaction":"a + b -> c", "forward_rate":1e7})
world.add_reaction({"reaction":"a + b <-> c", "forward_rate":1e7, "backward_rate":1e3})

world.instance_geom_object({"name":"my_obj", "shape":"BOX", "vertices":[[-0.5,-0.5,-0.001],[0.5,0.5,0.001]]})

world.add_release_site({"species":"a", "shape":world.geometry.my_obj, "number":1000}) 

world.add_release_site({"species":"b", "shape":world.geometry.my_obj, "number":1000}) 

world.run({})


