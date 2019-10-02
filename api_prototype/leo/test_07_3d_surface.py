"""
Description:
Box of A & B with reactions on a surface:
- A (volumetric) + B (surface) -> C (surface)

"""

import pymcell as pm

# Make worlds:
world = pm.make_world()

# Add objects:
box = pm.make_object(name = 'Box', type = 'CUBE') # default size and position
# adding partial box surface object for "# Add release patterns:" section:
# box_surfaces = pm.make_object(name = 'Surfaces', type = 'SURFACE', objects = [box], faces = [[0,1,2],[0,2,3],[4,5,6],[4,6,7]])
world.add_object(box)

# Add species:
mol_a = pm.make_species(name = 'a') # red, Sphere_1, 1e-6, and VOLUME by default
mol_b = pm.make_species(name = 'b', color = [0,0,1], type = 'SURFACE') # blue
mol_c = pm.make_species(name = 'c', color = [0,1,0], type = 'SURFACE') # green
world.add_species(mol_a, mol_b, mol_c)

# Add release patterns:
rel_a = pm.make_release_pattern(species_list = [mol_a], release_region = box)
# since mol_b is a surface molecule, I shouldn't have to specify that it only exists on the box surfaces. 
rel_b = pm.make_release_pattern(species_list = [mol_b], quantity = 200, release_region = box)
# Alternative: if you only wanted mol_b on some of the box surfaces, then you must specify further:
# rel_b_alt = pm.make_release_pattern(species = mol_b, quantity = 200, release_region = box_surfaces)
world.add_release_pattern(rel_a, rel_b)

# Add reactions:
react_1 = pm.make_reaction(name = 'React_1', reaction = 'a + b -> c')
world.add_reaction(react_1)

# Run simulations:
sim_1 = pm.make_simulation()  # using default iteration and time_step
world.run_simulation(sim_1)