# Test 1: Unbounded diffusion


# Parameters to vary
iterations = 1000
time_step = 1e-6
num_mols = 200
dc = 1e-6


# Import the things needed
import libMCell as m


# Make a world
sim = m.create_simulation() # The default simulation knows it is on iteration 0


# Set current time and timestep
sim.t = 0.0
sim.dt = time_step


# Add an iteration callback to capture all molecule positions (we may provide some of these, but they're not part of core libMCellPP)
def save_mols ( sim, data ):
  f = open ( data['file_demplate'] % sim.iteration, "w" )
  mols = sim.molecule_instance_list
  for m in mols:
    f.write ( "%g %g %g\n" % (m.x, m.y, m.z) )
  f.close()
sim.iteration_callback_list.append ( callback=save_mols, skip=0, data={'file_template':'viz_at_%d.txt'} )


# Create a species
mol_A = m.create_species(name="A",dc=dc) # Volume mol by default
sim.species_list.append(mol_A)


# Create a list of release points
release_points = [ [0,0,0] for i in range(num_mols) ]

# Add molecules to the simulation at the current time (t=0)
m.add_molecules_at_points ( mol=mol_A, points=release_points )  # Add by reference, could also use name='A'

# Run the simulation

sim.run(iterations=iterations)

