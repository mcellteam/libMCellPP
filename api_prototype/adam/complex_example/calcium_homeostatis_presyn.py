# this is one of possibly many submodules
# that implements the calcium homeostatsis presynaptic subsystem

import mcell as m

class CalciumHomeostasisPresyn(m.Subsystem): 
    def __init__(self):
        # load BNGL files and 
        
        # load information from MDL and add it to the existing information
        # information conflicts are detected and reported as errors 
        # e.g. species defined twice with the same name but with different diffusion constants
        #
        # everything that is included in 'instantiate geometry' and in 'instantiate releases' 
        # is stored in instantiation_data
        model.load_pmdl('calcium_homeostatis_presyn.bngl')
    
    # this is a little weird,
    # how to name these methods? -> they insert information into the World class, 
    # add... seems that we are adding information into this class
    
    # add information from submodule into the model
    def add_molecules_and_pathways(self, model: m.World):
        pass
    
    # returns information about releases that can be then programatically 
    # analyzed and applied onto the actual geometry
    def get_release_info(self) -> List[ReleaseInfo]:
        pass
    
    # add geometry and releases
    def add_reference_setup(self, model: m.World):
        pass