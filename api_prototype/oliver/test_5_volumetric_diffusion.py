import pymcell as m

# Make a world
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

# Create a species
mol_A = model.create_species(name="A",dc=1) # Volume mol by default

###
# Release molecules into the sheet_box
###

list_of_mols_to_release = [mol_A]
number_of_each_to_release = [100]
model.release_mols(list_of_mols_to_release, 
	nrel = number_of_each_to_release, 
	loc = "%o" % (box))

###
# Run the simulation
###

n_iter = 100
model.run(n_iter)