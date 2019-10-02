"""
Description: 
Unbounded diffusion

"""

import pymcell as pm

# Make worlds:
world = pm.make_world()

# Add species:
mol_a = pm.make_species(name = 'a', diffusion_const = 1e-6, type = 'VOLUME')
world.add_species(mol_a)

# Add release patterns:
rel_a = pm.make_release_pattern(species_list = [mol_a], location = [0,0,0], shape = 'SPHERICAL', probablity = 1, quantity = 1000)
world.add_release_pattern(rel_a)

# Add reactions:
react_1 = pm.make_reaction(name = 'React_1', reaction = 'a -> NULL', forward_rate = 1e6)
world.add_reaction(react_1)

# Run simulations:
sim_1 = pm.make_simulation(iterations = 1000, time_step = 1e-6)  # these are the default parameters
world.run_simulation(sim_1)