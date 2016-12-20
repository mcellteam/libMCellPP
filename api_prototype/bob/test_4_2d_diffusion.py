# 2D diffusion on a real 2D surface - initial release on a patch by either density or Boolean intersection of e.g. a sphere with a plane

# Note that this example could use an outside library to do the Boolean intersection.
# We might implement such functionality, but I suspect other libraries may be available.

# Parameters to vary
iterations = 1000
num_A = 200
sheet_size = 10
release_radius = 2


# Import the things needed
import pymcell as m
import random
import external_geometry_library as egl


# Make a world
sim = m.create_model()


# Set current time and timestep
sim.t = 0.0
sim.dt = 1e-6


# Add the standard iteration callback to capture molecule positions
sim.iteration_callback_list.append ( callback=m.viz_output_callback, data={['ALL']}, skip=0 )


# Create the species and add to simulation
mol_A = m.create_species(name="A",dc=1e-5,type=m.SURFACE_TYPE) # Volume mol by default
sim.species_list.append(mol_A)


# Create a sheet at z=0 (the old-fashioned way)
points = [
  [ -1, -1, 0 ],
  [  1, -1, 0 ],
  [  1,  1, 0 ],
  [ -1,  1, 0 ] ]

faces = [
  [ 0, 1, 2 ],
  [ 0, 2, 3 ] ]

# Scale the points in the x,y dimension
for p in points:
  p[0] *= sheet_size
  p[1] *= sheet_size

release_points = []

use_outside_library = False
if use_outside_library:
  egl_plane = egl.create_object_from_points_and_faces ( points, faces )
  egl_sphere = egl.create_sphere ( center=(0,0,0), radius=release_radius )
  (egl_point_list, egl_faces_inside, egl_faces_outside) = egl.subdivide_surface_with_solid ( egl_plane, egl_sphere )
  # Each element of the faces arrays is a list of 3 vertices in the point list

  final_plane = m.create_object_from_points_faces ( name="entire_plane", points=egl_point_list, faces=egl_faces_inside+egl_faces_outside )
  release_surf = m.create_surface_from_faces ( name="rel_surf", obj=final_plane, faces = egl_faces_inside )

  sim.object_list.append ( final_plane )

  release_points = []
  for i in range(num_A):
    p = m.random_point_on_face_list ( release_surf )
    release_points.append ( p )
else:
  while len(release_points) < num_A:
    x = random.uniform(-sheet_size, sheet_size)
    y = random.uniform(-sheet_size, sheet_size)
    if ((x*x)+(y*y)) < (release_radius*release_radius):
      release_points.append ( [x,y,0] )

# Release the molecules
sim.add_molecules_at_points ( mol=mol_A, points=release_points )  # Add by reference, could also use name='A'


# Run the simulation

sim.run(iterations=iterations)

