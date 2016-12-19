import PyMcell as pm

#Create world
world = pm.creat_world()
#Create N molecules of type A to be realesed 
molA = pm.create_mols(name = A, Dc = 1e-6, N=200)

#Release into the world from initial coordinates x_0, y_0, z_0 
molA.release(world, RS=(x_0, y_0, z_0), dt=0.1)
