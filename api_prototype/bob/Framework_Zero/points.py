from random import randint

# __import__('code').interact(local={k: v for ns in (globals(), locals()) for k, v in ns.items()})
# Alternative:
#  _a = {}
#  _a.update(globals())
#  _a.update(locals())
#  __import__('code').interact(local=_a)

class point:
  def __init__( self, x=0, y=0 ):
    self.x = x
    self.y = y
  def get_motion ( self, dt ):
    return ( (self.x, self.y), (self.x, self.y) )
  def move ( self, dt ):
    pass
  def print_self ( self ):
    print ( "x,y = (" + str(self.x) + "," + str(self.y) )

class brownian_point ( point ):
  def __init__( self, x=0, y=0 ):
    point.__init__(self, x, y)  ### Initialize the Base Class first
  def get_motion ( self, dt ):
    return ( (self.x, self.y), (self.x+randint(-2,2), self.y+randint(-2,2)) )
  def move ( self, dt ):
    self.x += randint(-2,2)
    self.y += randint(-2,2)

class newtonian_point ( point ):
  def __init__( self, x=0, y=0, vx=0, vy=0 ):
    point.__init__(self, x, y)  ### Initialize the Base Class first
    self.vx = vx
    self.vy = vy
  def get_motion ( self, dt ):
    return ( (self.x, self.y), (self.x+self.vx, self.y+self.vy) )
  def move ( self, dt ):
    self.x += self.vx
    self.y += self.vy


