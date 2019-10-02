"""
Description:
Object with a generally complex geometry from some list of vertices and faces.

"""

import pymcell as pm
import my_shape  # py file containing functions that return vertices and faces

# Make worlds:
world = pm.make_world()

# Add objects:
# get lists from my_shape.py, which was imported at the top
verts_list = my_shape.get_vertices()
faces_list = my_shape.get_faces()
"""
# could also list the geometry in this file if it isn't too extensive:
verts_list = [
     [ -5.0, -1.0, -5.0 ],
     [ -1.0, -0.5, 0.5 ],
     [ -1.0, 1.0, -5.0 ],
     [ -0.5, 1.0, 2.0 ],
     [ 7.0, -15.0, -1.0 ],
     [ 3.0, -1.0, 5.0 ],
     [ 4.0, 2.0, -0.5 ],
     [1.0, 1.0, 1.0 ] ]
faces_list = [ 
     [ 3, 0, 1 ],
     [ 7, 2, 3 ],
     [ 5, 6, 7 ],
     [ 1, 4, 5 ],
     [ 2, 4, 0 ],
     [ 7, 1, 5 ],
     [ 3, 2, 0 ],
     [ 7, 6, 2 ],
     [ 5, 4, 6 ],
     [ 1, 0, 4 ],
     [ 2, 6, 4 ],
     [ 7, 3, 1 ] ]
"""
funky_shape = pm.make_object(name = 'Polyhedron', type = 'POLYHEDRON', vertices = verts_list, faces = faces_list)
world.add_object(funky_shape)

# Add species:
mol_a = pm.make_species(name = 'a') # red, Sphere_1, 1e-6, and VOLUME by default
world.add_species(mol_a)

# Add release patterns:
rel_a = pm.make_release_pattern(species_list = [mol_a], release_region = funky_shape)
world.add_release_pattern(rel_a)

# Add reactions:

# Run simulations:
sim_1 = pm.make_simulation(time_step = 1e-5)  # using default iteration and custom time_step
world.run_simulation(sim_1)