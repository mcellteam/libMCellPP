//
//  geometry.cpp
//  pymcell
//
//  Created by Oliver Ernst on 2/23/20.
//

#include "geometry.hpp"

namespace mcl {

// ***************
// MARK: - Constructor
// ***************

Geometry::Geometry(std::string filename) {};
Geometry::Geometry(const Geometry& other) {
    _copy(other);
};
Geometry::Geometry(Geometry&& other) {
    _move(other);
};
Geometry& Geometry::operator=(const Geometry& other) {
    if (this != &other) {
        _clean_up();
        _copy(other);
    };
    return *this;
};
Geometry& Geometry::operator=(Geometry&& other) {
    if (this != &other) {
        _clean_up();
        _move(other);
    };
    return *this;
};
Geometry::~Geometry()
{
    _clean_up();
};
void Geometry::_clean_up() {
    // Remove myself from models that are subscribed to me
    while (_subscribed_models.size() != 0) {
        (*_subscribed_models.begin())->remove_geometry(this);
    }
};
void Geometry::_copy(const Geometry& other) {
    // Do not copy _subscribed_models
};
void Geometry::_move(Geometry& other) {
    _subscribed_models = other._subscribed_models;
    
    // Remove the old Geometry from all the subscribed models
    for (auto subscribed_model: _subscribed_models) {
        subscribed_model->remove_geometry(&other);
    }
    // Add the new Geometry to all the subscribed models
    for (auto subscribed_model: _subscribed_models) {
        subscribed_model->add_geometry(this);
    }
    
    // Reset the other
    other._subscribed_models.clear();
};

// ***************
// MARK: - ModelPart implementations
// ***************

void Geometry::add_subscriber(ModelGeometryIfce* model) {
    _subscribed_models.insert(model);
}
void Geometry::remove_subscriber(ModelGeometryIfce* model) {
    _subscribed_models.erase(model);
}

}
