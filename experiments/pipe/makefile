PYTHON_INCLUDE = /usr/include/python3.4m

# Linux:
INSTALL_DIR = ~/.config/blender/2.77/scripts/addons/

# Mac:
#INSTALL_DIR = ~/Library/Application\ Support/Blender/2.74/scripts/addons/


all: mcell_pipe_cpp mcell_pipe_c


mcell_pipe_cpp: mcell_pipe_cpp.o JSON.o makefile
	g++ -lm -o mcell_pipe_cpp mcell_pipe_cpp.o JSON.o

mcell_pipe_cpp.o: mcell_pipe_cpp.cpp JSON.h makefile
	g++ -c -std=c++11 -Wno-write-strings mcell_pipe_cpp.cpp


mcell_pipe_c: mcell_pipe_c.o JSON.o makefile
	gcc -lm -o mcell_pipe_c mcell_pipe_c.o JSON.o

mcell_pipe_c.o: mcell_pipe_c.c JSON.h makefile
	gcc -c mcell_pipe_c.c


JSON.o: JSON.c JSON.h makefile
	gcc -o JSON.o -c JSON.c -fPIC -I$(PYTHON_INCLUDE)


clean:
	rm -f mcell_pipe_cpp
	rm -f mcell_pipe_c
	rm -f *_wrap* *.pyc
	rm -f core
	rm -f *.o *.so
	rm -f *~

