#!/usr/bin/env python

import pyMCell as pymc

world = pymc.mcell_world()

world.add_species(name = "a", diffusion_constant = 1e-6, type = "VOLUME")

#variant
world.add_species({"diffusion_constant":1e-6, "type":"VOLUME")

world.add_release_site({"species":"a", "shape":"SPHERICAL", "number":1000}) 

world.run({})





#variants
a = world.add_species({"name":"a", "diffusion_constant":1e-6, "type":"VOLUME")

world.add_release_site({"species":a, "shape":"SPHERICAL", "number":1000}) 

world.add_release_site({"species":world.species.a, "shape":"SPHERICAL", "number":1000}) 

world.add_release_site({"species":world.get_species("a"), "shape":"SPHERICAL", "number":1000}) 


