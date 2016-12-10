# import pyMCell as m

import json


class DataModelItem(dict):

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
                        self[k] = DataModelItem(v, subpath)
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
                    l.append ( DataModelItem(item, path+'['+str(index)+']') )
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
            raise AttributeError("No such attribute: " + name)

    def __setattr__(self, name, value):
        self[name] = value

    def __delattr__(self, name):
        if name in self:
            del self[name]
        else:
            raise AttributeError("No such attribute: " + name)


class DataModelStub(DataModelItem):
    pass


class Parameters(DataModelItem):
    def __init__ ( self, dm, path ):
        # Start by reading all of the data model items generically
        super().__init__(dm,path)
        # Next perform any class-specific initialization
        self.print()

    def print(self):
        print ( "\nInitializing Parameters from Data Model" )
        for p in self.model_parameters:
            print ( "  " + p.par_name + " = " + str(p.par_expression) )


class Initialization(DataModelItem):
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


class GeometryObjects(DataModelItem):
    def __init__ ( self, dm, path ):
        # Start by reading all of the data model items generically
        super().__init__(dm,path)
        # Next perform any class-specific initialization
        self.print()

    def print(self):
        print ( "\nInitializing GeometryObjects from Data Model" )
        for o in self.object_list:
            print ( "  " + o.name + " is at " + str(o.location) + " with " + str(len(o.vertex_list)) + " points and " + str(len(o.element_connections)) + " faces" )


class ModelObjects(DataModelItem):
    def __init__ ( self, dm, path ):
        # Start by reading all of the data model items generically
        super().__init__(dm,path)
        # Next perform any class-specific initialization
        self.print()

    def print(self):
        print ( "\nInitializing ModelObjects from Data Model" )
        for m in self.model_object_list:
            print ( "  Model Object " + m.name )


class Species(DataModelItem):
    def __init__ ( self, dm, path ):
        # Start by reading all of the data model items generically
        super().__init__(dm,path)
        # Next perform any class-specific initialization
        self.print()

    def print(self):
        print ( "\nInitializing Species from Data Model" )
        for m in self.molecule_list:
            print ( "  " + m.mol_name + " is " + m.mol_type + " with diffusion_constant = " + str(m.diffusion_constant) )

class  SurfaceClasses (DataModelItem):
    def __init__ ( self, dm, path ):
        # Start by reading all of the data model items generically
        super().__init__(dm,path)
        # Next perform any class-specific initialization
        self.print()

    def print(self):
        print ( "\nInitializing SurfaceClasses from Data Model" )
        for sc in self.surface_class_list:
            print ( "  " + sc.name + " has " + str(len(sc.surface_class_prop_list)) + " surface properties" )

class  SurfaceRegionMods (DataModelItem):
    def __init__ ( self, dm, path ):
        # Start by reading all of the data model items generically
        super().__init__(dm,path)
        # Next perform any class-specific initialization
        self.print()

    def print(self):
        print ( "\nInitializing SurfaceRegionMods from Data Model" )
        for sr in self.modify_surface_regions_list:
            print ( "  " + sr.region_name + " is " + sr.name )

class  Reactions (DataModelItem):
    def __init__ ( self, dm, path ):
        # Start by reading all of the data model items generically
        super().__init__(dm,path)
        # Next perform any class-specific initialization
        self.print()

    def print(self):
        print ( "\nInitializing Reactions from Data Model" )
        for r in self.reaction_list:
            print ( "  Reaction Definition:  " + r.name + " [" + str(r.fwd_rate) + "," + str(r.bkwd_rate) + "]" )

class  ReleaseSites (DataModelItem):
    def __init__ ( self, dm, path ):
        # Start by reading all of the data model items generically
        super().__init__(dm,path)
        # Next perform any class-specific initialization
        self.print()

    def print(self):
        print ( "\nInitializing ReleaseSites from Data Model" )
        for rs in self.release_site_list:
            print ( "  " + rs.name + " releases " + rs.molecule + " with shape " + rs.shape )

class  ReleasePatterns (DataModelItem):
    def __init__ ( self, dm, path ):
        # Start by reading all of the data model items generically
        super().__init__(dm,path)
        # Next perform any class-specific initialization
        self.print()

    def print(self):
        print ( "\nInitializing ReleasePatterns from Data Model" )
        for rp in self.release_pattern_list:
            print ( "  Pattern " + str(rp.name) + " releases " + str(rp.number_of_trains) + " train(s)" )

class  Materials (DataModelItem):
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

