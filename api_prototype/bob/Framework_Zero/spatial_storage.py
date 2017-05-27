import math
import random

import pygtk
pygtk.require('2.0')
import gobject
import gtk


class locatable_object:
  def __init__ (self, x=0, y=0, c=(0.5,0.5,0.5)):
    self.x = x
    self.y = y
    self.c = c
    # This class can contain anything else
    self.highlight = False



class SpatialStorage:
  def __init__ ( self, xmin=0, ymin=0, xmax=1, ymax=1 ):
    self.xmin = xmin
    self.xmax = xmax
    self.ymin = ymin
    self.ymax = ymax
  def print_self ( self, depth=0 ):
    print ( "  "*depth + "Range = [" + str(self.xmin) + " < x < " + str(self.xmax) + "] [" + str(self.ymin) + " < y < " + str(self.ymax) + "]" )



class QuadTree(SpatialStorage):
  def __init__ ( self, xmin=0, ymin=0, xmax=1, ymax=1, max_objects=10 ):
    # print ( " Constructing a new QuadTree" )
    SpatialStorage.__init__(self, xmin=xmin, ymin=ymin, xmax=xmax, ymax=ymax) # Initialize parent first
    # Range: [min, max)
    self.max_objects = max_objects
    self.objects = []
    self.qne = None
    self.qnw = None
    self.qse = None
    self.qsw = None

  def split ( self ):
    left_xmin = self.xmin
    right_xmax = self.xmax
    left_xmax = left_xmin + ( (self.xmax - self.xmin) / 2.0 )
    right_xmin = left_xmax

    bot_ymin = self.ymin
    top_ymax = self.ymax
    bot_ymax = bot_ymin + ( (self.ymax - self.ymin) / 2.0 )
    top_ymin = bot_ymax

    self.qne = QuadTree ( right_xmin, top_ymin, right_xmax, top_ymax, self.max_objects )
    self.qnw = QuadTree ( left_xmin,  top_ymin, left_xmax,  top_ymax, self.max_objects )
    self.qse = QuadTree ( right_xmin, bot_ymin, right_xmax, bot_ymax, self.max_objects )
    self.qsw = QuadTree ( left_xmin,  bot_ymin, left_xmax,  bot_ymax, self.max_objects )
    
    original_objects = [ o for o in self.objects ]
    self.objects = []

    for o in original_objects:
      self.add_object ( o )

  def add_object ( self, o ):
    # print ( "Adding object at " + str(o.x) + "," + str(o.y) )
    if self.qne == None:
      # This is an unsubdivided (or leaf) node
      # print ( "  Found a leaf node when adding object at " + str(o.x) + "," + str(o.y) )
      if (len(self.objects) + 1) > self.max_objects:
        # One more would be too many, so subdivide
        self.split()
        self.add_object ( o )
      else:
        # It fits, so add it
        self.objects.append ( o )
    else:
      # This is already subdivided so find the right quadrant
      # o must have an x and y field
      if o.x < self.xmin + ( (self.xmax - self.xmin) / 2.0 ):
        # West
        if o.y < self.ymin + ( (self.ymax - self.ymin) / 2.0 ):
          # South
          self.qsw.add_object ( o )
        else:
          # North
          self.qnw.add_object ( o )
      else:
        # East
        if o.y < self.ymin + ( (self.ymax - self.ymin) / 2.0 ):
          # South
          self.qse.add_object ( o )
        else:
          # North
          self.qne.add_object ( o )


  def find_objects ( self, x, y ):
    # print ( "Finding objects near " + str(x) + "," + str(y) )
    if self.qne == None:
      # This is an unsubdivided (or leaf) node
      # print ( "  Found a leaf node" )
      return self.objects
    else:
      # This is already subdivided so find the right quadrant
      # o must have an x and y field
      if x < self.xmin + ( (self.xmax - self.xmin) / 2.0 ):
        # West
        if y < self.ymin + ( (self.ymax - self.ymin) / 2.0 ):
          # South
          return self.qsw.find_objects(x,y)
        else:
          # North
          return self.qnw.find_objects(x,y)
      else:
        # East
        if y < self.ymin + ( (self.ymax - self.ymin) / 2.0 ):
          # South
          return self.qse.find_objects(x,y)
        else:
          # North
          return self.qne.find_objects(x,y)


  def all_objects ( self, already_found ):
    # print ( "Finding all objects" )
    if self.qne == None:
      # This is an unsubdivided (or leaf) node
      # print ( "  Found a leaf node" )
      already_found.extend ( self.objects )
    else:
      # This is already subdivided so recurse through subquadrants
      self.qsw.all_objects(already_found)
      self.qnw.all_objects(already_found)
      self.qse.all_objects(already_found)
      self.qne.all_objects(already_found)


  def print_self ( self, depth=0 ):
    SpatialStorage.print_self(self, depth) # Call parent first
    # print ( "  "*depth + "Range = [" + str(self.xmin) + " < x < " + str(self.xmax) + "] [" + str(self.ymin) + " < y < " + str(self.ymax) + "]" )
    if self.qne != None:
      self.qne.print_self ( depth+1 )
      self.qnw.print_self ( depth+1 )
      self.qse.print_self ( depth+1 )
      self.qsw.print_self ( depth+1 )
    for o in self.objects:
      print ( "   " + "  "*depth + "Object at: " + str(o.x) + "," + str(o.y) )


  def draw ( self, canvas, pixmap, event, xminw, yminw, xmaxw, ymaxw, xoffset, xscale, yoffset, yscale ):
    drawable = canvas.window
    gc = canvas.get_style().fg_gc[gtk.STATE_NORMAL]
    #map_pos_neg_colors ( canvas, gc )

    # Draw the quadrant lines
    gc.foreground = canvas.get_colormap().alloc_color(30000, 30000, 30000)
    lx = xoffset + ( xscale * self.xmin )
    by = yoffset + ( yscale * self.ymin )

    rx = xoffset + ( xscale * self.xmax )
    ty = yoffset + ( yscale * self.ymax )

    pixmap.draw_rectangle ( gc, False, int(lx), int(by), int(rx-lx), int(ty-by) )

    #for q in self.quadrants:
    #  q.draw()

    # Draw all the objects that are not highlighted (background)
    for o in self.objects:
      if not o.highlight:
        cx = xoffset + ( xscale * o.x )
        cy = yoffset + ( yscale * o.y )
        gc.foreground = canvas.get_colormap().alloc_color(int(30000*o.c[0]),int(30000*o.c[1]),int(30000*o.c[2]))
        pixmap.draw_rectangle ( gc, True, int(cx)-2, int(cy)-2, 5, 5 )

    # Draw all the objects that are highlighted (foreground)
    for o in self.objects:
      if o.highlight:
        cx = xoffset + ( xscale * o.x )
        cy = yoffset + ( yscale * o.y )
        gc.foreground = canvas.get_colormap().alloc_color(int(65535*o.c[0]),int(65535*o.c[1]),int(65535*o.c[2]))
        pixmap.draw_rectangle ( gc, True, int(cx)-2, int(cy)-2, 5, 5 )

    gc.foreground = canvas.get_colormap().alloc_color(60000, 60000, 60000)
    if self.qne != None:
      # Draw each quadrant recursively
      self.qne.draw ( canvas, pixmap, event, (xmaxw-xminw)/2.0, (ymaxw-yminw)/2.0, xmaxw, ymaxw, xoffset, xscale, yoffset, yscale )
      self.qnw.draw ( canvas, pixmap, event, xminw, (ymaxw-yminw)/2.0, (xmaxw-xminw)/2.0, ymaxw, xoffset, xscale, yoffset, yscale )
      self.qse.draw ( canvas, pixmap, event, (xmaxw-xminw)/2.0, yminw, xmaxw, (ymaxw-yminw)/2.0, xoffset, xscale, yoffset, yscale )
      self.qsw.draw ( canvas, pixmap, event, xminw, yminw, (xmaxw-xminw)/2.0, (ymaxw-yminw)/2.0, xoffset, xscale, yoffset, yscale )




