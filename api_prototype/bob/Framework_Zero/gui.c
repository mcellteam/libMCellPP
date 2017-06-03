// https://developer.gnome.org/gtk-tutorial/2.90/x111.html

#include <stdlib.h>
#include <stdio.h>
#include <gtk/gtk.h>

static gboolean button_press ( GtkWidget *, GdkEvent * );
static void menuitem_response ( gchar * );



typedef struct shape_struct {
  char type;
  double x, y, w, h;
  long color;
  struct shape_struct *next;
} shape;

static shape *shapes = NULL;


static gboolean expose_event_callback( GtkWidget *widget, GdkEventExpose *event, gpointer data )
{
  g_print ( "Got an expose event with data = %d\n", (int)data );
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
    gdk_draw_arc ( widget->window, gc, FALSE, sx, sy, sw, sh, 0, 360*64 );
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

  gtk_init (&argc, &argv);

  window = gtk_window_new (GTK_WINDOW_TOPLEVEL);
  // gtk_widget_set_size_request ( GTK_WIDGET ( window ), 200, 100 );
  gtk_window_set_title ( GTK_WINDOW ( window ), "2D Diffusion" );
  g_signal_connect ( window, "delete-event", G_CALLBACK ( gtk_main_quit ), NULL );


  vbox = gtk_vbox_new ( FALSE, 0 );
  gtk_container_add ( GTK_CONTAINER ( window ), vbox );
  gtk_widget_show ( vbox );



  menu = gtk_menu_new();

  menu_item = gtk_menu_item_new_with_label ( "Toggle Legend" );
  gtk_menu_shell_append ( GTK_MENU_SHELL ( menu ), menu_item );
  g_signal_connect_swapped ( menu_item, "activate", G_CALLBACK ( menuitem_response ), (gpointer) g_strdup("ToggleLegend") );
  gtk_widget_show (menu_item);
  options_menu = gtk_menu_item_new_with_label ( "Options" );
  gtk_widget_show ( options_menu );
  gtk_menu_item_set_submenu ( GTK_MENU_ITEM (options_menu), menu );


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

  menu_bar = gtk_menu_bar_new();
  gtk_menu_shell_append ( GTK_MENU_SHELL ( menu_bar ), options_menu );
  gtk_menu_shell_append ( GTK_MENU_SHELL ( menu_bar ), speed_menu );



  gtk_box_pack_start ( GTK_BOX(vbox), menu_bar, FALSE, FALSE, 2 );
  gtk_widget_show ( menu_bar );


  drawing_area = gtk_drawing_area_new();
  g_signal_connect (drawing_area, "expose_event", G_CALLBACK (expose_event_callback), (gpointer)3);
  gtk_widget_set_size_request ( drawing_area, (gint)600, (gint)500 );
  gtk_box_pack_start ( GTK_BOX(vbox), drawing_area, TRUE, TRUE, 0 );
  gtk_widget_show ( drawing_area );



  hbox = gtk_hbox_new ( TRUE, 0 );
  gtk_box_pack_start (GTK_BOX (vbox), hbox, FALSE, FALSE, 0);

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

  gtk_widget_show ( hbox );

  gtk_widget_show  (window);

  gtk_main ();

  return 0;
}

static gboolean button_press ( GtkWidget *widget, GdkEvent *event ) {
  if ( event->type == GDK_BUTTON_PRESS ) {
    GdkEventButton *bevent = (GdkEventButton *) event;
    gtk_menu_popup ( GTK_MENU (widget), NULL, NULL, NULL, NULL, bevent->button, bevent->time );
    return TRUE;
  }
  return FALSE;
}

static void menuitem_response ( gchar *string ) {
  printf ( "%s\n", string );
}
