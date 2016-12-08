# Test 2: "1D diffusion" in a thin tube with initial release from a plane in the middle


# Parameters to vary
iterations = 1000
num_mols = 200
radius = 0.1
half_len = 10  # Warning: must be an integer or change geometry generation code below!!!


# Import the things needed
import libMCell as m
import random


# Make a world
sim = m.create_simulation() # The default simulation knows it is on iteration 0


# Set current time and timestep
sim.t = 0.0
sim.dt = 1e-6


# Add an iteration callback to capture all molecule positions
def save_mols ( sim, data ):
  f = open ( "viz_at_%d.txt" % sim.iteration, "w" )
  mols = sim.molecule_instance_list
  for m in mols:
    f.write ( "%g %g %g\n" % (m.x, m.y, m.z) )
  f.close()
sim.iteration_callback_list.append ( callback=save_mols, skip=0 )


# Create a species
mol_A = m.create_species(name="A",dc=1e-5) # Volume mol by default
sim.species_list.append(mol_A)


# Calculate random release points on a plane
release_points = []
num = 0
r2 = radius*radius
while num < num_mols:
  x = random.uniform(-radius,radius)
  y = random.uniform(-radius,radius)
  if ((x*x) + (y*y)) < r2:
    points.append ( [x,y] )
    num += 1


# Add molecules to the simulation at the current time (t=0)
sim.add_molecules_at_points ( mol=mol_A, points=release_points )  # Add by reference, could also use name='A'


# Create a cylinder from a rotated path

# Start with a 2-D template (half of the cylinder in the x-y plane)
two_d_path = [ [i,radius] for i in range(-half_len,half_len+1) ]
two_d_path.insert ( 0, [-half_len,0] )
two_d_path.append ( [half_len,0] )

cylinder_mesh = m.geometry.triangulate ( m.geometry.extrude.about_x_axis ( path=two_d_path, angle_start=0, angle_end=360, num_samples=32 ) )
cylinder = m.create_object_from_mesh ( name="My_Cylinder", mesh=cylinder_mesh, origin=[0,0,0], rotation=[0,0,0], scale=[1,1,1] )

sim.object_list.append(cylinder)


# Run the simulation

sim.run(iterations=iterations)
