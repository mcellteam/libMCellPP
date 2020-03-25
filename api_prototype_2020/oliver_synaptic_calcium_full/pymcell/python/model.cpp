#include "../libmcell/include/libmcell_bits/model.hpp"

#include <pybind11/pybind11.h>
namespace py = pybind11;

// For STL containers
#include <pybind11/stl.h>

void init_model(py::module &m) {
    
    py::class_<mcl::Model, mcl::ModelRxnIfce, mcl::ModelSpeciesIfce>(m, "Model")
    .def(py::init<double>())
    .def("run_timestep", &mcl::Model::run_timestep)
    .def_property("timepoint", &mcl::Model::get_timepoint, &mcl::Model::set_timepoint)
    .def_property("dt", &mcl::Model::get_dt, &mcl::Model::set_dt)
    .def("add_species", &mcl::Model::add_species)
    .def("remove_species", &mcl::Model::remove_species)
    .def("add_rxn", &mcl::Model::add_rxn)
    .def("remove_rxn", &mcl::Model::remove_rxn)
    .def("notify_fwd_rate_changed", &mcl::Model::notify_fwd_rate_changed)
    .def("notify_bkwd_rate_changed", &mcl::Model::notify_bkwd_rate_changed)
    .def("notify_diff_const_changed", &mcl::Model::notify_diff_const_changed);
}
