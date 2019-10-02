"""
Description: 
"2D diffusion" between two sheets
- initial release in a line source

"""

import pymcell as pm

# Make worlds:
world = pm.make_world()

# Add objects:
# "CUBE" (perhaps we need a better name?) is defined first by declaring the [x,y,z] edge lendths ("dimensions"), then \
# the normal_vector is given to define it's rotational orientation about the center.
box = pm.make_object(name = 'Box', type = 'CUBE', center = [0,0,0], edge_dimensions = [10,10,0.01])
world.add_object(box)

# Add species:
mol_a = pm.make_species(name = 'a')
mol_b = pm.make_species(name = 'b')
mol_c = pm.make_species(name = 'c')
world.add_species(mol_a, mol_b, mol_c)

# Add release patterns:
rel_a_b = pm.make_release_pattern(species_list = [mol_a, mol_b], release_region = box)
world.add_release_pattern(rel_a_b)

# Add reactions:
react_1 = pm.make_reaction(name = 'React_1', reaction = 'a + b -> c')
world.add_reaction(react_1)

# Run simulations:
sim_1 = pm.make_simulation()  # using default iteration and time_step
world.run_simulation(sim_1)
