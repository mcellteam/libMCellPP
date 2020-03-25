#include "../libmcell/include/libmcell_bits/model.hpp"
#include "model_rxn_ifce.hpp"

#include <pybind11/pybind11.h>
namespace py = pybind11;

// For STL containers
#include <pybind11/stl.h>

// Subclassing abstract base class explained here:
// https://pybind11.readthedocs.io/en/stable/advanced/classes.html

void init_model(py::module &m) {
    
    py::class_<mcl::ModelRxnIfce, mcl::PyModelRxnIfce>(m, "ModelRxnIfce")
    // .def(py::init<>()) // No constructor! It's ABC!
    .def("remove_rxn", &mcl::ModelRxnIfce::remove_rxn)
    .def("notify_fwd_rate_changed", &mcl::ModelRxnIfce::notify_fwd_rate_changed);

    py::class_<mcl::Model, mcl::ModelRxnIfce>(m, "Model")
    .def(py::init<>())
    .def("add_rxn", &mcl::Model::add_rxn)
    .def("remove_rxn", &mcl::Model::remove_rxn)
    .def("notify_fwd_rate_changed", &mcl::Model::notify_fwd_rate_changed);
    
}
