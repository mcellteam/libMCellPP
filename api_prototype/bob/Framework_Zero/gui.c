// https://developer.gnome.org/gtk-tutorial/2.90/x111.html

#include <stdlib.h>
#include <stdio.h>
#include <gtk/gtk.h>
#include <math.h>

static void menuitem_response ( gchar * );

typedef struct shape_struct {
  char type;
  double x, y, w, h;
  long color;
  struct shape_struct *next;
} shape;

static shape *shapes = NULL;

typedef struct zoom_pan_area_struct {
  double x_offset;
  double y_offset;
  double x_scale;
  double y_scale;
  int aspect_fixed; // bool
  long scroll_count;
  double scroll_factor;
  double zoom_scale;
  int dragging; // bool
  int last_x;
  int last_y;
} zoom_pan_area;

static zoom_pan_area zpa;

static void set_zoom_pan_defaults() {
  zpa.x_offset = 0.0;
  zpa.y_offset = 0.0;
  zpa.x_scale = 1.0;
  zpa.y_scale = 1.0;
  zpa.aspect_fixed = TRUE;
  zpa.scroll_count = 0;
  zpa.scroll_factor = 1.25;
  zpa.zoom_scale = 1.0;
  zpa.dragging = FALSE;
  zpa.last_x = 0;
  zpa.last_y = 0;
}

static void set_x_scale ( double user_x1, int win_x1, double user_x2, int win_x2 ) {
  zpa.x_scale  = (win_x2 - win_x1) / (user_x2 - user_x1);
  zpa.x_offset = win_x1 - ( user_x1 * zpa.x_scale );
}

static void set_y_scale ( double user_y1, int win_y1, double user_y2, int win_y2 ) {
  zpa.y_scale  = (win_y2 - win_y1) / (user_y2 - user_y1);
  zpa.y_offset = win_y1 - ( user_y1 * zpa.y_scale );
}

static double wx ( double user_x ) {
  return ( zpa.x_offset + (user_x * zpa.x_scale * zpa.zoom_scale ) );
}
static double wy ( double user_y ) {
  return ( zpa.y_offset + (user_y * zpa.y_scale * zpa.zoom_scale ) );
}
static double ww ( double user_w ) {
  return ( user_w * zpa.x_scale * zpa.zoom_scale );
}
static double wh ( double user_h ) {
  return ( user_h * zpa.y_scale * zpa.zoom_scale );
}

static int wxi ( double user_x ) {
  return ( (int)(round(wx(user_x))) );
}
static int wyi ( double user_y ) {
  return ( (int)(round(wy(user_y))) );
}
static int wwi ( double user_w ) {
  return ( (int)(round(ww(user_w))) );
}
static int whi ( double user_h ) {
  return ( (int)(round(wh(user_h))) );
}

static double x ( int win_x ) {
  return ( (win_x - zpa.x_offset) / (zpa.x_scale * zpa.zoom_scale) );
}
static double y ( int win_y ) {
  return ( (win_y - zpa.y_offset) / (zpa.y_scale * zpa.zoom_scale) );
}
static double w ( int win_w ) {
  return ( win_w / (zpa.x_scale * zpa.zoom_scale) );
}
static double h ( int win_h ) {
  return ( win_h / (zpa.y_scale * zpa.zoom_scale) );
}

static void zoom_at_point ( int zoom_delta, int at_x, int at_y ) {
  // First save the mouse location in user space before the zoom
  double user_x_at_zoom = x(at_x);
  double user_y_at_zoom = y(at_y);
  // Perform the zoom by changing the zoom scale
  zpa.scroll_count += zoom_delta;
  zpa.zoom_scale = pow (zpa.scroll_factor, zpa.scroll_count);
  // Get the new window coordinates of the previously saved user space location
  int win_x_after_zoom = wx ( user_x_at_zoom );
  int win_y_after_zoom = wy ( user_y_at_zoom );
  // Adjust the offsets (window coordinates) to keep user point at same location
  zpa.x_offset += at_x - win_x_after_zoom;
  zpa.y_offset += at_y - win_y_after_zoom;
}


