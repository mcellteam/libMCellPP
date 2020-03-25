//
//  model.cpp
//  libmcell
//
//  Created by Oliver Ernst on 2/22/20.
//

#include "model.hpp"
#include <iostream>

namespace mcl {

// ***************
// MARK: - Constructor
// ***************

Model::Model() {};
Model::Model(const Model& other) {
    _copy(other);
};
Model::Model(Model&& other) {
    _move(other);
};
Model& Model::operator=(const Model& other) {
    if (this != &other) {
        _clean_up();
        _copy(other);
    };
    return *this;
};
Model& Model::operator=(Model&& other) {
    if (this != &other) {
        _clean_up();
        _move(other);
    };
    return *this;
};
Model::~Model()
{
    _clean_up();
};
void Model::_clean_up() {
    // Remove all subscribed rxns
    for (auto const &rxn: _rxns) {
        rxn->remove_subscriber(this);
    }
};
void Model::_copy(const Model& other) {
    _rxns = other._rxns;
};
void Model::_move(Model& other) {
    _rxns = other._rxns;

    // Reset the other
    other._rxns.clear();
};

// ***************
// MARK: - Reactions
// ***************

void Model::add_rxn(Rxn* rxn) {
    _rxns.insert(rxn);

    // Subscriber
    rxn->add_subscriber(this);
}
void Model::remove_rxn(Rxn* rxn) {
    _rxns.erase(rxn);

    // Subscriber
    rxn->remove_subscriber(this);
}

// ***************
// MARK: - ModelRxnIfce implementations
// ***************

void Model::notify_fwd_rate_changed(Rxn* rxn, double fwd_rate) {
    std::cout << "!!! The model has been notified that the fwd rxn rate for rxn: " << rxn->get_name() << " has been changed to: " << fwd_rate << std::endl;
}

}
