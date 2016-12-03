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
# Run the simulation
###

n_iter = 100
for i_iter in range(0,n_iter):
	world.run_timestep() # runs by one timestep by default

	# Import some new vertex/face list
	v_list_new, f_list_new = import_geometry("my_file_" + str(i_iter) + ".mdl")

	# Try to update the geometry
	try:
		world.update_geometry_from_points(
			obj = world.obj_list[0],
			vert_list = v_list_new,
			face_list = f_list_new)
	except:
		print("Error: the specified geometry is too different from the original to update.")