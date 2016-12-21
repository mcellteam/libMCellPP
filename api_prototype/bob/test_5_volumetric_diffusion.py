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

class MCellGeometry ( object ):
  INSIDE = -1
  OUTSIDE = 1
  SURFACE = 0
  UNKNOWN = -10
  def is_inside ( self, x, y, z ):
    return UNKNOWN
  def normal_of_first_crossing ( from_x, from_y, from_z, to_x, to_y, to_z ):
    return UNKNOWN

class my_box ( MCellGeometry ):
  # This is an attempt to create geometry from an analytic description
  # This type of geometry would not have points and faces, but would satisfy this interface:
  #   is_inside (x,y,z)
  #   normal_of_first_crossing ( start_point, end_point )
  # It might also have a surface generation function for display purposes

  def __init__(self, x, y, z, rx, ry, rz):
    self.x = x
    self.y = y
    self.z = z
    self.rx = abs(rx)
    self.ry = abs(ry)
    self.rz = abs(rz)

  def is_inside ( self, x, y, z ):
    # Can return INSIDE, OUTSIDE, SURFACE, or UNKNOWN
    try:
      if x <= self.x - self.rx:
        if x == self.x:
          return MCellGeometry.SURFACE
        else:
          return MCellGeometry.OUTSIDE
      if x >= self.x + self.rx:
        if x == self.x:
          return MCellGeometry.SURFACE
        else:
          return MCellGeometry.OUTSIDE
      if y <= self.y - self.ry:
        if y == self.y:
          return MCellGeometry.SURFACE
        else:
          return MCellGeometry.OUTSIDE
      if y >= self.y + self.ry:
        if y == self.y:
          return MCellGeometry.SURFACE
        else:
          return MCellGeometry.OUTSIDE
      if z <= self.z - self.rz:
        if z == self.z:
          return MCellGeometry.SURFACE
        else:
          return MCellGeometry.OUTSIDE
      if z >= self.z + self.rz:
        if z == self.z:
          return MCellGeometry.SURFACE
        else:
          return MCellGeometry.OUTSIDE
      else:
        return MCellGeometry.INSIDE
    except:
      return MCellGeometry.UNKNOWN

  def dot ( self, a, b ):
    return ( (a[0] * b[0]) + (a[1] * b[1]) + (a[2] * b[2]) )

  def sub ( self, a, b ):
    diff = []
    for i in range(3):
      diff.append ( a[i] - b[i] )
    return diff

  def line_plane_intersection ( self, point_in_plane, normal_to_plane, p1_in_line, p2_in_line ):
    dot_normal_and_segment = self.dot ( normal_to_plane, self.sub(p2_in_line,p1_in_line) )
    if dot_normal_and_segment == 0:
      return []
    else:
      s_intersect = self.dot(normal_to_plane,self.sub(point_in_plane,p1_in_line)) / self.dot(normal_to_plane,self.sub(p2_in_line,p1_in_line))
      p_intersect = []
      for i in range(3):
        p_intersect.append ( p1_in_line[i] + ((p2_in_line[i]-p1_in_line[i]) * s_intersect) )
      return p_intersect
    

  def point_of_first_crossing ( self, from_x, from_y, from_z, to_x, to_y, to_z ):
    pass
    

  def normal_of_first_crossing ( self, from_x, from_y, from_z, to_x, to_y, to_z ):
    # Returns a normal or a status
    from_status = self.is_inside(from_x, from_y, from_z)
    to_status = self.is_inside(to_x, to_y, to_z)
    if (from_status == MCellGeometry.UNKNOWN) or (to_status == MCellGeometry.UNKNOWN):
      # One or both of the points can't be determined to be inside or outside
      return MCellGeometry.UNKNOWN
    elif (from_status == MCellGeometry.INSIDE) and (to_status == MCellGeometry.INSIDE):
      # The surface of convex object is not crossed so the particle stays inside
      return MCellGeometry.UNKNOWN
    elif (from_status == MCellGeometry.OUTSIDE) and (to_status == MCellGeometry.OUTSIDE):
      # Find nearest distance between line and center of sphere to see if they intersect
      return MCellGeometry.UNKNOWN
    else:
      # Find the first crossing
      pass
      


#  bounds_may_contain_surface ( xmin, xmax, ymin, ymax, zmin, zmax )
  
#  my_object.as_mesh ( suggested_face_length ) // Returns a mesh (actual or synthesized)


# Import the things needed
#import libMCell as m

b = my_box(0,0,0,3.65/2,2/2,5.61/2)

l1s = [0.63, -0.33, -1.73] # Starts inside the box
l1e = [1.8, -1.03, -4.08]  # Ends outside the box

l2s = [1.8,0.12,-3.42]     # Starts outside the box
l2e = [0.632,1.55,-1.42]   # Ends outside the box

print ( str ( b.line_plane_intersection ( [0, 0, -5.61/2], [0,0,-1], l1s, l1e ) ) )

__import__('code').interact(local={k: v for ns in (globals(), locals()) for k, v in ns.items()})
