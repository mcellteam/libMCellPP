import pymcell as m

# Make a model
model = m.create_world()

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

# A -> 0
rxn_1 = model.create_reaction("%m -> 0" % (mol_A), name="rxn 1", fwd_rate = 10)

# A -> B
rxn_2 = model.create_reaction("%m -> %m" % (mol_A, mol_B), name="rxn 2", fwd_rate = 10)

# A + B -> C
rxn_3 = model.create_reaction("%m + %m -> %m" % (mol_A, mol_B, mol_C), name="rxn 3", fwd_rate = 10)

# A + B <-> C
rxn_4 = model.create_reaction("%m + %m -> %m" % (mol_A, mol_B, mol_C), name="rxn 4", fwd_rate = 10, bkwd_rate = 10)

###
# Release molecules into the box
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
model.run(n_iter)