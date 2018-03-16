#!/usr/bin/env python

# Provide an interface to a user application that ...
#
#  - Allows direct use of all GTK drawing commands
#  - Allows most code to work with user coordinates
#  - Provides simple coordinate transform functions
#  - Transparent zoom and pan
#  - Application controlled zoom and pan requests
#  - Application controlled window sizing requests
#  - Easy menu interface (may be a separate module)
#  - Easy status bar interface (may be a separate module)
#
#  - Define initial scaling and window size:
#      win.set_x_scale ( 0.0,   0,  1.0, 640 )
#      win.set_y_scale ( 0.0, 480,  1.0,   0 )
#      win.set_fixed_aspect ( True )
#      win.set_scroll_factor ( 1.1 )
#  - Query current window size:
#      win.get_x_min ()
#      win.get_x_max ()
#      win.get_y_min ()
#      win.get_y_max ()
#  - Request refit
#      win.fitwidth  ( -3.1, 7.6, keep_aspect=False ) # implies left to right
#      win.fitheight (  200, 0.0, keep_aspect=False ) # implies top to bottom
#  - Convert user coordinates to window coordinates for drawing
#      win.wx ( user_x )
#      win.wy ( user_y )
#      win.ww ( user_w )
#      win.wh ( user_h )
#  - Convert window coordinates to user coordinates for callbacks
#      win.x ( win_x )
#      win.y ( win_y )
#      win.w ( win_w )
#      win.h ( win_h )

#
#  - Drawing callback
#      pixmap.draw_rectangle ( gc, True, win.x(0.33), win.y(1.2), win.w(0.5), win.h(0.1) )


import math

import pygtk
pygtk.require('2.0')
import gobject
import gtk

class zoom_pan_window:
  def __init__():
    # These are defined to move from user space to graphics space
    self.x_offset = 0.0
    self.y_offset = 0.0
    self.x_scale = 1.0
    self.y_scale = 1.0
    self.aspect_fixed = True
    self.scroll_factor = 1.1

  def wx ( user_x ):
    return ( self.x_offset + (user_x * self.x_scale ) )
  def wy ( user_y ):
    return ( self.y_offset + (user_y * self.y_scale ) )
  def ww ( user_w ):
    return ( user_w * self.x_scale )
  def wh ( user_h ):
    return ( user_h * self.y_scale )

  def x ( win_x ):
    pass
  def y ( win_y ):
    pass
  def w ( win_w ):
    pass
  def h ( win_h ):
    pass


  def set_x_scale ( user_x1, win_x1, user_x2, win_x2 ):
    self.x_scale  = float(win_x2 - win_x1) / (user_x2 - user_x1)
    self.x_offset = win_x1 - ( user_x1 * self.x_scale )
    
  def set_y_scale ( user_y1, win_y1, user_y2, win_y2 ):
    self.y_scale  = float(win_y2 - win_y1) / (user_y2 - user_y1)
    self.y_offset = win_y1 - ( user_y1 * self.y_scale )
    
  def set_fixed_aspect ( fixed_aspect ):
    pass
  def set_scroll_factor ( scroll_factor ):
    pass

  def get_x_min ():
    pass
  def get_x_max ():
    pass
  def get_y_min ():
    pass
  def get_y_max ():
    pass

  def fitwidth  ( user_xmin, user_xmax, keep_aspect=False ):
    pass  # implies left to right
  def fitheight ( user_ymin, user_ymax, keep_aspect=False ):
    pass # implies top to bottom


global_canvas = None
global_window = None


pixmap = None

# Creating or Resizing the Window generates configure events
def configure_event_callback ( canvas, event ):
  print ( "Configure event not handled" )
  return False  # Event has not been handled



# Needing to repaint the window generates expose events
def canvas_expose_callback ( canvas, event ):
  global pixmap

  x, y, width, height = event.area
  x=0
  y=0
  width, height = canvas.window.get_size()

  drawable = canvas.window
  gc = canvas.get_style().fg_gc[gtk.STATE_NORMAL]

  # Fill the background
  pixmap.draw_rectangle ( canvas.get_style().black_gc, True, 0, 0, width, height )

  gc.foreground = canvas.get_colormap().alloc_color(60000,10000,10000)
  pixmap.draw_rectangle ( gc, True, 100, 100, 50, 50 )


  # Restore the original foreground color to black (could save it before drawing)
  gc.foreground = canvas.get_colormap().alloc_color(0, 0, 0)

  canvas.window.draw_drawable(gc,pixmap,x,y,x,y,width,height)
  return True  # Event has been handled, do not propagate further



