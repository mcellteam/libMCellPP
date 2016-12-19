import PyMcell as pm

#creat the world 
world = pm.create_world()
# create molecule A
molA = pm_create_mols(name = A, dc = 1e-6, N=1000)
#make the box
box = wolrd.boundaries(x>-1, and, x<1, and y>-1, and y<1, and z>-1, and z<1)
#spread A across the box evenly at t=0
molA.spread(box)
# create molecule B
molB = pm_create_mols(name = B, dc = 1e-6, N =1000)
# create molecule C
molC = pm_create_mols(name = C, dc = 1e-6)
#intial distribution space
space = world.boundaries((x=1 and y>-1 and y<1 and z>-1 and z<1)+(y=1 and x>-1 and x<1 and z>-1 and z<1), 
	(z=1 and y>-1 and y<1 and x>-1 and x<1), (x=-1 and y>-1 and y<1 and z>-1 and z<1), 
	(y=-1 and x>-1 and x<1 and z>-1 and z<1), (z=-1 and y>-1 and y<1 and x>-1 and x<1)) 

#start reaction, with reactant moleceules distributed homogwneously in space at t=0
#unless they have alrealy been distributed, like molA in this case. Maybe the reaction method can check for that?
molA.reaction(reactants = [molB], products = [molC], dt =0.1, space = space, rate = 1e8, revesible = False)

#for part d the reversible parameter is set to True, everything else is the same 