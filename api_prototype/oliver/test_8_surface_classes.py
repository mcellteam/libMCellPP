import pymcell as m

# Make a model
model_list = []
model_list.append(m.create_model()) # Transparent world
model_list.append(m.create_model()) # Clamp world

# Set timestep
for model in model_list:
	model.dt = 0.1

###
# Box
###

# Create a box
box_list = []
for model in model_list:
	box_list.append(model.create_simple_object(name="My box", type="CUBE", center=[0,0,0], radius=[1,1,1]))

###
# Make two surface regions on opposing sides of the box
###

# Define surface region by it's elements
surf_reg_list = [[],[]]
for i,model in enumerate(model_list):
	surf_reg_list[i].append(model.create_surface_region(name="My region 1",
		objects = [box_list[i]],
		faces = [[1]]
		))
	surf_reg_list[i].append(model.create_surface_region(name="My region 2",
		objects = [box_list[i]],
		faces = [[6]]
		))

###
# Create molecule
###

mol_list = []
for model in model_list:
	mol_list.append(model.create_species(name="A",dc=1))

###
# Create the different surface classes
###

surf_class_list = [[],[]]
for i,model in enumerate(model_list):
	# Create a transparent surface class
	surf_class_list[i].append(model.create_surface_class(name="Transparent",
		molecules = [mol_list[i]],
		type = "TRANSPARENT"
		))

	# Create a absorptive surface class
	surf_class_list[i].append(model.create_surface_class(name="Absorptive",
		molecules = [mol_list[i]],
		type = "ABSORPTIVE"
		))

	# Create a clamp surface class
	surf_class_list[i].append(model.create_surface_class(name="Clamp",
		molecules = [mol_list[i]],
		type = "CLAMP",
		clamp_value = 1
		))

##########
# Assign surf class to regions
##########

# Assign the surface class to the regions
for i,model in enumerate(model_list):
	if i == 0:
		model.reg_list[0].surf_class_list.append(surf_class_list[i][0]) # transparent
		model.reg_list[1].surf_class_list.append(surf_class_list[i][0]) # transparent
	elif i == 1:
		model.reg_list[0].surf_class_list.append(surf_class_list[i][2]) # clamp
		model.reg_list[1].surf_class_list.append(surf_class_list[i][1]) # absorptive

##########
# Release the mols
##########

for i,model in enumerate(model_list):
	list_of_mols_to_release = [mol_list[i]]
	number_of_each_to_release = [100]
	model.release_mols(list_of_mols_to_release, 
		nrel = number_of_each_to_release, 
		loc = "%o" % (box_list[i]))

##########
# Run
##########

n_iter = 100
for model in model_list:
	model.run(n_iter)