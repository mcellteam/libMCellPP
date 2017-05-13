#!/usr/bin/env python

from framework_zero import *

class clock_ticker(schedulable_object):
  def execute ( self, scheduler, t, data=None):
    print ( "My clock ticked at t=" + str(t) )
    if t < 2:
      if ( round((t*100) + 0.0001) % 500 ) == 0:
        scheduler.schedule_item ( self, t+0.01 )
        scheduler.schedule_item ( self, t+0.02 )
        scheduler.schedule_item ( self, t+0.03 )
      scheduler.schedule_item ( self, t+0.1 )

def p ( x ):
  print ( "Executing my callabck with parameter " + str(x) )


if __name__ == "__main__":

    s = scheduler()
    o = schedulable_object()
    o.callback_list.append ( p )

    s.schedule_item ( o, 0 )
    s.schedule_item ( o, 1 )
    s.schedule_item ( o, 2 )
    s.schedule_item ( o, 10 )

    s.run()

