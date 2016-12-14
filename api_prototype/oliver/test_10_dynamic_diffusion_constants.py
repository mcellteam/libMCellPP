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
# Species
###

mol_A = m.create_species(name="A",dc=1)
world.species_list.append(mol_A)

###
# Run the simulation
###

n_iter = 100
for i_iter in range(0,n_iter):
	world.run_timestep() # runs by one timestep by default

	# Update the reaction rate
	world.species_list[0].dc += 1