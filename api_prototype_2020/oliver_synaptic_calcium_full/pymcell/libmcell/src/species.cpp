//
//  species.cpp
//  pymcell
//
//  Created by Oliver Ernst on 2/23/20.
//

#include "species.hpp"

namespace mcl {

// ***************
// MARK: - Constructor
// ***************

Species::Species(std::string name, double diff_const) {
    _name = name;
    _diff_const = diff_const;
};
Species::Species(const Species& other) {
    _copy(other);
};
Species::Species(Species&& other) {
    _move(other);
};
Species& Species::operator=(const Species& other) {
    if (this != &other) {
        _clean_up();
        _copy(other);
    };
    return *this;
};
Species& Species::operator=(Species&& other) {
    if (this != &other) {
        _clean_up();
        _move(other);
    };
    return *this;
};
Species::~Species()
{
    _clean_up();
};
void Species::_clean_up() {
    // Remove myself from models that are subscribed to me
    while (_subscribed_models.size() != 0) {
        (*_subscribed_models.begin())->remove_species(this);
    }
};
void Species::_copy(const Species& other) {
    // Do not copy _subscribed_models

    _name = other._name;
    _diff_const = other._diff_const;
};
void Species::_move(Species& other) {
    _subscribed_models = other._subscribed_models;
    
    // Remove the old rxn from all the subscribed models
    for (auto subscribed_model: _subscribed_models) {
        subscribed_model->remove_species(&other);
    }
    // Add the new rxn to all the subscribed models
    for (auto subscribed_model: _subscribed_models) {
        subscribed_model->add_species(this);
    }

    _name = other._name;
    _diff_const = other._diff_const;
    
    // Reset the other
    other._subscribed_models.clear();
};

// ***************
// MARK: - ModelPart implementations
// ***************

void Species::add_subscriber(ModelSpeciesIfce* model) {
    _subscribed_models.insert(model);
}
void Species::remove_subscriber(ModelSpeciesIfce* model) {
    _subscribed_models.erase(model);
}

// ***************
// MARK: - Name
// ***************

std::string Species::get_name() const {
    return _name;
}

// ***************
// MARK: - Diffusion constant
// ***************

double Species::get_diff_const() const {
    return _diff_const;
}
void Species::set_diff_const(double diff_const) {
    _diff_const = diff_const;
}

}
