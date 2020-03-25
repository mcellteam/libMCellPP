#include <string>

class Animal {
public:
    virtual ~Animal() { }
    virtual std::string go(int n_times) = 0;
};

class Dog : public Animal {
public:
    std::string go(int n_times) override {
        std::string result;
        for (int i=0; i<n_times; ++i)
            result += "woof! ";
        return result;
    }
};

#include <pybind11/pybind11.h>

class PyAnimal : public Animal {
public:
    /* Inherit the constructors */
    using Animal::Animal;

    /* Trampoline (need one for each virtual function) */
    std::string go(int n_times) override {
        PYBIND11_OVERLOAD_PURE(
            std::string, /* Return type */
            Animal,      /* Parent class */
            go,          /* Name of function in C++ (must match Python name) */
            n_times      /* Argument(s) */
        );
    }
};

namespace py = pybind11;

namespace mcl {

  PYBIND11_MODULE(pybind11_test_virtual, m) {
      py::class_<Animal, PyAnimal /* <--- trampoline*/>(m, "Animal")
          // .def(py::init<>()) // Do not put a constructor! It's an abstract base class
          .def("go", &Animal::go);

      py::class_<Dog, Animal>(m, "Dog")
          .def(py::init<>());
  }
}
