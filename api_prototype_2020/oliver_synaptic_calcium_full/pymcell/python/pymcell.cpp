#include <pybind11/pybind11.h>

namespace py = pybind11;

void init_rxn(py::module &);
void init_model(py::module &);
void init_species(py::module &);

namespace mcl {

PYBIND11_MODULE(pymcell, m) {
    // Optional docstring
    m.doc() = "Example of subscriber/observer pattern";
    
    init_species(m);
    init_rxn(m);
    init_model(m);
}
}
