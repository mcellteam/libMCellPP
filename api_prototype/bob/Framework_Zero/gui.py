#!/usr/bin/env python

# __import__('code').interact(local={k: v for ns in (globals(), locals()) for k, v in ns.items()})

import pygtk
pygtk.require ( '2.0' )
import gtk

import scheduler
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
      px = (width/2) + (10*m['x'])
      py = (height/2) + (10*m['y'])
      drawable.draw_rectangle(gc, True, int(px), int(py), 6, 6)
    gc.foreground = colormap.alloc_color(65535, 65535, 0)
    for coll in current_state['cols']:
      px = (width/2) + (10*coll['x'])
      py = (height/2) + (10*coll['y'])
      drawable.draw_rectangle(gc, True, int(px), int(py), 3, 3)
  # Restore the previous color
  gc.foreground = old_fg
  return False


# Buffer the state for redrawing when the simulation goes backward or foreward
def buffer_state():
  global diff_2d_sim
  global state_history
  global display_time_index
  current_state = {}
  # Save the current molecule positions for this time
  current_state['mols'] = []
  for m in diff_2d_sim.mols:
    current_state['mols'].append ( {'name':m.species.name, 'x':m.pt.x, 'y':m.pt.y, 'c':m.species.color} )
  # Save the history of detected collisions for this time
  current_state['cols'] = []
  for coll in diff_2d_sim.collisions:
    current_state['cols'].append ( {'x':coll[0], 'y':coll[1] } )
  current_state['t'] = diff_2d_sim.t
  state_history.append ( current_state )


def back_callback(drawing_area):
  global state_history
  global display_time_index
  if ( display_time_index+len(state_history) ) > 0:
    # It's OK to step backwards
    print ( "Display buffered data" )
    display_time_index += -1
  drawing_area.queue_draw()
  return True

def step_callback(drawing_area):
  global state_history
  global display_time_index
  if len(state_history) == 0:
    buffer_state()  # Save the original state
  if display_time_index < -1:
    # The history is already buffered
    print ( "Display buffered data" )
    display_time_index += 1
  else:
    # Buffer the history and step
    print ( "Display new data" )
    diff_2d_sim.step()
    buffer_state()
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

