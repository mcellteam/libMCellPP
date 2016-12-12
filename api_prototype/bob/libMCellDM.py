# import pyMCell as m

import json


class DataModelDict(dict):

    def __init__(self, dm, path):
        # print ( "Path = " + str(path) )
        path_obj_map = ( ('mcell.parameter_system', Parameters),
                         ('mcell.initialization', Initialization),
                         ('mcell.geometrical_objects', GeometryObjects),
                         ('mcell.model_objects', ModelObjects),
                         ('mcell.define_surface_classes', SurfaceClasses),
                         ('mcell.modify_surface_regions', SurfaceRegionMods),
                         ('mcell.define_molecules', Species),
                         ('mcell.define_reactions', Reactions),
                         ('mcell.release_sites', ReleaseSites),
                         ('mcell.define_release_patterns', ReleasePatterns),
                         ('mcell.materials', Materials),
                         ('mcell.mol_viz', MoleculeVisualization),
                         ('mcell.viz_output', VisualizationOutput),
                         ('mcell.reaction_data_output', ReactionOutput),
                         ('mcell.scripting', Scripting),
                         ('mcell.simulation_control', SimulationControl) )


        known_paths = []
        for p in path_obj_map:
            known_paths.append(p[0])

        if type(dm) == type({}):
            path_prefix = ""
            if len(path) > 0:
                path_prefix = path + "."
            # Sort the keys to match the order in path_obj_map
            dm_keys = [ k for k in dm.keys() ]  # This is a copy of the original keys. Some (or all) of these may be moved into sorted_dm_keys.
            sorted_dm_keys = []   # This list of keys will be sorted to reflect the preferred order in the path_obj_map.
            for p in path_obj_map:
                for k in dm.keys():
                    if p[0] == path_prefix + k:
                        sorted_dm_keys.append ( k )
                        dm_keys.pop(dm_keys.index(k))
            # Add the remaining keys that didn't match
            for k in dm_keys:
                sorted_dm_keys.append ( k )

            for k in sorted_dm_keys:
                v = dm[k]
                subpath = path_prefix + k
                if type(v) == type({}):
                    if (len(subpath) > 0) and (subpath in known_paths):
                        i = known_paths.index(subpath)
                        self[k] = path_obj_map[i][1](v, subpath)
                    else:
                        self[k] = DataModelDict(v, subpath)
                elif type(v) == type([]):
                    sub_list = []
                    self.fill_list(sub_list,v, subpath)
                    self[k] = sub_list
                else:
                    self[k] = dm[k]
        else:
            raise AttributeError("Dictionary required rather than " + str(type(dm)))

    def fill_list(self, l, dm, path):
        # print ( "Path = " + str(path) )
        if type(dm) == type([]):
            index = 0
            for item in dm:
                if type(item) == type({}):
                    l.append ( DataModelDict(item, path+'['+str(index)+']') )
                elif type(item) == type([]):
                    sub_list = []
                    self.fill_list(sub_list,item, path+'['+str(index)+']')
                    l.append ( sub_list )
                else:
                    l.append ( item )
        else:
            raise AttributeError("List required rather than " + str(type(dm)))


    def __getattr__(self, name):
        if name in self:
            return self[name]
        else:
            raise AttributeError("No such attribute: " + str(name))

    def __setattr__(self, name, value):
        self[name] = value

    def __delattr__(self, name):
        if name in self:
            del self[name]
        else:
            raise AttributeError("No such attribute: " + str(name))


class DataModelStub(DataModelDict):
    pass


class Parameters(DataModelDict):
    def __init__ ( self, dm, path ):
        # Start by reading all of the data model items generically
        super().__init__(dm,path)
        # Next perform any class-specific initialization
        print()

    def print(self):
        print ( "\nInitializing Parameters from Data Model" )
        for p in self.model_parameters:
            print ( "  " + p.par_name + " = " + str(p.par_expression) )


class Initialization(DataModelDict):
    def __init__ ( self, dm, path ):
        # Start by reading all of the data model items generically
        super().__init__(dm,path)
        # Next perform any class-specific initialization
        self.print()

    def print(self):
        p = self.partitions
        print ( "\nInitializing Partitions from Data Model:" )
        print ( "  x: [%s to %s by %s]\n  y: [%s to %s by %s]\n  z: [%s to %s by %s]" % (p.x_start, p.x_end, p.x_step, p.y_start, p.y_end, p.y_step, p.z_start, p.z_end, p.z_step) )
        ns = self.notifications
        print ( "\nInitializing Notifications:" )
        for n in ns.keys():
            print ( "  " + n + ": " + str(ns[n]) )
        ws = self.warnings
        print ( "\nInitializing Warnings:" )
        for w in ws.keys():
            print ( "  " + w + ": " + str(ws[w]) )


