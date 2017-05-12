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


if __name__ == "__main__":

    s = scheduler()
    c = clock_ticker()

    s.schedule_item ( c, 0 )
    s.run()

