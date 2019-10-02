"""
Description:
Dynamic changes
- Dynamic diffusion constants: changing the diffusion constant for a molecule
    + Example: A box of diffusing A particles that increase their diffusion constants over time
"""

import pymcell as pm
import dynamic_diffusion as dd # external .py file that defines different diff_consts at different times.

# Make worlds:
world = pm.make_world()

# Add objects:
box = pm.make_object(name = 'Box', type = 'CUBE') # default size and position
world.add_object(box)

# Add species:
diff_const = 1e-6 
mol_a = pm.make_species(name = 'a', diffusion_const = diff_const) # red, Sphere_1, 1e-6, and VOLUME by default
world.add_species(mol_a)

# Add release patterns:
rel_a = pm.make_release_pattern(species_list = [mol_a], release_region = box)
world.add_release_pattern(rel_a)

# Run simulations:
iters = 1000
t_step = 1e-6
sim_1 = pm.make_simulation(iterations = iters, time_step = t_step)
for i in range(0,iters):
    world.run_simulation_step(simulations = [sim_1], step_number = i) # step_duration = time_step by default
    diff_const = dd.get_diff_const(time = t_step*i) # returns diff_const depending on a given time of simulation
    # "name" is used to ID which object we're changing, then all "new_" parameters update the previous version
    world.modify_species(name = 'a', new_diffusion_const = diff_const)
