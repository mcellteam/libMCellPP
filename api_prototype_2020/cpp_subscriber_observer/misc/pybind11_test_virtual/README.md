# Test of inheritance of virtual methods in pybind11

This sort of works:
* `virtual` works via pybind11.
* `pure virtual` is done wrong.

## Compiling

```
c++ -O3 -Wall -shared -std=c++11 -fPIC `python3 -m pybind11 --includes` pybind11_test_virtual.cpp -o pybind11_test_virtual`python3-config --extension-suffix` -undefined dynamic_lookup
```

## Running

In Python:
```
from pybind11_test_virtual import *

d = Dog()
d.go(3)
```
should print
```
'woof! woof! woof! '
```

You cannot make an Animal directly, because it is ABC:
```
a = Animal()
```
should give and error:
```
TypeError: pybind11_test_virtual.Animal: No constructor defined!
```

But you can also subclass `Animal`:
```
class Cat(Animal):
   def __init__(self):
      pass
   def go(no_times):
      for i in range(0,no_times):
         print("meow")

c = Cat()
c.go(3)
```
should print
```
meow
meow
meow
```

## What doesn't work

Stupidly, even though `go` is pure virtual, you can subclass `Animal` and ignore it:
```
class Cat(Animal):
   def __init__(self):
      pass

c = Cat() # this should fail
```
It doesn't fail.... Wtf...
