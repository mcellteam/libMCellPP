all: toy_scheduler_c toy_scheduler_cpp


toy_scheduler_c: toy_scheduler.c makefile
	gcc -o toy_scheduler_c toy_scheduler.c

toy_scheduler_cpp: toy_scheduler.cpp makefile
	g++ -std=c++11 -o toy_scheduler_cpp toy_scheduler.cpp

clean:
	rm -f toy_scheduler_c
	rm -f toy_scheduler_cpp
	rm -f core
	rm -f *.o *.so
	rm -f *~

