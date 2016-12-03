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
# Make a surface region on top
###

# Define surface region by it's elements
surf_reg = m.create_surface_region(name="My region",
	objects = [box],
	faces = [[5,6]]
	)

# Add it to the mcell world
world.reg_list.append(surf_reg)

###
# Species
###

# Create a species
mol_A = m.create_species(name="A",dc=1,type="SURFACE")

# Add to the mcell world
world.species_list.append(mol_A)

###
# Release molecules into the sheet_box
###

list_of_mols_to_release = [mol_A]
number_of_each_to_release = [100]
orientation_of_each_mol = [";"]
world.release_mols(list_of_mols_to_release, 
	nrel = number_of_each_to_release, 
	loc = "%o[%r]" % (box,surf_reg),
	orientations = orientation_of_each_mol)

###
# Run the simulation
###

n_iter = 100
world.run(n_iter)