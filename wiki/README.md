# libMCell C++ Wiki

## Name of module: "pyMCell"

## Fundamental command to create an MCell World

```
my_model = m.create_model()
```

## MCell Base Class

The MCell base class will store properties and functions that are useful to all different types of objects. For example, the species class, the reaction class, etc. will all be subclasses of the MCell base class.

One of the things the base class will contain is the name of the instance. This is necessary for the following reason:
Objects will be stored in a dictionary form, with the keys being the names of the instances. For example, species will be stored in a species_dict, with keys being the names of the species. Unfortunately, this means that the `name` property will be stored twice: once as a key in a dictionary, and once as a property of the base class.

This raises the following questions:

1. How do we access the objects name? It will inherit the name property from the base class. Therefore it will be possible to simply write `my_species.name` to get the name.

2. How do we change the name of the object? We want to be able to change it in the same form as we access it: `my_species.name = "new name"`. However, the dictionary must now also be updated, such that the old key (the old name) is deleted, and the new key (the new name) is inserted. There are two ways to do this:

	i. (Worse) the name property is read-only. That is, `my_species.name = "new name"` is forbidden. Instead, a different function is provided `my_species.change_name("new name")` that 1) changes the name property, but also 2) makes the change in the dictionary `my_model.species_dict`.

	ii. (Better) the base class overloads the setter and getter functions of `name`, such that we can write `my_species.name = "new name"` which also runs extra commands to change the dictionary keys in `my_model.species_dict`. This is possible e.g. by the following code
	```
	class Base(object):
	    def __init__(self):
	        self._name = None
	    @property
	    def name(self):
	        return self._name
	    @name.setter
	    def name(self, value):
	        print("Here I can do other things like update the species_dict.")
	        self._name = value
	    @name.deleter
	    def name(self):
	        del self._name


	class Species(Base):
	    def __init__(self):
	        super().__init__()
	```
	Note that `name` is now actually a function disguised as a property, while the actual name is stored as `_name`. Potentially the user could directly edit `_name` and break the desired dictionary-key-update functionality - however, since this name is protected, the user will know they are doing some illegal.

A further functionality that the setter function of the name property should have is a check against possible duplicate names in the dictionary - this is not allowed.

Here is a nice working example of a species dict: [EXAMPLE](https://github.com/mcellteam/libMCellPP/blob/master/api_prototype/oliver/test_1_unbounded_diffusion.py).

## Basics

Models share nothing with eachother. Each model has its own:

1. Dictionary of species:

	i. Keyed by species name.

	ii. There is only one way to add species:
		b. Direct way:
		```
		my_species = my_model.create_species(...)
		```
		We considered previously being able to create a template species, separate from any model. However, this caused: 1) extra code, 2) confusion about the different ways to add species (clearer to just have one) and 3) no obvious benefit. If the user wants to create a template for a species, they can write their own in Python. In other words, why would you ever create a species that's not part of a simulation?
		
	iii. To access objects, the user may either use the handle that was given during assignment. Alternatively, by name:
	```
	my_species = my_model.species_dict["species_name"]
	```