class  MoleculeVisualization (DataModelItem):
    def __init__ ( self, dm, path ):
        # Start by reading all of the data model items generically
        super().__init__(dm,path)
        # Next perform any class-specific initialization
        self.print()

    def print(self):
        print ( "\nInitializing MoleculeVisualization from Data Model" )
        for m in self.viz_list:
            print ( "  Molecule " + m )

class  VisualizationOutput (DataModelItem):
    def __init__ ( self, dm, path ):
        # Start by reading all of the data model items generically
        super().__init__(dm,path)
        # Next perform any class-specific initialization
        self.print()

    def print(self):
        print ( "\nInitializing VisualizationOutput from Data Model" )
        print ( "  Visualization: from " + str(self.start) + " to " + str(self.end) + " by " + str(self.step) + " with all_iterations = " + str(self.all_iterations) )

class  ReactionOutput (DataModelItem):
    def __init__ ( self, dm, path ):
        # Start by reading all of the data model items generically
        super().__init__(dm,path)
        # Next perform any class-specific initialization
        self.print()

    def print(self):
        print ( "\nInitializing ReactionOutput from Data Model" )
        for ro in self.reaction_output_list:
            print ( "  " + ro.name )

class  Scripting (DataModelItem):
    def __init__ ( self, dm, path ):
        # Start by reading all of the data model items generically
        super().__init__(dm,path)
        # Next perform any class-specific initialization
        self.print()

    def print(self):
        print ( "\nInitializing Scripting from Data Model" )
        print ( "  Scripting has " + str(len(self.script_texts)) + " texts, and " + str(len(self.scripting_list)) + " items in the list" )

class  SimulationControl (DataModelItem):
    def __init__ ( self, dm, path ):
        # Start by reading all of the data model items generically
        super().__init__(dm,path)
        # Next perform any class-specific initialization
        self.print()

    def print(self):
        print ( "\nInitializing SimulationControl from Data Model" )
        print ( "  Simulation Control uses seeds from " + str(self.start_seed) + " to " + str(self.end_seed) )



dm_str = '{"iters":100, "init": {"warn":"off", "errlim":5 }, "mols": [ {"name":"a", "dc":1e-6 }, {"name":"b", "dc":2e-6 } ] }'

with open ( "moderate_model.json", "r" ) as f:
    dm_str = f.read()

dm = json.loads ( dm_str )

# print ( str(dm) )

dm = DataModelItem(dm,"")

mcell = dm.mcell

print()
print ( "=============================================================================" )
for k in mcell.keys():
  print ( "mcell." + k + " is of type " + str(type(mcell[k])) )
print ( "=============================================================================" )

"""
print()
print ( "Source ID   = " + mcell.cellblender_source_sha1 )
print ( "DM Version  = " + mcell.data_model_version )
print ( "Iterations  = " + str(mcell.initialization.iterations) )
print()
p = mcell.initialization.partitions
print ( "Partitions:   x: %s to %s by %s,   y: %s to %s by %s,   z: %s to %s by %s" % (p.x_start, p.x_end, p.x_step, p.y_start, p.y_end, p.y_step, p.z_start, p.z_end, p.z_step, ) )
print()
ns = mcell.initialization.notifications
print ( "Notifications:" )
for n in ns.keys():
    print ( "  " + n + ": " + str(ns[n]) )
print()
ws = mcell.initialization.warnings
print ( "Warnings:" )
for w in ws.keys():
    print ( "  " + w + ": " + str(ws[w]) )
print()
print ( "Parameters:" )
for p in mcell.parameter_system.model_parameters:
    print ( "  " + p.par_name + " = " + str(p.par_expression) )
print()
print ( "Molecules:" )
for m in mcell.define_molecules.molecule_list:
    print ( "  " + m.mol_name + " is " + m.mol_type + " with diffusion_constant = " + str(m.diffusion_constant) )
print()
print ( "Objects:" )
for o in mcell.geometrical_objects.object_list:
    print ( "  " + o.name + " has " + str(len(o.vertex_list)) + " points and " + str(len(o.element_connections)) + " faces" )
    if "define_surface_regions" in o.keys():
        print ( "    " + o.name + " contains " + str(len(o.define_surface_regions)) + " regions" )
print()
print ( "Surface Classes:" )
for s in mcell.define_surface_classes.surface_class_list:
    print ( "  " + s.name + " has " + str(len(s.surface_class_prop_list)) + " property definitions" )
print()
print ( "Modify Surface Regions:" )
for s in mcell.modify_surface_regions.modify_surface_regions_list:
    print ( "  " + s.name )
print()
"""

# __import__('code').interact(local={k: v for ns in (globals(), locals()) for k, v in ns.items()})

