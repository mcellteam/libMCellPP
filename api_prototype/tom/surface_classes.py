#!/usr/bin/env python

import pyMCell as pymc

world = pymc.mcell_world()

world.add_species(name = "a", diffusion_constant = 1e-6, type = "VOLUME")
world.add_species(name = "b", diffusion_constant = 1e-6, type = "SURFACE")
world.add_species(name = "c", diffusion_constant = 1e-6, type = "SURFACE")

world.add_surface_class({"name":"transp_a", "property":'TRANSPARENT', "species":world.species.a})
world.add_surface_class({"name":"absorb_a", "property":'ABSORPTIVE', "species":world.species.a})
world.add_surface_class({"name":"clamp_a", "property":'CLAMP_CONCENTRATION', "species":world.species.a, "clamp_value":1e-6})

world.add_reaction({"reaction":"a, + b' -> c'", "forward_rate":1e7})

world.instance_geom_object({"name":"my_obj", "shape":"BOX", "vertices":[[-0.5,-0.5,-0.001],[0.5,0.5,0.001]]})

world.geometry.my_obj.add_region({"name":"bottom", "faces":['BOTTOM'], "surface_class":world.surface_classes.transp_a})

world.geometry.my_obj.add_region({"name":"bottom", "faces":['LEFT'], "surface_class":world.surface_classes.absorp_a})

world.geometry.my_obj.add_region({"name":"bottom", "faces":['RIGHT'], "surface_class":world.surface_classes.clamp_a})

world.add_release_site({"species":"a", "shape":world.geometry.my_obj, "number":1000}) 

world.add_release_site({"species":"b'", "shape":world.geometry.my_obj.regions.bottom, "number":1000})

world.run({})


