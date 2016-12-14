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

mol_B = m.create_species(name="B",dc=1)
world.species_list.append(mol_B)

mol_C = m.create_species(name="C",dc=1)
world.species_list.append(mol_C)

###
# Define reactions
###

# A -> 0
rxn_1 = m.create_reaction("%m -> 0" % (mol_A), name="rxn 1", fwd_rate = 10)

# A -> B
rxn_2 = m.create_reaction("%m -> %m" % (mol_A, mol_B), name="rxn 2", fwd_rate = 10)

# A + B -> C
rxn_3 = m.create_reaction("%m + %m -> %m" % (mol_A, mol_B, mol_C), name="rxn 3", fwd_rate = 10)

# A + B <-> C
rxn_4 = m.create_reaction("%m + %m -> %m" % (mol_A, mol_B, mol_C), name="rxn 4", fwd_rate = 10, bkwd_rate = 10)

# Add to the world
world.rxn_list.append(rxn_1)
world.rxn_list.append(rxn_2)
world.rxn_list.append(rxn_3)
world.rxn_list.append(rxn_4)

###
# Release molecules into the box
###

list_of_mols_to_release = [mol_A, mol_B]
number_of_each_to_release = [100, 100]
world.release_mols(list_of_mols_to_release, 
	nrel = number_of_each_to_release, 
	loc = "%o" % (box))

###
# Run the simulation
###

n_iter = 100
world.run(n_iter)