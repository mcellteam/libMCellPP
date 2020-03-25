# Example of subscriber/observer pattern: C++ library and wrapped into Python via pybind11

## Contents

* [pymcell](pymcell): source for both the C++ library `libmcell` and the Python library `pymcell`. `libmcell` is nested inside `pymcell`.
* [example_cpp](example_cpp): an example in C++.
* [example_python](example_python): an example in Python.

## Building

First, get `pybind11`. [Here](https://pybind11.readthedocs.io/en/stable/compiling.html) are some docs.

Make sure you use `conda` to install `pybind11`. `pip` may lead to problems with `cmake` (`pybind11Config.cmake` is not installed).
```
conda install pybind11
```

### C++ (libmcell)

Navigate to [pymcell/libmcell](pymcell/libmcell). Then:
```
mkdir build
cd build
cmake ..
make
make install
```

### Python (pymcell)

Navigate to [pymcell](pymcell). Then:
```
mkdir build
cd build
cmake .. -DPYTHON_LIBRARY_DIR=/Users/oernst/opt/anaconda3/lib/python3.7/site-packages # Or wherever your site packages directory resides
make
make install
```

## Testing

### C++ (libmcell)

Navigate to [example_cpp](example_cpp). Build:
```
mkdir build
cd build
cmake ..
make
```
Then navigate to `example_cpp/bin` and fire up:
```
./example
```
You should see the callback message:
```
>>> The model has been notified that the fwd rxn rate for rxn: my rxn has been changed to: 3
```

### Python (libmcell)

Navigate to [example_python](example_python). Fire up:
```
python test.py
```
You should see the callback message:
```
>>> The model has been notified that the fwd rxn rate for rxn: my rxn has been changed to: 3
```

## Supplemental info on pybind11

A typical command with `pybind11` might look like the following:
```
c++ -O3 -Wall -shared -std=c++11 -fPIC `python3 -m pybind11 --includes` pymcell.cpp -o example`python3-config --extension-suffix` -undefined dynamic_lookup
```
BUT: we don't care, since we can use `cmake`.

I found the final `-undefined dynamic_lookup` to be required on Mac OS X.
