"""
Description: 
"1D diffusion" in a thin tube
- initial release in a plane in the middle

"""

import pymcell as pm

# Make worlds:
world = pm.make_world()

# Add objects:
# In make_object(), there are many input parameters, and if you don't include the necessary \ 
# parameters for the given object type, you'll get default values and perhaps a notification.
cylinder = pm.make_object(name = 'Cylinder', type = 'CYLINDER', center = [0,0,0], radius = 1, normal_vector = [1,0,0], extrude_length = 20)
plane = pm.make_object(name = 'Plane', type = 'PLANE', center = [0,0,0], normal_vector = [1,0,0])
world.add_object(cylinder, plane)

# Add species:
mol_a = pm.make_species(name = 'a', scale_factor = 2)
world.add_species(mol_a)

# Add release patterns:
rel_a = pm.make_release_pattern(species_list = [mol_a], release_region = plane, boundary = cylinder)
world.add_release_pattern(rel_a)

# Add reactions:
react_1 = pm.make_reaction(name = 'React_1', reaction = 'a -> NULL')
world.add_reaction(react_1)

# Run simulations:
sim_1 = pm.make_simulation()  # using default iteration and time_step
world.run_simulation(sim_1)