class SpatialHash(SpatialStorage):
  # Note that this could be heirarchical as well with SpatialHash objects as "leaves" in other SpatialHash objects
  def __init__ ( self, xmin=0, ymin=0, xmax=1, ymax=1, spatial_resolution=1.0 ):
    # print ( " Constructing a new QuadTree" )
    # Range: [min, max)
    SpatialStorage.__init__(self, xmin=xmin, ymin=ymin, xmax=xmax, ymax=ymax) # Initialize parent first
    self.spatial_resolution = spatial_resolution
    self.object_dict = {}

  def add_object ( self, o ):
    # o must have an x and y field
    xkey = int ( round ( o.x / self.spatial_resolution ) )
    ykey = int ( round ( o.y / self.spatial_resolution ) )
    key = (xkey, ykey)
    # print ( "Spatial Hash Key: " + key )
    if key in self.object_dict:
      self.object_dict[key]['objs'].append(o)
    else:
      self.object_dict[key] = { 'xkey':xkey, 'ykey':ykey, 'objs':[o] }

  def find_objects ( self, x, y ):
    xkey = int ( round ( x / self.spatial_resolution ) )
    ykey = int ( round ( y / self.spatial_resolution ) )
    key = (xkey, ykey)
    # print ( "Finding objects with Spatial Hash Key: " + key )
    if key in self.object_dict:
      # print ( "Found some" )
      return self.object_dict[key]['objs']
    else:
      # print ( "Found none" )
      return []

  def all_objects ( self, already_found ):
    # print ( "Finding all objects" )
    for k in self.object_dict:
      olist = self.object_dict[k]['objs']
      already_found.extend ( olist )

  def print_self ( self, depth=0 ):
    SpatialStorage.print_self(self, depth) # Call parent first
    for k in sorted(self.object_dict):
      olist = self.object_dict[k]['objs']
      print ( "  " + "  "*depth + "Spatial Key: " + str(k) )
      for o in olist:
        print ( "    " + "  "*depth + "Object at: " + str(o.x) + "," + str(o.y) )

  def draw ( self, canvas, pixmap, event, xminw, yminw, xmaxw, ymaxw, xoffset, xscale, yoffset, yscale ):
    # print ("Drawing Spatial Hash")
    drawable = canvas.window
    gc = canvas.get_style().fg_gc[gtk.STATE_NORMAL]
    #map_pos_neg_colors ( canvas, gc )

    # Draw the cell bounds
    gc.foreground = canvas.get_colormap().alloc_color(30000, 30000, 30000)

    lx = xoffset + ( xscale * self.xmin )
    by = yoffset + ( yscale * self.ymin )

    rx = xoffset + ( xscale * self.xmax )
    ty = yoffset + ( yscale * self.ymax )

    pixmap.draw_rectangle ( gc, False, int(lx), int(by), int(rx-lx), int(ty-by) )

    # Draw bounds around all objects
    gc.foreground = canvas.get_colormap().alloc_color(30000, 30000, 30000)
    for k in self.object_dict:
      olist = self.object_dict[k]['objs']
      for o in olist:
        res = self.spatial_resolution
        cx = xoffset + int ( xscale * round(o.x/res) * res )
        cy = yoffset + int ( yscale * round(o.y/res) * res )
        pixmap.draw_rectangle ( gc, False, int(cx-(xscale*res/2.0)), int(cy-(yscale*res/2.0)), int(xscale*res), int(yscale*res) )

    # Draw all the objects that are not highlighted (background)
    for k in self.object_dict:
      olist = self.object_dict[k]['objs']
      for o in olist:
        if not o.highlight:
          cx = xoffset + ( xscale * o.x )
          cy = yoffset + ( yscale * o.y )
          gc.foreground = canvas.get_colormap().alloc_color(int(30000*o.c[0]),int(30000*o.c[1]),int(30000*o.c[2]))
          pixmap.draw_rectangle ( gc, True, int(cx)-2, int(cy)-2, 5, 5 )

    # Draw all the objects that are highlighted (foreground)
    for k in self.object_dict:
      olist = self.object_dict[k]['objs']
      for o in olist:
        if o.highlight:
          cx = xoffset + ( xscale * o.x )
          cy = yoffset + ( yscale * o.y )
          gc.foreground = canvas.get_colormap().alloc_color(int(65535*o.c[0]),int(65535*o.c[1]),int(65535*o.c[2]))
          pixmap.draw_rectangle ( gc, True, int(cx)-2, int(cy)-2, 5, 5 )




