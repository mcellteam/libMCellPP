# Test in C++

Build:
```
mkdir build
cd build
cmake ..
make
```
Run:
```
cd bin
./example
```

You should see:
```
!!! The model has been notified that the fwd rxn rate for rxn: my rxn has been changed to: 3
```
which is the desired callback in the model class.
