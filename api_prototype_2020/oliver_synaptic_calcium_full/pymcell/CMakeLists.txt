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
	python/geometry.cpp
	python/model_geometry_ifce.hpp
	python/model_rxn_ifce.hpp
	python/model_species_ifce.hpp
	python/model.cpp 
	python/pymcell.cpp 
	python/result_timestep.cpp 
	python/rxn.cpp 
	python/species.cpp
	libmcell/src/geometry.cpp
	libmcell/src/model.cpp
	libmcell/src/result_timestep.cpp
	libmcell/src/rxn.cpp
	libmcell/src/species.cpp
	libmcell/include/libmcell_bits/geometry.hpp
	libmcell/include/libmcell_bits/model_geometry_ifce.hpp
	libmcell/include/libmcell_bits/model_rxn_ifce.hpp
	libmcell/include/libmcell_bits/model_species_ifce.hpp
	libmcell/include/libmcell_bits/model.hpp
	libmcell/include/libmcell_bits/result_timestep.hpp
	libmcell/include/libmcell_bits/rxn.hpp
	libmcell/include/libmcell_bits/species.hpp
)

install(TARGETS pymcell
  COMPONENT python
  LIBRARY DESTINATION "${PYTHON_LIBRARY_DIR}"
  )

