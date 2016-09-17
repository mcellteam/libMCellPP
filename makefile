PYTHON_INCLUDE = /usr/include/python3.4m

# Linux:
INSTALL_DIR = ~/.config/blender/2.77/scripts/addons/

# Mac:
#INSTALL_DIR = ~/Library/Application\ Support/Blender/2.74/scripts/addons/


all: libMCell.a libMCell.so _libMCell.so mcell_main mcell_main_c mcell_simple mcell_simple_count


# Library for static linking
libMCell.a: libMCell.o rng.o JSON.o makefile
	ar rcs libMCell.a libMCell.o rng.o JSON.o

# Library for dynamic linking
libMCell.so: libMCell.o rng.o JSON.o makefile
	g++ -o libMCell.so -shared -fPIC libMCell.a

# Library for Python
_libMCell.so: libMCell.cpp rng.cpp libMCell.h rng.h libMCell.i makefile
	swig -python -c++ -o libMCell_wrap.cpp libMCell.i
	g++ -c -std=c++11 -Wno-write-strings -fpic -I. -I/usr/include libMCell_wrap.cpp rng.cpp libMCell.cpp -I/usr/include/python2.7 -I/usr/lib/python2.7/config
	g++ -o _libMCell.so -shared -I/usr/include rng.o libMCell.o libMCell_wrap.o

# Library object module itself
libMCell.o: libMCell.cpp libMCell.h makefile
	g++ -o libMCell.o -c -std=c++11 -fpic -Wno-write-strings libMCell.cpp

# Library object module to read a JSON Data Model
JSON.o: JSON.c JSON.h makefile
	gcc -o JSON.o -c JSON.c -fpic -I$(PYTHON_INCLUDE)

# Library object module for MCell Random Number Generation
rng.o: rng.cpp rng.h makefile
	g++ -o rng.o -c rng.cpp -fpic -I$(PYTHON_INCLUDE)


# The C version doesn't use the library
mcell_main_c: mcell_main_c.o JSON.o makefile
	gcc -lm -o mcell_main_c mcell_main_c.o JSON.o

mcell_main_c.o: mcell_main_c.c JSON.h makefile
	gcc -c mcell_main_c.c


# This is a version that reads a JSON file instead of MDL
mcell_main.o: mcell_main.cpp libMCell.h makefile
	g++ -o mcell_main.o -c -std=c++11 -Wno-write-strings mcell_main.cpp

mcell_main: mcell_main.o libMCell.a makefile
	g++ -o mcell_main -lm mcell_main.o libMCell.a


# This is a simple stand-alone program to demonstrate libMCell
mcell_simple.o: mcell_simple.cpp libMCell.h makefile
	g++ -o mcell_simple.o -c -std=c++11 -Wno-write-strings mcell_simple.cpp

mcell_simple: mcell_simple.o libMCell.a makefile
	g++ -o mcell_simple -lm mcell_simple.o libMCell.a


#This is a simple stand-alone program to demonstrate libMCell with count events
mcell_simple_count.o: mcell_simple_count.cpp libMCell.h makefile
	g++ -o mcell_simple_count.o -c -std=c++11 -Wno-write-strings mcell_simple_count.cpp

mcell_simple_count: mcell_simple_count.o libMCell.a makefile
	g++ -o mcell_simple_count -lm mcell_simple_count.o libMCell.a


clean:
	rm -f mcell_main
	rm -f mcell_main_c
	rm -f mcell_simple
	rm -f mcell_simple_count
	rm -f *_wrap* *.pyc
	rm -f core
	rm -f *.o *.a *.so
	rm -f libMCell.py
	rm -f *.class *.jar
	rm -f *~

cleansubs:
	rm -rf react_data
	rm -rf viz_data
	rm -f __pycache__/*
	rmdir __pycache__

# Alternate Implementation Test Cases (may not be part of final libMCell)

test_c: mcell_main_c
	./mcell_main_c proj_path=. data_model=dm.json

test_ppy: pure_python_sim.py
	python pure_python_sim.py proj_path=. data_model=dm.txt

# Primary Usage Test Cases - These should work with libMCell

# Note: the Python version accepts a Python data model,
#       and the C++ version accepts a JSON data model.

test_cpp: mcell_main
	./mcell_main proj_path=. data_model=dm.json

test_py: mcell_main.py _libMCell.so
	python mcell_main.py proj_path=. data_model=dm.txt

install: mcell_main mcell_main_c
	cp -v mcell_main $(INSTALL_DIR)cellblender/libMCell/
	cp -v mcell_main_c $(INSTALL_DIR)cellblender/libMCell/