def mouse_motion_callback ( canvas, event ):
  width, height = canvas.window.get_size()
  if event.state == 0:
    print ( "Hover: x = " + str(event.x) + ", y = " + str(event.y) + "  state = " + str(event.state) )
  else:
    print ( "Drag:  x = " + str(event.x) + ", y = " + str(event.y) + "  state = " + str(event.state) )
    #__import__('code').interact(local = locals())

  canvas.queue_draw()

  return True  # Event has been handled, do not propagate further


def mouse_scroll_callback ( canvas, event ):
  print ( "Mouse Scroll Callback with event at (" + str(event.x) + "," + str(event.y) + ") : " + str(event) )
  #__import__('code').interact(local = locals())
  if event.direction == gtk.gdk.SCROLL_UP:
    print ( "Mouse scrolled up" )
  elif event.direction == gtk.gdk.SCROLL_DOWN:
    print ( "Mouse scrolled down" )
  elif event.direction == gtk.gdk.SCROLL_LEFT:
    print ( "Mouse scrolled left" )
  elif event.direction == gtk.gdk.SCROLL_RIGHT:
    print ( "Mouse scrolled right" )
  else:
    print ( "Mouse scrolled other?" )
  return True  # Event has been handled, do not propagate further



# Update when a mouse button is pressed
def button_press_callback ( widget, event ):
  widget.queue_draw()
  return True  # Event has been handled, do not propagate further

# Update when a mouse button is pressed
def key_press_callback ( widget, event ):
  print ( "Key press event: " + str(event) )
  widget.queue_draw()
  return True  # Event has been handled, do not propagate further





