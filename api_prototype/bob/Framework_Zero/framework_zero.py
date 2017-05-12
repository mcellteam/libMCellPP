import sys
import pygtk
pygtk.require ( '2.0' )
import gtk

class schedulable_object:

  def __init__ ( self ):
    pass

  def execute ( self, scheduler, t, data=None ):
    pass


class scheduled_time_slot:
  def __init__ ( self, sable_object, t ):
    self.t = t
    self.obj = sable_object
    

class scheduler:

  def __init__ ( self ):
    self.t = 0
    self.slots = []
    pass

  def schedule_item_absolute_first ( self, sable_object, t ):
    pass

  def schedule_item_first ( self, sable_object, t ):
    pass

  def schedule_item ( self, sable_object, t ):
    slot = scheduled_time_slot( sable_object, t )
    self.slots.append ( slot )
    pass

  def schedule_item_last ( self, sable_object, t ):
    pass

  def schedule_item_absolute_last ( self, sable_object, t ):
    pass

  def run ( self ):
    while len(self.slots) > 0:
      slot = self.slots[0]
      self.slots.remove(slot)
      slot.obj.execute ( self, slot.t )
    pass

  def run_through ( self, t ):
    pass

