import PyMcell as pm

#create the world
world = pm.create_world()
#create the box
box = world.boundaries(x>-1 and x<1 and y>-1 and y<1 and z>-1 and z<1)
#creat the class
class surface(): 		#a region defined by the function f, and boundaries 
	def __init(f(x,y,z), x1, y1, z1, x2, y2, z2, p, side):
		self.f(x,y,z) = f(x, y, z)
		self.x1 = x1
		self.x2 = x2
		self.y1 = y1
		self.y2 = y2
		self.z1 = z1
		self.z2 = z1
		self.p = p #Transparent, absorbtive or reflective property
		self.side = side #which side of the given plane/region
side = surface(x=1, 1,-1,-1, 1, 1, 1, transparent, left)