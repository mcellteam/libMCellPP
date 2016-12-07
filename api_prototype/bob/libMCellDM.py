# import libMCell as m

import json

class DataModelObject(dict):

    def __init__(self, dm):
        if type(dm) == type({}):
          for k in dm.keys():
            v = dm[k]
            if type(v) == type({}):
              self[k] = DataModelObject(v)
            elif type(v) == type([]):
              sub_list = []
              self.fill_list(sub_list,v)
              self[k] = sub_list
            else:
              self[k] = dm[k]
        else:
          raise AttributeError("Dictionary required rather than " + str(type(dm)))

    def fill_list(self, l, dm):
        if type(dm) == type([]):
          for item in dm:
            if type(item) == type({}):
              l.append ( DataModelObject(item) )
            elif type(item) == type([]):
              sub_list = []
              self.fill_list(sub_list,item)
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

print ( str(dm) )

dm = DataModelObject(dm)

print()
print ( "Iterations  = " + str(dm.mcell.initialization.iterations) )
print ( "Warnings    = " + str(dm.mcell.initialization.warnings) )
print()
print ( "Parameters:" )
for p in dm.mcell.parameter_system.model_parameters:
    print ( "  " + p.par_name + " = " + str(p.par_expression) )
print()
print ( "Molecules:" )
for m in dm.mcell.define_molecules.molecule_list:
    print ( "  " + m.mol_name + ": diffusion_constant = " + str(m.diffusion_constant) )
print()
print ( "Objects:" )
for o in dm.mcell.geometrical_objects.object_list:
    print ( "  " + o.name + " has " + str(len(o.vertex_list)) + " points and " + str(len(o.element_connections)) + " faces" )
print()
print ( "Surface Classes:" )
for s in dm.mcell.define_surface_classes.surface_class_list:
    print ( "  " + s.name + " has " + str(len(s.surface_class_prop_list)) + " property definitions" )
print()

# __import__('code').interact(local={k: v for ns in (globals(), locals()) for k, v in ns.items()})

