import random

# __import__('code').interact(local={k: v for ns in (globals(), locals()) for k, v in ns.items()})
# Alternative:
#  _a = {}
#  _a.update(globals())
#  _a.update(locals())
#  __import__('code').interact(local=_a)

class location:
  def __init__(self):
    pass

class point_location (location):
  def __init__( self, x=0, y=0 ):
    location.__init__(self)  ### Initialize the Base Class first
    self.x = x
    self.y = y
  def get_motion ( self, dt ):
    return ( (self.x, self.y), (self.x, self.y) )
  def move ( self, x, y ):
    self.x = x
    self.y = y
  def print_self ( self ):
    print ( "x,y = (" + str(self.x) + "," + str(self.y) )

class brownian_point ( point_location ):
  r = None  # r is a class variable and must be referenced by class name: brownian_point.r
  def __init__( self, x=0, y=0 ):
    point_location.__init__(self, x, y)  ### Initialize the Base Class first
    brownian_point.r = random.Random()
    brownian_point.r.seed(13)  # Interesting seeds: 4 7 11
  def get_motion ( self, dt ):
    return ( (self.x, self.y), (self.x+brownian_point.r.randint(-2,2), self.y+brownian_point.r.randint(-2,2)) )

class newtonian_point ( point_location ):
  def __init__( self, x=0, y=0, vx=0, vy=0 ):
    point_location.__init__(self, x, y)  ### Initialize the Base Class first
    self.vx = vx
    self.vy = vy
  def get_motion ( self, dt ):
    return ( (self.x, self.y), (self.x+self.vx, self.y+self.vy) )


