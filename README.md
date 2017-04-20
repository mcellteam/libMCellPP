# libMCell C++

C++ Version of MCell

The C++ version of libMCell is intended to provide a convenient and high performance interface to the capabilities of the MCell code base. This Wiki page describes some of the features of libMCell as it is being designed. It is a work in progress.

See also: http://mcellteam.github.io/libMCellPP/

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

## Counting Example

Counting has been a somewhat complicated process in MCell because the MDL language has tried to anticipate and offer as many counting options and capabilities as imagined to be useful. The anticipated C++/Python API for libMCell will, instead, expose the features needed for end users to write their own counting code. The library will also include various convenience functions built on top of this API to provide the traditional MCell counting functionality. The following example sketches out the proposed API.

```
# TCO = Trigger, Condition, Outcome event model

# Superclass of all TCO events will contain the time of the event
class TCO_event:
    def __init__(self):
      self.time = 0

# Superclass of all TCO event listeners
class TCO_listener:
      def execute(self, the_event):
          return

# The molecule creation event subclass contains the molecule (or molecules?)
#   that have been created
class TCO_mol_creation_event(TCO_event):
    def __init__(self):
       self.the_molecule = None  # the instance of the molecule (not species) that was created


# Here's our event handler to count mol a in the world:
class mol_a_listener(TCO_listener):

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

## Data Model / API correspondence

The following data model naming reflects changes resulting from the December 14th, 2016 meeting:

```
['mcell_model']['api_version']   (long)
['mcell_model']['blender_version'][#]   (long)
['mcell_model']['cellblender_source_sha1']   (str)
['mcell_model']['cellblender_version']   (str)
['mcell_model']['data_model_version']   (str)
['mcell_model']['species']['data_model_version']   (str)
['mcell_model']['species']['species_list'][#]['custom_space_step']   (str)
['mcell_model']['species']['species_list'][#]['custom_time_step']   (str)
['mcell_model']['species']['species_list'][#]['data_model_version']   (str)
['mcell_model']['species']['species_list'][#]['diffusion_constant']   (str)
['mcell_model']['species']['species_list'][#]['display']['color'][#]   (float)
['mcell_model']['species']['species_list'][#]['display']['emit']   (float)
['mcell_model']['species']['species_list'][#]['display']['glyph']   (str)
['mcell_model']['species']['species_list'][#]['display']['scale']   (float)
['mcell_model']['species']['species_list'][#]['export_viz']   (bool)
['mcell_model']['species']['species_list'][#]['maximum_step_length']   (str)
['mcell_model']['species']['species_list'][#]['mol_bngl_label']   (str)
['mcell_model']['species']['species_list'][#]['mol_name']   (str)
['mcell_model']['species']['species_list'][#]['mol_type']   (str)
['mcell_model']['species']['species_list'][#]['target_only']   (bool)
['mcell_model']['reactions']['data_model_version']   (str)
['mcell_model']['reactions']['reaction_list'][#]['bkwd_rate']   (str)
['mcell_model']['reactions']['reaction_list'][#]['data_model_version']   (str)
['mcell_model']['reactions']['reaction_list'][#]['fwd_rate']   (str)
['mcell_model']['reactions']['reaction_list'][#]['name']   (str)
['mcell_model']['reactions']['reaction_list'][#]['products']   (str)
['mcell_model']['reactions']['reaction_list'][#]['reactants']   (str)
['mcell_model']['reactions']['reaction_list'][#]['rxn_name']   (str)
['mcell_model']['reactions']['reaction_list'][#]['rxn_type']   (str)
['mcell_model']['reactions']['reaction_list'][#]['variable_rate']   (str)
['mcell_model']['reactions']['reaction_list'][#]['variable_rate_switch']   (bool)
['mcell_model']['reactions']['reaction_list'][#]['variable_rate_text']   (str)
['mcell_model']['reactions']['reaction_list'][#]['variable_rate_valid']   (bool)
['mcell_model']['release_patterns']['data_model_version']   (str)
['mcell_model']['release_patterns']['release_pattern_list'][#]['data_model_version']   (str)
['mcell_model']['release_patterns']['release_pattern_list'][#]['delay']   (str)
['mcell_model']['release_patterns']['release_pattern_list'][#]['name']   (str)
['mcell_model']['release_patterns']['release_pattern_list'][#]['number_of_trains']   (str)
['mcell_model']['release_patterns']['release_pattern_list'][#]['release_interval']   (str)
['mcell_model']['release_patterns']['release_pattern_list'][#]['train_duration']   (str)
['mcell_model']['release_patterns']['release_pattern_list'][#]['train_interval']   (str)
['mcell_model']['surface_classes']['data_model_version']   (str)
['mcell_model']['surface_classes']['surface_class_list'][#]['data_model_version']   (str)
['mcell_model']['surface_classes']['surface_class_list'][#]['name']   (str)
['mcell_model']['surface_classes']['surface_class_list'][#]['surface_class_prop_list'][#]['affected_mols']   (str)
['mcell_model']['surface_classes']['surface_class_list'][#]['surface_class_prop_list'][#]['clamp_value']   (str)
['mcell_model']['surface_classes']['surface_class_list'][#]['surface_class_prop_list'][#]['data_model_version']   (str)
['mcell_model']['surface_classes']['surface_class_list'][#]['surface_class_prop_list'][#]['molecule']   (str)
['mcell_model']['surface_classes']['surface_class_list'][#]['surface_class_prop_list'][#]['name']   (str)
['mcell_model']['surface_classes']['surface_class_list'][#]['surface_class_prop_list'][#]['surf_class_orient']   (str)
['mcell_model']['surface_classes']['surface_class_list'][#]['surface_class_prop_list'][#]['surf_class_type']   (str)
['mcell_model']['geometrical_objects']['object_list'][#]['define_surface_regions'][#]['include_elements'][#]   (long)
['mcell_model']['geometrical_objects']['object_list'][#]['define_surface_regions'][#]['name']   (str)
['mcell_model']['geometrical_objects']['object_list'][#]['element_connections'][#][#]   (long)
['mcell_model']['geometrical_objects']['object_list'][#]['location'][#]   (float)
['mcell_model']['geometrical_objects']['object_list'][#]['material_names'][#]   (str)
['mcell_model']['geometrical_objects']['object_list'][#]['name']   (str)
['mcell_model']['geometrical_objects']['object_list'][#]['vertex_list'][#][#]   (float)
['mcell_model']['initialization']['accurate_3d_reactions']   (bool)
['mcell_model']['initialization']['center_molecules_on_grid']   (bool)
['mcell_model']['initialization']['data_model_version']   (str)
['mcell_model']['initialization']['interaction_radius']   (str)
['mcell_model']['initialization']['iterations']   (str)
['mcell_model']['initialization']['microscopic_reversibility']   (str)
['mcell_model']['initialization']['notifications']['all_notifications']   (str)
['mcell_model']['initialization']['notifications']['box_triangulation_report']   (bool)
['mcell_model']['initialization']['notifications']['diffusion_constant_report']   (str)
['mcell_model']['initialization']['notifications']['file_output_report']   (bool)
['mcell_model']['initialization']['notifications']['final_summary']   (bool)
['mcell_model']['initialization']['notifications']['iteration_report']   (bool)
['mcell_model']['initialization']['notifications']['molecule_collision_report']   (bool)
['mcell_model']['initialization']['notifications']['partition_location_report']   (bool)
['mcell_model']['initialization']['notifications']['probability_report']   (str)
['mcell_model']['initialization']['notifications']['probability_report_threshold']   (str)
['mcell_model']['initialization']['notifications']['progress_report']   (bool)
['mcell_model']['initialization']['notifications']['release_event_report']   (bool)
['mcell_model']['initialization']['notifications']['varying_probability_report']   (bool)
['mcell_model']['initialization']['partitions']['data_model_version']   (str)
['mcell_model']['initialization']['partitions']['include']   (bool)
['mcell_model']['initialization']['partitions']['recursion_flag']   (bool)
['mcell_model']['initialization']['partitions']['x_end']   (str)
['mcell_model']['initialization']['partitions']['x_start']   (str)
['mcell_model']['initialization']['partitions']['x_step']   (str)
['mcell_model']['initialization']['partitions']['y_end']   (str)
['mcell_model']['initialization']['partitions']['y_start']   (str)
['mcell_model']['initialization']['partitions']['y_step']   (str)
['mcell_model']['initialization']['partitions']['z_end']   (str)
['mcell_model']['initialization']['partitions']['z_start']   (str)
['mcell_model']['initialization']['partitions']['z_step']   (str)
['mcell_model']['initialization']['radial_directions']   (str)
['mcell_model']['initialization']['radial_subdivisions']   (str)
['mcell_model']['initialization']['space_step']   (str)
['mcell_model']['initialization']['surface_grid_density']   (str)
['mcell_model']['initialization']['time_step']   (str)
['mcell_model']['initialization']['time_step_max']   (str)
['mcell_model']['initialization']['vacancy_search_distance']   (str)
['mcell_model']['initialization']['warnings']['all_warnings']   (str)
['mcell_model']['initialization']['warnings']['degenerate_polygons']   (str)
['mcell_model']['initialization']['warnings']['high_probability_threshold']   (str)
['mcell_model']['initialization']['warnings']['high_reaction_probability']   (str)
['mcell_model']['initialization']['warnings']['lifetime_threshold']   (str)
['mcell_model']['initialization']['warnings']['lifetime_too_short']   (str)
['mcell_model']['initialization']['warnings']['missed_reaction_threshold']   (str)
['mcell_model']['initialization']['warnings']['missed_reactions']   (str)
['mcell_model']['initialization']['warnings']['missing_surface_orientation']   (str)
['mcell_model']['initialization']['warnings']['negative_diffusion_constant']   (str)
['mcell_model']['initialization']['warnings']['negative_reaction_rate']   (str)
['mcell_model']['initialization']['warnings']['useless_volume_orientation']   (str)
['mcell_model']['materials']['material_dict']['left_cube_mat']['diffuse_color']['a']   (float)
['mcell_model']['materials']['material_dict']['left_cube_mat']['diffuse_color']['b']   (float)
['mcell_model']['materials']['material_dict']['left_cube_mat']['diffuse_color']['g']   (float)
['mcell_model']['materials']['material_dict']['left_cube_mat']['diffuse_color']['r']   (float)
['mcell_model']['materials']['material_dict']['right_cube_mat']['diffuse_color']['a']   (float)
['mcell_model']['materials']['material_dict']['right_cube_mat']['diffuse_color']['b']   (float)
['mcell_model']['materials']['material_dict']['right_cube_mat']['diffuse_color']['g']   (float)
['mcell_model']['materials']['material_dict']['right_cube_mat']['diffuse_color']['r']   (float)
['mcell_model']['model_objects']['data_model_version']   (str)
['mcell_model']['model_objects']['model_object_list'][#]['name']   (str)
['mcell_model']['surface_class_assignments']['data_model_version']   (str)
['mcell_model']['surface_class_assignments']['surface_class_assignment_list'][#]['data_model_version']   (str)
['mcell_model']['surface_class_assignments']['surface_class_assignment_list'][#]['name']   (str)
['mcell_model']['surface_class_assignments']['surface_class_assignment_list'][#]['object_name']   (str)
['mcell_model']['surface_class_assignments']['surface_class_assignment_list'][#]['region_name']   (str)
['mcell_model']['surface_class_assignments']['surface_class_assignment_list'][#]['region_selection']   (str)
['mcell_model']['surface_class_assignments']['surface_class_assignment_list'][#]['surf_class_name']   (str)
['mcell_model']['mol_viz']['active_seed_index']   (long)
['mcell_model']['mol_viz']['color_index']   (long)
['mcell_model']['mol_viz']['color_list'][#][#]   (float)
['mcell_model']['mol_viz']['data_model_version']   (str)
['mcell_model']['mol_viz']['file_dir']   (str)
['mcell_model']['mol_viz']['file_index']   (long)
['mcell_model']['mol_viz']['file_name']   (str)
['mcell_model']['mol_viz']['file_num']   (long)
['mcell_model']['mol_viz']['file_start_index']   (long)
['mcell_model']['mol_viz']['file_step_index']   (long)
['mcell_model']['mol_viz']['file_stop_index']   (long)
['mcell_model']['mol_viz']['manual_select_viz_dir']   (bool)
['mcell_model']['mol_viz']['render_and_save']   (bool)
['mcell_model']['mol_viz']['seed_list'][#]   (str)
['mcell_model']['mol_viz']['viz_enable']   (bool)
['mcell_model']['mol_viz']['viz_list'][#]   (str)
['mcell_model']['parameters']['_extras']['ordered_id_names'][#]   (str)
['mcell_model']['parameters']['parameter_list'][#]['_extras']['par_id_name']   (str)
['mcell_model']['parameters']['parameter_list'][#]['_extras']['par_valid']   (bool)
['mcell_model']['parameters']['parameter_list'][#]['_extras']['par_value']   (float)
['mcell_model']['parameters']['parameter_list'][#]['par_description']   (str)
['mcell_model']['parameters']['parameter_list'][#]['par_expression']   (str)
['mcell_model']['parameters']['parameter_list'][#]['par_name']   (str)
['mcell_model']['parameters']['parameter_list'][#]['par_units']   (str)
['mcell_model']['parameters']['parameter_list'][#]['sweep_enabled']   (bool)
['mcell_model']['count_output']['always_generate']   (bool)
['mcell_model']['count_output']['combine_seeds']   (bool)
['mcell_model']['count_output']['data_model_version']   (str)
['mcell_model']['count_output']['mol_colors']   (bool)
['mcell_model']['count_output']['output_buf_size']   (str)
['mcell_model']['count_output']['plot_layout']   (str)
['mcell_model']['count_output']['plot_legend']   (str)
['mcell_model']['count_output']['count_output_list'][#]['count_location']   (str)
['mcell_model']['count_output']['count_output_list'][#]['data_file_name']   (str)
['mcell_model']['count_output']['count_output_list'][#]['data_model_version']   (str)
['mcell_model']['count_output']['count_output_list'][#]['mdl_file_prefix']   (str)
['mcell_model']['count_output']['count_output_list'][#]['mdl_string']   (str)
['mcell_model']['count_output']['count_output_list'][#]['molecule_name']   (str)
['mcell_model']['count_output']['count_output_list'][#]['name']   (str)
['mcell_model']['count_output']['count_output_list'][#]['object_name']   (str)
['mcell_model']['count_output']['count_output_list'][#]['plotting_enabled']   (bool)
['mcell_model']['count_output']['count_output_list'][#]['reaction_name']   (str)
['mcell_model']['count_output']['count_output_list'][#]['region_name']   (str)
['mcell_model']['count_output']['count_output_list'][#]['rxn_or_mol']   (str)
['mcell_model']['count_output']['rxn_step']   (str)
['mcell_model']['release_sites']['data_model_version']   (str)
['mcell_model']['release_sites']['release_site_list'][#]['data_model_version']   (str)
['mcell_model']['release_sites']['release_site_list'][#]['location_x']   (str)
['mcell_model']['release_sites']['release_site_list'][#]['location_y']   (str)
['mcell_model']['release_sites']['release_site_list'][#]['location_z']   (str)
['mcell_model']['release_sites']['release_site_list'][#]['molecule']   (str)
['mcell_model']['release_sites']['release_site_list'][#]['name']   (str)
['mcell_model']['release_sites']['release_site_list'][#]['object_expr']   (str)
['mcell_model']['release_sites']['release_site_list'][#]['orient']   (str)
['mcell_model']['release_sites']['release_site_list'][#]['pattern']   (str)
['mcell_model']['release_sites']['release_site_list'][#]['quantity']   (str)
['mcell_model']['release_sites']['release_site_list'][#]['quantity_type']   (str)
['mcell_model']['release_sites']['release_site_list'][#]['release_probability']   (str)
['mcell_model']['release_sites']['release_site_list'][#]['shape']   (str)
['mcell_model']['release_sites']['release_site_list'][#]['site_diameter']   (str)
['mcell_model']['release_sites']['release_site_list'][#]['stddev']   (str)
['mcell_model']['scripting']['data_model_version']   (str)
['mcell_model']['scripting']['dm_external_file_name']   (str)
['mcell_model']['scripting']['dm_internal_file_name']   (str)
['mcell_model']['scripting']['force_property_update']   (bool)
['mcell_model']['scripting']['show_data_model_scripting']   (bool)
['mcell_model']['scripting']['show_simulation_scripting']   (bool)
['mcell_model']['simulation_control']['data_model_version']   (str)
['mcell_model']['simulation_control']['end_seed']   (str)
['mcell_model']['simulation_control']['name']   (str)
['mcell_model']['simulation_control']['run_limit']   (str)
['mcell_model']['simulation_control']['start_seed']   (str)
['mcell_model']['viz_output']['all_iterations']   (bool)
['mcell_model']['viz_output']['data_model_version']   (str)
['mcell_model']['viz_output']['end']   (str)
['mcell_model']['viz_output']['export_all']   (bool)
['mcell_model']['viz_output']['start']   (str)
['mcell_model']['viz_output']['step']   (str)
```

