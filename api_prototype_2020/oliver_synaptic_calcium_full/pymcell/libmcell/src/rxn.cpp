//
//  rxn.cpp
//  libmcell
//
//  Created by Oliver Ernst on 2/22/20.
//

#include "rxn.hpp"

namespace mcl {

// ***************
// MARK: - Constructor
// ***************

Rxn::Rxn(std::string name, double fwd_rate, std::vector<Species*> reactants, std::vector<Species*> products) {
    _name = name;
    _fwd_rate = fwd_rate;
    _bkwd_rate_exits = false;
    _bkwd_rate = 0.0;
    _reactants = reactants;
    _products = products;
};
Rxn::Rxn(std::string name, double fwd_rate, double bkwd_rate, std::vector<Species*> reactants, std::vector<Species*> products) {
    _name = name;
    _fwd_rate = fwd_rate;
    _bkwd_rate_exits = true;
    _bkwd_rate = bkwd_rate;
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
        (*_subscribed_models.begin())->remove_rxn(this);
    }
};
void Rxn::_copy(const Rxn& other) {
    // Do not copy _subscribed_models
    
    _name = other._name;
    _fwd_rate = other._fwd_rate;
    _bkwd_rate_exits = other._bkwd_rate_exits;
    _bkwd_rate = other._bkwd_rate;
    _reactants = other._reactants;
    _products = other._products;
};
void Rxn::_move(Rxn& other) {
    _subscribed_models = other._subscribed_models;
    
    // Remove the old rxn from all the subscribed models
    for (auto subscribed_model: _subscribed_models) {
        subscribed_model->remove_rxn(&other);
    }
    // Add the new rxn to all the subscribed models
    for (auto subscribed_model: _subscribed_models) {
        subscribed_model->add_rxn(this);
    }

    _name = other._name;
    _fwd_rate = other._fwd_rate;
    _bkwd_rate_exits = other._bkwd_rate_exits;
    _bkwd_rate = other._bkwd_rate;
    _reactants = other._reactants;
    _products = other._products;
    
    // Reset the other
    other._subscribed_models.clear();
    other._reactants.clear();
    other._products.clear();
};

// ***************
// MARK: - ModelPart implementations
// ***************

void Rxn::add_subscriber(ModelRxnIfce* model) {
    _subscribed_models.insert(model);
}
void Rxn::remove_subscriber(ModelRxnIfce* model) {
    _subscribed_models.erase(model);
}

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
    
    for (auto subscribed_model: _subscribed_models) {
        subscribed_model->notify_fwd_rate_changed(this, _fwd_rate);
    }
}

bool Rxn::check_bkwd_rate_exists() const {
    return _bkwd_rate_exits;
}
double Rxn::get_bkwd_rate() const {
    if (_bkwd_rate_exits) {
        return _bkwd_rate;
    } else {
        return 0.0;
    }
}
void Rxn::set_bkwd_rate(double bkwd_rate) {
    _bkwd_rate = bkwd_rate;
    
    for (auto subscribed_model: _subscribed_models) {
        subscribed_model->notify_bkwd_rate_changed(this, _bkwd_rate);
    }
}

// ***************
// MARK: - Reactants and products
// ***************

std::vector<Species*> Rxn::get_reactants() const {
    return _reactants;
}
std::vector<Species*> Rxn::get_products() const {
    return _products;
}

}
