import pymcell as m

# Make a world
world = m.make_mcell_world()

# Set timestep
world.dt = 0.1

###
# Cylinder
###

# Create a cylinder
cylinder = m.create_simple_object(name="My Cylinder", type="CYLINDER", center=[0,0,0], radius=[0.1,0.1,100])

# Add it to the mcell world
world.obj_list.append(cylinder)

###
# To release the mols, also make a thin box
###

# Create a box
box = m.create_simple_object(name="My Box", type="CUBE", center=[0,0,0], radius=[0.1,0.1,0.01])

# Add it to the mcell world
world.obj_list.append(box)

###
# Species
###

# Create a species
mol_A = m.create_species(name="A",dc=1) # Volume mol by default

# Add to the mcell world
world.species_list.append(mol_A)

###
# Release molecules at the intersection of the box with the cylinder
###

list_of_mols_to_release = [mol_A]
number_of_each_to_release = [100]
world.release_mols(list_of_mols_to_release, 
	nrel = number_of_each_to_release, 
	loc = "%o[ALL] * %o[ALL]" % (cylinder,box))

###
# Run the simulation
###

n_iter = 100
world.run(n_iter)