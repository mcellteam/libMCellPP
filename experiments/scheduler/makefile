all: toy_scheduler_c toy_scheduler_cpp sorting_tests

#OPTS = -Ofast -fmax-errors=2
OPTS = -O0 -g

toy_scheduler_c: toy_scheduler.c sched_util.c sched_util.h config.h makefile
	gcc $(OPTS) -o toy_scheduler_c toy_scheduler.c sched_util.c

toy_scheduler_cpp: toy_scheduler.cpp makefile
	g++ $(OPTS) -std=c++11 -o toy_scheduler_cpp toy_scheduler.cpp

sorting_tests: sorting_tests.cpp makefile
	g++ $(OPTS) -std=c++11 -o sorting_tests sorting_tests.cpp

clean:
	rm -f toy_scheduler_c
	rm -f toy_scheduler_cpp
	rm -f sorting_tests
	rm -f core
	rm -f *.o *.so
	rm -f *~

