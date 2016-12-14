# libMCell C++ Wiki

## Name of module: "pyMCell"

## Fundamental command to create an MCell Model

```
my_model = m.create_model()
```

Models created in the same process can share with each other, since they are in the same memory space.

## MCell Base Class

The MCell base class will store properties and functions that are useful to all different types of objects. For example, the species class, the reaction class, etc. will all be subclasses of the MCell base class.

The name of the base class is:
```
MCellBase
```

One of the things the base class will contain is the name of the instance. Changing the name of objects is **forbidden**. Alternatively you may delete and re-add the object.

The base class must contain a list of the parent object dictionaries that reference it. This is because when the name of the object is changed, the dictionaries that reference it must also change their keys to match.

## Basics

Each model has its own:

1. List of species
 i. How do you make a species? There are two ways:
 ```
 my_species = m.create_species(...)
 my_model.species_list.append(my_species)
 ```
 or:
 ```
 my_species = my_model.create_species(...)
 ```

 The `my_species` object in either case may be appended to multiple models. In this case, the memory is shared.

 ii. How do you access a species? There are 3 ways:
  a. You have the handle when you made it
  b. `my_model.species_list[0]`
  c. Access by name via a special function: `my_model.species_list.get("name")`. This means that in addition to a `species_list` there needs to be an internal dictionary from the species name to the species object.

  Why is there an internal dictionary?
  a. Searching the list could be slow
  b. It should be private because when the name of a species is changed using it's handle:
  ```
  my_species.name = "new name"
  ```
  the dictionary will need to update the key associated with this species object. This can possibly fail if the key is a duplicate.


