"""
Description:
Box of A & B with reactions:
- A -> 0 decay
- A -> B decay
- A + B -> C irreversible
- A + B <-> C reversible

"""

import pymcell as pm

# Make worlds:
world = pm.make_world()

# Add objects:
box = pm.make_object(name = 'Box', type = 'CUBE') # default size and position
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
react_1 = pm.make_reaction(name = 'React_1', reaction = 'a -> NULL')  # 1e3 forward_rate by default
react_2 = pm.make_reaction(name = 'React_2', reaction = 'a -> b', forward_rate = 1e4)
react_3 = pm.make_reaction(name = 'React_3', reaction = 'a + b -> c', forward_rate = 5e3)  # isn't this redundant? 
react_4 = pm.make_reaction(name = 'React_4', reaction = 'a + b <-> c', forward_rate = 5e3, backward_rate = 1e8)
world.add_reaction(react_1,react_2,react_3,react_4)

# Run simulations:
sim_1 = pm.make_simulation()  # using default iteration and time_step
world.run_simulation(sim_1)