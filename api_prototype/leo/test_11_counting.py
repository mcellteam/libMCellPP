"""
Description: 
Counting statements
- A box (maybe with some region definition) with A+B->C reaction where we count each of the following at each timestep:
    + What: molecule, reaction, event/trigger
    + Where: World, object, region
    + When: frequency of counting
    + How: Front hits/back hits, e.g. on a plane that goes through the box
"""

import pymcell as pm

# Make worlds:
world = pm.make_world()

# Add objects:
box = pm.make_object(type = 'CUBE') # default size and position
plane = pm.make_object(type = 'SURFACE', normal_vector = [0,1,0]) # 1x1 plane created on the x-z plane
world.add_object(box, plane)

# Add species:
mol_a = pm.make_species(name = 'a') # red, Sphere_1, 1e-6, and VOLUME by default
mol_b = pm.make_species(name = 'b', color = [0,0,1]) # blue 
mol_c = pm.make_species(name = 'c', color = [0,1,0]) # green
world.add_species(mol_a, mol_b, mol_c)

# Add release patterns:
rel_a_b = pm.make_release_pattern(species_list = [mol_a, mol_b], release_region = box)
world.add_release_pattern(rel_a_b)

# Add reactions:
react_a_b = pm.make_reaction(name = 'react_1', reaction = 'a + b -> c')
world.add_reaction(react_a_b)

# Run simulations:
iters = 50
t_step = 1e-6
sim_1 = pm.make_simulation(iterations = iters, time_step = t_step)
for i in range(0,iters):
    world.run_simulation_step(simulations = [sim_1], step_number = i)
    print 'Time: ', i*t_step
    print 'mol_a count: ', world.get_species_count(name = 'a', time = i*t_step)
    print 'mol_b count: ', world.get_species_count(name = 'b', time = i*t_step)
    print 'mol_c count: ', world.get_species_count(name = 'c', time = i*t_step)
    print 'Reaction a+b->c count: ', world.get_reaction_count(name = 'react_1', time = i*t_step)
    # ... and so on ... world.get_what_you_want_count()
