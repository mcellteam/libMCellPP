import PyMcell as pm

#create world 
world = pm.create_world()

#Make space for diffusion
space = world.boundaries(z>0 and z<0.0001)

#Create N molecules of type A to be realesed 
molA = pm.create_mols(name = A, Dc = 1e-6, N=200)

#Release into the space from x=0, z=0 line 
molA.release(space, RS=(x=0, z=0.00005), dt=0.1)