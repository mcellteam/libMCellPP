import math
import random

# __import__('code').interact(local={k: v for ns in (globals(), locals()) for k, v in ns.items()})
# Alternative:
#  _a = {}
#  _a.update(globals())
#  _a.update(locals())
#  __import__('code').interact(local=_a)


class location:
  # Base class supporting any notion of "location"
  def __init__(self):
    pass
  def print_self ( self ):
    print ( "Undefined location" )


class point_location (location):
  def __init__( self, x=0, y=0 ):
    location.__init__(self)  ### Initialize the Base Class first
    self.x = x
    self.y = y
  def get_motion ( self, dt ):
    # The point_location class doesn't have it's own motion, so return the same points as 'from' and 'to':
    return ( (self.x, self.y), (self.x, self.y) )
  def move ( self, x, y ):
    self.x = x
    self.y = y
  def print_self ( self ):
    print ( "x,y = (" + str(self.x) + "," + str(self.y) )


class point_radius (point_location):
  def __init__( self, x=0, y=0, r=0 ):
    point_location.__init__(self,x=x,y=y)  ### Initialize the Base Class first
    self.r = r
  def print_self ( self ):
    print ( "x,y,r = (" + str(self.x) + "," + str(self.y) + "," + str(self.r) )


class brownian_point ( point_radius ):
  rand = None  # rand is a class variable and must be referenced by class name: brownian_point.r
  def __init__( self, x=0, y=0, r=0, dc=1 ):
    point_radius.__init__(self, x, y, r)  ### Initialize the Base Class first
    if brownian_point.rand == None:
      # Initialize the random number generator for the class (and all instances)
      brownian_point.rand = random.Random()
      brownian_point.rand.seed(1)
    self.dc = dc
  def get_motion ( self, dt ):
    ds = math.sqrt(4.0 * 1.0e8 * self.dc * dt)
    dx = brownian_point.rand.gauss(0.0,ds) * 0.70710678118654752440
    dy = brownian_point.rand.gauss(0.0,ds) * 0.70710678118654752440
    return ( (self.x, self.y), (self.x+dx, self.y+dy) )


class newtonian_point ( point_radius ):
  def __init__( self, x=0, y=0, vx=0, vy=0, r=0 ):
    point_radius.__init__(self, x, y, r)  ### Initialize the Base Class first
    self.vx = vx
    self.vy = vy
  def get_motion ( self, dt ):
    return ( (self.x, self.y), (self.x+(dt*self.vx), self.y+(dt*self.vy)) )


