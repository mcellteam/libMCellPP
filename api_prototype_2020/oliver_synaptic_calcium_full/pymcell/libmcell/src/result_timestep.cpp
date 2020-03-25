//
//  result_timestep.cpp
//  libmcell
//
//  Created by Oliver Ernst on 2/23/20.
//

#include "result_timestep.hpp"

namespace mcl {

// ***************
// MARK: - Constructor
// ***************

ResultTimestep::ResultTimestep(bool success) {
    _success = success;
};
ResultTimestep::ResultTimestep(const ResultTimestep& other) {
    _copy(other);
};
ResultTimestep::ResultTimestep(ResultTimestep&& other) {
    _move(other);
};
ResultTimestep& ResultTimestep::operator=(const ResultTimestep& other) {
    if (this != &other) {
        _clean_up();
        _copy(other);
    };
    return *this;
};
ResultTimestep& ResultTimestep::operator=(ResultTimestep&& other) {
    if (this != &other) {
        _clean_up();
        _move(other);
    };
    return *this;
};
ResultTimestep::~ResultTimestep()
{
    _clean_up();
};
void ResultTimestep::_clean_up() {
    // ...
};
void ResultTimestep::_copy(const ResultTimestep& other) {
    _success = other._success;
};
void ResultTimestep::_move(ResultTimestep& other) {
    _success = other._success;
};

// ***************
// MARK: - Success
// ***************

bool ResultTimestep::get_success() const {
    return _success;
}


}
