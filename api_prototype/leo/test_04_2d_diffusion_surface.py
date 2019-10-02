"""
Description: 
2D diffusion on a real 2D surface
- initial release on a patch by either density or Boolean intersection of e.g. a sphere with a plane

"""

import pymcell as pm

# Make worlds:
world = pm.make_world()

# Add objects:
box = pm.make_object(name = 'Box', type = 'CUBE')
# could also write: faces = ['BOTTOM']
surface = pm.redefine_object(name = 'Surface', type = 'SURFACE', objects = [box], faces = [[0,1,2],[0,2,3]])
world.add_object(box, surface)

# Add species:
mol_a = pm.make_species(name = 'a', type = 'SURFACE', scale_factor = .5)
world.add_species(mol_a)

# Add release patterns:
rel_a = pm.make_release_pattern(species_list = [mol_a], release_region = surface)
world.add_release_pattern(rel_a)

# Run simulations:
sim_1 = pm.make_simulation()  # using default iteration and time_step
world.run_simulation(sim_1)