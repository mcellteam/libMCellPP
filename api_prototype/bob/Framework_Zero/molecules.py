from random import randint
from location import *

# __import__('code').interact(local={k: v for ns in (globals(), locals()) for k, v in ns.items()})
# Alternative:
#  _a = {}
#  _a.update(globals())
#  _a.update(locals())
#  __import__('code').interact(local=_a)

class mol_species:
  def __init__( self, name, color=(65535,0,0) ):
    self.name = name
    self.color = color
  def print_self ( self ):
    print ( "Species " + name )

class molecule:
  def __init__( self, species, pt=None ):
    self.species = species
    if pt == None:
      self.pt = point_location(0,0)
    else:
      self.pt = pt
  def print_self ( self ):
    print ( "Mol " + self.species.name + " is at x,y = (" + str(self.pt.x) + "," + str(self.pt.y) )

