#!/usr/bin/env python

#__import__('code').interact(local = locals())

import math

import pygtk
pygtk.require('2.0')
import gobject
import gtk

import app_window



import time

# Needing to repaint the window generates expose events
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

  for i in range(20):
    gc.foreground = colormap.alloc_color((i%2)*35535,(1+i%2)*35535,(1+i%2)*35535)
    drawable.draw_rectangle(gc, True, zpa.wxi(0.3+(0.05*i)), zpa.wyi(0.1+(0.05*i)), zpa.wwi(2.8), abs(zpa.whi(2.8)))
  
  t = time.time()
  cr = drawable.cairo_create()
  cr.set_source_rgb (1,1,1)
  cr.move_to(15,21)
  cr.show_text(str(t))

  gc.foreground = colormap.alloc_color(65000,65000,65000)
  cr.move_to(zpa.wxi(0.0),zpa.wyi(0.0))
  cr.show_text("Origin")
  drawable.draw_line(gc, 0, zpa.wyi(0), width, zpa.wyi(0))
  drawable.draw_line(gc, zpa.wxi(0), 0, zpa.wxi(0), height)

  gc.foreground = colormap.alloc_color(32000,32000,65000)

  # Note the abs(zpa.whi()) in the next line. Some primitives make assumptions about start point and size!!!  
  drawable.draw_arc(gc, False, zpa.wxi(-1), zpa.wyi(1), zpa.wwi(2), abs(zpa.whi(0.5)), 0, 360*64)
  drawable.draw_line(gc, zpa.wxi(-1), zpa.wyi(1), zpa.wxi(1), zpa.wyi(0))
  drawable.draw_line(gc, zpa.wxi(-1), zpa.wyi(0), zpa.wxi(0), zpa.wyi(1))
  drawable.draw_line(gc, zpa.wxi(0.9), zpa.wyi(0), zpa.wxi(0.9), zpa.wyi(1))
  drawable.draw_line(gc, zpa.wxi(0.0), zpa.wyi(0.1), zpa.wxi(1.0), zpa.wyi(0.1))

  gc.foreground = old_fg
  return False

def reset_callback(zpa):
  zpa.set_defaults()
  zpa.set_x_scale ( -1.0,   0, 1.0, 400 )
  zpa.set_y_scale (  0.0, 300, 1.0,   0 )
  zpa.queue_draw()
  return True

def menu_callback ( widget, data=None ):
  print ( "Menu callback called with data = " + str(data) )
  print ( "  widget = " + str(widget) )
  return False


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

  menu_bar = gtk.MenuBar()
  vbox.pack_start(menu_bar, expand=False, fill=False, padding=0)

  (file_menu, file_item) = zpa.add_menu ( "_File" )

  zpa.add_menu_item ( file_menu, menu_callback, "_Open...", "Open", 'O' )
  zpa.add_menu_sep  ( file_menu )
  zpa.add_menu_item ( file_menu, menu_callback, "_Save", "Save" )
  zpa.add_menu_item ( file_menu, menu_callback, "Save _As...", "Save As...", 'S', mask=gtk.gdk.CONTROL_MASK|gtk.gdk.SHIFT_MASK )
  zpa.add_menu_sep  ( file_menu )
  zpa.add_menu_item ( file_menu, menu_callback, "_Quit", "Quit", 'Q' )

  menu_bar.append ( file_item )
  menu_bar.show()


  ###########
  
  drawing_area = zpa.get_drawing_area()
  drawing_area.connect ( "expose_event", expose_callback, zpa )

  reset_callback ( zpa )

  ###########
  
  vbox.pack_start(drawing_area, True, True, 0)

  drawing_area.show()
  drawing_area.grab_focus()

  hbox = gtk.HBox ( True, 0 )
  hbox.show()
  vbox.pack_start ( hbox, False, False, 0 )

  redraw_button = gtk.Button("Reset")
  hbox.pack_start ( redraw_button, True, True, 0 )
  redraw_button.connect_object ( "clicked", reset_callback, zpa )
  redraw_button.show()


  window.show()

  zpa.set_cursor ( gtk.gdk.HAND2 )

  # gtk.idle_add ( reset_callback, zpa )

  gtk.main()
  return 0

if __name__ == '__main__':
  main()
