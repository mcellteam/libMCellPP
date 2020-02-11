import mcell as m


def main():
    iterations = 1000
    
    # create a new instance of MCell World with optional instance name 
    model = m.create('my_only_model') 
    
    # load information from MDL and add it to the existing information
    # information conflicts are detected and reported as errors 
    # e.g. species defined twice with the same name but with different diffusion constants
    model.load_mdl('test_01.mdl')
    
    # run the simulation for a given number of iterations
    model.run_iterations(iterations)

if __name__ == "__main__":
    main()