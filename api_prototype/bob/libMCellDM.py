# import pyMCell as m

import json


class DataModelItem(dict):

    def __init__(self, dm, path):
        # print ( "Path = " + str(path) )
        known_paths = {  'mcell.parameter_system' : Parameters,
                         'mcell.initialization' : Initialization,
                         'mcell.geometrical_objects' : GeometryObjects,
                         'mcell.model_objects' : ModelObjects,
                         'mcell.define_surface_classes' : DataModelStub,
                         'mcell.modify_surface_regions' : DataModelStub,
                         'mcell.define_molecules' : Species,
                         'mcell.define_reactions' : DataModelStub,
                         'mcell.release_sites' : DataModelStub,
                         'mcell.define_release_patterns' : DataModelStub,
                         'mcell.materials' : DataModelStub,
                         'mcell.mol_viz' : DataModelStub,
                         'mcell.viz_output' : DataModelStub,
                         'mcell.reaction_data_output' : DataModelStub,
                         'mcell.scripting' : DataModelStub,
                         'mcell.simulation_control' : DataModelStub  }

        #if (len(path) > 0) and (path in known_paths.keys()):
        #    print ( "Data Model Category = " + path )

        if type(dm) == type({}):
            for k in dm.keys():
                v = dm[k]
                subpath = k
                if len(path) > 0:
                    subpath = path + "." + k
                if type(v) == type({}):
                    if (len(subpath) > 0) and (subpath in known_paths.keys()):
                        self[k] = known_paths[subpath](v, subpath)
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
        print ( "\nInitializing Parameters from Data Model" )
        for p in self.model_parameters:
            print ( "  " + p.par_name + " = " + str(p.par_expression) )


class Initialization(DataModelItem):
    def __init__ ( self, dm, path ):
        # Start by reading all of the data model items generically
        super().__init__(dm,path)
        # Next perform any class-specific initialization
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
        print ( "\nInitializing GeometryObjects from Data Model" )
        for o in self.object_list:
            print ( "  " + o.name + " is at " + str(o.location) + " with " + str(len(o.vertex_list)) + " points and " + str(len(o.element_connections)) + " faces" )


class ModelObjects(DataModelItem):
    def __init__ ( self, dm, path ):
        # Start by reading all of the data model items generically
        super().__init__(dm,path)
        # Next perform any class-specific initialization
        print ( "\nInitializing ModelObjects from Data Model" )
        for m in self.model_object_list:
            print ( "  Model Object " + m.name )


class Species(DataModelItem):
    def __init__ ( self, dm, path ):
        # Start by reading all of the data model items generically
        super().__init__(dm,path)
        # Next perform any class-specific initialization
        print ( "\nInitializing Species from Data Model" )
        for m in self.molecule_list:
            print ( "  " + m.mol_name + " is " + m.mol_type + " with diffusion_constant = " + str(m.diffusion_constant) )





dm_str = '{"iters":100, "init": {"warn":"off", "errlim":5 }, "mols": [ {"name":"a", "dc":1e-6 }, {"name":"b", "dc":2e-6 } ] }'

with open ( "moderate_model.json", "r" ) as f:
    dm_str = f.read()

dm = json.loads ( dm_str )

# print ( str(dm) )

dm = DataModelItem(dm,"")

mcell = dm.mcell

print()
for k in mcell.keys():
  print ( "mcell." + k + " is of type " + str(type(mcell[k])) )

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

__import__('code').interact(local={k: v for ns in (globals(), locals()) for k, v in ns.items()})

