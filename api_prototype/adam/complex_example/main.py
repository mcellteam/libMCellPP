ONLY_CHP = True

def main():
    iterations = 1000

    # load an initialize all submodules
    chp = calcium_homeostatis_presyn()
    # ... other submodules
    
    if ONLY_CHP:
        # run method uses default geometry and releases
        chp.run(iterations) 
        
        # for validation, there are diverse model export methods
        # chp.export_to_...?
        # 
        # later, a library will be available to do validation
        
    else:
        # create a new instance of MCell World with optional instance name 
        model = m.create_empty_model() # world? module?
        
        # add all information about reactions and molecule types (species?)
        # and whatever else might be needed, but not geometry neither releases
        # includes also counts?
        # what about diverse triggers? -> handled by submodule code?
        #   -> how doe we get to that information?
        model.include_submodule(chp)
        
        # load information from MDL and add it to the existing information
        # information conflicts are detected and reported as errors 
        # e.g. species defined twice with the same name but with different diffusion constants
        model.load_pmdl('model_geometry.bngl')

        # generate releases
        # somehow use info from submodule and from geometry information and determine where 
        # should molecules appear
        model.generate_releases_for_all_submodules() # [chp, ...] 
        
        # it is also possible to load thid information from a bngl file, but that assumes 
        # we already know all the species 
        # model.load_pmdl('model_releases.bngl')
    
        # do we need initialization? run can check it automatically, but 
        # are there other cases? maybe we can just check initialization every time it is needed
        # so far - not needed
        #  model.initialize()
        
        # run the simulation for a given number of iterations (no
        model.run(iterations)

if __name__ == "__main__":
    main()