import pymcell as m

# Make a model
model = m.create_model()

# Set timestep
model.dt = 0.1

###
# Import a box with a plane through the middle
###

v_list, f_list = import_geometry("my_box.mdl")

# Create the box
box = model.create_polygon_object(name="My box",
	vert_list = v_list,
	face_list = f_list)

###
# Make a surface region over the dividing plane in the middle
###

surf_reg_plane = model.create_surface_region(name="Middle plane",
	objects = [box],
	faces = [4,5]
	)

###
# Species
###

mol_A = model.create_species(name="A",dc=1)

mol_B = model.create_species(name="B",dc=1,type="SURFACE")

mol_C = model.create_species(name="C",dc=1)

###
# Define reactions
###

# A' + B' @ surf_reg_plane -> C,
rxn = model.create_reaction("%m + %m @ %r -> %m" % (mol_A, mol_B, surf_reg_plane, mol_C), name="rxn", fwd_rate = 10)

###
# Release molecules into box
###

list_of_mols_to_release = [mol_A]
number_of_each_to_release = [100]
model.release_mols(
	list_of_mols_to_release, 
	nrel = number_of_each_to_release, 
	loc = [0.5,0,0])

list_of_mols_to_release = [mol_B]
number_of_each_to_release = [100]
model.release_mols(
	list_of_mols_to_release, 
	nrel = number_of_each_to_release, 
	loc = "%o[%r]" % (box, surf_reg_plane),
	orientation = [1]
	)

###
# Run the simulation
###

n_iter = 100
for i_iter in range(0,n_iter):
	model.run_timestep() # runs by one timestep by default

	# Print the positions of all B particles on the plane
	mol_pos_plane = [mol.loc for mol in model.mol_list if (mol.type == mol_B and m.is_loc_in_region(mol.loc, surf_reg_plane) == True)]
	print(mol_pos_plane)