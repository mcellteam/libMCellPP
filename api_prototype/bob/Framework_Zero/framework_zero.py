import sys
import pygtk
pygtk.require ( '2.0' )
import gtk

class schedulable_object:

  def __init__ ( self ):
    pass

  def execute ( self, scheduler, t, data=None ):
    print ( "Executing at time = " + str(t) )


class scheduled_time_slot:
  def __init__ ( self, t ):
    self.t = t
    self.absolute_first = None
    self.absolute_last = None
    self.obj_list = []
  def append ( self, sable_object ):
    self.obj_list.append ( sable_object )
    

class scheduler:

  def __init__ ( self ):
    self.t = 0
    self.slots = {}
    pass

  def schedule_item_absolute_first ( self, sable_object, t ):
    pass

  def schedule_item_first ( self, sable_object, t ):
    pass

  def schedule_item ( self, sable_object, t ):
    slot = scheduled_time_slot( t ).append ( sable_object )
    self.slots[t] = slot
    pass

  def schedule_item_last ( self, sable_object, t ):
    pass

  def schedule_item_absolute_last ( self, sable_object, t ):
    pass

  def run ( self ):
    while len(self.slots) > 0:
      # Get the first slot (earliest time)
      earliest_key = sorted(self.slots.keys())[0]
      slot = self.slots[earliest_key]
      for o in slot.obj_list:
        o.execute ( self, slot.t )

  def run_through ( self, t ):
    pass


if __name__ == "__main__":

    s = scheduler()
    o = schedulable_object()

    s.schedule_item ( o, 0 )
    s.schedule_item ( o, 1 )
    s.schedule_item ( o, 2 )
    s.schedule_item ( o, 10 )
    s.run()

