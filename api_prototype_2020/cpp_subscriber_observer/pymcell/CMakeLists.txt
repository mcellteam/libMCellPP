cmake_minimum_required(VERSION 3.1)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

set(CMAKE_CXX_FLAGS "-O3")
set(CMAKE_CXX_FLAGS_RELEASE "-O3")

project(pymcell)

include_directories("${CMAKE_SOURCE_DIR}/libmcell/include/libmcell_bits")

find_package(pybind11 REQUIRED)
pybind11_add_module(pymcell 
	python/pymcell.cpp 
	python/rxn.cpp 
	python/model.cpp 
	python/model_rxn_ifce.hpp
	libmcell/include/libmcell_bits/rxn.hpp 
	libmcell/include/libmcell_bits/model.hpp 
	libmcell/include/libmcell_bits/model_rxn_ifce.hpp 
	libmcell/src/rxn.cpp 
	libmcell/src/model.cpp
)

install(TARGETS pymcell
  COMPONENT python
  LIBRARY DESTINATION "${PYTHON_LIBRARY_DIR}"
  )
