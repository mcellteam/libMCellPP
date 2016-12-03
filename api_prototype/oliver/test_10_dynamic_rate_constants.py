import pymcell as m

# Make a world
world = m.make_mcell_world()

# Set timestep
world.dt = 0.1

###
# Box
###

# Create a box
box = m.create_simple_object(name="My box", type="CUBE", center=[0,0,0], radius=[1,1,1])

# Add it to the mcell world
world.obj_list.append(box)

###
# Species
###

mol_A = m.create_species(name="A",dc=1)
world.species_list.append(mol_A)

mol_B = m.create_species(name="B",dc=1)
world.species_list.append(mol_B)

###
# Define reactions
###

# A -> B
rxn = m.create_reaction("%m -> %m" % (mol_A, mol_B), name="rxn", fwd_rate = 10)

# Add to the world
world.rxn_list.append(rxn)

###
# Run the simulation
###

n_iter = 100
for i_iter in range(0,n_iter):
	world.run_timestep() # runs by one timestep by default

	# Update the reaction rate
	world.rxn_list[0].fwd_rate += 1