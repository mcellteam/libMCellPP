######
# This file shows how to implement a species dict where the species 
# inherit the name from the base class and check for illegal assignments
# as well as update the key in the species_dict when the name is changed
######

# import pymcell as m

# Make a fake pymcell

def create_model():
	return Model()

class Model():
	def __init__(self):
		self.species_dict = {}

	def create_species(self,name,dc):
		if name in self.species_dict:
			raise NameError("Species name: " + str(name) + " exists.")

		self.species_dict[name] = Species(name, dc)
		self.species_dict[name]._parent_dict = self.species_dict
		return self.species_dict[name]

class Base(object):
	def __init__(self, name):
		self._name = name
		self._parent_dict = None
	@property
	def name(self):
		return self._name
	@name.setter
	def name(self, new_name):
		# Check that new name
		if new_name in self._parent_dict:
			raise NameError("Species name: " + str(new_name) + " exists.")

		# Pop the old key and insert the new one
		if self._parent_dict != None:
			self._parent_dict[new_name] = self._parent_dict.pop(self._name)
		self._name = new_name
	@name.deleter
	def name(self):
		del self._name

class Species(Base):
	def __init__(self, name, dc):
		super().__init__(name)
		self.dc = dc

# Make a world
model = create_model()

# Create a species
mol_A = model.create_species(name="A",dc=1)

# __import__('code').interact(local={k: v for ns in (globals(), locals()) for k, v in ns.items()})

#####
# DO THE RELEASE....
#####
