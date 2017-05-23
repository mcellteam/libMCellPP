import sys
from math import sin
from math import cos
from math import sqrt

from scheduler import *
from location import *
from molecules import *
from geometry import *

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


class spiral_point ( point_radius ):
  def __init__( self, x=0, y=0, r=0, spiral_angle=0, spiral_radius=0 ):
    point_radius.__init__(self, x, y, r)  ### Initialize the Base Class first
    self.cx = x                   # Center x of the spiral
    self.cy = y                   # Center y of the spiral
    self.r = r                    # Radius of the point
    self.angle = spiral_angle     # Current angle of the spiral
    self.radius = spiral_radius   # Current radius of the spiral
  def get_motion ( self, dt ):
    self.angle += 0.25 # Radians
    self.radius += 2
    new_x = self.cx + ( self.radius * cos(self.angle) )
    new_y = self.cy + ( self.radius * sin(self.angle) )
    return ( (self.x, self.y), (new_x, new_y) )


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
        molecule ( mol_a, brownian_point(x=40,y=0,dc=1e-5,r=3) ),
        molecule ( mol_a, brownian_point(x=0,y=40,dc=1e-5,r=3) ),
        molecule ( mol_a, brownian_point(x=80,y=80,dc=1e-5,r=3) ),
        molecule ( mol_a, brownian_point(x=-60,y=10,dc=1e-5,r=3) ),
        molecule ( mol_b, point_location(x=40,y=40) ),
        molecule ( mol_b, point_location(x=-40,y=-40) ),
        molecule ( mol_c, newtonian_point(x=-40,y=80,vx=-90,vy=0,r=3) ),
        molecule ( mol_c, newtonian_point(x=-40,y=80,vx=0,vy=-90,r=3) ),
        molecule ( mol_c, newtonian_point(x=-40,y=80,vx=90,vy=90,r=3) ),
        molecule ( mol_s, spiral_point(0,0,r=6) ),
      ]

    # Create a few polygon objects
    self.objects = [
        point_face_object ( "Triangle 1", x=30, y=0, points=[[0,100], [50,-10], [-50,-10]] ),
        point_face_object ( "Square 1", x=-50, y=0, points=[[-90,-90], [-90,90], [90,90], [90,-90]] ),
        reg_polygon_object ( "3-gon", x=-120, y=-80, num_faces=3, radius=30 ),
        reg_polygon_object ( "4-gon", x=-60, y=-80, num_faces=4, radius=30 ),
        reg_polygon_object ( "5-gon", x=0, y=-80, num_faces=5, radius=30 ),
        reg_polygon_object ( "6-gon", x=60, y=-80, num_faces=6, radius=30 ),
        reg_polygon_object ( "7-gon", x=120, y=-80, num_faces=7, radius=30 ),
        reg_polygon_object ( "24-gon", x=0, y=80, color=(65000,0,0), num_faces=24, radius=50 ),
      ]

    print ( str ( self.objects ) )
    self.collisions = []

    # Set some simulation values
    self.t = 0
    self.dt = 2

    # Create a baseline scheduler
    self.scheduler = scheduler()

    self.scheduler.schedule_item ( time_step_action(self,200), [10] )
    self.scheduler.schedule_item ( diffuse_action(self), [0.5] )
    
  def diffuse ( self ):
    print ( "Start diffuse" )
    # Simple Collision Detection using distance
    for mol_index in range(len(self.mols)):
      m = self.mols[mol_index]
      # Get the start and end points for this molecule's motion for this time step.
      pt_start, pt_end = m.pt.get_motion(0.01)
      # Assume a default radius of zero
      m_rad = 0
      # Check if the point for this molecule is a subclass of something with a radius
      if issubclass ( m.pt.__class__, point_radius ):
        m_rad = m.pt.r
      # Check for a collision between this molecule and others along that line
      for target_index in range (mol_index+1,len(self.mols)):
        target_mol = self.mols[target_index]
        # Assume a radius of zero
        t_rad = 0
        # Check if the point for this molecule is a subclass of something with a radius
        if issubclass ( target_mol.pt.__class__, point_radius ):
          t_rad = target_mol.pt.r
        dx = target_mol.pt.x - pt_end[0]
        dy = target_mol.pt.y - pt_end[1]
        if sqrt( (dx*dx) + (dy*dy) ) <  (m_rad+t_rad):
          print ( "  Collision Detected between " + m.species.name + "(" + str(m.pt.x) + "," + str(m.pt.y) + ") and " + target_mol.species.name + "(" + str(target_mol.pt.x) + "," + str(target_mol.pt.y) + ")" )
          print ( "     Distance = " + str(sqrt( (dx*dx) + (dy*dy) )) + ", and combined radii = " + str(m_rad+t_rad) )
          self.collisions.append ( ( (target_mol.pt.x+pt_end[0])/2.0, (target_mol.pt.y+pt_end[1])/2.0 ) )
      m.pt.move ( pt_end[0], pt_end[1] )
    print ( "End diffuse" )

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

