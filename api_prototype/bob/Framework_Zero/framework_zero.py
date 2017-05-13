import sys
import pygtk
pygtk.require ( '2.0' )
import gtk

class schedulable_object:

  def __init__ ( self ):
    pass

  def execute ( self, scheduler, t, data=None ):
    print ( "Executing at time = " + str(t) )


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

  def get_slot ( self, t ):
    slot = None
    if t in self.slots:
      slot = self.slots[t]
    else:
      slot = self.slots[t] = scheduled_time_slot( t )
    return slot

  def schedule_item_absolute_first ( self, sable_object, t ):
    slot = self.get_slot(t)
    if slot.absolute_first != None:
      raise Exception ( "Error, attempt to schedule multiple items first " + str(t) );
    slot.absolute_first = sable_object

  def schedule_item_first ( self, sable_object, t ):
    slot = self.get_slot(t)
    slot.obj_list.insert ( 0, sable_object )
    pass

  def schedule_item ( self, sable_object, t ):
    slot = self.get_slot(t)
    slot.obj_list.append ( sable_object )

  def schedule_item_last ( self, sable_object, t ):
    slot = self.get_slot(t)
    slot.obj_list.append ( sable_object )
    pass

  def schedule_item_absolute_last ( self, sable_object, t ):
    slot = self.get_slot(t)
    if slot.absolute_last != None:
      raise Exception ( "Error, attempt to schedule multiple items last at time " + str(t) );
    slot.absolute_last = sable_object

  def run ( self ):
    while len(self.slots) > 0:
      # Get the first slot (earliest time)
      earliest_key = sorted(self.slots.keys())[0]
      slot = self.slots[earliest_key]
      if slot.absolute_first != None:
        slot.absolute_first.execute ( self, slot.t )
      while len(slot.obj_list) > 0:
        o = slot.obj_list[0]
        o.execute ( self, slot.t )
        slot.obj_list.remove(o)
      if slot.absolute_last != None:
        slot.absolute_last.execute ( self, slot.t )
      self.slots.pop(earliest_key)

  def run_through ( self, t ):
    pass


def print_callback ( x ):
  print ( "Executing with parameter " + str(x) )

if __name__ == "__main__":

    s = scheduler()
    o = schedulable_object()

    s.schedule_item ( o, 0 )
    s.schedule_item ( o, 1 )
    s.schedule_item ( o, 3 )
    s.schedule_item ( named_schedulable_object('Also'), 3 )
    s.schedule_item_first ( named_schedulable_object('Before First 3'), 3 )
    s.schedule_item_last ( named_schedulable_object('After 3'), 3 )
    s.schedule_item_last ( named_schedulable_object('After After 3'), 3 )
    s.schedule_item_first ( named_schedulable_object('Before Before First 3'), 3 )
    s.schedule_item ( o, 10 )
    
    s.schedule_item ( named_schedulable_object('A20a'), 20 )
    s.schedule_item ( named_schedulable_object('A20b'), 20 )
    s.schedule_item ( named_schedulable_object('A21'), 21 )
    s.schedule_item_absolute_first ( named_schedulable_object('A20_FIRST'), 20 )
    s.schedule_item_absolute_last  ( named_schedulable_object('A20_LAST'), 20 )
    s.schedule_item ( named_schedulable_object('A20c'), 20 )

    s.schedule_item ( o, 2 )

    o = schedulable_object_with_callback_list()
    o.callback_list.append ( print_callback )   ## This used the syntax from today's discussion
    ## o.add_callback(print_callback)           ## This is the better way (hides implementation)

    s.schedule_item ( o, 30 )
    s.schedule_item ( o, 31 )
    s.schedule_item ( o, 32 )

    s.run()

