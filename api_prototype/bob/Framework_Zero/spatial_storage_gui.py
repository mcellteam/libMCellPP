#!/usr/bin/env python

# Based on https://gitlab.snl.salk.edu/NeuralNetworkCoding/AssortedPrograms/ ... /BackProp.py

from spatial_storage import locatable_object
from spatial_storage import QuadTree
from spatial_storage import SpatialHash

import math
import random

global_algorithm = None
global_data = []

global_canvas = None
global_window = None


import pygtk
pygtk.require('2.0')
import gobject
import gtk


pixmap = None
numcolors = 16
pos_colors = None
neg_colors = None

# Creating or Resizing the Window generates configure events
def configure_event_callback ( canvas, event ):
  global pixmap
  x,y,width,height = canvas.get_allocation()
  # print width, height
  new_pixmap = gtk.gdk.Pixmap(canvas.window, width, height)
  new_pixmap.draw_rectangle ( canvas.get_style().black_gc, True, 0, 0, width, height )
  # Copy the old pixmap into the new one
  if pixmap != None:
    new_pixmap.draw_drawable(canvas.get_style().black_gc,pixmap,0,0,0,0,-1,-1)
  pixmap = new_pixmap
  return True


def map_pos_neg_colors ( canvas, gc ):
  global pos_colors
  global neg_colors
  global numcolors
  if (pos_colors == None) or (neg_colors == None):
    pos_colors = []
    neg_colors = []
    cmap = canvas.get_colormap()
    for i in range(numcolors):
      pos_colors.append ( cmap.alloc_color(0, i*65535/numcolors, 0) )
      neg_colors.append ( cmap.alloc_color(i*65535/numcolors, 0, 0) )
  gc.background = canvas.get_colormap().alloc_color(0, 0, 0)
  gc.foreground = canvas.get_colormap().alloc_color(65535, 0, 0)







# Needing to repaint the window generates expose events
def draw_global_algorithm ( canvas, event ):
  global global_algorithm
  
  global pixmap
  global pos_colors
  global neg_colors
  global numcolors
  x, y, width, height = event.area
  x=0
  y=0
  width, height = canvas.window.get_size()

  drawable = canvas.window
  gc = canvas.get_style().fg_gc[gtk.STATE_NORMAL]
  map_pos_neg_colors ( canvas, gc )

  # Fill the background
  pixmap.draw_rectangle ( canvas.get_style().black_gc, True, 0, 0, width, height )

  if global_algorithm != None:

    xscale = width / (global_algorithm.xmax - global_algorithm.xmin)
    xoffset = width - (xscale * global_algorithm.xmax)

    yscale = height / (global_algorithm.ymax - global_algorithm.ymin)
    yoffset = height - (yscale * global_algorithm.ymax)


    global_algorithm.draw ( canvas, pixmap, event, x, y, x+width, y+height, xoffset, xscale, yoffset, yscale )


  # Restore the original foreground color to black (could save it before drawing)
  gc.foreground = canvas.get_colormap().alloc_color(0, 0, 0)

  canvas.window.draw_drawable(gc,pixmap,x,y,x,y,width,height)
  return False



# Needing to repaint the window generates expose events
def canvas_expose_callback ( canvas, event ):
  draw_global_algorithm ( canvas, event )
  return False



def mouse_motion_callback ( canvas, event ):
  global global_algorithm

  width, height = canvas.window.get_size()

  if global_algorithm != None:

    xscale = width / (global_algorithm.xmax - global_algorithm.xmin)
    xoffset = width - (xscale * global_algorithm.xmax)

    yscale = height / (global_algorithm.ymax - global_algorithm.ymin)
    yoffset = height - (yscale * global_algorithm.ymax)

    x = (event.x - xoffset) / xscale
    y = (event.y - yoffset) / yscale

    all_objs = []
    global_algorithm.all_objects(all_objs)
    for obj in all_objs:
      obj.highlight = False

    objs = global_algorithm.find_objects(x, y)
    #print ( "Mouse moved: " + str(event.x) + "," + str(event.y) + " " + str(xscale) + " " + str(xoffset) + " " + str(yscale) + " " + str(yoffset) + " " + str(x) + " " + str(y) )
    #print ( "Found " + str(len(objs)) + " objects" )
    for obj in objs:
      obj.highlight = True

    # print ( "Mouse moved: " + str(x) + "," + str(y) + " #: " + str(len(objs)) + " / " + str(len(all_objs)) )

    canvas.queue_draw()

  return False


def mouse_scroll_callback ( canvas, event ):
  print ( "Mouse Scroll Callback with event: " + str(event) )
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




# Update when a mouse button is pressed
def button_press_callback ( widget, event ):
  widget.queue_draw()
  return True




