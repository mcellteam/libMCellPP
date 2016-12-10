import pymcell as m

# Make a model
model = m.create_model()

# Set timestep
model.dt = 0.1

###
# Import some geometry
###

v_list, f_list = import_geometry("my_file.mdl")

###
# Create the object
###

poly = model.create_polygon_obj(
	name="My box", 
	vert_list = v_list, 
	face_list = f_list)

###
# POSSIBLY: Also import regions
###

v_list, f_list, r_dict = import_geometry("my_file.mdl")

###
# Create the object
###

poly_with_regions = model.create_polygon_obj(
	name="My box", 
	vert_list = v_list, 
	face_list = f_list, 
	region_dict = r_dict)

###
# Run the simulation
###

n_iter = 100
model.run(n_iter)