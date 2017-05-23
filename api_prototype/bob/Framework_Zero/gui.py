#!/usr/bin/env python

# __import__('code').interact(local={k: v for ns in (globals(), locals()) for k, v in ns.items()})

import pygtk
pygtk.require ( '2.0' )
import gtk

import scheduler
import location
import sim_2d

diff_2d_sim = sim_2d.diff_2d_sim()

# Creating or Resizing the Window generates configure events
def configure_event ( widget, event ):
  x,y,width,height = widget.get_allocation()
  return True

state_history = []
display_time_index = -1

# Needing to repaint the window generates expose events
def expose_event ( widget, event ):
  global diff_2d_sim
  global state_history
  global display_time_index
  x, y, width, height = event.area  # This is the area of the portion newly exposed
  width, height = widget.window.get_size()  # This is the area of the entire window
  x, y = widget.window.get_origin()
  drawable = widget.window
  colormap = widget.get_colormap()
  gc = widget.get_style().fg_gc[gtk.STATE_NORMAL]
  # Save the current color
  old_fg = gc.foreground
  # Clear the screen with black
  gc.foreground = colormap.alloc_color(0,0,0)
  drawable.draw_rectangle(gc, True, 0, 0, width, height)
  # Buffer the original value if the history is empty
  if len(state_history) == 0:
    buffer_state()
  # Show draw the current state referenced by display_time_index
  if len(state_history) > 0:
    current_state = state_history[display_time_index]
    for m in current_state['mols']:
      gc.foreground = colormap.alloc_color(int(m['c'][0]),int(m['c'][1]),int(m['c'][2]))
      px = (width/2) + (1*m['x'])
      py = (height/2) + (1*m['y'])
      drawable.draw_arc(gc, True, int(px)-m['r'], int(py)-m['r'], 2*m['r'], 2*m['r'], 0, 360*64)
    gc.foreground = colormap.alloc_color(60000, 60000, 60000)
    for coll in current_state['cols']:
      px = (width/2) + (1*coll['x'])
      py = (height/2) + (1*coll['y'])
      drawable.draw_rectangle(gc, True, int(px), int(py), 3, 3)
    for o in current_state['objs']:
      print ( "Drawing object " + o['name'] )
      gc.foreground = colormap.alloc_color(int(o['c'][0]),int(o['c'][1]),int(o['c'][2]))
      cx = (width/2) + (1*o['x'])
      cy = (height/2) + (1*o['y'])
      for f in o['faces']:
        p1 = ( cx+o['x']+o['points'][f[0]][0], cy+o['y']+o['points'][f[0]][1] )
        p2 = ( cx+o['x']+o['points'][f[1]][0], cy+o['y']+o['points'][f[1]][1] )
        drawable.draw_line ( gc, p1[0], p1[1], p2[0], p2[1] )
  # Restore the previous color
  gc.foreground = old_fg
  return False


# Buffer the state for redrawing when the simulation goes backward or foreward
def buffer_state():
  global diff_2d_sim
  global state_history
  global display_time_index
  current_state = {}
  print ( "Buffering state " )
  # Save the current molecule positions for this time
  current_state['mols'] = []
  for m in diff_2d_sim.mols:
    m_draw = {'name':m.species.name, 'x':m.pt.x, 'y':m.pt.y, 'r':2, 'c':m.species.color}
    if issubclass ( m.pt.__class__, location.point_radius ):
      m_draw['r'] = m.pt.r
    current_state['mols'].append ( m_draw )
  # Save the history of detected collisions for this time
  current_state['cols'] = []
  for coll in diff_2d_sim.collisions:
    current_state['cols'].append ( { 'x':coll[0], 'y':coll[1] } )
  current_state['objs'] = []
  for obj in diff_2d_sim.objects:
    print ( "Buffering object " + obj.name )
    current_state['objs'].append ( { 'name':obj.name, 'x':obj.x, 'y':obj.y, 'c':obj.color, 'points':[p for p in obj.points], 'faces':[f for f in obj.faces] } )
  current_state['t'] = diff_2d_sim.t

  state_history.append ( current_state )


