"""
Description:
- This file can be used as a reference for what each function call expects as parameters.
- Also shows default parameter definitions if the parameter is not included in the call. 
"""

import pymcell as pm

#-----------------------------------#
# Make worlds:
"""
Default Parameters:
    name = 'world_1' # then world_2, ...
    
Other Parameters:

"""
# Example_1: 
world = pm.make_world() 

#-----------------------------------#
# Add objects:
"""
Default Parameters: 
    name = 'obj_1'  # then obj_2, ...
    center = [0,0,0]
    normal_vector = [0,0,1]  # the x-y plane
    extrude_direction = normal_vector   
    display = 'SOLID' 
    triangulate = False
    
Other Parameters:
    type
    vertices = []
    faces = []
    radius
    extrude_length
    objects = [] # which objects the other parameters (such as "faces") are referencing
    etc. (see notebook, p.60)
"""
# Example_1:
box = pm.make_object(name = 'Box', type = 'CUBE') # default size and position
world.add_object(box)

# Example_2:
box_surfaces = pm.make_object(name = 'Surfaces', type = 'SURFACE', objects = [box], faces = [[0,1,2],[0,2,3],[4,5,6],[4,6,7]])
world.add_object(box_surfaces)

# Exmaple 3:
funky_shape = pm.make_object(name = 'Polyhedron', type = 'POLYHEDRON', vertices = verts_list, faces = faces_list)
world.add_object(funky_shape)

#-----------------------------------#
# Add species:
"""
Default Parameters:
    name = 'mol_1' # then mol_2, ...
    diffusion_const = 1e-6
    type = 'VOLUME'
    color = [1.0, 0, 0] # RGB spectrum
    scale_factor = 1
    shape = 'Sphere_1'

Other Parameters:

"""
# Example_1:
mol_a = pm.make_species(name = 'a', diffusion_const = 1e-5, type = 'SURFACE')
world.add_species(mol_a)

# Example_2:
mol_b = pm.make_species(name = 'b', color = [1.0, 1.0, 0]) # yellow
world.add_species(mol_b)

#-----------------------------------#
# Add release patterns:
"""
Defaults:
    name = 'rel_1' # then rel_2, ...
    boundary = release_region

Other Parameters:
    release_region
    species_list = []

"""
# Example_1: 
# Note that you can include multiple species to the release patterns, but all those species will then have all the same release parameters (quantity, probability, etc.)
rel_a = pm.make_release_pattern(species_list = [mol_a], location = [0,0,0], shape = 'SPHERICAL', probablity = 1, quantity = 1000)
world.add_release_pattern(rel_a)

#-----------------------------------#
# Add reactions:
"""
Default Parameters:
    name = 'react_1' # then react_2, ...
    forward_rate = 1e6
    rate = forward_rate
    backward_rate = 1e6
    
Other Parameters:
    reaction 

"""
# Example 1:
react_1 = pm.make_reaction(name = 'a_to_null', reaction = 'a -> NULL', forward_rate = 1e6)
world.add_reaction(react_1)

#-----------------------------------#
# Run simulations:
"""
Default Parameters:
    name = 'sim_1' # then 'sim_2', ...
    iterations = 1000
    time_step = 1e-6

Other Parameters:

"""
# Example 1:
sim_1 = pm.make_simulation()
world.run_simulation(sim_1)

#Example 2:
sim_1 = pm.make_simulation(iterations = 200, time_step = 5e-5)
world.run_simulation(sim_1)
world.modify_species(name = 'a', new_diffusion_const = 1e-4)
world.run_simulation(sim_1) # running modified simulation