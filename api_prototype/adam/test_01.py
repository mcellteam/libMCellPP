import mcell as m


def main():
    iterations = 1000
    
    # create a new instance of MCell World with optional instance name 
    model = m.create('my_only_model')
    
    # load information from MDL and add it to the existing information
    # information conflicts are detected and reported as errors 
    # e.g. species defined twice with the same name but with different diffusion constants
    model.load_pmdl('test_01.pmdl')

    # do we need initialization? run can check it automatically, but 
    # are there other cases? maybe we can just check initialization every time it is needed
    # so far - not needed
    #  model.initialize()
    
    # run the simulation for a given number of iterations (no
    model.run(iterations)

if __name__ == "__main__":
    main()