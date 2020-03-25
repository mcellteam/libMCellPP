//
//  model_geometry_ifce.hpp
//  libmcell
//
//  Created by Oliver Ernst on 2/22/20.
//

#ifndef model_geometry_ifce_hpp
#define model_geometry_ifce_hpp

#include <stdio.h>

#endif /* model_geometry_ifce_hpp */

namespace mcl {

class Geometry;

class ModelGeometryIfce {
public:
    virtual void add_geometry(Geometry* rxn) = 0;
    virtual void remove_geometry(Geometry* rxn) = 0;
    
    // Virtual destructor
    virtual ~ModelGeometryIfce() {}; // This must have an implementation, else pybind11 complains!
};

}
