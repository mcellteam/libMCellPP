ONLY_CHP1 = True

def main():
    iterations = 1000

    model = m.create_empty_model()

    # load an initialize all submodules
    chp1 = calcium_homeostatis_presyn1()
    chp2 = calcium_homeostatis_presyn2()
    chp3 = calcium_homeostatis_presyn3()
    
    if ONLY_CHP1:
        
        # only pathways and molecule types
        model.include_submodule(chp1)
        
        # subsystems do not load their geometry or release info, they only contain information 
        # on where to find it + extra code that might generate it
        model.load_geometry(chp1.default_geometry)
        model.load_releases(chp1.default_releases)
        
        model.run(iterations) 
        
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
        model.include_submodules([chp1, chp2, chp2])
        
        # load information from MDL and add it to the existing information
        # information conflicts are detected and reported as errors 
        # e.g. species defined twice with the same name but with different diffusion constants
        model.load_pmdl('model_geometry.bngl')

        # load releases from a bngl file, this that assumes 
        # we already know all the species in the model
        # model.load_pmdl('model_releases.bngl')
        model.load_pmdl('model_releases.bngl')
        

        # generate releases
        # somehow use info from submodule and from geometry information and determine where 
        # should molecules appear
        # -> we can keep this for later
        #model.generate_releases_for_all_submodules() # [chp, ...] 
    
        # do we need initialization? run can check it automatically, but 
        # are there other cases? maybe we can just check initialization every time it is needed
        # so far - not needed
        #  model.initialize()
        
        # run the simulation for a given number of iterations (no
        model.run(iterations)

if __name__ == "__main__":
    main()