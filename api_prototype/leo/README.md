# Notes on Code Structure

## 1. make_x(), add_x(), modify_x() functions

This allows for the making of species, reactions, etc., without necessarily adding those world properties into the given world. 
This may be a desirable feature for the user if they're creating multiple worlds at once, or they're code checks pre-made properties to 
determine if they will be included in the simulation. 

Introducing modify_x() was my solution to accommodating dynamic modeling. A good example of its implementation is test_10_reaction.py.

## 2. Defining objects/shapes

Using pm.make_object(), there should be 2 ways to define an object:

    ### 1. Basic (box, sphere, cylinder, etc.)

    Allows for quick and simple geometry definition. \
    Description Parameters:

    ```
    type = “CUBE”, “CYLDINER”, “SPHERE”, etc.
    center = [0,0,0]
    edge_dimensions = [1,0.5, 2]  # [ x-length, y-length, z-length ]
    radius = 1
    normal_vector = [0,0,1]
    rotate_about = [1,0,0]  # rotates about a line created by this point and the previously defined center point.
    extrude_length = 1
    ```

      ### 2. Advanced (irregular or nonsymmetric shapes)

    Allows for more complicated geometry definition. \
    Description Parameters:

    ```
    vertices = [ 
		[ -1,  -1,   0  ], 
		[  1,    0,   0  ], 
		[ -1,    1,   0  ], 
		[  0,    0,   1  ]  ]
    faces =  [
	      [  0,  1,  2  ],
	      [  0,  2,  3  ]  ] 
    line_equation = 
    ```
We should make a nice library/reference chart of parameters that can be specified for each type of object (ex. "CYLINDER" needs center, 
normal_vector, radius, and extrude_length), including all their default values if left unspecified.


