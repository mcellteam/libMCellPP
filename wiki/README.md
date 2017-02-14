# Overview

This document aims to provide a spec. for a future pyMCell/libMCell package.

* [The Event Scheduler](#The Event Scheduler)
* [pyMCell API](#pyMCell API)

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


