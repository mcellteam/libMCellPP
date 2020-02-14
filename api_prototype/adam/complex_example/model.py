# not a part of the model

# submodule is the same thing as a model (module?), 
# a model can be merged into another model

import mcell as m

class Model(): # corresponts to class World from C++ implementation
    def __init__(self):
        pass
    
    # does not add releases neither geometry
    def add_subsystem(self, s: m.Subsystem):
        # subsystem should provide some API where 
        # we can read out all the needed information
        # prefferably 
        pass
    
    def add_geometry(self, ):