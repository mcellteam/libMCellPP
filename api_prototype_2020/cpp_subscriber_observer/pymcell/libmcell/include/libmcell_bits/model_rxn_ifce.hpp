//
//  model_rxn_ifce.hpp
//  libmcell
//
//  Created by Oliver Ernst on 2/22/20.
//

#ifndef model_rxn_ifce_hpp
#define model_rxn_ifce_hpp

#include <stdio.h>

#endif /* model_rxn_ifce_hpp */

namespace mcl {

class Rxn;

class ModelRxnIfce {
public:
    virtual void remove_rxn(Rxn* rxn) = 0;
    virtual void notify_fwd_rate_changed(Rxn* rxn, double fwd_rate) = 0;
    
    // Virtual destructor
    virtual ~ModelRxnIfce() {}; // Must have implementation! Else pybind11 is lost.
};

}
