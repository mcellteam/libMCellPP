#!/usr/bin/env python

#__import__('code').interact(local = locals())

from spatial_storage import locatable_object
from spatial_storage import QuadTree
from spatial_storage import SpatialHash

import math
import random
import time

import pygtk
pygtk.require('2.0')
import gobject
import gtk

import app_window

global_algorithm = None
global_data = []

global_canvas = None
global_window = None
global_zpa = None

# Needing to repaint the window generates expose events
def expose_callback ( widget, event, zpa ):
  global global_algorithm
  # print ( "expose_callback" )

  width, height = widget.window.get_size()  # This is the area of the entire window
  drawable = widget.window
  colormap = widget.get_colormap()
  gc = widget.get_style().fg_gc[gtk.STATE_NORMAL]
  # Save the current color
  old_fg = gc.foreground

  # Clear the screen with black
  gc.foreground = colormap.alloc_color(0,0,0)
  drawable.draw_rectangle(gc, True, 0, 0, width, height)

  if global_algorithm == None:
    #print ( "Select an algorithm" )
    pass
  else:
    global_algorithm.draw_app ( widget, event, zpa )

  gc.foreground = old_fg
  return False

def mouse_motion_callback ( canvas, event ):
  # print ( "Mouse moved: " )
  global global_algorithm
  global global_zpa

  width, height = canvas.window.get_size()

  if (global_algorithm != None) and (global_zpa != None):

    x = global_zpa.x(event.x)
    y = global_zpa.y(event.y-2)

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

    global_zpa.queue_draw()
  return False


def menu_callback ( widget, data=None ):
  global global_algorithm
  global global_zpa
  global global_data
  #print ( "Menu callback called with data = " + str(data) )
  #print ( "  widget = " + str(widget) )
  if data == "Debug":
    __import__('code').interact(local = locals())

  if data == "Step":
    global_algorithm.step = True

  if data == "Start":
    global_algorithm.last_update_time = time.time()

  elif data == "Stop":
    global_algorithm.last_update_time = 1e308  # This is a very very long time away

  elif (len(data) >=8) and (data[0:8] == "QuadTree"):
    max_objects = 5
    if (len(data) > 19) and (data[0:19] == "QuadTree_Max_Items_"):
      max_objects = int(data[19:])
    global_algorithm = QuadTree( xmin=-2, ymin=-2, xmax=2, ymax=2, max_objects=max_objects )
    for obj in global_data:
      global_algorithm.add_object ( obj )
    #global_window.update_statusbar ( "QuadTree" )

  elif data == "SpatialHash":
    global_algorithm = SpatialHash( xmin=-2, ymin=-2, xmax=2, ymax=2, spatial_resolution=0.2 )
    for obj in global_data:
      global_algorithm.add_object ( obj )
    #global_window.update_statusbar ( "SpatialHash" )

  elif (len(data) > 9) and (data[0:9] == "GAUSSIAN_"):
    n = int(data[9:])
    global_data = []
    for i in range(n):
      global_data.append ( locatable_object(random.gauss(0,.1), random.gauss(0,0.1), (0.0,1.0,0.0)) )
    if global_zpa != None:
      global_zpa.set_x_scale ( -2.0,   60, 2.0, 340 )
      global_zpa.set_y_scale ( -2.0,   10, 2.0, 290 )
    global_algorithm.clear()
    for obj in global_data:
      global_algorithm.add_object ( obj )

  elif data == "CLUSTERS":

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

    if global_zpa != None:
      global_zpa.set_x_scale ( -2.0,   60, 2.0, 340 )
      global_zpa.set_y_scale ( -2.0,   10, 2.0, 290 )

    if global_algorithm != None:
      global_algorithm.clear()
      for obj in global_data:
        global_algorithm.add_object ( obj )

  elif data == "DIAGONAL_10":
    global_data = []
    for i in range(0,10):
      global_data.append ( locatable_object(i/10.0, i/10.0, (1.0,0,0)) )
    if global_zpa != None:
      global_zpa.set_x_scale ( -2.0,   60, 2.0, 340 )
      global_zpa.set_y_scale ( -2.0,   10, 2.0, 290 )
    global_algorithm.clear()
    for obj in global_data:
      global_algorithm.add_object ( obj )

  elif (len(data) > 3) and (data[0:3] == "DT_"):
    # Get from DT_#
    dt = float(data[3:])
    print ( "dt = " + str(dt) )
    global_algorithm.display_interval = dt


  if global_zpa != None:
    global_zpa.queue_draw()

  return False

