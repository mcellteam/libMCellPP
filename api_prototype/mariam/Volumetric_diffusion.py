import PyMcell as pm

#create world 
world = pm.create_world()

#Make space for diffusion
space = world.boundaries(x>-1 and x<1 and y>-1 and y<1 and z>-1 and z<1)

#Create N molecules of type A to be realesed 
molA = pm.create_mols(name = A, Dc = 1e-6, N=200)

#Release into the space from the origin
molA.release(space, RS=(x=0, z=0, y=0), dt=0.1)