class GeometryObjects(DataModelDict):
    def __init__ ( self, dm, path ):
        # Start by reading all of the data model items generically
        super().__init__(dm,path)
        # Next perform any class-specific initialization
        self.print()

    def print(self):
        print ( "\nInitializing GeometryObjects from Data Model" )
        for o in self.object_list:
            print ( "  " + o.name + " is at " + str(o.location) + " with " + str(len(o.vertex_list)) + " points and " + str(len(o.element_connections)) + " faces" )


class ModelObjects(DataModelDict):
    def __init__ ( self, dm, path ):
        # Start by reading all of the data model items generically
        super().__init__(dm,path)
        # Next perform any class-specific initialization
        self.print()

    def print(self):
        print ( "\nInitializing ModelObjects from Data Model" )
        for m in self.model_object_list:
            print ( "  Model Object " + m.name )


class Species(DataModelDict):
    def __init__ ( self, dm, path ):
        # Start by reading all of the data model items generically
        super().__init__(dm,path)
        # Next perform any class-specific initialization
        self.print()

    def print(self):
        print ( "\nInitializing Species from Data Model" )
        for m in self.molecule_list:
            print ( "  " + m.mol_name + " is " + m.mol_type + " with diffusion_constant = " + str(m.diffusion_constant) )

class  SurfaceClasses (DataModelDict):
    def __init__ ( self, dm, path ):
        # Start by reading all of the data model items generically
        super().__init__(dm,path)
        # Next perform any class-specific initialization
        self.print()

    def print(self):
        print ( "\nInitializing SurfaceClasses from Data Model" )
        for sc in self.surface_class_list:
            print ( "  " + sc.name + " has " + str(len(sc.surface_class_prop_list)) + " surface properties" )

class  SurfaceRegionMods (DataModelDict):
    def __init__ ( self, dm, path ):
        # Start by reading all of the data model items generically
        super().__init__(dm,path)
        # Next perform any class-specific initialization
        self.print()

    def print(self):
        print ( "\nInitializing SurfaceRegionMods from Data Model" )
        for sr in self.modify_surface_regions_list:
            print ( "  " + sr.region_name + " is " + sr.name )

class  Reactions (DataModelDict):
    def __init__ ( self, dm, path ):
        # Start by reading all of the data model items generically
        super().__init__(dm,path)
        # Next perform any class-specific initialization
        self.print()

    def print(self):
        print ( "\nInitializing Reactions from Data Model" )
        for r in self.reaction_list:
            print ( "  Reaction Definition:  " + r.name + " [" + str(r.fwd_rate) + "," + str(r.bkwd_rate) + "]" )

class  ReleaseSites (DataModelDict):
    def __init__ ( self, dm, path ):
        # Start by reading all of the data model items generically
        super().__init__(dm,path)
        # Next perform any class-specific initialization
        self.print()

    def print(self):
        print ( "\nInitializing ReleaseSites from Data Model" )
        for rs in self.release_site_list:
            print ( "  " + rs.name + " releases " + rs.molecule + " with shape " + rs.shape )

class  ReleasePatterns (DataModelDict):
    def __init__ ( self, dm, path ):
        # Start by reading all of the data model items generically
        super().__init__(dm,path)
        # Next perform any class-specific initialization
        self.print()

    def print(self):
        print ( "\nInitializing ReleasePatterns from Data Model" )
        for rp in self.release_pattern_list:
            print ( "  Pattern " + str(rp.name) + " releases " + str(rp.number_of_trains) + " train(s)" )

class  Materials (DataModelDict):
    def __init__ ( self, dm, path ):
        # Start by reading all of the data model items generically
        super().__init__(dm,path)
        # Next perform any class-specific initialization
        self.print()

    def print(self):
        print ( "\nInitializing Materials from Data Model" )
        for k in self.material_dict.keys():
            c = self.material_dict[k].diffuse_color
            print ( "  Material " + str(k) + " color is: [ R=%g  G=%g  B=%g   a=%g ]" % ( c.r, c.g, c.b, c.a) )

class  MoleculeVisualization (DataModelDict):
    def __init__ ( self, dm, path ):
        # Start by reading all of the data model items generically
        super().__init__(dm,path)
        # Next perform any class-specific initialization
        self.print()

    def print(self):
        print ( "\nInitializing MoleculeVisualization from Data Model" )
        for m in self.viz_list:
            print ( "  Molecule " + m )

