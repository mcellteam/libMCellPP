#include "../libmcell/include/libmcell_bits/species.hpp"

#include <pybind11/pybind11.h>
namespace py = pybind11;

// For STL containers
#include <pybind11/stl.h>

void init_species(py::module &m) {
    
    py::class_<mcl::Species>(m, "Species")
    .def(py::init<std::string, double>())
    .def("get_name", &mcl::Species::get_name);
}