static gboolean mouse_scroll_callback( GtkWidget *widget, GdkEventScroll *event, gpointer data )
{
  // g_print ( "Got a mouse scroll event with data = %ld\n", (long)data );
  // g_print ( "  location = %lg,%lg", event->x, event->y );
  if (event->direction == GDK_SCROLL_UP) {
    // g_print ( "    up\n" );
    zoom_at_point (  1, event->x, event->y );
  } else if (event->direction == GDK_SCROLL_DOWN) {
    // g_print ( "    down\n" );
    zoom_at_point ( -1, event->x, event->y );
  }
  gdk_window_invalidate_rect (widget->window, NULL, TRUE);
  return TRUE;
}




static gboolean button_press_callback ( GtkWidget *widget, GdkEventButton *event ) {
  if (event->button == 1) {
    // g_print ( "button press\n" );
    zpa.last_x = event->x;
    zpa.last_y = event->y;
    zpa.dragging = TRUE;
  }
  gdk_window_invalidate_rect (widget->window, NULL, TRUE);
  return TRUE;  // Event has been handled, do not propagate further
}

static gboolean button_release_callback ( GtkWidget *widget, GdkEventButton *event ) {
  if (event->button == 1) {
    // g_print ( "button release\n" );
    zpa.x_offset += (event->x - zpa.last_x);
    zpa.y_offset += (event->y - zpa.last_y);
    zpa.last_x = event->x;
    zpa.last_y = event->y;
    zpa.dragging = FALSE;
  }
  gdk_window_invalidate_rect (widget->window, NULL, TRUE);
  return TRUE;  // Event has been handled, do not propagate further
}

static gboolean mouse_motion_callback( GtkWidget *widget, GdkEventMotion *event, gpointer data ) {
  int x, y;
  GdkModifierType state;

  if (event->is_hint) {
    gdk_window_get_pointer (event->window, &x, &y, &state);
  } else {
    x = event->x;
    y = event->y;
    state = event->state;
  }

  // g_print ( "Got a mouse motion event with data = %ld\n", (long)data );
  // g_print ( "  location = %lg,%lg\n", event->x, event->y );
  // g_print ( "  state = %d\n", state );

  if (state == 0) {
  } else if (state == 256) {
    zpa.x_offset += (x - zpa.last_x);
    zpa.y_offset += (y - zpa.last_y);
    zpa.last_x = x;
    zpa.last_y = y;
    gdk_window_invalidate_rect (widget->window, NULL, TRUE);
  }
  return TRUE;
}

static gboolean expose_event_callback( GtkWidget *widget, GdkEventExpose *event, gpointer data )
{
  // g_print ( "Got an expose event with data = %ld\n", (long)data );
  /* Redraw the screen from the backing pixmap */
  //gdk_draw_drawable (widget->window, widget->style->fg_gc[gtk_widget_get_state (widget)], pixmap,
  //                   event->area.x, event->area.y, event->area.x, event->area.y, event->area.width, event->area.height);
  GdkGC *gc;
  gc = gdk_gc_new ( widget->window );
  GdkColormap *colormap;
  colormap = gtk_widget_get_colormap(widget);
  // colormap = gdk_colormap_get_system();
  GdkColor color;

  gdk_draw_rectangle (widget->window, widget->style->black_gc, TRUE, 0, 0, widget->allocation.width, widget->allocation.height);
  // gdk_draw_arc ( widget->window, widget->style->white_gc, FALSE, 0, 0, widget->allocation.width, widget->allocation.height, 0, 360*64 );
  shape *next_shape;
  next_shape = shapes;
  int sx, sy, sw, sh;
  while (next_shape != NULL) {
    sx = next_shape->x * widget->allocation.width;
    sy = next_shape->y * widget->allocation.height;
    sw = next_shape->w * widget->allocation.width;
    sh = next_shape->h * widget->allocation.height;
    color.red   = ((next_shape->color >> 16) & 0x00ffL) << 8;
    color.green = ((next_shape->color >>  8) & 0x00ffL) << 8;
    color.blue  = ((next_shape->color >>  0) & 0x00ffL) << 8;
    gdk_colormap_alloc_color ( colormap, &color, FALSE, TRUE );
    gdk_gc_set_foreground ( gc, &color );
    // g_print ( "  Drawing Circle: x = %d, y = %d, w = %d, h = %d\n", sx, sy, sw, sh );
    gdk_draw_arc ( widget->window, gc, FALSE, wxi(sx), wyi(sy), ww(sw), wh(sh), 0, 360*64 );
    next_shape = next_shape->next;
  }
  return TRUE;
}

