import math
import random

# __import__('code').interact(local={k: v for ns in (globals(), locals()) for k, v in ns.items()})
# Alternative:
#  _a = {}
#  _a.update(globals())
#  _a.update(locals())
#  __import__('code').interact(local=_a)


class model_object:
  # Base class supporting any notion of a geometrical object (might not be points/faces)
  def __init__(self):
    pass
  def print_self ( self ):
    print ( "Undefined object" )


class point_face_object (model_object):
  def __init__( self, name="", x=0, y=0, color=(32000,32000,32000), points=[], faces=[] ):
    model_object.__init__(self)  ### Initialize the Base Class first
    self.name = name
    self.color = color
    self.points = [ p for p in points ]
    self.faces = [ f for f in faces ]
    self.x = x
    self.y = y
    if (len(points) > 0) and (len(faces) == 0):
      # Make faces for the points
      for i in range(len(self.points)):
        print ( "  Making face with " + str(i) + "," + str((i+1)%len(self.points)) )
        self.faces.append ( (i, (i+1)%len(self.points)) )
  def get_motion ( self, dt ):
    # The point_face_object class motion isn't defined yet
    return ( None )
  def move ( self, x, y ):
    self.x = x
    self.y = y
  def print_self ( self ):
    print ( "Object " + self.name + ": x,y = (" + str(self.x) + "," + str(self.y) )
    for point in self.points:
      print ( "  " + str(point) )
    for face in self.faces:
      print ( "  " + str(face) )


class reg_polygon_object (point_face_object):
  def __init__( self, name="", x=0, y=0, color=(32000,32000,32000), num_faces=3, radius=1 ):
    points = []
    delta = 2 * math.pi / num_faces
    for i in range(num_faces):
      points.append ( [int(radius*math.cos(i*delta)), int(radius*math.sin(i*delta))] )
    point_face_object.__init__(self, name=name, x=x, y=y, color=color, points=points)  ### Initialize the Base Class with points
  def get_motion ( self, dt ):
    # The point_face_object class motion isn't defined yet
    return ( None )
  def move ( self, x, y ):
    self.x = x
    self.y = y
  def print_self ( self ):
    print ( "Object " + self.name + ": x,y = (" + str(self.x) + "," + str(self.y) )
    for point in self.points:
      print ( "  " + str(point) )
    for face in self.faces:
      print ( "  " + str(face) )

