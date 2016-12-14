import pymcell as m

# Make a world
world = m.make_mcell_world()

# Set timestep
# NOTE: maybe there should be no number of iterations
world.dt = 0.1

# All statements proceed in two parts:
# 1) Create a thing
# 2) Add it to the MCell world

###
# Species
###

# Create a species
mol_A = m.create_species(name="A",dc=1) # Volume mol by default

# Add to the mcell world
world.species_list.append(mol_A)

###
# Release molecules
###

# SEE README FOR TWO ALTERNATE WAYS TO RELEASE MOLECULES

# Way # 1 (passive/scheduled):
list_of_mols_to_release = [mol_A]
number_of_each_to_release = [100]
releaser = m.create_release_obj(list_of_mols_to_release,
    nrel = number_of_each_to_release,
    loc = [0,0,0],
    time = 0)
world.releaser_list.append(releaser)

# Way # 2 (active):
list_of_mols_to_release = [mol_A]
number_of_each_to_release = [100]
world.release_mols(list_of_mols_to_release, 
	nrel = number_of_each_to_release, 
	loc = [0,0,0])

# ALSO SEE README:
# Should we write 'mol_A' or 'world.species_list[0]'?
# 'mol_A' is a template, and 'world.species_list[0]' is the actual instantiation of the obj in the world
# In the first case, only 'mol_A' should be allowed - we are creating a template
# In the second case, either should be allowed. 'world.species_list[0]' should know via a pointer
# that it belongs to the template type 'mol_A'

###
# Run the simulation
###

n_iter = 100
world.run(n_iter)