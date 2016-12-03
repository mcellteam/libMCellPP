import pymcell as m

# Make a world
world = m.make_mcell_world()

# Set timestep
world.dt = 0.1

###
# Thin sheet/box
###

# Create a sheet_box
sheet_box = m.create_simple_object(name="My box", type="CUBE", center=[0,0,0], radius=[1,1,0.01])

# Add it to the mcell world
world.obj_list.append(sheet_box)

###
# Species
###

# Create a species
mol_A = m.create_species(name="A",dc=1) # Volume mol by default

# Add to the mcell world
world.species_list.append(mol_A)

###
# Release molecules into the sheet_box
###

list_of_mols_to_release = [mol_A]
number_of_each_to_release = [100]
world.release_mols(list_of_mols_to_release, 
	nrel = number_of_each_to_release, 
	loc = "%o" % (sheet_box))

###
# Run the simulation
###

n_iter = 100
world.run(n_iter)