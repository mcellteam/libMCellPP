from random import randint

import scheduler as d
s = d.scheduler()

for i in range(12):
  s.print_self(1)
  s.schedule_item ( d.scheduled_item(), [1111111] )  ## Could use this: [0.1*i]

# Try scheduling more items in one of those sub-bins:

for i in range(3):
  s.print_self(1)
  s.schedule_item ( d.scheduled_item(), [1111111,5] )  ## Could use this: [0.1*i]


# These were testing the scheduler
if False:

  # Schedule an item in the past
  self.scheduler.schedule_item ( scheduled_item(), [-1] )

  # Schedule an item at t=0
  self.scheduler.schedule_item ( scheduled_item(), [0] )

  # Schedule an item in the future
  self.scheduler.schedule_item ( scheduled_item(), [1] )

  # Schedule 2 items at the same time. These will create a new scheduler and give them random times.
  self.scheduler.schedule_item ( scheduled_item(), [2] )
  self.scheduler.schedule_item ( scheduled_item(), [2] )

  # Schedule a short series of items at the top level
  for i in range(2):
    self.scheduler.schedule_item ( scheduled_item(), [3 + (0.01*i)] )

  # Manually schedule a new scheduler
  new_scheduler = scheduler()
  self.scheduler.schedule_item ( new_scheduler, [4] )

  # Add some items to the new scheduler. The priorities are with one parent priority.
  new_scheduler.schedule_item ( scheduled_item(), [1] )
  new_scheduler.schedule_item ( scheduled_item(), [2] )
  new_scheduler.schedule_item ( scheduled_item(), [3] )

  # Manually schedule a new scheduler
  another_new_scheduler = scheduler()
  # Add some items to the new scheduler. The priorities are with one parent priority.
  another_new_scheduler.schedule_item ( scheduled_item(), [100] )
  another_new_scheduler.schedule_item ( scheduled_item(), [200] )
  # Add the newest scheduler to the previous scheduler between 2 and 3
  new_scheduler.schedule_item ( another_new_scheduler, [2.5] )


  self.scheduler.schedule_item ( priority_scheduled_item(), [5] )
  for i in range(4):
    self.scheduler.schedule_item ( priority_scheduled_item(), [6 + (0.01*i)] )
  self.scheduler.schedule_item ( priority_scheduled_item(), [7] )

  # Manually schedule a new scheduler
  test_sched_limits = scheduler()
  self.scheduler.schedule_item ( test_sched_limits, [9] )
  for i in range(2):
    test_sched_limits.schedule_item ( priority_scheduled_item() )

if False:
      self.scheduler.schedule_item ( priority_scheduled_item(), [9.1] )
      self.scheduler.schedule_item ( scheduled_item(), [10] )


