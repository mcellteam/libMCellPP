#ifndef model_rxn_ifce_hpp
#define model_rxn_ifce_hpp

#include "../libmcell/include/libmcell_bits/model_rxn_ifce.hpp"

#endif

#include <pybind11/pybind11.h>

// Subclassing abstract base class explained here:
// https://pybind11.readthedocs.io/en/stable/advanced/classes.html

namespace mcl {

class PyModelRxnIfce : public ModelRxnIfce {
public:
    /* Inherit the constructors */
    using ModelRxnIfce::ModelRxnIfce;

    void remove_rxn(Rxn* rxn) override {
        PYBIND11_OVERLOAD_PURE(
            void, /* Return type */
            ModelRxnIfce,      /* Parent class */
            remove_rxn,          /* Name of function in C++ (must match Python name) */
            rxn      /* Argument(s) */
        );
    }
    void notify_fwd_rate_changed(Rxn* rxn, double fwd_rate) override {
        PYBIND11_OVERLOAD_PURE(
            void, /* Return type */
            ModelRxnIfce,      /* Parent class */
            notify_fwd_rate_changed,          /* Name of function in C++ (must match Python name) */
            rxn, fwd_rate      /* Argument(s) */
        );
    }
};

}
