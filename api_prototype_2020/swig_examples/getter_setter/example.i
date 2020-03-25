%include <attribute.i>

%module example

%attribute(Example, int, x, get_x, set_x);

%{
     #include "example.hpp"
%}

class Example {
    public:
      void set_x(int x);
      int get_x() const;
};
