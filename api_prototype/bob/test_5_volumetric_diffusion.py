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
  def check_inside ( self, x, y, z ):
    return UNKNOWN
  def point_and_normal_of_first_crossing ( self, from_x, from_y, from_z, to_x, to_y, to_z ):
    return UNKNOWN


class my_box ( MCellGeometry ):
  # This is an attempt to create geometry from an analytic description
  # This type of geometry would not have points and faces, but would satisfy this interface:
  #   check_inside (x,y,z)
  #   point_and_normal_of_first_crossing ( self, from_x, from_y, from_z, to_x, to_y, to_z )
  # It might also have a surface generation function for display purposes

  def __init__(self, x, y, z, rx, ry, rz):
    self.x = x
    self.y = y
    self.z = z
    self.rx = abs(rx)
    self.ry = abs(ry)
    self.rz = abs(rz)

  def check_inside ( self, x, y, z, tol=0 ):
    # Can return INSIDE, OUTSIDE, SURFACE, or UNKNOWN
    try:
      if x <= self.x - (self.rx+tol):
        if x == self.x:
          return MCellGeometry.SURFACE
        else:
          return MCellGeometry.OUTSIDE
      if x >= self.x + (self.rx+tol):
        if x == self.x:
          return MCellGeometry.SURFACE
        else:
          return MCellGeometry.OUTSIDE
      if y <= self.y - (self.ry+tol):
        if y == self.y:
          return MCellGeometry.SURFACE
        else:
          return MCellGeometry.OUTSIDE
      if y >= self.y + (self.ry+tol):
        if y == self.y:
          return MCellGeometry.SURFACE
        else:
          return MCellGeometry.OUTSIDE
      if z <= self.z - (self.rz+tol):
        if z == self.z:
          return MCellGeometry.SURFACE
        else:
          return MCellGeometry.OUTSIDE
      if z >= self.z + (self.rz+tol):
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

  def dist ( self, a, b ):
    sumsq = 0
    for i in range(3):
      sumsq += ( a[i] - b[i] ) * ( a[i] - b[i] )
    return math.sqrt(sumsq)

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
    

  def point_and_normal_of_first_crossing ( self, from_x, from_y, from_z, to_x, to_y, to_z ):
    start = [ from_x, from_y, from_z ]
    end   = [ to_x,   to_y,   to_z   ]
    best_point = None
    best_normal = None
    best_dist = 0
    for axis in range(3):
      for direction in range(2):
        point_in_plane = [ self.x, self.y, self.z ]
        radius_by_axis = [ self.rx, self.ry, self.rz ]
        unit_normal = [ 0, 0, 0 ]
        if direction < 0.5:
          point_in_plane[axis] += -radius_by_axis[axis]
          unit_normal[axis] = -1
        else:
          point_in_plane[axis] +=  radius_by_axis[axis]
          unit_normal[axis] = 1
        intersect = self.line_plane_intersection ( point_in_plane, unit_normal, start, end )
        print ( "Intersection is at " + str ( intersect ) )
        print ( "   for plane with point at " + str(point_in_plane) + " and normal of " + str(unit_normal) )
        if self.check_inside ( intersect[0], intersect[1], intersect[2], tol=(self.rx+self.ry+self.rz)/10000 ) == MCellGeometry.INSIDE:
          print ( "      point is inside" )
          if best_point is None:
            best_point = [ i for i in intersect ]
            best_normal = [ i for i in unit_normal ]
            best_dist = self.dist(start,best_point)
          else:
            dist = self.dist(start,intersect)
            if dist < best_dist:
              best_point = [ i for i in intersect ]
              best_normal = [ i for i in unit_normal ]
              best_dist = dist
    return ( (best_point,best_normal) )

      


#  my_object.as_mesh ( suggested_face_length ) // Returns a mesh (actual or synthesized)


# Import the things needed
#import libMCell as m

b = my_box ( 0, 0, 0,  3.65/2, 2/2, 5.61/2 )

l1s = [0.63, -0.33,  -1.73]  # Starts inside the box
l1e = [1.8,  -1.03,  -4.08]  # Ends outside the box

l2s = [1.8,   0.135, -3.42]  # Starts outside the box
l2e = [0.632, 1.55,  -1.42]  # Ends outside the box

l3s = [-1.40866,   -1.22087, 3.2971]  # Starts outside the box
l3e = [-1.93893, -0.52276,  1.49946]  # Ends outside the box

l4s = [1.20695, 1.4389,  1.67758]  # Starts outside the box
l4e = [1.56646, 0.09742, 3.11677]  # Ends outside the box

l5s = [1.01337, -0.19045, -0.15663]  # Starts outside the box
l5e = [2.39857, -0.32674, 1.2796]  # Ends outside the box

#print ( "Line 1 Intersection is at " + str ( b.line_plane_intersection ( [0, 0, -5.61/2], [0,0,-1], l1s, l1e ) ) )
print ( "Line 1 Point of first crossing ..." )
(bp,bn) = b.point_and_normal_of_first_crossing ( l1s[0], l1s[1], l1s[2], l1e[0], l1e[1], l1e[2] )
print ( "Best point is " + str(bp) )
print ( "Best normal is " + str(bn) )

print ( "" )
print ( "Line 2 Point of first crossing ..." )
(bp,bn) = b.point_and_normal_of_first_crossing ( l2s[0], l2s[1], l2s[2], l2e[0], l2e[1], l2e[2] )
print ( "Best point is " + str(bp) )
print ( "Best normal is " + str(bn) )

print ( "" )
print ( "Line 3 Point of first crossing ..." )
(bp,bn) = b.point_and_normal_of_first_crossing ( l3s[0], l3s[1], l3s[2], l3e[0], l3e[1], l3e[2] )
print ( "Best point is " + str(bp) )
print ( "Best normal is " + str(bn) )

print ( "" )
print ( "Line 4 Point of first crossing ..." )
(bp,bn) = b.point_and_normal_of_first_crossing ( l4s[0], l4s[1], l4s[2], l4e[0], l4e[1], l4e[2] )
print ( "Best point is " + str(bp) )
print ( "Best normal is " + str(bn) )

print ( "" )
print ( "Line 5 Point of first crossing ..." )
(bp,bn) = b.point_and_normal_of_first_crossing ( l5s[0], l5s[1], l5s[2], l5e[0], l5e[1], l5e[2] )
print ( "Best point is " + str(bp) )
print ( "Best normal is " + str(bn) )



# __import__('code').interact(local={k: v for ns in (globals(), locals()) for k, v in ns.items()})
