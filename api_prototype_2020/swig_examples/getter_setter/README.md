# Example of how to wrap setters/getters in Swig 4

Make sure you get the latest SWIG 4.

## Contents

* `example.hpp` and `example.cpp` is the C++ code.
* `example.i` is the interface.
* `setup.py` is the distutils setup script.
* `test.py` is a test.

## Running

To run, first build:
```
python setup.py build_ext --inplace
```

`distutils` knows about SWIG now so that saves some `g++` calls and digging up the where all your Python headers live.

It will generate a build directory, the SWIG wrapped C++ code `example_wrap.cpp`, as well as the `example.py` garbage illegible header and the `_example.cpython-37m-darwin.so` shared library (or something similar if you are on another distro).

To test, run:
```
python test.py
```
as usual.

The interface file `example.i` should be broadly self-explainable. The apparent duplication of code is explained [here](https://stackoverflow.com/questions/32208350/swig-why-we-need-to-declare-functions-twice) - in short, only the methods you declare explicitly at the bottom are exposed in Python.
