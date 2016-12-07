# Traditional Version

import libMCell

my_sim = libMCell.create_simulation()
my_sim.create_molecule_species(name='red', dc='1e-5', color=[1,0,0])
my_sim.create_release_site(my_sim['data_model']['define_molecules']['molecule_list'][0], 100)
my_sim.run_simulation(1000)

