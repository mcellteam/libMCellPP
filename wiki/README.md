# Overview

This document aims to provide a spec. for a future pyMCell/libMCell package.

* [The Event Scheduler](# The Event Scheduler)
* [pyMCell API](# pyMCell API)
* [Lessons from the neuropil model](# Lessons from the neuropil model)

# The Event Scheduler

(copied from earlier discussions of the scheduler)

## Event Model

The libMCell event model will implement an event-generator/event-listener interface. It will follow the "Trigger, Condition, Outcome" model described in earlier MCell documentation. These are implemented as specific instances of the generic TCO class:

* Trigger == an event
* Condition == context of event
* Outcome == what happens if conditions are met

The "Trigger" portion will consist of the following built-in event types:

* Begin Simulation event

* End Simulation event

* Time-based events:
    * Iteration step
    * User-requested break

* Reaction/Release/Placement events: (what where when how how_many)
    * mol a created
    * mol a destroyed
    * reaction named "my_rxn" checked
    * reaction named "my_rxn" happens 

* Diffusion events: (p0, p1, t, collision list)
    * mol a moved
    * molecule a collides with molecule b
    * mol a hits front or back of obj "sphere" or sphere[triangle i]
    * mol a crosses from front or crosses from back of obj "sphere" or sphere[triangle i]
    * mol a absorbed on front or back of obj "sphere" or sphere[triangle i]

* Dynamic geometry events:
    * obj "sphere" added
    * obj "sphere" removed
    * obj "sphere" changed

* User-defined event types:
    * impiilemented as user-specified subclasses of the generic TCO class

Each of these events can be enabled and handled by user code in the form of "callbacks". If written in C++, these callbacks should be as fast as the current MCell internal code, but much more flexible. Callbacks of this type can handle all of an application's custom counting and visualization needs without the need for an extensive API.








# pyMCell API

## Name of module: "pyMCell"

## What is an MCell data model?

[What is an MCell data model?](./model.md)

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

One of the things the base class will contain is the name of the instance. Changing the name of objects is allowed. Doing so will trigger the execution of appropriate update functions.

The base class must contain a list of the parent object dictionaries that reference it. This is because when the name of the object is changed, the dictionaries that reference it must also change their keys to match.

## Basics

Each model has its own:

1. List of species which inherit from `MCellBase`

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




# Lessons from the neuropil model

(in no particular order)

## Object returns

Function returns are sometimes confusing because: (1) they return unusable objects (objects that have not been exposed via. SWIG to Python), and (2) deleting the returned objects affects the simulation.

For example, when setting up a `count` statement for a species, we are given back a whole list of return objects. Deleting these objects causes the molecule not to be counted (from a quick but possibly wrong analysis, the symbol in the hashtable disappears). This may actually be a desired effect, but it should be clearly documented what the returned objects are, and when it is ok to delete them. Ideally, there will be some consistency in the behavior here across functions (if deleting the count returned object causes the count to disappear, then deleting a release object should cause the release to disappear).

Unusable objects should either (1) be exposed and made usable, or (2) not be returned.

## Passing objects vs. names

Some functions currently take names of objects as input (e.g. to change a reaction rate, pass the name of a reaction), while others take objects (e.g. to release some molecule in a volume, pass the species object). This should be unified - in particular, passing the objects directly is the more Python-ic way.

## Typemaps

The interface for passing objects from Python to MCell is currently clunky. In particular, only some lists of objects (e.g. `[strings]`) have a typemap that converts it into the appropriate C objects (`char**`). For example, lists of molecule objects are currently not passed this way, and are added to special list objects using a helper function `mcell_add_to_species_list`. A quick list of things that need typemaps:
* Lists of strings (exists), doubles (exists), ints
* Lists of molecules
* Lists of reactions
* Lists of geometry/mesh objects

## Molecule position inquiries

A very useful and necessary feature will be to be able to inquire about the positions of molecules. This includes the ability to access position information, as well as to test whether a molecule is inside a volume or not. This function already partially exists in MCell, with two problems:

1. It is not easy to expose to libMCell/pyMCell, because it is intimately tied to waypoints and partitions. The upside of this is that the function evaluation is very fast.
2. It does not support tests for subvolumes which may violate the "outward facing normals" criteria. Consider the case of two compartments joined by a single plane:

```
---------------
|      |      |
|   1  |  2   |
|      |      |
---------------
```

It should be possible to test whether or not a molecule is inside volume 1 or volume 2. There are two general approaches to answer this question:

* An initial determination at simulation time determines: (1) what subvolume the molecule is in, and (2) for every surface element at a given normal orientation, which compartment are we leaving and entering. The simulation then keeps track of which subvolume a given molecule is in at all times. This corresponds to more metadata stored on molecules and walls, but few subsequent computations.

  However, it also has to address the problem of composability of volumes. For example:

```
-------------------
|      |     2    |
|      |          |
|      |   -----  |
|   1  |   | 3 |  |
|      |   -----  |
|      |          |
-------------------
```

Now, a given molecule keeps track of: "Am I in subvolume 1/2/3?" However, if the molecule is inside subvolume 3, what should it answer to the question of "Are you in subvolume 2?" Technically, we have here a subsubvolume 3 which is a subvolume of volume 2. This kind of a composition hierarchy will also need to be determined / stored somewhere.

Adding to this, what do we do in the following situation

```
-------------------
|   1  |     2    |
|      |          |
|   ------------  |
|   |  |   3   |  |
|   ------------  |
|      |          |
-------------------
```

A part of subsubvolume 3 is a subvolume of 2, and a different part is a subvolume of 1. How do we define the composition hierarchy now? The simulation would have to work out something along the lines of reassigning names, e.g.

```
-------------------
|   1  |     2    |
|      |          |
|   ------------  |
|   |3a|   3b  |  |
|   ------------  |
|      |          |
-------------------
```

* The second general approach is the one taken by MCell now - to have a general function that can test on the fly whether or not a molecule is inside a given volume. However, it requires the normals to be outward facing in order for its waypoint method to function correctly. Returning to the original example

```
---------------
|      |      |
|   1  |  2   |
|      |      |
---------------
```

It is impossibly to assign the normals such that **both** subvolumes have outward facing normals. Tom here suggested that this can be solved by the introduction of **submanifolds**. (Note: this is transcribed from memory, and may differ from Tom's suggestion).

A submanifold will be defined for each subvolume 1 and 2. For each, every face belonging to the submanifold will be assigned a flag: 1 or -1. The flags are assigned such that the submanifold has outward facing normals, with the normal direction of a face being defined as:

```
(flag) * (regular normal direction in MCell)
```

With this information, it should be possible to answer whether or not a given particle is inside any given closed volume using the waypoint method.

This seems like the better choice of the two!



