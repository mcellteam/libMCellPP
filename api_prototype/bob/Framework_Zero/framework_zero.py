import sys
import pygtk
pygtk.require ( '2.0' )
import gtk

class schedulable_object:

  def __init__ ( self ):
    self.callback_list = []
    pass

  #def execute ( self, scheduler, t, data=None ):
  #  print ( "Executing at time = " + str(t) )

def p ( x ):
  print ( "executing with parameter " + str(x) )

class named_schedulable_object(schedulable_object):
  def __init__(self, name):
    self.name = name
  def execute ( self, scheduler, t, data=None):
    print ( "Executing " + self.name + " at t=" + str(t) )


class schedulable_object_with_callback_list(schedulable_object):

  def __init__(self):
    self.callback_list = []

  def add_callback(self, cb):
    self.callback_list.append ( cb )

  def execute ( self, scheduler, t, data=None):
    print ( "Executing callbacks in list at t=" + str(t) )
    for cb in self.callback_list:
      cb(self)



class scheduled_time_slot:
  def __init__ ( self, sable_object, t ):
    self.t = t
    self.absolute_first = None
    self.absolute_last = None
    self.obj = sable_object
    

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
    slot = scheduled_time_slot( sable_object, t )
    self.slots[t] = slot
    pass

  def schedule_item_last ( self, sable_object, t ):
    pass

  def schedule_item_absolute_last ( self, sable_object, t ):
    pass

  def run ( self ):
    while len(self.slots) > 0:
      slot = self.slots.pop( sorted(self.slots.keys())[0] )
      for cb in slot.obj.callback_list:
        cb(slot.obj)

  def run_through ( self, t ):
    pass


if __name__ == "__main__":

    s = scheduler()
    o = schedulable_object()
    o.callback_list.append ( p )

    s.schedule_item ( o, 0 )
    s.schedule_item ( o, 1 )
    s.schedule_item ( o, 2 )
    s.schedule_item ( o, 10 )
    s.run()

