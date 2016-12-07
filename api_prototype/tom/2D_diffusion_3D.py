#!/usr/bin/env python

import pyMCell as pymc

world = pymc.mcell_world()

world.add_species(name = "a", diffusion_constant = 1e-6, type = "VOLUME")

world.add_release_site({"species":"a", "shape":"SPHERICAL", "number":1000}) 

world.instance_geom_object({"name":"my_obj", "shape":"BOX", "vertices":[[-0.5,-0.5,-0.001],[0.5,0.5,0.001]]})

world.run({})


#variants
world.instance_geom_object({"name":"my_obj", "shape":"POLYGON_LIST", "vertices":vertex_list,"faces":face_list})

world.instance_geom_object({"name":"my_obj", "shape":"POLYGON_LIST", "vertices":mesh.vertices,"faces":mesh.faces})

world.instance_geom_object({"name":"my_obj", "shape":"POLYGON_LIST", "polygon_data":my_obj.data})

