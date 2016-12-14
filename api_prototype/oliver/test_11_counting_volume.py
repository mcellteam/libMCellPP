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

mol_C = m.create_species(name="C",dc=1)
world.species_list.append(mol_C)

###
# Define reactions
###

# A + B -> C
rxn = m.create_reaction("%m + %m -> %m" % (mol_A, mol_B, mol_C), name="rxn", fwd_rate = 10)

# Add to the world
world.rxn_list.append(rxn)

###
# Release molecules into box
###

list_of_mols_to_release = [mol_A, mol_B]
number_of_each_to_release = [100, 100]
world.release_mols(list_of_mols_to_release, 
	nrel = number_of_each_to_release, 
	loc = "%o" % (box))

###
# Run the simulation
###

n_iter = 100
for i_iter in range(0,n_iter):
	world.run_timestep() # runs by one timestep by default

	# Print the positions of all molecules
	mol_pos_all = [mol.loc for mol in world.mol_list]
	print(mol_pos_all)

	# Print the positions of all molecules in the box object
	mol_pos_box = [mol.loc for mol in world.mol_list if m.is_loc_in_region(mol.loc, world.obj_list[0]) == True]
	print(mol_pos_box)

	# Print any reactions that occurred in the last timestep
	rxn_recent = len([rxn.type for rxn in world.recent_rxn_list])
	# world.recent_rxn_list might contain the reactions that occurred during the last timestep
	# Each reaction might have some properties: type (i.e. name or if none is given the strin A+B->C), location, time 
	print(rxn_recent)





