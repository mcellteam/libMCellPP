//
//  rxn.cpp
//  libmcell
//
//  Created by Oliver Ernst on 2/22/20.
//

#include "rxn.hpp"
#include <iostream>

namespace mcl {

// ***************
// MARK: - Constructor
// ***************

Rxn::Rxn(std::string name, double fwd_rate, std::vector<std::string> reactants, std::vector<std::string> products) {
    _name = name;
    _fwd_rate = fwd_rate;
    _reactants = reactants;
    _products = products;
};
Rxn::Rxn(const Rxn& other) {
    _copy(other);
};
Rxn::Rxn(Rxn&& other) {
    _move(other);
};
Rxn& Rxn::operator=(const Rxn& other) {
    if (this != &other) {
        _clean_up();
        _copy(other);
    };
    return *this;
};
Rxn& Rxn::operator=(Rxn&& other) {
    if (this != &other) {
        _clean_up();
        _move(other);
    };
    return *this;
};
Rxn::~Rxn()
{
    _clean_up();
};
void Rxn::_clean_up() {
    // Remove myself from models that are subscribed to me
    while (_subscribed_models.size() != 0) {
         (*_subscribed_models.begin())->remove_rxn(this); // this calls remove_subscriber
    }
};
void Rxn::_copy(const Rxn& other) {
    _name = other._name;
    _fwd_rate = other._fwd_rate;
    _reactants = other._reactants;
    _products = other._products;
};
void Rxn::_move(Rxn& other) {
    _name = other._name;
    _fwd_rate = other._fwd_rate;
    _reactants = other._reactants;
    _products = other._products;
    
    // Reset the other
    other._reactants.clear();
    other._products.clear();
};

// ***************
// MARK: - Name
// ***************

std::string Rxn::get_name() const {
    return _name;
}

// ***************
// MARK: - Forward rate
// ***************

double Rxn::get_fwd_rate() const {
    return _fwd_rate;
}
void Rxn::set_fwd_rate(double fwd_rate) {
    _fwd_rate = fwd_rate;
    
    for (auto const &subscribed_model: _subscribed_models) {
        subscribed_model->notify_fwd_rate_changed(this, _fwd_rate);
    }
}

// ***************
// MARK: - ModelPart implementations
// ***************

void Rxn::add_subscriber(ModelRxnIfce* model) {
    _subscribed_models.insert(model);
}
void Rxn::remove_subscriber(ModelRxnIfce* model) {
    _subscribed_models.erase(model);
}

}