static void button_callback ( GtkWidget *widget, gpointer data )
{
  g_print ("The %s button was pressed\n", (char *)data);
  if (strcmp((char *)data,"Circle") == 0) {
    g_print ("Adding a circle!!\n");
    shape *new_shape = (shape *) malloc ( sizeof(shape) );
    new_shape->type = 'c';
    double x = drand48();
    double y = drand48();
    double r = drand48() * 0.5;
    while (r < 0.01) {
      r = r + 0.01;
    }
    while ((x+r) >= 1.0) {
      x = x * 0.9;
      r = r * 0.9;
    }
    while ((y+r) >= 1.0) {
      y = y * 0.9;
      r = r * 0.9;
    }
    new_shape->x = x;
    new_shape->y = y;
    new_shape->w = r;
    new_shape->h = r;
    new_shape->color = rand() % 256;
    new_shape->color = (new_shape->color << 8) | rand() % 256;
    new_shape->color = (new_shape->color << 8) | rand() % 256;
    new_shape->next = shapes;
    g_print ( "  New Circle: x = %f, y = %f, w = %f, h = %f\n", new_shape->x, new_shape->y, new_shape->w, new_shape->h );
    shapes = new_shape;
    // gtk_widget_queue_draw (widget);
    gdk_window_invalidate_rect (widget->window, NULL, TRUE);
    //gtk_widget_queue_draw_area ( widget, 0, 0, widget->allocation.width, widget->allocation.height );

    // gdk_draw_arc ( pixmap, widget->style->white_gc, TRUE, 10, 10, 60, 60, 0, 360*64 );
    // gdk_draw_rectangle (pixmap, widget->style->white_gc, TRUE, 10, 10, 60, 60);
    // gtk_widget_queue_draw (widget);
  }
  //gdk_draw_rectangle (pixmap, widget->style->white_gc, TRUE,
	//	      update_rect.x, update_rect.y, update_rect.width, update_rect.height);
  //gtk_widget_queue_draw_area (widget,
	//	              update_rect.x, update_rect.y,
	//	              update_rect.width, update_rect.height);

}



