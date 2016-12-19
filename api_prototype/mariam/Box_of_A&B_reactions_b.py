import PyMcell as pm

#creat the world 
world = pm.create_world()
# create molecule A
molA = pm_create_mols(name = A, dc = 1e-6, N=1000)
# create molecule B
molB = pm_create_mols(name = B, dc = 1e-6)
#intial distribution space
space = world.boundaries(x>-1 and x<1 and y>-1 and y<1 and z>-1 and z<1)

#start reaction, with reactant molecules distributed homogeneously in space at t=0
molA.reaction(reactants = NULL, products = [molB], dt =0.1, space = space, rate = 1e8, revesible = False)