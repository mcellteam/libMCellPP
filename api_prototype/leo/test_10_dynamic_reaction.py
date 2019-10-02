"""
Description:
Dynamic changes:
- Dynamic rate constants: changing the rate constant of a reaction
    + Example: A box with A+B->C that where the rate constant depends on the number of A,B, or C
"""

import pymcell as pm

# Make worlds:
world = pm.make_world()

# Add objects:
box = pm.make_object(type = 'CUBE') # default name, size, and position
world.add_object(box)

# Add species:
mol_a = pm.make_species(name = 'a') # red, Sphere_1, 1e-6, and VOLUME by default
mol_b = pm.make_species(name = 'b', color = [0,0,1]) # blue
mol_c = pm.make_species(name = 'c', color = [0,1,0]) # green
world.add_species(mol_a, mol_b, mol_c)

# Add release patterns:
rel_a_b = pm.make_release_pattern(species_list = [mol_a, mol_b], release_region = box)
world.add_release_pattern(rel_a_b)

# Add reactions:
dynmc_rate = 1e5
react_dynmc = pm.make_reaction(name = 'react_1', reaction = 'a + b -> c', rate = dynmc_rate)
world.add_reaction(react_dynmc)

# Run simulations:
iters = 1000
t_step = 1e-6
step_len = 10
sim_1 = pm.make_simulation(iterations = iters, time_step = t_step)
for i in range(0,iters, step_len):
    world.run_simulation_step(simulations = [sim_1], step_number = i, step_duration = t_step(step_len) )
    dynmc_rate += 1e-6    
    # "name" is used to ID which object we're changing, then all "new_" parameters update the previous version
    world.modify_reaction(name = 'react_1', new_rate = dynmc_rate) # rate is slowly increasing
