import PyMcell as pm

# Create world
world = pm.create_world()

# Make the space available for diffusion
space = world.boundaries(y^2+z^2<0.1)

#Create N molecules of type A to be realesed 
molA = pm.create_mols(name = A, Dc = 1e-6, N=200)

#Release into the space from x=0 plane 
molA.release(space, RS=(x=0), dt=0.1)
