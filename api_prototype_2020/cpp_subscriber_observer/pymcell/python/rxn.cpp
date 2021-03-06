#include "../libmcell/include/libmcell_bits/rxn.hpp"

#include <pybind11/pybind11.h>
namespace py = pybind11;

// For STL containers
#include <pybind11/stl.h>

void init_rxn(py::module &m) {
        
    py::class_<mcl::Rxn>(m, "Rxn")
    .def(py::init<std::string, double, std::vector<std::string>, std::vector<std::string>>(), py::arg("name"), py::arg("fwd_rate"), py::arg("reactants"), py::arg("products"))
    .def("get_name", &mcl::Rxn::get_name)
    .def_property("fwd_rate", &mcl::Rxn::get_fwd_rate, &mcl::Rxn::set_fwd_rate);
    
}
