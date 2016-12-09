# Test 6: Box of A & B with reactions:
#   A -> 0 decay
#   A -> B decay
#   A + B -> C irreversible
#   A + B <-> C reversible


# Parameters to vary
iterations = 1000
num_A = 200
num_B = 100
decay_rate_A = 1e3
ab_decay = 1e3
ab_to_c_rate = 1e6
ab_c_rate = 1e8
box_len = 0.5


# Import the things needed
import libMCell as m
import random


# Make a world
sim = m.create_simulation()


# Set current time and timestep
sim.t = 0.0
sim.dt = 1e-6


# Add an iteration callback to capture positions
def save_mols ( sim ):
  f = open ( "viz_at_%d.txt" % sim.iteration, "w" )
  mols = sim.molecule_instance_list
  for m in mols:
    f.write ( "%g %g %g\n" % (m.x, m.y, m.z) )
  f.close()
sim.iteration_callback_list.append ( callback=save_mols, skip=0 )


# Create the species and add to simulation
mol_A = m.create_species(name="A",dc=1e-5) # Volume mol by default
mol_B = m.create_species(name="B",dc=1e-5) # Volume mol by default
mol_C = m.create_species(name="C",dc=0)    # Volume mol by default
sim.species_list.append(mol_A)
sim.species_list.append(mol_B)
sim.species_list.append(mol_C)

# Define the reactions and add to simulation
decay_A_rxn = m.create_reaction("%m -> 0" % (mol_A), name="decay_A", fwd_rate=decay_rate_A)
ab_decay_rxn = m.create_reaction("%m -> %m" % (mol_A, mol_B), name="A_to_B_decay", fwd_rate=ab_decay)
ab_to_c_rxn = m.create_reaction("%m + %m -> %m" % (mol_A, mol_B, mol_C), name="ab_to_c", fwd_rate=ab_to_c_rate)
ab_c_rxn = m.create_reaction("A + B <-> C", name="ab_c", fwd_rate=ab_c_rate, bkwd_rate=ab_c_rate)

# Add to the simulation
sim.rxn_list.append(decay_A_rxn)
sim.rxn_list.append(ab_decay_rxn)
sim.rxn_list.append(ab_to_c_rxn)
sim.rxn_list.append(ab_c_rxn)

# f = None # This is the file that will be written to

# Add a start simulation callback to open the file
#def open_my_count_files ( sim, data ):
#  global f
#  f = open ( "count_mols.txt", "w" )
#sim.before_start_callback_list.append ( open_my_count_file )

# Add an end simulation callback to close the file
#def close_my_count_files ( sim, data ):
#  global f
#  f.close()
#sim.after_end_callback_list.append ( close_my_count_file )


# Add an iteration callback to count molecule C
def count_mols ( sim, data ):
  f = data['file']
  mol_names = data['mols']
  c_count = 0
  mols = sim.molecule_instance_list
  # Alternatively to avoid the name check: mols = sim.molecule_instance_list_with_name ( ["C"] )
  for m in mols:
    if m.species.name in mol_names:
      c_count += 1

f = open ( "count_mols.txt", "w" )
sim.iteration_callback_list.append ( callback=count_mols, dt=10*sim.dt, data={'file':f, 'mols':["C"]} )


# Create a cube (the old-fashioned way)
points = [
  [ -1.0, -1.0, -1.0 ],
  [ -1.0, -1.0, 1.0 ],
  [ -1.0, 1.0, -1.0 ],
  [ -1.0, 1.0, 1.0 ],
  [ 1.0, -1.0, -1.0 ],
  [ 1.0, -1.0, 1.0 ],
  [ 1.0, 1.0, -1.0 ],
  [ 1.0, 1.0, 1.0 ] ]

faces = [
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

# Scale the points
for p in points:
  for i in range(3):
    p[i] *= box_len
    

# Create the object
cube = m.create_object_from_points_faces ( name="My_Cube", points=points, faces=faces )
sim.object_list.append(cube)


# Release the molecules
m.add_molecules_to_volume ( cube )


# Run the simulation

sim.run(iterations=iterations)

f.close()