def back_callback(drawing_area):
  global state_history
  global display_time_index
  if ( display_time_index+len(state_history) ) > 0:
    # It's OK to step backwards
    display_time_index += -1
    print ( "Display buffered data for index " + str(display_time_index) )
  drawing_area.queue_draw()
  return True

def step_callback(drawing_area):
  global state_history
  global display_time_index
  if len(state_history) == 0:
    buffer_state()  # Save the original state
  if display_time_index < -1:
    # The history is already buffered
    display_time_index += 1
    print ( "Display buffered data for index " + str(display_time_index) )
  else:
    # Buffer the history and step
    if diff_2d_sim.scheduler.items_left() > 0:
      print ( "Display new data" )
      diff_2d_sim.step()
      buffer_state()
    else:
      print ( "No events scheduled, cannot advance time." )
  drawing_area.queue_draw()
  return True

def step_in_callback(drawing_area):
  global diff_2d_sim
  global state_history
  global display_time_index
  diff_2d_sim.step_in()
  drawing_area.queue_draw()
  return True

def step_10_callback(drawing_area):
  for i in range(10):
    step_callback(drawing_area)
  return True

def dump_callback(drawing_area):
  global diff_2d_sim
  diff_2d_sim.print_self()
  return True

def reset_callback(drawing_area):
  global diff_2d_sim
  global state_history
  global display_time_index
  diff_2d_sim = sim_2d.diff_2d_sim()
  state_history = []
  display_time_index = -1
  drawing_area.queue_draw()


# Create the window and connect the events
def main():

  window = gtk.Window ( gtk.WINDOW_TOPLEVEL )
  window.set_name ( "2D Diffusion" )
  
  vbox = gtk.VBox ( False, 0 )
  window.add(vbox)
  vbox.show()

  window.connect ( "destroy", lambda w: gtk.main_quit() )
  
  drawing_area = gtk.DrawingArea()
  drawing_area.set_size_request(600,500)
  vbox.pack_start(drawing_area, True, True, 0)
  
  drawing_area.show()
  
  drawing_area.connect ( "expose_event", expose_event )
  drawing_area.connect ( "configure_event", configure_event )

  drawing_area.set_events ( gtk.gdk.EXPOSURE_MASK
                          | gtk.gdk.LEAVE_NOTIFY_MASK
                          | gtk.gdk.BUTTON_PRESS_MASK
                          | gtk.gdk.POINTER_MOTION_MASK
                          | gtk.gdk.POINTER_MOTION_HINT_MASK )

  hbox = gtk.HBox ( True, 0 )
  hbox.show()
  vbox.pack_start ( hbox, False, False, 0 )

  back_button = gtk.Button("Back")
  hbox.pack_start ( back_button, True, True, 0 )
  back_button.connect_object ( "clicked", back_callback, drawing_area )
  back_button.show()

  step_button = gtk.Button("Step")
  hbox.pack_start ( step_button, True, True, 0 )
  step_button.connect_object ( "clicked", step_callback, drawing_area )
  step_button.show()

  dump_button = gtk.Button("Dump")
  hbox.pack_start ( dump_button, True, True, 0 )
  dump_button.connect_object ( "clicked", dump_callback, drawing_area )
  dump_button.show()

  """ # These bypass the buffering and shouldn't be used until fixed.
  step_in_button = gtk.Button("Step In")
  hbox.pack_start ( step_in_button, True, True, 0 )
  step_in_button.connect_object ( "clicked", step_in_callback, drawing_area )
  step_in_button.show()

  step_10_button = gtk.Button("Step 10")
  hbox.pack_start ( step_10_button, True, True, 0 )
  step_10_button.connect_object ( "clicked", step_10_callback, drawing_area )
  step_10_button.show()
  """

  reset_button = gtk.Button("Reset")
  hbox.pack_start ( reset_button, True, True, 0 )
  reset_button.connect_object ( "clicked", reset_callback, drawing_area )
  reset_button.show()

  window.show()

  gtk.main()
  return 0

if __name__ == "__main__":
  main()

