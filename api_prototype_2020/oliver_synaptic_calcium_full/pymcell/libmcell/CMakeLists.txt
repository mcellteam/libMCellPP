cmake_minimum_required(VERSION 3.1)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

set(CMAKE_CXX_FLAGS "-O3")
set(CMAKE_CXX_FLAGS_RELEASE "-O3")

project(libmcell)

include_directories(/usr/local/include)

AUX_SOURCE_DIRECTORY(src SRC_FILES)

file (GLOB HEADER_FILES "include/libmcell_bits/*.hpp")
file (GLOB HEADER_FILES_FWDS "include/libmcell_bits/fwds/*.hpp")

add_library(libmcell SHARED
	src/geometry.cpp
	src/model.cpp
	src/result_timestep.cpp
	src/rxn.cpp
	src/species.cpp
	include/libmcell_bits/geometry.hpp
	include/libmcell_bits/model_geometry_ifce.hpp
	include/libmcell_bits/model_rxn_ifce.hpp
	include/libmcell_bits/model_species_ifce.hpp
	include/libmcell_bits/model.hpp
	include/libmcell_bits/result_timestep.hpp
	include/libmcell_bits/rxn.hpp
	include/libmcell_bits/species.hpp
	${HEADER_FILES_FWDS}
)

target_include_directories(libmcell PRIVATE include/libmcell_bits include/libmcell_bits/fwds)

install(TARGETS libmcell DESTINATION lib)

install(FILES
	include/libmcell
	DESTINATION include)

install(DIRECTORY
	include/libmcell_bits
	DESTINATION include)