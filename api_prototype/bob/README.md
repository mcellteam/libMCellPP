# libMCel  Python API

## Blender add-on to create a Blender Object from an SWC formatted file

This addon can read an SWC formatted file and generate either a line object or a mesh object.

* **[Description/Tutorial](files/description)**
* **[Tips and Usage Notes](files/notes)**
* **[Examples](files/examples)**
* **[Source Files](files/source)**

![libMCell++](files/images/libMCellPP.png?raw=true "libMCell++")

# Assorted CellBlender Models
## Models that don't fit any other category

This directory contains models that haven't been put in any other grouping.

Current Models:

![Organelle Demo](Organelle_Demo.png?raw=true "Organelle Demo")


* **[Timed_Releases.json](Timed_Releases.json)**  - Demonstration of Timed Releases with Scripting.

![Timed Releases](Timed_Releases.gif?raw=true "Timed Releases")


* **[Vertex_Release.json](Vertex_Release.json)**  - Demonstration of Object Vertex Release.

![Vertex Release](Vertex_Release.gif?raw=true "Vertex Release")



# libMCell C++

C++ Version of MCell

The C++ version of libMCell is intended to provide a convenient and high performance interface to the capabilities of the MCell code base. This Wiki page describes some of the features of libMCell as it is being designed. It is a work in progress.

## Purpose and Goal

**libMCell C++** should do the following:

* Provide the compute engine for the traditional MCell program.
* Provide a C++ API for MCell applications written directly in C++.
* Provide the backbone for a Python API which closely corresponds to the C++ API.
* Provide an interface for CellBlender.
* Provide both a C++ and Python interface for use with other software.

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
    * User-requestedi break

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

## Counting Example

Counting has been a somewhat complicated process in MCell because the MDL language has tried to anticipate and offer as many counting options and capabilities as imagined to be useful. The anticipated C++/Python API for libMCell will, instead, expose the features needed for end users to write their own counting code. The library will also include various convenience functions built on top of this API to provide the traditional MCell counting functionality. The following example sketches out the proposed API.

```
# TCO = Trigger, Condition, Outcome event model

# Superclass of all TCO events will contain the time of the event
class TCO_event:
     timewith pneumatic tires

# Superclass of all TCO event listeners
class TCO_listener:
      def execute(self, the_event):
          return

# The molecule creation event subclass contains the molecule (or molecules?)
#   that have been created
class TCO_mol_creation_event(TCO_event):
     the_molecule  # the instance of the molecule (not species) that was created


# Here's our event handler to count mol a in the world:
class mol_a_listener(TCO_listener):

    count=0

    def __init__(self):
      self.count = 0

    def execute(self, the_event):

        if (type(the_event) is TCO_mol_creation_event):
            if (the_event.the_molecule.species.name == "a":
              self.count+=1
        elif (type(the_event) is TCO_mol_destruction_event):
            if (the_event.the_molecule.species.name == "a":
              self.count-=1
        else:
           Oops!

        return


# Here's our event handler to count any mol in the world:
class mol_listener(TCO_listener):
 
    count = None
    mol_name = None

    def __init__(self, mol_name):
      self.count = 0
      self.mol_name = mol_name

    def execute(self, the_event):

        if (type(the_event) is TCO_mol_creation_event):
            if (the_event.the_molecule.species.name == self.mol_name:
              self.count+=1
        elif (type(the_event) is TCO_mol_destruction_event):
            if (the_event.the_molecule.species.name == self.mol_name:
              self.count-=1
        else:
           Oops!

        return

# Here's our counter which counts any mol in the world,
#   and registers itself in the model:
class mol_counter(TCO_listener):
 
    count = None
    mol_name = None

    def __init__(self, the_model, mol_name):
      self.count = 0
      self.mol_name = mol_name
      the_model.register_event_handler(
        pm.TCO_mol_creation_flag | pm.TCO_mol_destruction_flag, self
        )

    def execute(self, the_event):

        if (type(the_event) is TCO_mol_creation_event):
            if (the_event.the_molecule.species.name == self.mol_name:
              self.count+=1
        elif (type(the_event) is TCO_mol_destruction_event):
            if (the_event.the_molecule.species.name == self.mol_name:
              self.count-=1
        else:
           Oops!

        return



```



## Traditional MCell

Eventually, the traditional mcell program will become an MDL-parsing interface to libMCell.

## Status

This repository contains work on a C++ version of libMCell. Many of these files
were orginally from the CellBlender project under the "libMCell" subdirectory.

Project status is uncertain.

