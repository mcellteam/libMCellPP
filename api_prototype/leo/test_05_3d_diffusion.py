"""
Description:
Volumetric diffusion in a box/sphere

"""

import pymcell as pm

# Make worlds:
world = pm.make_world()

# Add objects:
box = pm.make_object(name = 'Box', type = 'CUBE') # default size and position
world.add_object(box)

# Add species:
mol_a = pm.make_species(name = 'a', scale_factor = .5) 
world.add_species(mol_a)

# Add release patterns:
rel_a = pm.make_release_pattern(species_list = [mol_a], release_region = box)
world.add_release_pattern(rel_a)

# Run simulations:
sim_1 = pm.make_simulation()  # using default iteration and time_step
world.run_simulation(sim_1)