int main( int   argc, char *argv[] )
{
  GtkWidget *window;
  GtkWidget *menu;
  GtkWidget *menu_bar;
  GtkWidget *options_menu;
  GtkWidget *speed_menu;
  GtkWidget *menu_item;
  GtkWidget *vbox;
  GtkWidget *drawing_area;
  GtkWidget *hbox;
  GtkWidget *button;
  char buf[128];
  int i;

  set_zoom_pan_defaults();
  set_x_scale ( 0.0, 0, 100.0, 100 );
  set_x_scale ( 0.0, 0, 100.0, 100 );

  gtk_init (&argc, &argv);

  // Create a top-level GTK window
  window = gtk_window_new (GTK_WINDOW_TOPLEVEL);
  gtk_window_set_title ( GTK_WINDOW ( window ), "2D Diffusion" );

  g_signal_connect ( window, "delete-event", G_CALLBACK ( gtk_main_quit ), NULL );


  // Create a vertical box to hold the menu, drawing area, and buttons
  vbox = gtk_vbox_new ( FALSE, 0 );
  gtk_container_add ( GTK_CONTAINER ( window ), vbox );
  gtk_widget_show ( vbox );


  // Create a menu bar and add it to the vertical box
  menu_bar = gtk_menu_bar_new();
  gtk_box_pack_start ( GTK_BOX(vbox), menu_bar, FALSE, FALSE, 2 );

  // Create an "Options" menu
  menu = gtk_menu_new();
  menu_item = gtk_menu_item_new_with_label ( "Toggle Legend" );
  gtk_menu_shell_append ( GTK_MENU_SHELL ( menu ), menu_item );
  g_signal_connect_swapped ( menu_item, "activate", G_CALLBACK ( menuitem_response ), (gpointer) g_strdup("ToggleLegend") );
  gtk_widget_show (menu_item);
  options_menu = gtk_menu_item_new_with_label ( "Options" );
  gtk_widget_show ( options_menu );
  gtk_menu_item_set_submenu ( GTK_MENU_ITEM (options_menu), menu );


  // Create a "Speed" menu
  menu = gtk_menu_new();

  menu_item = gtk_menu_item_new_with_label ( "Fast" );
  gtk_menu_shell_append ( GTK_MENU_SHELL ( menu ), menu_item );
  g_signal_connect_swapped ( menu_item, "activate", G_CALLBACK ( menuitem_response ), (gpointer) g_strdup("Fast") );
  gtk_widget_show (menu_item);

  menu_item = gtk_menu_item_new_with_label ( "Medium" );
  gtk_menu_shell_append ( GTK_MENU_SHELL ( menu ), menu_item );
  g_signal_connect_swapped ( menu_item, "activate", G_CALLBACK ( menuitem_response ), (gpointer) g_strdup("Medium") );
  gtk_widget_show (menu_item);

  menu_item = gtk_menu_item_new_with_label ( "Slow" );
  gtk_menu_shell_append ( GTK_MENU_SHELL ( menu ), menu_item );
  g_signal_connect_swapped ( menu_item, "activate", G_CALLBACK ( menuitem_response ), (gpointer) g_strdup("Slow") );
  gtk_widget_show (menu_item);

  speed_menu = gtk_menu_item_new_with_label ( "Speed" );
  gtk_widget_show ( speed_menu );
  gtk_menu_item_set_submenu ( GTK_MENU_ITEM (speed_menu), menu );

  // Append the menus to the menu bar itself
  gtk_menu_shell_append ( GTK_MENU_SHELL ( menu_bar ), options_menu );
  gtk_menu_shell_append ( GTK_MENU_SHELL ( menu_bar ), speed_menu );

  // Show the menu bar itself (everything must be shown!!)
  gtk_widget_show ( menu_bar );


  // Create the drawing area
  drawing_area = gtk_drawing_area_new();
  g_signal_connect ( drawing_area, "expose_event", G_CALLBACK (expose_event_callback), (gpointer)3 );
  g_signal_connect ( drawing_area, "scroll_event", G_CALLBACK (mouse_scroll_callback), (gpointer)3 );
  g_signal_connect ( drawing_area, "button_press_event", G_CALLBACK (button_press_callback), (gpointer)3 );
  g_signal_connect ( drawing_area, "button_release_event", G_CALLBACK (button_release_callback), (gpointer)3 );
  g_signal_connect ( drawing_area, "motion_notify_event", G_CALLBACK (mouse_motion_callback), (gpointer)3 );
  gtk_widget_set_events (drawing_area, (gint)(GDK_EXPOSURE_MASK | GDK_SCROLL_MASK | GDK_BUTTON_PRESS_MASK | GDK_BUTTON_RELEASE_MASK | GDK_POINTER_MOTION_MASK | GDK_POINTER_MOTION_HINT_MASK) );
  gtk_widget_set_size_request ( drawing_area, (gint)600, (gint)500 );
  gtk_box_pack_start ( GTK_BOX(vbox), drawing_area, TRUE, TRUE, 0 );
  gtk_widget_show ( drawing_area );




  // Create a horizontal box to hold application buttons
  hbox = gtk_hbox_new ( TRUE, 0 );
  gtk_box_pack_start (GTK_BOX (vbox), hbox, FALSE, FALSE, 0);
  gtk_widget_show ( hbox );

  // Add some application specific buttons and their callbacks

  button = gtk_button_new_with_label ( "Circle" );
  g_signal_connect (button, "clicked", G_CALLBACK (button_callback), (gpointer)"Circle");
  gtk_box_pack_start (GTK_BOX (hbox), button, TRUE, TRUE, 0);
  gtk_widget_show (button);

  button = gtk_button_new_with_label ( "Step" );
  g_signal_connect (button, "clicked", G_CALLBACK (button_callback), (gpointer)"Step");
  gtk_box_pack_start (GTK_BOX (hbox), button, TRUE, TRUE, 0);
  gtk_widget_show (button);

  button = gtk_button_new_with_label ( "Dump" );
  g_signal_connect (button, "clicked", G_CALLBACK (button_callback), (gpointer)"Dump");
  gtk_box_pack_start (GTK_BOX (hbox), button, TRUE, TRUE, 0);
  gtk_widget_show (button);

  button = gtk_button_new_with_label ( "Reset" );
  g_signal_connect (button, "clicked", G_CALLBACK (button_callback), (gpointer)"Reset");
  gtk_box_pack_start (GTK_BOX (hbox), button, TRUE, TRUE, 0);
  gtk_widget_show (button);

  // Show the main window
  gtk_widget_show  (window);

  // Turn control over to GTK to run everything from here onward.
  gtk_main ();

  return 0;
}


static void menuitem_response ( gchar *string ) {
  printf ( "%s\n", string );
}
