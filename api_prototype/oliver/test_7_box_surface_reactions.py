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
# Make a surface region all around
###

# Define surface region by it's elements
all_faces = list(range(1:6))
surf_reg = m.create_surface_region(name="My region",
	objects = [box],
	faces = [all_faces]
	)

# Add it to the mcell world
world.reg_list.append(surf_reg)

###
# Species
###

mol_A = m.create_species(name="A",dc=1)
world.species_list.append(mol_A)

mol_B = m.create_species(name="B",dc=1,type="SURFACE")
world.species_list.append(mol_B)

mol_C = m.create_species(name="C",dc=1,type="SURFACE")
world.species_list.append(mol_C)

###
# Define reactions
###

# A + B @ box[surf_reg] -> C
rxn_1 = m.create_reaction("%m; + %m; @ %o[%r] -> %m;" % (mol_A,mol_B,box,surf_reg,mol_C), name="rxn 1", fwd_rate = 10)

# Add to the world
world.rxn_list.append(rxn_1)

###
# Release molecules into the box
###

list_of_mols_to_release = [mol_A, mol_B]
number_of_each_to_release = [100, 100]
world.release_mols(list_of_mols_to_release, 
	nrel = number_of_each_to_release, 
	loc = ["%o" % (box), "%o[%r]" % (box, surf_reg)], orientations = ["",";"])

###
# Run the simulation
###

n_iter = 100
world.run(n_iter)