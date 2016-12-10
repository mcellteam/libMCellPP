# libMCell C++ Wiki

## Name of module: "pyMCell"

## Fundamental command to create an MCell World

```
my_model = m.create_model()
```

## Basics

Models share nothing with eachother. Each model has its own:

1. Dictionary of species
	i. Keyed by unique ID in the model (unique within the model, althrough may be random duplicates between models). The unique ID is not assigned until the species object has been added to the model.
	ii. There are two ways to add species:
		a. Template way:
		```
		my_species_template = m.create_species(...)
		my_species = my_model.species_dict.add(my_species_template)
		```
		The species are stored in a dict because the order doesn't matter, and accessing by names is useful.
		`my_species_template` does NOT have a unique ID. A unique ID is not assigned until the species is added to a model. The unique ID is the key in the dictionary.
		When you add the species to the `species_dict`, a deep-copy operations occurs which copies the species properties from `my_species_template` into a unique memory location.
		b. Direct way:
		```
		my_species = my_model.create_species(...)
		```

2. Dictionary of maps from species names to species IDs

