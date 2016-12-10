import pymcell as m

# Make a model
model = m.create_model()

# Set timestep
model.dt = 0.1

###
# Cylinder
###

# Create a cylinder
cylinder = model.create_simple_object(name="My Cylinder", type="CYLINDER", center=[0,0,0], radius=[0.1,0.1,100])

###
# To release the mols, also make a thin box
###

# Create a box
box = model.create_simple_object(name="My Box", type="CUBE", center=[0,0,0], radius=[0.1,0.1,0.01])

###
# Species
###

# Create a species
mol_A = model.create_species(name="A",dc=1) # Volume mol by default

###
# Release molecules at the intersection of the box with the cylinder
###

list_of_mols_to_release = [mol_A]
number_of_each_to_release = [100]
model.release_mols(list_of_mols_to_release, 
	nrel = number_of_each_to_release, 
	loc = "%o[ALL] * %o[ALL]" % (cylinder,box))

###
# Run the simulation
###

n_iter = 100
model.run(n_iter)