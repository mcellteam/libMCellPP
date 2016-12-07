#!/usr/bin/env python

import pyMCell as pymc
import math


class my_var_rxn_rate_listener(TCO_listener):

  def __init__(self, the_model, k):
    self.k = k
    the_model.register_event_listener(self, pymc.timestep_event)

  def execute(self, the_event):
    val = math.exp(-self.k*the_event.time)
    return val


world = pymc.mcell_world()

world.add_species(name = "a", diffusion_constant = 1e-6, type = "VOLUME")
world.add_species(name = "b", diffusion_constant = 1e-6, type = "SURFACE")
world.add_species(name = "c", diffusion_constant = 1e-6, type = "SURFACE")

world.add_reaction({"name":"ab_to_c", "reaction":"a, + b' -> c'", "forward_rate":my_var_rxn_rate_listener(world, 1e3)})

world.instance_geom_object({"name":"my_obj", "shape":"BOX", "vertices":[[-0.5,-0.5,-0.001],[0.5,0.5,0.001]]})

world.geometry.my_obj.add_region({"name":"bottom", "faces":['BOTTOM']})

world.add_release_site({"species":"a", "shape":world.geometry.my_obj, "number":1000}) 

world.add_release_site({"species":"b'", "shape":world.geometry.my_obj.regions.bottom, "number":1000})

# Note world.add_counter is a convenience API to world.register_event_listener)
world.add_counter({"name":"a_world","what":world.species.a, "where":"WORLD"})
world.add_counter({"name":"a_my_obj","what":world.species.a, "where":world.geometry.my_obj})
world.add_counter({"name":"a_my_obj_hits","what":world.species.a, "where":world.geometry.my_obj, "how":"BACK_HITS"})
world.add_counter({"name":"c_my_obj_bottom","what":world.species.c, "where":world.geometry.my_obj.regions.bottom, "when":10*world.timestep})
world.add_counter({"name":"a_world","what":world.reactions.ab_to_c, "where":"WORLD"})

world.counters.a_world.write("a_world.dat")

world.run({})


