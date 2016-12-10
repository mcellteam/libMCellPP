import pymcell as m

# Make a model
model = m.create_model()

# Set timestep
model.dt = 0.1

###
# Box
###

# Create a box
box = model.create_simple_object(name="My box", type="CUBE", center=[0,0,0], radius=[1,1,1])


###
# Species
###

mol_A = model.create_species(name="A",dc=1)

mol_B = model.create_species(name="B",dc=1)

mol_C = model.create_species(name="C",dc=1)

###
# Define reactions
###

# A + B -> C
rxn = model.create_reaction("%m + %m -> %m" % (mol_A, mol_B, mol_C), name="rxn", fwd_rate = 10)

###
# Release molecules into box
###

list_of_mols_to_release = [mol_A, mol_B]
number_of_each_to_release = [100, 100]
model.release_mols(list_of_mols_to_release, 
	nrel = number_of_each_to_release, 
	loc = "%o" % (box))

###
# Run the simulation
###

n_iter = 100
for i_iter in range(0,n_iter):
	model.run_timestep() # runs by one timestep by default

	# Print the positions of all molecules
	mol_pos_all = [mol.loc for mol in model.mol_list]
	print(mol_pos_all)

	# Print the positions of all molecules in the box object
	mol_pos_box = [mol.loc for mol in model.mol_list if m.is_loc_in_region(mol.loc, box) == True]
	print(mol_pos_box)

	# Print any reactions that occurred in the last timestep
	rxn_recent = len([rxn.type for rxn in model.recent_rxn_list])
	# model.recent_rxn_list might contain the reactions that occurred during the last timestep
	# Each reaction might have some properties: type (i.e. name or if none is given the strin A+B->C), location, time 
	print(rxn_recent)





