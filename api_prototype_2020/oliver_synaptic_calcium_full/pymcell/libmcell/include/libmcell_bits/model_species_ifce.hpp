//
//  model_species_ifce.hpp
//  libmcell
//
//  Created by Oliver Ernst on 2/22/20.
//

#ifndef model_species_ifce_hpp
#define model_species_ifce_hpp

#include <stdio.h>

#endif /* model_species_ifce_hpp */

namespace mcl {

class Species;

class ModelSpeciesIfce {
public:
    virtual void add_species(Species* rxn) = 0;
    virtual void remove_species(Species* rxn) = 0;
    virtual void notify_diff_const_changed(Species* species, double diff_const) = 0;
    
    // Virtual destructor
    virtual ~ModelSpeciesIfce() {}; // This must have an implementation, else pybind11 complains!
};

}