class menu_window:

  def idle_callback ( self ):
    global global_canvas
    global_canvas.queue_draw()
    print ( "Idle" )
    return True

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

  def run_callback ( self, widget, data=None ):
    global_window.update_statusbar ( "Running ..." )



  def cmd_callback ( self, widget, data=None ):
    global global_algorithm
    global global_data
    global global_window

    print ( "Command with data = " + str(data) )

    if data == "QuadTree":
      global_algorithm = QuadTree( xmin=-2, ymin=-2, xmax=2, ymax=2, max_objects=5 )
      for obj in global_data:
        global_algorithm.add_object ( obj )
      global_window.update_statusbar ( "QuadTree" )

    if data == "SpatialHash":
      global_algorithm = SpatialHash( xmin=-2, ymin=-2, xmax=2, ymax=2, spatial_resolution=0.2 )
      for obj in global_data:
        global_algorithm.add_object ( obj )
      global_window.update_statusbar ( "SpatialHash" )

    if data == "RANDOM":

      global_data = []

      for i in range(1,7):
        global_data.append ( locatable_object(i/10.0, i/10.0, (1.0,0,0)) )

      for i in range(15,20):
        global_data.append ( locatable_object(i/10.0, -i/10.0, (0,1.0,0)) )

      for i in range(100):
        x = random.gauss(0.75,0.1)
        y = random.gauss(x, 0.05)
        global_data.append ( locatable_object(x-2, -(1+y), (0.2,0.2,1.0)) )

      for i in range(100):
        global_data.append ( locatable_object(random.gauss(0,0.05), random.gauss(-1,0.05), (1.0,1.0,0.0)) )

      for i in range(100):
        global_data.append ( locatable_object(random.uniform(-2,-1.5), random.uniform(-1,0), (0,1.0,1.0)) )

      for i in range(100):
        global_data.append ( locatable_object(random.gauss(1,.1), random.gauss(1,0.5), (1.0,0,1.0)) )

      for i in range(50):
        global_data.append ( locatable_object(random.uniform(0.1,0.4), random.uniform(2.1,2.2), (0.8,0.6,0)) )

      for i in range(50):
        global_data.append ( locatable_object(random.uniform(0.6,0.9), random.uniform(-2.2,-2.1), (0.8,0.6,0)) )

      for i in range(50):
        global_data.append ( locatable_object(random.uniform(2.1,2.2), random.uniform(0.65,0.85), (0.8,0.6,0)) )

      for i in range(50):
        global_data.append ( locatable_object(random.uniform(-2.2,-2.1), random.uniform(-1.4,-1.1), (0.8,0.6,0)) )

      global_algorithm.clear()
      for obj in global_data:
        global_algorithm.add_object ( obj )


    # global_window.update_statusbar()
    global_canvas.queue_draw()

    return False


  def dump_callback ( self, widget, data=None ):
    global global_algorithm
    global_algorithm.print_self()


  def set_cursor_callback ( self, widget, data=None ):
    self.drawing_area.window.set_cursor ( gtk.gdk.Cursor(gtk.gdk.DRAFT_SMALL) )  # DRAFT_SMALL TARGET SB_UP_ARROW CROSS CROSSHAIR CENTER_PTR CIRCLE DIAMOND_CROSS IRON_CROSS PLUS CROSS_REVERSE DOT DOTBOX FLEUR

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
    self.window.set_size_request(800, 800)
    self.window.set_title ( "Python Spatial Storage" )
    self.window.connect ( "delete_event", self.delete_callback )
    # Prepare for tooltips
    self.tooltips = gtk.Tooltips()

    self.vbox = gtk.VBox ( homogeneous=False, spacing=0 )
    self.window.add(self.vbox)  # The window can only contain one child object

    self.window.show() # Must show before usable to create any pixmaps

    self.menu_bar = gtk.MenuBar()
    self.accel_group = gtk.AccelGroup()
    self.window.add_accel_group(self.accel_group)


    (self.file_menu, self.file_item) = self.add_menu ( "_File" )

    self.add_menu_item ( self.file_menu, self.open_callback, "_Open...", "Open", 'O' )
    self.add_menu_sep  ( self.file_menu )
    self.add_menu_item ( self.file_menu, self.save_callback, "_Save", "Save", 'S' )
    self.add_menu_item ( self.file_menu, self.save_as_callback, "Save _As...", "Save As...", 'S', mask=gtk.gdk.CONTROL_MASK|gtk.gdk.SHIFT_MASK )
    self.add_menu_sep  ( self.file_menu )
    self.add_menu_item ( self.file_menu, self.quit_callback, "_Quit", "Quit", 'Q' )

    (self.algorithm_menu, self.algorithm_item) = self.add_menu ( "_Algorithm" )

    self.add_menu_item ( self.algorithm_menu, self.cmd_callback, "QuadTree", "QuadTree" )
    self.add_menu_item ( self.algorithm_menu, self.cmd_callback, "SpatialHash", "SpatialHash" )

    (self.display_menu, self.display_item) = self.add_menu ( "_Data" )

    self.add_menu_item ( self.display_menu, self.cmd_callback, "Random", "RANDOM" )
    self.add_menu_item ( self.display_menu, self.dump_callback, "Dump", "DUMP" )

    (self.run_menu, self.run_item) = self.add_menu ( "_Run" )

    self.add_menu_item ( self.run_menu, self.run_callback, "_Converge", "RUN_-1", 'C' )
    self.add_menu_sep  ( self.run_menu )
    self.add_menu_item ( self.run_menu, self.run_callback, "Run _1", "RUN_1", '1' )
    self.add_menu_item ( self.run_menu, self.run_callback, "Run _2", "RUN_2", '2' )
    self.add_menu_item ( self.run_menu, self.run_callback, "Run _3", "RUN_3", '3' )
    self.add_menu_item ( self.run_menu, self.run_callback, "Run _4", "RUN_4", '4' )
    self.add_menu_item ( self.run_menu, self.run_callback, "Run _5", "RUN_5", '5' )
    self.add_menu_item ( self.run_menu, self.run_callback, "Run 10", "RUN_10" )
    self.add_menu_item ( self.run_menu, self.run_callback, "Run 100", "RUN_100" )
    self.add_menu_item ( self.run_menu, self.run_callback, "Run 1000", "RUN_1000", 'K' )
    self.add_menu_item ( self.run_menu, self.run_callback, "Run 10000", "RUN_10000" )
    self.add_menu_item ( self.run_menu, self.run_callback, "Run 100000", "RUN_100000" )
    self.add_menu_item ( self.run_menu, self.run_callback, "Run 1000000", "RUN_1000000", 'M' )
    self.add_menu_sep  ( self.run_menu )
    self.add_menu_item ( self.run_menu, self.cmd_callback, "_Restart", "Restart", 'R' )
    self.add_menu_sep  ( self.run_menu )
    self.add_menu_item ( self.run_menu, self.cmd_callback, "_Start", "Start" )
    self.add_menu_item ( self.run_menu, self.cmd_callback, "Sto_p", "Stop" )
    self.add_menu_item ( self.run_menu, self.cmd_callback, "Rese_t", "Reset" )

    (self.print_menu, self.print_item) = self.add_menu ( "_Print" )

    self.add_menu_item ( self.print_menu, self.print_callback, "Print 1", 1 )
    self.add_menu_item ( self.print_menu, self.print_callback, "Print 2", 2 )
    self.add_menu_item ( self.print_menu, self.print_callback, "Print 4", 4 )
    self.add_menu_item ( self.print_menu, self.print_callback, "Print 10", 10 )
    self.add_menu_item ( self.print_menu, self.print_callback, "Print 100", 100 )
    self.add_menu_item ( self.print_menu, self.print_callback, "Print 1000", 1000 )
    self.add_menu_item ( self.print_menu, self.print_callback, "Print 10000", 10000 )
    self.add_menu_item ( self.print_menu, self.print_callback, "Print 100000", 100000 )
    self.add_menu_item ( self.print_menu, self.print_callback, "Print 1000000", 1000000 )


    self.menu_bar.append ( self.file_item )
    self.menu_bar.append ( self.algorithm_item )
    self.menu_bar.append ( self.display_item )
    self.menu_bar.append ( self.run_item )
    self.menu_bar.append ( self.print_item )

    self.vbox.pack_start(self.menu_bar, expand=False, fill=False, padding=0)
    self.menu_bar.show()



    self.drawing_area = gtk.DrawingArea()
    global global_canvas
    global_canvas = self.drawing_area

    self.drawing_area.connect ( "configure_event", configure_event_callback )
    self.drawing_area.connect ( "expose_event", canvas_expose_callback )
    self.drawing_area.connect ( "button_press_event", button_press_callback )
    self.drawing_area.connect ( "motion_notify_event", mouse_motion_callback )
    self.drawing_area.connect ( "scroll_event", mouse_scroll_callback )

    self.drawing_area.connect ( "realize", self.set_cursor_callback )

    self.drawing_area.set_events ( gtk.gdk.EXPOSURE_MASK
                                 | gtk.gdk.LEAVE_NOTIFY_MASK
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
  global_window.cmd_callback ( None, "QuadTree" )
  global_window.cmd_callback ( None, "RANDOM" )
  gtk.main()


if __name__ == '__main__':
  global global_window
  menu_win = menu_window()
  global_window = menu_win
  main()
