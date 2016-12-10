import pymcell as m

# Make a model
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

mol_A = model.create_species(name="A",dc=1)

mol_B = model.create_species(name="B",dc=1)

###
# Define reactions
###

# A -> B
rxn = model.create_reaction("%m -> %m" % (mol_A, mol_B), name="rxn", fwd_rate = 10)

###
# Run the simulation
###

n_iter = 100
for i_iter in range(0,n_iter):
	model.run_timestep() # runs by one timestep by default

	# Update the reaction rate
	rxn.fwd_rate += 1