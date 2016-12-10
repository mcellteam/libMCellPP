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
# Make a surface region on top
###

# Define surface region by it's elements
surf_reg = model.create_surface_region(name="My region",
	objects = [box],
	faces = [[5,6]]
	)

###
# Species
###

# Create a species
mol_A = model.create_species(name="A",dc=1,surf=True)

###
# Release molecules into the sheet_box
###

list_of_mols_to_release = [mol_A]
number_of_each_to_release = [100]
orientation_of_each_mol = [0]
model.release_mols(list_of_mols_to_release, 
	nrel = number_of_each_to_release, 
	loc = "%o[%r]" % (box,surf_reg),
	orientations = orientation_of_each_mol)

###
# Run the simulation
###

n_iter = 100
model.run(n_iter)