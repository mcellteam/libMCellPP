![libMCell](libMCellCPPs.png?raw=true "libMCell")

# List of Test Cases for the API

1. Unbounded diffusion

a) Unbounded diffusion (through self-discovery)
```
>>> import libMCell
>>> dir(libMCell)
['__all__', '__name__', ... 'create_simulation']
>>> my_sim = libMCell.create_simulation()
>>> dir(my_sim)
['create_molecule_species', 'create_release_site', 'create_reaction', 'run_simulation' ...]
>>> type(my_sim)
<class 'dict'>
>>> my_sim.keys()
['data_model']
>>> my_sim['data_model'].keys()
['api_version', 'define_molecules', 'define_reactions', 'release_sites', 'initialization']
>>> my_sim['data_model']['define_molecules'].keys()
['molecule_list']
>>> len(my_sim['data_model']['define_molecules']['molecule_list']
0
>>> help(my_sim.create_molecule_species)
Help on create_molecule_species in module libMCell:
  create_molecule_species(name, dc=, type=, color=)
     name: required name for the species
     dc: diffusion constant (defaults to 0)
     type: 2D or 3D (defaults to 3D)
     color: list [r,g,b] (defaults to gray)
>>> my_sim.create_molecule_species(name='red', dc='1e-5', color=[1,0,0])
>>> len(my_sim['data_model']['define_molecules']['molecule_list']
1
>>> my_sim['data_model']['define_molecules']['molecule_list'][0]['color']
[1.0, 0.0, 0.0]
>>> help(my_sim.create_release_site)
Help on create_release_site in module libMCell:
  create_release_site(mol, num, location=, name= )
     mol: molecule species to be released
     num: number of individual molecules to release
     location: coordinates [x,y,z] (defaults to [0,0,0])
     name: optional name of the release site
>>> my_sim.create_release_site(my_sim['data_model']['define_molecules']['molecule_list'][0], 100)
>>> len(my_sim['data_model']['release_sites']['release_site_list'])
1
>>> my_sim['data_model']['release_sites']['release_site_list'][0].keys()
['name', 'molecule', 'quantity', 'quantity_type', 'release_probability', 'shape',
 'object_expr', 'orient', 'pattern', 'location_x', 'location_y', 'location_z',
 'site_diameter', 'stddev']
>>> my_sim['data_model']['release_sites']['release_site_list'][0]['quantity']
100
>>> help(my_sim.run_simulation)
Help on run_simulation in module libMCell:
  run_simulation(iterations=)
     iterations: number of iterations to run (defaults to 1)
>>> my_sim.run_simulation(1000)
```

b) Unbounded diffusion (same commands but no self-discovery)
```
>>> import libMCell
>>> my_sim = libMCell.create_simulation()
>>> my_sim.create_molecule_species(name='red', dc='1e-5', color=[1,0,0])
>>> my_sim.create_release_site(my_sim['data_model']['define_molecules']['molecule_list'][0], 100)
>>> my_sim.run_simulation(1000)
```


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


Fick's Law Script using Data Model Scripting
---------------------------------------------

