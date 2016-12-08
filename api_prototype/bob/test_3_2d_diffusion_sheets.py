# "2D diffusion" between two sheets - initial release in a line source

# Parameters to vary
iterations = 1000
num_A = 200
sheet_size = 10
gap = 0.01


# Import the things needed
import libMCell as m
import random


# Make a world
sim = m.create_simulation()


# Set current time and timestep
sim.t = 0.0
sim.dt = 1e-6


# Add the standard iteration callback to capture molecule positions
sim.iteration_callback_list.append ( callback=m.viz_output_callback, data={['ALL']}, skip=0 )


# Create the species and add to simulation
mol_A = m.create_species(name="A",dc=1e-5) # Volume mol by default
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

# Create the top sheet
top_sheet = m.create_object_from_points_faces ( name="Top_Sheet", points=points, faces=faces, origin=[0,0,gap/2] )
sim.object_list.append(top_sheet)

# Create the bottom sheet
bottom_sheet = m.create_object_from_points_faces ( name="Bottom_Sheet", points=points, faces=faces, origin=[0,0,-gap/2] )
sim.object_list.append(bottom_sheet)


# Create a line of evenly spaced release points (could be random just about as easily)
release_points = []
for i in range(num_A):
  release_points.append ( [ 0, 0, (i*gap/num_A)-(gap/2) ] )

# Release the molecules
sim.add_molecules_at_points ( mol=mol_A, points=release_points )  # Add by reference, could also use name='A'


# Run the simulation

sim.run(iterations=iterations)

