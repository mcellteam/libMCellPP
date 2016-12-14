import pymcell as m

###
# Box
###

# Create a box
box = m.create_simple_object(name="My box", type="CUBE", center=[0,0,0], radius=[1,1,1])

###
# Make two surface regions on opposing sides of the box
###

# Define surface region by it's elements
surf_reg_1 = m.create_surface_region(name="My region 1",
	objects = [box],
	faces = [[1]]
	)

surf_reg_2 = m.create_surface_region(name="My region 2",
	objects = [box],
	faces = [[6]]
	)

###
# Create molecule
###

mol_A = m.create_species(name="A",dc=1)

###
# Create the different surface classes
###

# Create a transparent surface class
surf_class_t = m.create_surface_class(name="Transparent",
	molecules = [mol_A],
	type = "TRANSPARENT"
	)

# Create a absorptive surface class
surf_class_a = m.create_surface_class(name="Absorptive",
	molecules = [mol_A],
	type = "ABSORPTIVE"
	)

# Create a clamp surface class
surf_class_c = m.create_surface_class(name="Clamp",
	molecules = [mol_A],
	type = "CLAMP",
	clamp_value = 1
	)

##########
# Transparency
##########

# Make a world
world_t = m.make_mcell_world()

# Set timestep
world_t.dt = 0.1

# Add the box to the world
world_t.obj_list.append(box)

# Add the surface classes to the world
world_t.reg_list.append(surf_reg_1)
world_t.reg_list.append(surf_reg_2)

# Add the molecule to the world
world_t.species_list.append(mol_A)

# Assign the surface class to the regions
world_t.reg_list[0].surf_class_list.append(surf_class_t)
world_t.reg_list[1].surf_class_list.append(surf_class_t)

# Release the mols
list_of_mols_to_release = [mol_A]
number_of_each_to_release = [100]
world_t.release_mols(list_of_mols_to_release, 
	nrel = number_of_each_to_release, 
	loc = "%o" % (box))

# Run
n_iter = 100
world_t.run(n_iter)


##########
# Clamp/absorption
##########

# Make a world
world_ca = m.make_mcell_world()

# Set timestep
world_ca.dt = 0.1

# Add the box to the world
world_ca.obj_list.append(box)

# Add the surface classes to the world
world_ca.reg_list.append(surf_reg_1)
world_ca.reg_list.append(surf_reg_2)

# Add the molecule to the world
world_ca.species_list.append(mol_A)

# Assign the surface class to the regions
world_ca.reg_list[0].surf_class_list.append(surf_class_c)
world_ca.reg_list[1].surf_class_list.append(surf_class_a)

# (No need to release molecules due to the clamp concentration?)

# Run
n_iter = 100
world_ca.run(n_iter)