//
//  geometry.hpp
//  pymcell
//
//  Created by Oliver Ernst on 2/23/20.
//

#ifndef geometry_hpp
#define geometry_hpp

#include <stdio.h>
#include <string>
#include <set>
#include "model_geometry_ifce.hpp"

#endif /* geometry_hpp */

namespace mcl {

class Geometry {
    
private:
    
    // Subscribed models
    std::set<ModelGeometryIfce*> _subscribed_models;
    
    // Internal copy func/clean up
    void _clean_up();
    void _copy(const Geometry& other);
    void _move(Geometry &other);
    
public:
            
    // ***************
    // MARK: - Constructor
    // ***************
    
    Geometry(std::string filename);
    Geometry(const Geometry& other);
    Geometry& operator=(const Geometry& other);
    Geometry(Geometry&& other);
    Geometry& operator=(Geometry&& other);
    ~Geometry();
    
    // ***************
    // MARK: - Add/remove subscribers
    // ***************
    
    void add_subscriber(ModelGeometryIfce* model);
    void remove_subscriber(ModelGeometryIfce* model);
    
};

}
