"""
Description:
Dynamic changes
- Dynamic geometry: an interface to change the mesh at each timestep
    + Example: An initial box that updates it's geometry at each timestep with some new list of vertices and faces
"""

import pymcell as pm

# Make worlds:
world = pm.make_world()

# Add objects:
x_len = 1
y_len = 1
z_len = 1
dynmc_box = pm.make_object(name = 'Dynamic_box', type = 'CUBE', edge_dimensions = [x_len,y_len,z_len]) # default position
world.add_object(dynmc_box)

# Add species:
diff_const = 1e-6
mol_a = pm.make_species(name = 'a') # red, Sphere_1, 1e-6, and VOLUME by default
world.add_species(mol_a)

# Add release patterns:
rel_a = pm.make_release_pattern(species_list = [mol_a], release_region = dynmc_box)
world.add_release_pattern(rel_a)

# Run simulations:
iters = 500
sim_1 = pm.make_simulation(iterations = iters, time_step = 1e-5)
for i in range(0,iters):
    world.run_simulation_step(simulations = [sim_1], step_number = i) # step_duration = sim_1.time_step by default 
    # "name" is used to ID which object we're changing, then all "new_" parameters update the previous version
    world.modify_object(name = 'Dynamic_box', new_edge_dimensions = [1,1,1.0 + i/250]) # z dim growing slowly.
