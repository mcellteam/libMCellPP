# General Notes

## Adding things to the MCell world

All statements to add things to the MCell world consist of two parts:

1. Create a thing
2. Add it to the MCell world

For example, to make a species:

1. `mol_A = m.create_species(name="A",dc=1)` 
2. `world.species_list.append(mol_A)`

This has the advantage that we could also create two worlds, and add a molecule to each, for example:
```
world_1.species_list.append(mol_A)
world_1.species_list.append(mol_A)
```

## Checks for objects

Objects need to be checked if they're watertight and manifold. This could be done immediately when they are added to the world:
```
box = m.create_simple_object(name="My box", type="CUBE", center=[0,0,0], radius=[1,1,1]) # No checks yet
world.obj_list.append(box) # Here we check, if it fails, issue an error
```

## Number of iterations

MCell currently has a number of iterations parameter - perhaps this is not necessary. The user can decide at runtime to advance step-by-step, or multiple steps at once.

## Releasing molecules

After creating a species:

1. `mol_A = m.create_species(name="A",dc=1)` 
2. `world.species_list.append(mol_A)`

We want to release it. This can done two ways:

1. Create a release object and add it to MCell

	```
	list_of_mols_to_release = [mol_A]
	number_of_each_to_release = [100]
	releaser = m.create_release_obj(list_of_mols_to_release,
		nrel = number_of_each_to_release,
		loc = [0,0,0],
		time = 0)
	world.releaser_list.append(releaser)
	```

2. Release the molecules directly

	```
	list_of_mols_to_release = [mol_A]
	number_of_each_to_release = [100]
	world.release_mols(list_of_mols_to_release,
		nrel = number_of_each_to_release,
		loc = [0,0,0])
	```

Furthermore, there is a difference between writing `mol_A` and `world.species_list[0]`. `mol_A` is a template for a species, while `world.species_list[0]` is the actual instantiation of that molecule in the `world`. 

In the first case, only `mol_A` should be allowed, since when we run `create_release_obj` we are creating a release template.

In the second case, both should be allowed - the actual instantiation of the molecule `world.species_list[0]` should via a pointer know that it is of the template type `mol_A`.