import sys

# __import__('code').interact(local={k: v for ns in (globals(), locals()) for k, v in ns.items()})
# Alternative:
#  _a = {}
#  _a.update(globals())
#  _a.update(locals())
#  __import__('code').interact(local=_a)


# Simple command line program to show scheduler operation:
#
# import scheduler as d
# s = d.scheduler()
# for i in range(12):
#     s.print_self(1)
#     s.schedule_item ( d.priority_scheduled_item(), 3 )  ## Could use this: [0.1*i]
#


#next_available_id = 0
#def next_id():
#  global next_available_id
#  next_id = next_available_id
#  next_available_id += 1
#  return next_id

class scheduled_item:
  def __init__(self):
    # Note that adding ID's to items is not needed. It's only here to help verify the algorithms.
    #self.my_id = next_id()
    #print ( "Creating scheduled_item with next_id =" + str(self.my_id) )
    pass
  def execute(self):
    print ( "             #### Warning: Execute for base class: " + str(self.__class__) + " does nothing" )
  def depth_indent ( self, depth ):
    #return ( "  " * depth ) + "id:" + str(self.my_id) + "  "
    return ( "  " * depth ) + "  "
  def print_self ( self, depth, prefix="", suffix="" ):
    print ( self.depth_indent(depth) + prefix + str(self.__class__) + suffix  )

class priority_scheduled_item(scheduled_item):
  # self.priority_list is a list of priorities, one for each scheduled dimension
  # Any dimensions beyond this list are considered "don't know" or "don't care"
  # The priorities are floating point numbers
  # Items are scheduled in increasing priority (smaller values happen before larger)
  # It's best not to schedule both specified and unspecified items in the same scheduler
  def __init__(self, priority_list=[]):
    scheduled_item.__init__(self)  ### Initialize the Base Class first
    self.priority_list = priority_list
  def print_self ( self, depth, prefix="", suffix="" ):
    print ( self.depth_indent(depth) + prefix + str(self.__class__) + suffix )

class scheduler(priority_scheduled_item):
  def __init__(self):
    priority_scheduled_item.__init__(self)  ### Initialize the Base Class first
    self.scheduled_items = {}
    self.next_unspecified_priority = 0          # Could be:  long(0)
    self.max_unspecified_priority = sys.maxint  # Could be:  long(sys.maxint)
  def schedule_item ( self, item, priority_list=[] ):
    # Parameters: item is a subclass of scheduled_item, priority_list is list of real
    priority = None
    remaining_list = None
    if len(priority_list) > 0:
      priority = priority_list[0]
      remaining_list = priority_list[1:]
      print ( "Using specified priority of " + str(priority) )
    else:
      priority = self.next_unspecified_priority
      print ( "Using unspecified priority of " + str(priority) )
      self.next_unspecified_priority += 1
      if self.next_unspecified_priority >= (self.max_unspecified_priority):
        # This happens when the number of items scheduled at a single point
        # in time (or priority) is greater than maxint. One response would
        # be to wrap around and begin resplitting the schedulers yet again:
        self.next_unspecified_priority = 0
        # This would force another split of the 0th entry in this scheduler.
        # This is probably not correct and should split above this scheduler.
        # But since it's so rare, just print an error and exit.
        print ( "Warning: the execution order of the items scheduled at the same instant may not be correct" )
        sys.exit ( 111111 )
      remaining_list = []
    if priority in self.scheduled_items:
      # This slot is already in use, so check to see if it's another scheduler already
      old_item = self.scheduled_items[priority]
      if issubclass ( old_item.__class__, scheduler ):
        old_priority_list = old_item.priority_list
        self.scheduled_items[priority].schedule_item ( item, remaining_list )
      else:
        # This slot is already in use by a non-scheduler, so subdivide with another scheduler by next priority
        # First get the old item
        old_item = self.scheduled_items[priority]
        old_priority_list = []
        if issubclass ( old_item.__class__, priority_scheduled_item ):
          old_priority_list = old_item.priority_list
        # Replace with a new scheduler
        self.scheduled_items[priority] = scheduler()
        self.scheduled_items[priority].priority = old_priority_list
        # Put the old item in the scheduler
        self.scheduled_items[priority].schedule_item ( old_item, old_priority_list )
        # Put the new item in the scheduler
        self.scheduled_items[priority].schedule_item ( item, remaining_list )
    else:
      # Add this item as a leaf
      self.scheduled_items[priority] = item
  def execute(self):
    print ( " Overloaded execute for type = " + str(self.__class__)  )
    self.run()
  def run ( self, steps=-1 ):
    priorities = sorted(self.scheduled_items.keys())
    step_num = 0
    for p in priorities:
      print ( " Length of scheduled_items = " + str(len(self.scheduled_items)) )
      if (steps >= 0) and (step_num >= steps):
        print ( " Stopped with steps=" + str(steps) + ", and step_num=" + str(step_num) )
        break
      # Note that this execute function may execute all sub-scheduled events
      self.scheduled_items[p].execute()
      self.scheduled_items.pop(p,None)
      step_num += 1
  def step_in ( self ):
    priorities = sorted(self.scheduled_items.keys())
    if len(priorities) > 0:
      p = priorities[0]
      item = self.scheduled_items[p]
      if issubclass ( item.__class__, scheduler ):
        # This is a scheduler, so step into it
        item.step_in()
        # If after stepping in, there's nothing left, remove the scheduler
        if len(item.scheduled_items) == 0:
          self.scheduled_items.pop(p,None)
      else:
        # Call the regular execute function and pop the item
        self.scheduled_items[p].execute()
        self.scheduled_items.pop(p,None)
  def print_self ( self, depth, prefix="", suffix="" ):
    priorities = sorted(self.scheduled_items.keys())
    print ( self.depth_indent(depth) + prefix + str(self.__class__) + " " + str(priorities) + suffix )
    for p in priorities:
      self.scheduled_items[p].print_self(depth+1, str(p)+": " )

