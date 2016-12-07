# import libMCell as m

import json

class DataModelObject(dict):

    def __init__(self, dm, path):
        # print ( "Path = " + str(path) )
        known_paths = ['mcell.viz_output',
                       'mcell.initialization',
                       'mcell.simulation_control',
                       'mcell.geometrical_objects',
                       'mcell.modify_surface_regions',
                       'mcell.define_molecules',
                       'mcell.materials',
                       'mcell.define_reactions',
                       'mcell.release_sites',
                       'mcell.define_surface_classes',
                       'mcell.reaction_data_output',
                       'mcell.parameter_system',
                       'mcell.define_release_sites',
                       'mcell.scripting',
                       'mcell.model_objects']
        if (len(path) > 0) and (path[1:] in known_paths):
            print ( "Data Model Category = " + path[1:] )

        if type(dm) == type({}):
            for k in dm.keys():
                v = dm[k]
                if type(v) == type({}):
                    self[k] = DataModelObject(v, path+"."+k)
                elif type(v) == type([]):
                    sub_list = []
                    self.fill_list(sub_list,v, path+"."+k)
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
                    l.append ( DataModelObject(item, path+'['+str(index)+']') )
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


dm_str = '{"iters":100, "init": {"warn":"off", "errlim":5 }, "mols": [ {"name":"a", "dc":1e-6 }, {"name":"b", "dc":2e-6 } ] }'

with open ( "moderate_model.json", "r" ) as f:
    dm_str = f.read()

dm = json.loads ( dm_str )

# print ( str(dm) )

dm = DataModelObject(dm,"")

print()
print ( "Source ID   = " + dm.mcell.cellblender_source_sha1 )
print ( "DM Version  = " + dm.mcell.data_model_version )
print ( "Iterations  = " + str(dm.mcell.initialization.iterations) )
print()
p = dm.mcell.initialization.partitions
print ( "Partitions:   x: %s to %s by %s,   y: %s to %s by %s,   z: %s to %s by %s" % (p.x_start, p.x_end, p.x_step, p.y_start, p.y_end, p.y_step, p.z_start, p.z_end, p.z_step, ) )
print()
ns = dm.mcell.initialization.notifications
print ( "Notifications:" )
for n in ns.keys():
    print ( "  " + n + ": " + str(ns[n]) )
print()
ws = dm.mcell.initialization.warnings
print ( "Warnings:" )
for w in ws.keys():
    print ( "  " + w + ": " + str(ws[w]) )
print()
print ( "Parameters:" )
for p in dm.mcell.parameter_system.model_parameters:
    print ( "  " + p.par_name + " = " + str(p.par_expression) )
print()
print ( "Molecules:" )
for m in dm.mcell.define_molecules.molecule_list:
    print ( "  " + m.mol_name + " is " + m.mol_type + " with diffusion_constant = " + str(m.diffusion_constant) )
print()
print ( "Objects:" )
for o in dm.mcell.geometrical_objects.object_list:
    print ( "  " + o.name + " has " + str(len(o.vertex_list)) + " points and " + str(len(o.element_connections)) + " faces" )
    if "define_surface_regions" in o.keys():
        print ( "    " + o.name + " contains " + str(len(o.define_surface_regions)) + " regions" )
print()
print ( "Surface Classes:" )
for s in dm.mcell.define_surface_classes.surface_class_list:
    print ( "  " + s.name + " has " + str(len(s.surface_class_prop_list)) + " property definitions" )
print()
print ( "Modify Surface Regions:" )
for s in dm.mcell.modify_surface_regions.modify_surface_regions_list:
    print ( "  " + s.name )
print()

# __import__('code').interact(local={k: v for ns in (globals(), locals()) for k, v in ns.items()})

