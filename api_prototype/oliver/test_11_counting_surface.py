import pymcell as m

# Make a world
world = m.make_mcell_world()

# Set timestep
world.dt = 0.1

###
# Import a box with a plane through the middle
###

v_list, f_list = import_geometry("my_box.mdl")

# Create the box
box = m.create_polygon_object(name="My box",
	vert_list = v_list,
	face_list = f_list)

# Add it to the mcell world
world.obj_list.append(box)

###
# Make a surface region over the dividing plane in the middle
###

surf_reg_plane = m.create_surface_region(name="Middle plane",
	objects = [box],
	faces = [4,5]
	)

# Add it to the mcell world
world.reg_list.append(surf_reg_plane)

###
# Species
###

mol_A = m.create_species(name="A",dc=1)
world.species_list.append(mol_A)

mol_B = m.create_species(name="B",dc=1,type="SURFACE")
world.species_list.append(mol_B)

mol_C = m.create_species(name="C",dc=1)
world.species_list.append(mol_C)

###
# Define reactions
###

# A' + B' @ surf_reg_plane -> C,
rxn = m.create_reaction("%m + %m @ %r -> %m" % (mol_A, mol_B, surf_reg_plane, mol_C), name="rxn", fwd_rate = 10)

# Add to the world
world.rxn_list.append(rxn)

###
# Release molecules into box
###

list_of_mols_to_release = [mol_A]
number_of_each_to_release = [100]
world.release_mols(
	list_of_mols_to_release, 
	nrel = number_of_each_to_release, 
	loc = [0.5,0,0])

list_of_mols_to_release = [mol_B]
number_of_each_to_release = [100]
world.release_mols(
	list_of_mols_to_release, 
	nrel = number_of_each_to_release, 
	loc = "%o[%r]" % (box, surf_reg_plane),
	orientation = ["'"]
	)

###
# Run the simulation
###

n_iter = 100
for i_iter in range(0,n_iter):
	world.run_timestep() # runs by one timestep by default

	# Print the positions of all B particles on the plane
	mol_pos_plane = [mol.loc for mol in world.mol_list if (mol.type == mol_B and m.is_loc_in_region(mol.loc, world.reg_list[0]) == True)]
	print(mol_pos_plane)