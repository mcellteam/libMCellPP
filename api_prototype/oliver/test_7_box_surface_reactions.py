import pymcell as m

# Make a model
model = m.create_world()

# Set timestep
model.dt = 0.1

###
# Box
###

# Create a box
box = model.create_simple_object(name="My box", type="CUBE", center=[0,0,0], radius=[1,1,1])

###
# Make a surface region all around
###

# Define surface region by it's elements
all_faces = list(range(1:6))
surf_reg = model.create_surface_region(name="My region",
	objects = [box],
	faces = [all_faces]
	)

###
# Species
###

mol_A = model.create_species(name="A",dc=1)

mol_B = model.create_species(name="B",dc=1,type="SURFACE")

mol_C = model.create_species(name="C",dc=1,type="SURFACE")

###
# Define reactions
###

# A + B @ box[surf_reg] -> C
rxn_1 = model.create_reaction("%m; + %m; @ %o[%r] -> %m;" % (mol_A,mol_B,box,surf_reg,mol_C), name="rxn 1", fwd_rate = 10)

###
# Release molecules into the box
###

list_of_mols_to_release = [mol_A, mol_B]
number_of_each_to_release = [100, 100]
model.release_mols(list_of_mols_to_release, 
	nrel = number_of_each_to_release, 
	loc = ["%o" % (box), "%o[%r]" % (box, surf_reg)], orientations = ["",";"])

###
# Run the simulation
###

n_iter = 100
model.run(n_iter)