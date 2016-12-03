import pymcell as m

# Make a world
world = m.make_mcell_world()

# Set timestep
world.dt = 0.1

###
# Import some geometry
###

v_list, f_list = import_geometry("my_file.mdl")

###
# Create the object
###

poly = m.create_polygon_obj(
	name="My box", 
	vert_list = v_list, 
	face_list = f_list)

# Add it to the mcell world
world.obj_list.append(poly)

###
# POSSIBLY: Also import regions
###

v_list, f_list, r_dict = import_geometry("my_file.mdl")

###
# Create the object
###

poly_with_regions = m.create_polygon_obj(
	name="My box", 
	vert_list = v_list, 
	face_list = f_list, 
	region_dict = r_dict)

# Add it to the mcell world
world.obj_list.append(poly_with_regions)

###
# Run the simulation
###

n_iter = 100
world.run(100)