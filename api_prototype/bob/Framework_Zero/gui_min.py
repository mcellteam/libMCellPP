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


def expose_callback ( widget, event, zpa ):
  width, height = widget.window.get_size()  # This is the area of the entire window
  drawable = widget.window
  colormap = widget.get_colormap()
  gc = widget.get_style().fg_gc[gtk.STATE_NORMAL]
  # Save the current color
  old_fg = gc.foreground

  # Clear the screen with black
  gc.foreground = colormap.alloc_color(0,0,0)
  drawable.draw_rectangle(gc, True, 0, 0, width, height)

  # Do custom drawing here based on the current zpa.user_data dictionary

  if zpa.user_data['option'] == "Spiral":
    # Create a spiral
    gc.foreground = colormap.alloc_color(10000,40000,5000)
    px = 0.0
    py = 0.0
    for i in range ( 1500 ):
      a = 0.1 * i
      r = 0.5 * i * zpa.user_data['size']
      x = r * math.cos(a)
      y = r * math.sin(a)
      drawable.draw_line ( gc, zpa.wxi(px), zpa.wyi(py), zpa.wxi(x), zpa.wyi(y) )
      px = x
      py = y

  if zpa.user_data['option'] == "Rect":
    # Create a spiral
    gc.foreground = colormap.alloc_color(10000,10000,60000)
    for i in range ( 20 ):
      hx = i * 40 * zpa.user_data['size']
      hy = i * 30 * zpa.user_data['size']
      drawable.draw_rectangle ( gc, False, zpa.wxi(-hx), zpa.wyi(-hy), zpa.wwi(2*hx), zpa.whi(2*hy) )

  t = time.time()
  cr = drawable.cairo_create()
  cr.set_source_rgb (1,1,1)
  cr.move_to(15,21)
  cr.show_text("Time at fixed location: " + str(t))
  gc.foreground = colormap.alloc_color(65535,0,0)
  drawable.draw_rectangle(gc, True, 12, 25, 190, 2)


  gc.foreground = old_fg
  return False


def menu_callback ( widget, data=None ):
  if type(data) == type((True,False)):
    # Any tuple passed is assumed to be: (command, zpa)
    command = data[0]
    zpa = data[1]
    if command == "Spiral":
      zpa.user_data['option'] = command
      zpa.queue_draw()
    elif command == "Rect":
      zpa.user_data['option'] = command
      zpa.queue_draw()
    elif command == "Fast":
      zpa.user_data['speed'] = 25.0
    elif command == "Med":
      zpa.user_data['speed'] = 10.0
    elif command == "Slow":
      zpa.user_data['speed'] = 2.0
  return True

def background_callback ( zpa ):
  if zpa.user_data['running']:
    t = time.time()
    if t - zpa.user_data['last_update'] > 0.05:
      zpa.user_data['last_update'] = t
      zpa.user_data['size'] = 0.8 + (0.4*math.sin(t*zpa.user_data['speed']))
      zpa.queue_draw()
  return True

def run_callback ( zpa ):
  # print ( "Run " )
  zpa.user_data['running'] = True
  return True

def stop_callback ( zpa ):
  # print ( "Stop " )
  zpa.user_data['running'] = False
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
  # The zpa.user_data is helpful to avoid globals
  zpa.user_data = { 'running':False,
                    'last_update':-1,
                    'option': "Rect",
                    'speed': 10.0,
                    'size': 1.0
                  }

  menu_bar = gtk.MenuBar()
  vbox.pack_start(menu_bar, expand=False, fill=False, padding=0)

  (options_menu, options_item) = zpa.add_menu ( "_Options" )
  if True: # An easy way to indent and still be legal Python
    zpa.add_menu_item ( options_menu, menu_callback, "Spiral",     ("Spiral",zpa) )
    zpa.add_menu_item ( options_menu, menu_callback, "Rectangles", ("Rect"  ,zpa) )

  (speed_menu, speed_item) = zpa.add_menu ( "_Speed" )
  if True: # An easy way to indent and still be legal Python
    zpa.add_menu_item ( speed_menu, menu_callback, "Fast",   ("Fast",zpa ) )
    zpa.add_menu_item ( speed_menu, menu_callback, "Medium", ("Med", zpa ) )
    zpa.add_menu_item ( speed_menu, menu_callback, "Slow",   ("Slow",zpa ) )

  zpa.set_x_scale ( -1000.0,   0, 1000.0, 400 )
  zpa.set_y_scale ( -1000.0,   0 ,1000.0, 300 )

  menu_bar.append ( options_item )
  menu_bar.append ( speed_item )

  menu_bar.show()

  drawing_area = zpa.get_drawing_area()
  drawing_area.connect ( "expose_event", expose_callback, zpa )
  
  vbox.pack_start(drawing_area, True, True, 0)

  drawing_area.show()
  drawing_area.grab_focus()

  hbox = gtk.HBox ( True, 0 )
  hbox.show()
  vbox.pack_start ( hbox, False, False, 0 )

  run_button = gtk.Button("Run")
  hbox.pack_start ( run_button, True, True, 0 )
  run_button.connect_object ( "clicked", run_callback, zpa )
  run_button.show()

  stop_button = gtk.Button("Stop")
  hbox.pack_start ( stop_button, True, True, 0 )
  stop_button.connect_object ( "clicked", stop_callback, zpa )
  stop_button.show()

  window.show()

  zpa.set_cursor ( gtk.gdk.HAND2 )

  menu_callback ( None, "QuadTree" )
  gtk.idle_add ( background_callback, zpa )

  gtk.main()
  return 0

if __name__ == '__main__':
  main()
