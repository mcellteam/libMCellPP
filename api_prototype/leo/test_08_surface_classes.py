"""
Description:
Surface classes
- Box with one transparent side to molecule A
- Box with absorptive side to molecule A
- Box with concentration clamp of A on one side and absorptive on the opposing side

"""

import pymcell as pm

# Make worlds:
world_trans = pm.make_world() # "name = " defaults to "World_1"
world_abs = pm.make_world()  # "name = " defaults to "World_2"
world_clamp_abs = pm.make_world()

# Add objects:
box = pm.make_object(name = 'Box', type = 'CUBE') # default size and position
world_trans.add_object(box)
world_abs.add_object(box)
world_clamp_abs.add_object(box)

# Add species:
mol_a = pm.make_species(name = 'a') # red, Sphere_1, 1e-6, and VOLUME by default
world_trans.add_species(mol_a)
world_abs.add_species(mol_a)
world_clamp_abs.add_species(mol_a)

# Add surface classes:
trans_surf = pm.make_surface_class(type = 'TRANSPARENT', molecules = [mol_a])
abs_surf = pm.make_surface_class(type = 'ABSORPTIVE', molecules = [mol_a])
clamp_surf = pm.make_surface_class(type = 'CLAMP_CONCENTRATION', objects = [box], faces = [[1,3,5],[2,5,6]], molecules = [mol_a])
world_trans.add_surface_class(surface_classes = [trans_surf], objects = [box], faces = [[0,2,4],[3,4,7]])
world_abs.add_surface_class(surface_classes = [abs_surf], objects = [box], faces = [[1,3,5],[2,5,6]])
world_clamp_abs.add_surface_class(surface_classes = [clamp_surf], objects = [box], faces = [[0,2,4],[3,4,7]])
world_clamp_abs.add_surface_class(surface_classes = [abs_surf], objects = [box], faces = [[1,3,5],[2,5,6]])

# Add release patterns:
rel_a = pm.make_release_pattern(species_list = [mol_a], release_region = box)
world_trans.add_release_pattern(rel_a)
world_abs.add_release_pattern(rel_a)
# assuming CLAMP_CONCENTRATION allows for diffusion, so we don't need to add an additional release in to world_clamp_abs

# Add reactions:
# nada que hacer aqui

# Run simulations:
sim_long = pm.make_simulation(iterations = 200)  # using custom iterations and default time_step
sim_short = pm.make_simulation(iterations = 1500)  # using custom iterations and default time_step
world_trans.run_simulation(sim_short)
world_abs.run_simulation(sim_short)
world_clamp_abs.run_simulation(sim_long)