class  VisualizationOutput (DataModelDict):
    def __init__ ( self, dm, path ):
        # Start by reading all of the data model items generically
        super().__init__(dm,path)
        # Next perform any class-specific initialization
        self.print()

    def print(self):
        print ( "\nInitializing VisualizationOutput from Data Model" )
        print ( "  Visualization: from " + str(self.start) + " to " + str(self.end) + " by " + str(self.step) + " with all_iterations = " + str(self.all_iterations) )

class  ReactionOutput (DataModelDict):
    def __init__ ( self, dm, path ):
        # Start by reading all of the data model items generically
        super().__init__(dm,path)
        # Next perform any class-specific initialization
        self.print()

    def print(self):
        print ( "\nInitializing ReactionOutput from Data Model" )
        for ro in self.reaction_output_list:
            print ( "  " + ro.name )

class  Scripting (DataModelDict):
    def __init__ ( self, dm, path ):
        # Start by reading all of the data model items generically
        super().__init__(dm,path)
        # Next perform any class-specific initialization
        self.print()

    def print(self):
        print ( "\nInitializing Scripting from Data Model" )
        print ( "  Scripting has " + str(len(self.script_texts)) + " texts, and " + str(len(self.scripting_list)) + " items in the list" )

class  SimulationControl (DataModelDict):
    def __init__ ( self, dm, path ):
        # Start by reading all of the data model items generically
        super().__init__(dm,path)
        # Next perform any class-specific initialization
        self.print()

    def print(self):
        print ( "\nInitializing SimulationControl from Data Model" )
        print ( "  Simulation Control uses seeds from " + str(self.start_seed) + " to " + str(self.end_seed) )

import sys
import argparse

def main(argv=None):
    arg_parser = argparse.ArgumentParser()
    group = arg_parser.add_mutually_exclusive_group()
    group.add_argument ( "-f", "--data_model_name", type=str, help="name of the data model to use" )
    group.add_argument ( "-t", "--test_only", action='store_true', help="use the default self-contained data model" )
    arg_parser.add_argument ( "-v", "--verbose", action='store_true', help="print additional details" )
    arg_parser.add_argument ( "-i", "--interactive", action='store_true', help="drop into an interactive shell after loading" )
    args = arg_parser.parse_args()

    dm_str = ''
    if args.test_only:
        dm_str = """{ "mcell":
                      {
                        "initialization": {
                          "time_step": "1e-6",
                          "iterations": "123",
                          "partitions": {
                            "data_model_version": "DM_2016_04_15_1600",
                            "include": true,
                            "x_start": "-2.1",
                            "x_end": "2.1",
                            "x_step": "0.1",
                            "y_start": "-1",
                            "y_end": "1",
                            "y_step": "0.1",
                            "z_start": "-1",
                            "z_end": "1",
                            "z_step": "0.1"
                          },
                          "notifications": {
                            "all_notifications": "INDIVIDUAL"
                          },
                          "warnings": {
                            "all_warnings": "INDIVIDUAL"
                          }
                        },
                        "define_molecules": {
                          "data_model_version": "DM_2014_10_24_1638",
                          "molecule_list": [
                            {"mol_name":"a", "mol_type":"3D", "diffusion_constant":"1e-6", "data_model_version": "DM_2016_01_13_1930" },
                            {"mol_name":"b", "mol_type":"3D", "diffusion_constant":"2e-6", "data_model_version": "DM_2016_01_13_1930" }
                          ]
                        },
                        "define_reactions": {
                          "data_model_version": "DM_2014_10_24_1638",
                          "reaction_list": [
                            {
                              "name": "left_vol + right_vol -> left_right_vol",
                              "data_model_version": "DM_2014_10_24_1638",
                              "reactants": "left_vol + right_vol",
                              "bkwd_rate": "",
                              "variable_rate_text": "",
                              "rxn_name": "",
                              "rxn_type": "irreversible",
                              "fwd_rate": "1e10",
                              "products": "left_right_vol",
                              "variable_rate_valid": false,
                              "variable_rate": "",
                              "variable_rate_switch": false
                            }
                          ]
                        }
                      }
                    }"""
    else:
        with open ( args.data_model_name, "r" ) as f:
            dm_str = f.read()

    dm = json.loads ( dm_str )

    if args.verbose:
        print ( str(dm) )

    dm = DataModelDict(dm,"")

    mcell = dm.mcell

    print()
    print ( "=============================================================================" )
    for k in mcell.keys():
      print ( "mcell." + k + " is of type " + str(type(mcell[k])) )
    print ( "=============================================================================" )

    if args.interactive:
        __import__('code').interact(local={k: v for ns in (globals(), locals()) for k, v in ns.items()})

if __name__ == '__main__':
    sys.exit(main())
