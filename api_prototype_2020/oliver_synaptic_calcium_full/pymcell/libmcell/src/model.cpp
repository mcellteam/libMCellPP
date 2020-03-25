//
//  model.cpp
//  libmcell
//
//  Created by Oliver Ernst on 2/22/20.
//

#include "model.hpp"
#include <iostream>
#include <exception>

namespace mcl {

// ***************
// MARK: - Constructor
// ***************

Model::Model(double dt) {
    _dt = dt;
    _timepoint = 0;
};
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
    // Remove all subscribed...
    for (auto rxn: _rxns) {
        rxn->remove_subscriber(this);
    }
    for (auto species: _species) {
        species->remove_subscriber(this);
    }
    for (auto geometry: _geometries) {
        geometry->remove_subscriber(this);
    }
};
void Model::_copy(const Model& other) {
    _dt = other._dt;
    _timepoint = other._timepoint;
    _rxns = other._rxns;
    _species = other._species;
    _geometries = other._geometries;
    
    // Also need to tell those rxns/species/geometries of this new subscriber
    for (auto rxn: _rxns) {
        rxn->add_subscriber(this);
    }
    for (auto species: _species) {
        species->add_subscriber(this);
    }
    for (auto geometry: _geometries) {
        geometry->add_subscriber(this);
    }
};
void Model::_move(Model& other) {
    _dt = other._dt;
    _timepoint = other._timepoint;
    _rxns = other._rxns;
    _species = other._species;
    _geometries = other._geometries;

    // Switch over the pointers
    for (auto rxn: _rxns) {
        rxn->remove_subscriber(&other);
        rxn->add_subscriber(this);
    }
    for (auto species: _species) {
        species->remove_subscriber(this);
        species->add_subscriber(this);
    }
    for (auto geometry: _geometries) {
        geometry->remove_subscriber(this);
        geometry->add_subscriber(this);
    }

    // Reset the other
    other._rxns.clear();
    other._species.clear();
    other._geometries.clear();
};

// ***************
// MARK: - Run timestep
// ***************

ResultTimestep Model::run_timestep() {
    std::cout << "!!! Running a timestep from timepoint " << _timepoint << " to: " << _timepoint+1 << std::endl;
    
    // Increment timepoint
    _timepoint++;
    
    // Return success
    return ResultTimestep(true);
}

// ***************
// MARK: - Timestep
// ***************

int Model::get_timepoint() const {
    return _timepoint;
}
void Model::set_timepoint(int timepoint) {
    _timepoint = timepoint;
}

double Model::get_dt() const {
    return _dt;
}
void Model::set_dt(double dt) {
    _dt = dt;
}

// ***************
// MARK: - Species
// ***************

void Model::add_species(Species* species) {
    _species.insert(species);
    
    // Subscriber
    species->add_subscriber(this);
}
void Model::remove_species(Species* species) {
    _species.erase(species);

    // Subscriber
    species->remove_subscriber(this);
}

// ***************
// MARK: - Reactions
// ***************

void Model::add_rxn(Rxn* rxn) {
    // Check all species exist
    for (auto sp: rxn->get_reactants()) {
        if (_species.count(sp) == 0) {
            throw std::invalid_argument("All species in the reaction must be added.");
        }
    }
    for (auto sp: rxn->get_products()) {
        if (_species.count(sp) == 0) {
            throw std::invalid_argument("All species in the reaction must be added.");
        }
    }

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
// MARK: - Geometry
// ***************

void Model::add_geometry(Geometry *geometry) {
    _geometries.insert(geometry);
    
    // Subscriber
    geometry->add_subscriber(this);
}
void Model::remove_geometry(Geometry *geometry) {
    _geometries.erase(geometry);

    // Subscriber
    geometry->remove_subscriber(this);
}

// ***************
// MARK: - ModelRxnIfce implementations
// ***************

void Model::notify_fwd_rate_changed(Rxn* rxn, double fwd_rate) {
    std::cout << "!!! The model has been notified that the fwd rxn rate for rxn: " << rxn->get_name() << " has been changed to: " << fwd_rate << std::endl;
}

void Model::notify_bkwd_rate_changed(Rxn* rxn, double bkwd_rate) {
    std::cout << "!!! The model has been notified that the bkwd rxn rate for rxn: " << rxn->get_name() << " has been changed to: " << bkwd_rate << std::endl;
}

// ***************
// MARK: - ModelSpeciesIfce implementations
// ***************

void Model::notify_diff_const_changed(Species* species, double diff_const) {
    std::cout << "!!! The model has been notified that the diff const for species: " << species->get_name() << " has been changed to: " << diff_const << std::endl;
}

}
