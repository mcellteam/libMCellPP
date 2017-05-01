define ALL
main_loop
endef

# Remove default handling of all suffixes:
.SUFFIXES:

# Preserve intermediate files which would otherwise be deleted as not a target:
.SECONDARY:

# C++ Standards: c++98 gnu++98 c++0x gnu++0x c++11 c++14

.PHONY: all
all: $(ALL)

# $@ is the target
# $* is the stem with which an implicit rule matches
# $< is the first prerequisite
# $? all prerequisites newer than target (space separated)
# $+ all prerequisites (space separated)
# $^ all prerequisites (space separated)

%.o: %.cpp makefile
	@echo "Making \""$@"\" from \""$*.cpp"\":"
	g++ -g -std=c++14 -o $@ -c $*.cpp

%: %.o makefile
	@echo "Making \""$@"\" from \""$*.o"\":"
	g++ -g -lm -o $@ $*.o

.PHONY: clean
clean:
	rm -f $(ALL)
	rm -f a.out
	rm -f core
	rm -f *.o *.so *.ii
	rm -f *~

# Have "make test" execute the first prerequisite
.PHONY: test
test: $(ALL)
	@echo "========================="
	@./$<
	@echo "========================="

