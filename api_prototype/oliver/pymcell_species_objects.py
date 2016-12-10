######
# This file shows how to implement a species, object and region dict using the base class
######

# import pymcell as m

# Make a fake pymcell

def create_model():
	return Model()

class Model():
	def __init__(self):

		# Dictionary of species names to species objects
		self.species_dict = {}

		# Dictionary of geometry object names to objects
		self.geom_dict = {}

	# Create a new species
	def create_species(self,name,dc, surf_flag = False):
		# Check that the new name is not in use
		if name in self.species_dict:
			raise NameError("Species name: " + str(name) + " exists.")

		self.species_dict[name] = Species(name, dc, surf_flag)
		self.species_dict[name]._parent_dict = self.species_dict
		return self.species_dict[name]

	# Create a new geometry
	def create_geometry(self,name,vert_list,face_list,reg_names_to_faces_dict = None):
		# Check that the new name is not in use
		if name in self.geom_dict:
			raise NameError("Geometry name: " + str(name) + " exists.")

		self.geom_dict[name] = Geometry(name, vert_list, face_list, reg_names_to_faces_dict)
		self.geom_dict[name]._parent_dict = self.geom_dict
		return self.geom_dict[name]


class Base(object):
	def __init__(self, name):
		self._name = name
		self._parent_dict = None

	# Name: property (function)
	@property
	def name(self):
		return self._name

	# Name: override setter
	@name.setter
	def name(self, new_name):

		# Check that a parent dictionary exists
		if self._parent_dict != None:
			# Check that the new name is not in use
			if new_name in self._parent_dict:
				raise NameError("Species name: " + str(new_name) + " exists.")

			# Pop the old key and insert the new one
			self._parent_dict[new_name] = self._parent_dict.pop(self._name)

		# Assign the new name
		self._name = new_name

	# Name: override deleter
	@name.deleter
	def name(self):
		raise NotImplementedError("Deleting species names is not allowed.")
		# del self._name

class Species(Base):
	def __init__(self, name, dc, surf_flag):
		super().__init__(name)
		self.dc = dc
		self.surf_flag = surf_flag

class Geometry(Base):
	def __init__(self, name, vert_list, face_list, reg_names_to_faces_dict):
		super().__init__(name)
		self.vert_list = vert_list
		self.face_list = face_list
		if reg_names_to_faces_dict == None:
			self.reg_dict = None
		else:
			# Make a new Region object for each region
			self.reg_dict = {}
			for reg_name, fs in reg_names_to_faces_dict.items():
				# Check that the name is not in use
				if reg_name in self.reg_dict:
					raise NameError("Duplicate region name: " + str(reg_name) + " on geometry: " + str(self.name))

				self.reg_dict[reg_name] = Region(reg_name,fs)
				self.reg_dict[reg_name]._parent_dict = self.reg_dict

class Region(Base):
	def __init__(self, name, face_list):
		super().__init__(name)
		self.face_list = face_list

# Make a world
model = create_model()

# Create a species
mol = model.create_species(name="A",dc=1)

# Create a geometry
box = model.create_geometry("My Box", [], [], {"My Region":[1,2,3]})

__import__('code').interact(local={k: v for ns in (globals(), locals()) for k, v in ns.items()})

#####
# DO THE RELEASE....
#####
