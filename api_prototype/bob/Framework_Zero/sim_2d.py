from random import randint
import sys
from math import sin
from math import cos

from scheduler import *
from location import *
from molecules import *

# __import__('code').interact(local={k: v for ns in (globals(), locals()) for k, v in ns.items()})
# Alternative:
#  _a = {}
#  _a.update(globals())
#  _a.update(locals())
#  __import__('code').interact(local=_a)


class diffuse_action(priority_scheduled_item):
  def __init__(self,diff_sim):
    priority_scheduled_item.__init__(self)  ### Initialize the Base Class first
    self.sim = diff_sim
  def execute(self):
    print ( " Overloaded execute for type = " + str(self.__class__)  )
    print ( " Diffuse Molecules at t=" + str(self.sim.t) )
    self.sim.diffuse()


class time_step_action(priority_scheduled_item):
  def __init__(self,diff_sim,stop_time=None):
    priority_scheduled_item.__init__(self)  ### Initialize the Base Class first
    self.sim = diff_sim
    self.stop_time = stop_time
  def execute(self):
    print ( " Overloaded execute for type = " + str(self.__class__)  )
    print ( " Time Step at t=" + str(self.sim.t) + ", with stop_time=" + str(self.stop_time) )
    if (self.stop_time is None) or (self.sim.t < self.stop_time):
      print ( " Time Step from t=" + str(self.sim.t) + " to t=" + str(self.sim.t+self.sim.dt) )
      self.sim.diffuse()
      self.sim.t += self.sim.dt
      self.sim.scheduler.schedule_item ( time_step_action(self.sim, self.stop_time), [self.sim.t] )
      #self.sim.scheduler.schedule_item ( diffuse_action(self.sim), [self.sim.t] )


class spiral_point ( point_location ):
  def __init__( self, x=0, y=0 ):
    point_location.__init__(self, x, y)  ### Initialize the Base Class first
    self.cx = x
    self.cy = y
    self.angle = 0
    self.radius = 0
  def move ( self, dt ):
    self.angle += 0.5 # Radians
    self.radius += 0.5
    self.x = self.cx + ( self.radius * cos(self.angle) )
    self.y = self.cy + ( self.radius * sin(self.angle) )


class diff_2d_sim:
  def __init__ ( self ):
    print ( " Constructing a new simulation" )

    # Simulation specific data
    
    # Create some molecule species
    mol_a = mol_species('a', (65535,0,0) )
    mol_b = mol_species('b', (0,65535,0) )
    mol_c = mol_species('c', (0,0,65535) )
    mol_s = mol_species('s', (65535,65535,65535) )

    # Create some molecule instances
    self.mols = [
        molecule(mol_a,brownian_point(1,0)),
        molecule(mol_a,brownian_point(0,1)),
        molecule(mol_a,brownian_point(1,2)),
        molecule(mol_b,point_location(2,0)),
        molecule(mol_b,point_location(1,1)),
        molecule(mol_c,newtonian_point(-1,2,-1,0)),
        molecule(mol_c,newtonian_point(-1,2,0,-1)),
        molecule(mol_c,newtonian_point(-1,2,1,1)),
        molecule(mol_s,spiral_point(0,0)),
      ]

    # Set some simulation values
    self.t = 0
    self.dt = 2

    # Create a baseline scheduler
    self.scheduler = scheduler()

    self.scheduler.schedule_item ( time_step_action(self,50), [10] )
    self.scheduler.schedule_item ( diffuse_action(self), [0.5] )
    
  def diffuse ( self ):
    for m in self.mols:
      m.pt.move(0.01)

  def step ( self ):
    print ( "Before run(1): t=" + str(self.t) )
    self.scheduler.run(1)
    print ( "After run(1): t=" + str(self.t) )

  def step_in ( self ):
    print ( "Before step_in(): t=" + str(self.t) )
    self.scheduler.step_in()
    print ( "After step_in(): t=" + str(self.t) )

  def print_self ( self ):
    print ( "vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv t = " + str(self.t) + " vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv" )
    self.scheduler.print_self(1)
    print ( "^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ t = " + str(self.t) + " ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^" )

