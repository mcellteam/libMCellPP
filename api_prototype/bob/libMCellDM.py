# import libMCell as m

import json

class DataModelObject(dict):

    def __init__(self, dm):
        print ( "init" )
        for k in dm.keys():
          v = dm[k]
          if type(v) == type({}):
            self[k] = DataModelObject(v)
          elif type(v) == type([]):
            l = []
            for item in v:
              l.append ( DataModelObject(item) )
            self[k] = l
          else:
            self[k] = dm[k]

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


dm = json.loads ( '{"iters":100, "init": {"warn":"off", "errlim":5 }, "mols": [ {"name":"a", "dc":1e-6 }, {"name":"b", "dc":2e-6 } ] }' )

print ( str(dm) )

dm = DataModelObject(dm)

print()

print ( "Iterations  = " + str(dm.iters) )
print ( "Warnings    = " + str(dm.init.warn) )
print ( "Error Limit = " + str(dm.init.errlim) )
print ( "Molecules:" )
for m in dm.mols:
    print ( "  " + m.name + ".dc = " + str(m.dc) )

print()

__import__('code').interact(local={k: v for ns in (globals(), locals()) for k, v in ns.items()})