class zoom_pan_window:

  def background_callback ( self, arg1, data=None ):
    # print ( "Background work with arg1 = " + str(arg1) )
    global global_canvas
    global_canvas.queue_draw()
    return True  # Event has been handled, do not propagate further


  def delete_callback ( self, widget, event, data=None ):
    gtk.main_quit()
    return False

  def open_callback ( self, widget, data=None ):
    print ( "Open with data = " + str(data) )
    return False

  def save_callback ( self, widget, data=None ):
    print ( "Save with data = " + str(data) )
    return False

  def save_as_callback ( self, widget, data=None ):
    print ( "Save As with data = " + str(data) )
    return False


  def cmd_callback ( self, widget, data=None ):
    # The "self" is a menu_window instance
    global global_window

    print ( "Command with data = " + str(data) )

    if data == "Step":
      pass
    elif data[0:3] == "DT_":
      # Get from DT_#
      dt = float(data[3:])
      print ( "dt = " + str(dt) )

    global_canvas.queue_draw()

    return True  # Event has been handled, do not propagate further


  def zoom_callback ( self, widget, data=None ):
    # The "self" is a menu_window instance
    global global_window

    print ( "Zoom with data = " + str(data) )
    global_canvas.queue_draw()

    return True  # Event has been handled, do not propagate further


  def set_cursor_callback ( self, widget, data=None ):
    self.drawing_area.window.set_cursor ( gtk.gdk.Cursor(gtk.gdk.HAND2) )  # DRAFT_SMALL TARGET HAND1 SB_UP_ARROW CROSS CROSSHAIR CENTER_PTR CIRCLE DIAMOND_CROSS IRON_CROSS PLUS CROSS_REVERSE DOT DOTBOX FLEUR
    return True  # Event has been handled, do not propagate further

  def mouse_enter_callback ( self, widget, data=None ):
    self.drawing_area.grab_focus()
    return True  # Event has been handled, do not propagate further

  def print_callback ( self, widget, data=None ):
    return False

  def quit_callback ( self, widget, data=None ):
    print ( "Quit with data = " + str(data) )
    gtk.main_quit()
    return False

  def update_statusbar(self, status=""):
    # clear any previous message, underflow is allowed
    self.status_bar.pop(0)
    self.status_bar.push ( 0, status )

  def add_menu ( self, label ):
    menu = gtk.Menu()
    item = gtk.MenuItem(label)
    item.set_submenu ( menu )
    item.show()
    return (menu, item)

  def add_menu_item ( self, parent, callback, label, data, key=None, mask=gtk.gdk.CONTROL_MASK, ):
    item = gtk.MenuItem(label=label)
    item.connect ( "activate", callback, data )
    if key != None:
      item.add_accelerator("activate", self.accel_group, ord(key), mask, gtk.ACCEL_VISIBLE)
    parent.append ( item )
    item.show()

  def add_menu_sep ( self, parent ):
    item = gtk.SeparatorMenuItem()
    parent.append ( item )
    item.show()


  def __init__(self):
    self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
    self.window.set_size_request(400, 400)
    self.window.set_title ( "Python Zoom and Pan" )
    self.window.connect ( "delete_event", self.delete_callback )
    # Prepare for tooltips
    self.tooltips = gtk.Tooltips()

    self.vbox = gtk.VBox ( homogeneous=False, spacing=0 )
    self.window.add(self.vbox)  # The window can only contain one child object

    self.window.show() # Must show before usable to create any pixmaps

    self.menu_bar = gtk.MenuBar()
    self.accel_group = gtk.AccelGroup()
    self.window.add_accel_group(self.accel_group)


    (self.zoom_menu, self.zoom_item) = self.add_menu ( "_Zoom" )

    self.add_menu_item ( self.zoom_menu, self.zoom_callback, "_In x 2", "in_x_2" )
    self.add_menu_item ( self.zoom_menu, self.zoom_callback, "_Out x 2", "out_x_2" )
    self.add_menu_item ( self.zoom_menu, self.zoom_callback, "_All", "all" )

    self.menu_bar.append ( self.zoom_item )

    (self.run_menu, self.run_item) = self.add_menu ( "_Run" )

    self.add_menu_item ( self.run_menu, self.cmd_callback, "Step", "Step", 'S' )
    self.add_menu_item ( self.run_menu, self.cmd_callback, "Start", "Start" )
    self.add_menu_item ( self.run_menu, self.cmd_callback, "Sto_p", "Stop" )

    self.menu_bar.append ( self.run_item )

    self.vbox.pack_start(self.menu_bar, expand=False, fill=False, padding=0)
    self.menu_bar.show()



    self.drawing_area = gtk.DrawingArea()
    global global_canvas
    global_canvas = self.drawing_area
    self.drawing_area.set_flags ( gtk.CAN_FOCUS )

    self.drawing_area.connect ( "configure_event", configure_event_callback )
    self.drawing_area.connect ( "expose_event", canvas_expose_callback )
    self.drawing_area.connect ( "enter_notify_event", self.mouse_enter_callback )
    self.drawing_area.connect ( "key_press_event", key_press_callback )
    self.drawing_area.connect ( "button_press_event", button_press_callback )
    self.drawing_area.connect ( "motion_notify_event", mouse_motion_callback )
    self.drawing_area.connect ( "scroll_event", mouse_scroll_callback )

    self.drawing_area.connect ( "realize", self.set_cursor_callback )

    self.drawing_area.set_events ( gtk.gdk.EXPOSURE_MASK
                                 | gtk.gdk.ENTER_NOTIFY_MASK
                                 | gtk.gdk.LEAVE_NOTIFY_MASK
                                 | gtk.gdk.KEY_PRESS_MASK
                                 | gtk.gdk.BUTTON_PRESS_MASK
                                 | gtk.gdk.POINTER_MOTION_MASK
                                 | gtk.gdk.POINTER_MOTION_HINT_MASK )

    self.drawing_area.grab_focus()

    self.vbox.pack_start(self.drawing_area, expand=True, fill=True, padding=0)
    self.drawing_area.show()


    self.status_bar = gtk.Statusbar()
    self.vbox.pack_start(self.status_bar, expand=False, fill=True, padding=0)
    self.status_bar.show()

    self.vbox.show()

    self.update_statusbar()


    #__import__('code').interact(local = locals())



def main():
  global global_window
  global_window = zoom_pan_window()
  # Make a few calls to initialize the otherwise blank window
  #global_window.cmd_callback ( None, "QuadTree" )
  #global_window.cmd_callback ( None, "RANDOM" )
  # gtk.idle_add ( global_window.background_callback, "Arg1" )
  gtk.main()


if __name__ == '__main__':
  main()