This is what the "Data Model API" looks like for building the Fick's Law Example


    # Import cellblender to get the data model and project directory functions

    import cellblender as cb

    # Get a copy of the data model and change directories to the project directory for any file I/O

    dm = cb.get_data_model(geometry=True)

    # Print some information about the data model

    print ( "###############################################################" )

    print ( "Data Model Top Level Keys = " + str(dm.keys()) )
    print ( "MCell Keys = " + str(dm['mcell'].keys()) )

    print ( "###############################################################" )


    # Define parameters and set default values (these will also be available as local variables in this script)
    #  The format for each parameter is:   Name, Value, Units, Description
    #    All values are given as strings!!!

    pars = [
      # These control the geometry of the model
      ['n',    "40",    '',     'Number of segments to sample along the x dimension'],
      ['lx',   "2.0",   'um',   'Length x = Total length of sample box in x dimension'],
      ['ly',   "0.2",   'um',   'Length y = Total length of sample box in y dimension'],
      ['lz',   "0.2",   'um',   'Length z = Total length of sample box in z dimension'],
      ['ext',  "0.02",  'um',   'Extended length for counting boxes and counting planes'],
      ['tol',  "0.995", 'um',   'Scale factor of sampling boxes to avoid coincident faces (0.995 works well)'],
      ['rtol', "0.001", 'um',   'Release plane tolerance - smaller is closer to ideal (0.001 works well)'],
      # These control the instrumentation of the model
      ['plot_segment_counts',   "1",  '',   'Plot count of vm molecules in each segment when non-zero'],
      ['plot_front_crossings',  "0",  '',   'Plot front crossings of vm molecules when non-zero'],
      # These describe the behavior of the model
      ['dc',    "5e-6",   'cm^2/sec',    'Diffusion Constant of Molecules'],
      ['nrel',  "1000",   'Count',       'Number of molecules to release'],
      # These control the simulation itself
      ['iters', "600",   '',      'Number of iterations to run'],
      ['seeds', "10",    '',      'Number of seeds to run'],
      ['dt',    "1e-6",  'sec',   'Time step for each iteration of the simulation'],
     ]

    # Update local parameter list values from the existing data model with user-modified settings BEFORE regenerating it

    dm_par_list = dm['mcell']['parameter_system']['model_parameters']
    for dm_par in dm_par_list:
        print ( "Data Model Parameter " + dm_par['par_name'] + " = " + dm_par['par_expression'] )
        for p in pars:
            if dm_par['par_name'] == p[0]:
                # Update the local expression based on the parameter found in the incoming data model
                p[1] = dm_par['par_expression']
                p[2] = dm_par['par_units']
                p[3] = dm_par['par_description']


    # Create the local variables from the updated values to use in this script
    for p in pars:
        locals()[p[0]] = eval(p[1])


    # Create the new mcell data model inside the existing data model (this deletes the previous mcell data model)

    dm['mcell'] = { 'data_model_version' : "DM_2014_10_24_1638" }


    # Restore the parameters that were either initialized from scratch or preserved from the previous data model

    dm['mcell']['parameter_system'] = { 'model_parameters':[] }   # Parameters are currently unversioned
    for p in pars:
        dm['mcell']['parameter_system']['model_parameters'].append ( { 'par_name':p[0], 'par_expression':p[1], 'par_units':p[2], 'par_description':p[3] } )


    # Define a function to make either a plane or a box from its center and lengths in each dimension (one zero dimension gives a plane)

    def make_obj ( center_x, center_y, center_z, len_x, len_y, len_z ):
        obj = {}
        obj['vertex_list'] = []
        obj['element_connections'] = []

        if len_x == 0:
          # Make a plane perpendicular to the x axis
          obj['vertex_list'].append ( [ center_x, center_y-(len_y/2.0), center_z-(len_z/2.0) ] )
          obj['vertex_list'].append ( [ center_x, center_y-(len_y/2.0), center_z+(len_z/2.0) ] )
          obj['vertex_list'].append ( [ center_x, center_y+(len_y/2.0), center_z+(len_z/2.0) ] )
          obj['vertex_list'].append ( [ center_x, center_y+(len_y/2.0), center_z-(len_z/2.0) ] )
          obj['element_connections'].append ( [ 0, 2, 1 ] )
          obj['element_connections'].append ( [ 0, 3, 2 ] )
        elif len_y == 0:
          # Make a plane perpendicular to the y axis
          obj['vertex_list'].append ( [ center_x-(len_x/2.0), center_y, center_z-(len_z/2.0) ] )
          obj['vertex_list'].append ( [ center_x-(len_x/2.0), center_y, center_z+(len_z/2.0) ] )
          obj['vertex_list'].append ( [ center_x+(len_x/2.0), center_y, center_z+(len_z/2.0) ] )
          obj['vertex_list'].append ( [ center_x+(len_x/2.0), center_y, center_z-(len_z/2.0) ] )
          obj['element_connections'].append ( [ 0, 2, 1 ] )
          obj['element_connections'].append ( [ 0, 3, 2 ] )
        elif len_z == 0:
          # Make a plane perpendicular to the z axis
          obj['vertex_list'].append ( [ center_x-(len_x/2.0), center_y-(len_y/2.0), center_z ] )
          obj['vertex_list'].append ( [ center_x-(len_x/2.0), center_y+(len_y/2.0), center_z ] )
          obj['vertex_list'].append ( [ center_x+(len_x/2.0), center_y+(len_y/2.0), center_z ] )
          obj['vertex_list'].append ( [ center_x+(len_x/2.0), center_y-(len_y/2.0), center_z ] )
          obj['element_connections'].append ( [ 0, 2, 1 ] )
          obj['element_connections'].append ( [ 0, 3, 2 ] )
        else:
          # Make a box
          obj['vertex_list'].append ( [ center_x+(len_x/2.0), center_y+(len_y/2.0), center_z-(len_z/2.0) ] )
          obj['vertex_list'].append ( [ center_x+(len_x/2.0), center_y-(len_y/2.0), center_z-(len_z/2.0) ] )
          obj['vertex_list'].append ( [ center_x-(len_x/2.0), center_y-(len_y/2.0), center_z-(len_z/2.0) ] )
          obj['vertex_list'].append ( [ center_x-(len_x/2.0), center_y+(len_y/2.0), center_z-(len_z/2.0) ] )
          obj['vertex_list'].append ( [ center_x+(len_x/2.0), center_y+(len_y/2.0), center_z+(len_z/2.0) ] )
          obj['vertex_list'].append ( [ center_x+(len_x/2.0), center_y-(len_y/2.0), center_z+(len_z/2.0) ] )
          obj['vertex_list'].append ( [ center_x-(len_x/2.0), center_y-(len_y/2.0), center_z+(len_z/2.0) ] )
          obj['vertex_list'].append ( [ center_x-(len_x/2.0), center_y+(len_y/2.0), center_z+(len_z/2.0) ] )
          obj['element_connections'].append ( [ 1, 2, 3 ] )
          obj['element_connections'].append ( [ 7, 6, 5 ] )
          obj['element_connections'].append ( [ 4, 5, 1 ] ) # Right end
          obj['element_connections'].append ( [ 5, 6, 2 ] )
          obj['element_connections'].append ( [ 2, 6, 7 ] ) # Left end
          obj['element_connections'].append ( [ 0, 3, 7 ] )
          obj['element_connections'].append ( [ 0, 1, 3 ] )
          obj['element_connections'].append ( [ 4, 7, 5 ] )
          obj['element_connections'].append ( [ 0, 4, 1 ] ) # Right end
          obj['element_connections'].append ( [ 1, 5, 2 ] )
          obj['element_connections'].append ( [ 3, 2, 7 ] ) # Left end
          obj['element_connections'].append ( [ 4, 0, 7 ] )

        return obj


    # Add materials for the objects

    dm['mcell']['materials'] = { 'material_dict' : {} }   # Materials are currently unversioned
    dm['mcell']['materials']['material_dict']['box_color']   = { 'diffuse_color' : {'a':0.3, 'r':0.2, 'g':0.4, 'b':1.0} }
    dm['mcell']['materials']['material_dict']['rel_color']   = { 'diffuse_color' : {'a':0.2, 'r':0.9, 'g':0.7, 'b':0.5} }
    dm['mcell']['materials']['material_dict']['vol_color']   = { 'diffuse_color' : {'a':0.1, 'r':0.9, 'g':0.7, 'b':0.5} }
    dm['mcell']['materials']['material_dict']['plane_color'] = { 'diffuse_color' : {'a':0.7, 'r':0.5, 'g':0.7, 'b':1.0} }



    # Create container objects for geometrical objects and model objects

    dm['mcell']['geometrical_objects'] = {}   # Geometrical objects are currently unversioned
    dm['mcell']['model_objects'] = { 'data_model_version':"DM_2014_10_24_1638" }

    # Each container also includes a list

    dm['mcell']['geometrical_objects']['object_list'] = []
    dm['mcell']['model_objects']['model_object_list'] = []


    # Add objects to the lists

    # Make the main box for diffusing the molecules

    box = make_obj ( 0, 0, 0, 10*lx, ly, lz ) # Make the box much longer to reduce boundary effects from absorptive ends
    box['name'] = 'box'
    box['material_names'] = [ 'box_color' ]

    # Make the thin box for releasing the molecules

    rel = make_obj ( 0, 0, 0, rtol, ly-rtol, lz-rtol )
    rel['name'] = 'rel'
    rel['material_names'] = [ 'rel_color' ]

    # Make the surface regions for the two absorptive ends to keep them from accumulating
    box['define_surface_regions'] = []
    box['define_surface_regions'].append ( { 'name':"left_end", 'include_elements':[ 4, 10 ] } )
    box['define_surface_regions'].append ( { 'name':"right_end", 'include_elements':[ 2, 8 ] } )

    # Add the box to the geometrical objects and the model objects
    dm['mcell']['geometrical_objects']['object_list'].append ( box )
    dm['mcell']['model_objects']['model_object_list'].append ( { 'name':box['name'] } )

    dm['mcell']['geometrical_objects']['object_list'].append ( rel )
    dm['mcell']['model_objects']['model_object_list'].append ( { 'name':rel['name'] } )

    # Make the counting boxes and planes as requested by the parameter flags
    for i in range(n):

        x = (i - ((n-1)/2.0)) / (n/lx)

        if plot_segment_counts != 0:
          box = make_obj ( x, 0, 0, tol*(lx/n), ly+ext, lz+ext )
          box['name'] = 'vol_%03d' % i
          box['material_names'] = [ 'vol_color' ]
          dm['mcell']['geometrical_objects']['object_list'].append ( box )
          dm['mcell']['model_objects']['model_object_list'].append ( { 'name':box['name'] } )

        if (plot_front_crossings != 0) and (i > 0):
          plane = make_obj ( x-(lx/(2*n)), 0, 0, 0.0, ly+ext+ext, lz+ext+ext )
          plane['name'] = 'plane_%03d' % i
          plane['material_names'] = [ 'plane_color' ]
          dm['mcell']['geometrical_objects']['object_list'].append ( plane )
          dm['mcell']['model_objects']['model_object_list'].append ( { 'name':plane['name'] } )


    # Create a molecule list and create a "vm" molecule along with its display properties in that list

    dm['mcell']['define_molecules'] = { 'data_model_version' : "DM_2014_10_24_1638" }
    mol = { 'mol_name':"vm", 'mol_type':"3D", 'diffusion_constant':"dc", 'data_model_version':"DM_2016_01_13_1930" }
    mol['display'] = {'color':[0.0,1.0,0.0], 'emit':1.0, 'glyph':"Cube", 'scale':0.5 }
    dm['mcell']['define_molecules']['molecule_list'] = [ mol ]


    # Create a release site

    rel_site = {
                  'name' : "center_rel",
                  'molecule' : "vm",
                  'quantity' : "nrel",
                  'quantity_type' : "NUMBER_TO_RELEASE",
                  'release_probability' : "1",
                  'shape' : "OBJECT",
                  'object_expr' : "rel",
                  'orient' : ";",
                  'pattern' : "",
                  'location_x' : "0",
                  'location_y' : "0",
                  'location_z' : "0",
                  'site_diameter' : "0",
                  'stddev' : "0",
                  'data_model_version' : "DM_2015_11_11_1717"
               }

    dm['mcell']['release_sites'] = { 'release_site_list':[ rel_site ], 'data_model_version':"DM_2014_10_24_1638" }

    # Define surface classes

    dm['mcell']['define_surface_classes'] = { 'surface_class_list':[], 'data_model_version':"DM_2014_10_24_1638" }

    # Use a table to construct the various classes with associated properties

    surf_classes = [
      [ 'transp', 'vm_transp', ';', "TRANSPARENT",         "0" ],
      [ 'absorb', 'vm_absorb', ';', "ABSORPTIVE",          "0" ] ]

    # Loop through the table and add each class to the data model

    for c in surf_classes:
      sc_prop = { 'data_model_version':"DM_2015_11_08_1756",
                  'name':c[1],
                  'affected_mols':"SINGLE",
                  'molecule':"vm",
                  'surf_class_orient':c[2],
                  'surf_class_type':c[3],
                  'clamp_value':c[4]
                }

      sc_entry = { 'data_model_version':"DM_2014_10_24_1638",
                   'name':c[0],
                   'surface_class_prop_list':[ sc_prop ]
                 }

      dm['mcell']['define_surface_classes']['surface_class_list'].append ( sc_entry )


    # Assign the surface classes with the "modify_surface_regions" key

    dm['mcell']['modify_surface_regions'] = { 'modify_surface_regions_list':[], 'data_model_version': "DM_2014_10_24_1638" }


    # Modify the left end to be absorptive

    dm['mcell']['modify_surface_regions']['modify_surface_regions_list'].append (
        {
          'name':"absorb left",
          'object_name':"box",
          'region_name':"left_end",
          'surf_class_name':"absorb",
          'region_selection':"SEL",
          'data_model_version':"DM_2015_11_06_1732"
        } )

    # Modify the right end to be absorptive

    dm['mcell']['modify_surface_regions']['modify_surface_regions_list'].append (
        {
          'name':"absorb right",
          'object_name':"box",
          'region_name':"right_end",
          'surf_class_name':"absorb",
          'region_selection':"SEL",
          'data_model_version':"DM_2015_11_06_1732" } )

    # Modify the release box, all counting boxes, and counting planes (if any) to be transparent

    dm['mcell']['modify_surface_regions']['modify_surface_regions_list'].append (
      {
        'name':"transp rel",
        'object_name':"rel",
        'region_name':"",
        'surf_class_name':"transp",
        'region_selection':"ALL",
        'data_model_version':"DM_2015_11_06_1732"
      } )

    for i in range(n):

        if plot_segment_counts != 0:
          name = 'vol_%03d' % i
          dm['mcell']['modify_surface_regions']['modify_surface_regions_list'].append (
            {
              'name':"transp "+name,
              'object_name':name,
              'region_name':"",
              'surf_class_name':"transp",
              'region_selection':"ALL",
              'data_model_version':"DM_2015_11_06_1732"
            } )

        if (plot_front_crossings != 0) and (i > 0):
          name = 'plane_%03d' % i
          dm['mcell']['modify_surface_regions']['modify_surface_regions_list'].append (
            {
              'name':"transp "+name,
              'object_name':name,
              'region_name':"",
              'surf_class_name':"transp",
              'region_selection':"ALL",
              'data_model_version':"DM_2015_11_06_1732"
            } )


    # Define the counting output

    dm['mcell']['reaction_data_output'] = {
        'data_model_version':"DM_2014_10_24_1638",
        'reaction_output_list':[],
        'rxn_step':"10*dt",
        'combine_seeds':False,
        'mol_colors':True,
        'plot_layout':" plot ",
        'plot_legend':"x",
        'mol_colors':False
        }

    dm['mcell']['reaction_data_output']['reaction_output_list'].append (
        {
          'data_model_version':"DM_2015_10_07_1500",
           'name':"vm in box",
           'rxn_or_mol':"Molecule",
           'mdl_string':"",
           'mdl_file_prefix':"",
           'count_location':"Object",
           'object_name':"box",
           'region_name':"",
           'reaction_name':"",
           'molecule_name':"vm"
        } )

    # Create the counting structures for the counting object as requested

    for i in range(n):
        if plot_segment_counts != 0:
            name = 'vol_%03d' % i
            if plot_segment_counts != 0:
              dm['mcell']['reaction_data_output']['reaction_output_list'].append (
                {
                  'data_model_version':"DM_2015_10_07_1500",
                  'name':"vm in "+name,
                  'rxn_or_mol':"Molecule",
                  'mdl_string':"",
                  'mdl_file_prefix':"",
                  'count_location':"Object",
                  'object_name':name,
                  'region_name':"",
                  'reaction_name':"",
                  'molecule_name':"vm"
                } )
        if (plot_front_crossings != 0) and (i > 0):
          name = 'plane_%03d' % i
          mdl_string = "COUNT[vm,Scene."+name+",FRONT_CROSSINGS]"
          dm['mcell']['reaction_data_output']['reaction_output_list'].append (
            {
              'data_model_version':"DM_2015_10_07_1500",
              'name':"MDL: "+mdl_string,
              'rxn_or_mol':"MDLString",
              'mdl_file_prefix':name+"_front_cross",
              'mdl_string':mdl_string,
              'count_location':"World",
              'object_name':"",
              'region_name':"",
              'reaction_name':"",
              'molecule_name':""
            } )


    # Set up the simulation running parameters

    dm['mcell']['initialization'] = { 'data_model_version':"DM_2014_10_24_1638" }
    dm['mcell']['initialization']['iterations'] = "iters"
    dm['mcell']['initialization']['time_step'] = "dt"

    dm['mcell']['simulation_control'] = { 'data_model_version': 'DM_2016_04_15_1430' }
    dm['mcell']['simulation_control']['start_seed'] = '1'
    dm['mcell']['simulation_control']['end_seed'] = 'seeds'





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

