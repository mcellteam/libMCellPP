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
# Run the simulation
###

n_iter = 100
for i_iter in range(0,n_iter):
	model.run_timestep() # runs by one timestep by default

	# Import some new vertex/face list
	v_list_new, f_list_new = import_geometry("my_file_" + str(i_iter) + ".mdl")

	# Try to update the geometry
	try:
		model.update_geometry_from_points(
			obj = box,
			vert_list = v_list_new,
			face_list = f_list_new)
	except:
		print("Error: the specified geometry is too different from the original to update.")