def step_callback(zpa):
  menu_callback ( None, "Step" )
  return True

def run_callback(zpa):
  menu_callback ( None, "Start" )
  return True

def stop_callback(zpa):
  menu_callback ( None, "Stop" )
  return True


def reset_callback(zpa):
  zpa.reset_view()
  zpa.queue_draw()
  return True


def background_callback ( zpa ):
  # print ( "Background work with zpa = " + str(zpa) )
  # print ( "Background work with arg2 = " + str(arg2) )
  global global_algorithm
  global global_zpa

  if global_algorithm != None:
    global_algorithm.update()

  if global_zpa != None:
    global_zpa.queue_draw()

  return True



def main():
  print ( 80 * "=" )

  window = gtk.Window ( gtk.WINDOW_TOPLEVEL )
  window.set_title ( "User Window Testing" )

  window.connect ( "destroy", lambda w: gtk.main_quit() )

  vbox = gtk.VBox ( homogeneous=False, spacing=0 )
  window.add(vbox)

  window.show() # Must show before usable to create any pixmaps
  vbox.show()

  accel_group = gtk.AccelGroup()
  window.add_accel_group(accel_group)

  zpa = app_window.zoom_pan_area(window,400,300,"SquareWin")
  global global_zpa
  global_zpa = zpa

  menu_bar = gtk.MenuBar()
  vbox.pack_start(menu_bar, expand=False, fill=False, padding=0)
  """
  (file_menu, file_item) = zpa.add_menu ( "_File" )

  zpa.add_menu_item ( file_menu, menu_callback, "_Open...", "Open", 'O' )
  zpa.add_menu_sep  ( file_menu )
  zpa.add_menu_item ( file_menu, menu_callback, "_Save", "Save" )
  zpa.add_menu_item ( file_menu, menu_callback, "Save _As...", "Save As...", 'S', mask=gtk.gdk.CONTROL_MASK|gtk.gdk.SHIFT_MASK )
  zpa.add_menu_sep  ( file_menu )
  zpa.add_menu_item ( file_menu, menu_callback, "_Quit", "Quit", 'Q' )
  """

  (algorithm_menu, algorithm_item) = zpa.add_menu ( "_Algorithm" )
  if True:
    zpa.add_menu_item ( algorithm_menu, menu_callback, "_QuadTree", "QuadTree" )
    (quadtree_menu, quadtree_item) = zpa.add_menu ( "QuadTree Options" )
    if True:
      zpa.add_menu_item ( quadtree_menu, menu_callback, "Max Items 1", "QuadTree_Max_Items_1" )
      zpa.add_menu_item ( quadtree_menu, menu_callback, "Max Items 2", "QuadTree_Max_Items_2" )
      zpa.add_menu_item ( quadtree_menu, menu_callback, "Max Items 5", "QuadTree_Max_Items_5" )
      zpa.add_menu_item ( quadtree_menu, menu_callback, "Max Items 10", "QuadTree_Max_Items_10" )
      zpa.add_menu_item ( quadtree_menu, menu_callback, "Max Items 20", "QuadTree_Max_Items_20" )
      zpa.add_menu_item ( quadtree_menu, menu_callback, "Max Items 50", "QuadTree_Max_Items_50" )
      zpa.add_menu_item ( quadtree_menu, menu_callback, "Max Items 100", "QuadTree_Max_Items_100" )
    algorithm_menu.append ( quadtree_item )
    zpa.add_menu_item ( algorithm_menu, menu_callback, "SpatialHash", "SpatialHash" )

  (display_menu, display_item) = zpa.add_menu ( "_Data" )
  if True:
    zpa.add_menu_item ( display_menu, menu_callback, "Clusters", "CLUSTERS" )
    zpa.add_menu_item ( display_menu, menu_callback, "Gaussian 10", "GAUSSIAN_10" )
    zpa.add_menu_item ( display_menu, menu_callback, "Gaussian 100", "GAUSSIAN_100" )
    zpa.add_menu_item ( display_menu, menu_callback, "Gaussian 1000", "GAUSSIAN_1000" )
    zpa.add_menu_item ( display_menu, menu_callback, "Gaussian 10000", "GAUSSIAN_10000" )
    zpa.add_menu_item ( display_menu, menu_callback, "Diagonal 10", "DIAGONAL_10" )
    zpa.add_menu_item ( display_menu, menu_callback, "Dump", "DUMP" )

  (run_menu, run_item) = zpa.add_menu ( "_Run" )
  if True:
    zpa.add_menu_item ( run_menu, menu_callback, "Step", "Step", 'S' )
    zpa.add_menu_item ( run_menu, menu_callback, "_Start", "Start" )
    zpa.add_menu_item ( run_menu, menu_callback, "Sto_p", "Stop" )
    zpa.add_menu_item ( run_menu, menu_callback, "Rese_t View", "Reset" )
    zpa.add_menu_sep  ( run_menu )
    zpa.add_menu_item ( run_menu, menu_callback, "dt _0.0",  "DT_0.0"      )
    zpa.add_menu_item ( run_menu, menu_callback, "dt 0.01",  "DT_0.01"     )
    zpa.add_menu_item ( run_menu, menu_callback, "dt 0.1",   "DT_0.1"      )
    zpa.add_menu_item ( run_menu, menu_callback, "dt 0.2",   "DT_0.2"      )
    zpa.add_menu_item ( run_menu, menu_callback, "dt 0.5",   "DT_0.5"      )
    zpa.add_menu_item ( run_menu, menu_callback, "dt _1.0",  "DT_1",   '1' )
    zpa.add_menu_item ( run_menu, menu_callback, "dt _2.0",  "DT_2",   '2' )
    zpa.add_menu_item ( run_menu, menu_callback, "dt _3.0",  "DT_3",   '3' )
    zpa.add_menu_item ( run_menu, menu_callback, "dt _4.0",  "DT_4",   '4' )
    zpa.add_menu_item ( run_menu, menu_callback, "dt _5.0",  "DT_5",   '5' )
    zpa.add_menu_item ( run_menu, menu_callback, "dt 10.0",  "DT_10"       )
    zpa.add_menu_sep  ( run_menu )
    zpa.add_menu_item ( run_menu, menu_callback, "De_bug", "Debug" )

  """
  (print_menu, print_item) = zpa.add_menu ( "_Print" )

  print_intervals = [1, 2, 4, 10, 100, 1000, 10000, 100000, 1000000]
  for i in print_intervals:
    zpa.add_menu_item ( print_menu, menu_callback, "Print "+str(i), i )
  """

  """
  menu_bar.append ( file_item )
  """
  menu_bar.append ( algorithm_item )
  menu_bar.append ( display_item )
  menu_bar.append ( run_item )
  """
  menu_bar.append ( print_item )
  """

  menu_bar.show()


  ###########
  
  drawing_area = zpa.get_drawing_area()
  drawing_area.connect ( "expose_event", expose_callback, zpa )
  drawing_area.connect ( "motion_notify_event", mouse_motion_callback )

  reset_callback ( zpa )

  ###########
  
  vbox.pack_start(drawing_area, True, True, 0)

  drawing_area.show()
  drawing_area.grab_focus()

  hbox = gtk.HBox ( True, 0 )
  hbox.show()
  vbox.pack_start ( hbox, False, False, 0 )

  step_button = gtk.Button("Step")
  hbox.pack_start ( step_button, True, True, 0 )
  step_button.connect_object ( "clicked", step_callback, zpa )
  step_button.show()

  run_button = gtk.Button("Run")
  hbox.pack_start ( run_button, True, True, 0 )
  run_button.connect_object ( "clicked", run_callback, zpa )
  run_button.show()

  stop_button = gtk.Button("Stop")
  hbox.pack_start ( stop_button, True, True, 0 )
  stop_button.connect_object ( "clicked", stop_callback, zpa )
  stop_button.show()

  redraw_button = gtk.Button("Reset View")
  hbox.pack_start ( redraw_button, True, True, 0 )
  redraw_button.connect_object ( "clicked", reset_callback, zpa )
  redraw_button.show()


  window.show()

  zpa.set_cursor ( gtk.gdk.HAND2 )

  # gtk.idle_add ( reset_callback, zpa )
  menu_callback ( None, "QuadTree" )
  menu_callback ( None, "CLUSTERS" )
  gtk.idle_add ( background_callback, zpa )

  gtk.main()
  return 0

if __name__ == '__main__':
  main()
