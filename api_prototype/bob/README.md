![libMCell](libMCellCPPs.png?raw=true "libMCell")

# List of Test Cases for the API

1. Unbounded diffusion
2. "1D diffusion" in a thin tube
	* initial release in a plane in the middle
3. "2D diffusion" between two sheets
	* initial release in a line source
4. 2D diffusion on a real 2D surface
	* initial release on a patch by either density or Boolean intersection of e.g. a sphere with a plane
5. Volumetric diffusion in a box/sphere
6. Box of A & B with reactions:
	* A -> 0 decay
	* A -> B decay
	* A + B -> C irreversible
	* A + B <-> C reversible
7. Box of A & B with reactions on a surface:
	* A (volumetric) + B (surface) -> C (surface)
8. Surface classes
	* Box with one transparent side to molecule A
	* Box with absorptive side to molecule A
	* Box with concentration clamp of A on one side and absorptive on the opposing side
9. Object with a generally complex geometry from some list of vertices and faces
10. Dynamic changes
	* Dynamic geometry: an interface to change the mesh at each timestep
		* Example: An initial box that updates it's geometry at each timestep with some new list of vertices and faces
	* Dynamic rate constants: changing the rate constant of a reaction
		* Example: A box with A+B->C that where the rate constant depends on the number of A,B, or C
	* Dynamic diffusion constants: changing the diffusion constant for a molecule
		* Example: A box of diffusing A particles that increase their diffusion constants over time
11. Counting statements
	* A box (maybe with some region definition) with A+B->C reaction where we count each of the following at each timestep:
		* What: molecule, reaction, event/trigger
		* Where: World, object, region
		* When: frequency of counting
		* How: Front hits/back hits, e.g. on a plane that goes through the box

# Reaction Idea from Meeting:

```
mol_a = create_molecule_species ( ... )
mol_b = create_molecule_species ( ... )
mol_c = create_molecule_species ( ... )
my_reaction = create_reaction ( "%m + %m -> %m", mol_a, mol_b, mol_c );
```

# libMCell API (C++ version)

This is an existing C++ version of unbounded diffusion of 2 different molecules from two different release sites.

```
#include <iostream>
#include <string>
#include <vector>

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <math.h>

#include "libMCell.h"

using namespace std; 

int main ( int argc, char *argv[] ) {

  cout << "\n\n" << endl;
  cout << "*********************************************" << endl;
  cout << "*   MCell C++ Test Program using libMCell   *" << endl;
  cout << "*********************************************" << endl;
  cout << "\n" << endl;

  //This is a hard-coded simulation as a simple example of the API

  MCellSimulation *mcell = new MCellSimulation();

  MCellMoleculeSpecies *mol_a = new MCellMoleculeSpecies();
  mol_a->name = "A";
  mol_a->diffusion_constant = 1e-6;
  mcell->add_molecule_species( mol_a );

  MCellMoleculeSpecies *mol_b = new MCellMoleculeSpecies();
  mol_b->name = "B";
  mol_b->diffusion_constant = 2e-5;
  mcell->add_molecule_species( mol_b );

  MCellReleaseSite *rel_a = new MCellReleaseSite();
  rel_a->x = 0.0;
  rel_a->y = 0.0;
  rel_a->z = 0.0;
  rel_a->molecule_species = mol_a;
  rel_a->quantity = 300;
  mcell->add_molecule_release_site ( rel_a );

  MCellReleaseSite *rel_b = new MCellReleaseSite();
  rel_b->x = 0.3;
  rel_b->y = 0.2;
  rel_b->z = 0.1;
  rel_b->molecule_species = mol_b;
  rel_b->quantity = 700;
  mcell->add_molecule_release_site ( rel_b );

  mcell->num_iterations = 200;
  mcell->time_step = 1e-7;

  mcell->run_simulation(".");

  return ( 0 );
}
```

# libMCell API (Python version)

This is an existing Python version of unbounded diffusion of 2 different molecules from two different release sites.

```
# file: mcell_main.py

import sys

from libMCell import *

print ( "\n\nMCell Python Prototype using libMCell %d arguments:\n" % len(sys.argv) )
proj_path = ""
data_model_file_name = ""
data_model_full_path = ""
for arg in sys.argv:
  print ( "   " + str(arg) )
  if arg[0:10] == "proj_path=":
    proj_path = arg[10:]
  if arg[0:11] == "data_model=":
    data_model_file_name = arg[11:]
print ( "\n\n" )


mcell = MCellSimulation()

mol_a = MCellMoleculeSpecies()
mol_a.name = "A"
mol_a.diffusion_constant = 1e-7
mcell.add_molecule_species ( mol_a )

mol_b = MCellMoleculeSpecies()
mol_b.name = "B"
mol_b.diffusion_constant = 2e-7
mcell.add_molecule_species ( mol_b )

rel_a = MCellReleaseSite()
rel_a.x = 0.0
rel_a.y = 0.0
rel_a.z = 0.0
rel_a.molecule_species = mol_a
rel_a.quantity = 3
mcell.add_molecule_release_site ( rel_a )

rel_b = MCellReleaseSite()
rel_b.x = 0.3
rel_b.y = 0.2
rel_b.z = 0.1
rel_b.molecule_species = mol_b
rel_b.quantity = 7
mcell.add_molecule_release_site ( rel_b )

mcell.num_iterations = 200
mcell.time_step = 1e-7

mcell.run_simulation(proj_path)


print "Done."
```




Start all examples with a handle to a simulation:

```
MCellSimulation *test1 = new MCellSimulation();
```

First question: should creating anything (molecule, reaction, etc) be tied to a simulation:

Should it be this:

```
MCellMoleculeSpecies *mol_a = new MCellMoleculeSpecies();
```

or this:

```
MCellMoleculeSpecies *mol_a = new test1.new_molecule_species();
```

The first allows creation of molecules outside of a simulation, while the second

Test 1 - Unbounded Diffusion

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

