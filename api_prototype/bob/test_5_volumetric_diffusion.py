# Test 5: Volumetric diffusion in a box/sphere


# Parameters to vary
iterations = 1000
num_A = 200
num_B = 100
decay_rate_A = 1e3
ab_decay = 1e3
ab_to_c_rate = 1e6
ab_c_rate = 1e8
box_len = 0.5

import math

class my_sphere ( MCellGeometry ):
  # This is an attempt to create geometry from an analytic description
  # This type of geometry would not have points and faces, but would satisfy this interface:
  #  is_inside (x,y,z)
  #  normal_of_first_crossing ( start_point, end_point )

  def __init__(self, x, y, z, r):
    self.x = x
    self.y = y
    self.z = z
    self.r = r

  def is_inside(x,y,z):
    # Can return INSIDE, OUTSIDE, SURFACE, or UNKNOWN
    try:
      dx = x - self.x
      dy = y - self.y
      dz = z - self.z
      r2 = r*r
      dist2 = (x*x) + (y*y) + (z*z)
      if dist2 < r2:
        return MCellGeometry.INSIDE
      elif dist2 > r2:
        return MCellGeometry.OUTSIDE
      else
        return MCellGeometry.SURFACE
    except:
      return MCellGeometry.UNKNOWN

  my_object.normal_of_first_crossing ( from_x, from_y, from_z, to_x, to_y, to_z ):
    # Returns a normal or a status
    from_status = self.is_inside(from_x, from_y, from_z)
    to_status = self.is_inside(to_x, to_y, to_z)
    if (from_status == MCellGeometry.UNKNOWN) or (to_status == MCellGeometry.UNKNOWN):
      return MCellGeometry.UNKNOWN
    elif (from_status == MCellGeometry.INSIDE) and (to_status == MCellGeometry.INSIDE):
      return MCellGeometry.


  bounds_may_contain_surface ( xmin, xmax, ymin, ymax, zmin, zmax )
  
  my_object.as_mesh ( suggested_face_length ) // Returns a mesh (actual or synthesized)


# Import the things needed
import libMCell as m

