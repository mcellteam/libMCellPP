// https://developer.gnome.org/gtk-tutorial/2.90/x111.html

#include <stdio.h>
#include <gtk/gtk.h>

static gboolean button_press ( GtkWidget *, GdkEvent * );
static void menuitem_response ( gchar * );

int main( int   argc, char *argv[] )
{
  GtkWidget *window;
  GtkWidget *menu;
  GtkWidget *menu_bar;
  GtkWidget *options_menu;
  GtkWidget *speed_menu;
  GtkWidget *menu_item;
  GtkWidget *vbox;
  GtkWidget *button;
  char buf[128];
  int i;

  gtk_init (&argc, &argv);

  window = gtk_window_new (GTK_WINDOW_TOPLEVEL);
  gtk_widget_set_size_request ( GTK_WIDGET ( window ), 200, 100 );
  gtk_window_set_title ( GTK_WINDOW ( window ), "2D Diffusion" );
  g_signal_connect ( window, "delete-event", G_CALLBACK ( gtk_main_quit ), NULL );



  menu = gtk_menu_new();

  menu_item = gtk_menu_item_new_with_label ( "Toggle Legend" );
  gtk_menu_shell_append ( GTK_MENU_SHELL ( menu ), menu_item );
  g_signal_connect_swapped ( menu_item, "activate", G_CALLBACK ( menuitem_response ), (gpointer) g_strdup("Toggle Legend") );
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



  vbox = gtk_vbox_new ( FALSE, 0 );
  gtk_container_add ( GTK_CONTAINER ( window ), vbox );
  gtk_widget_show ( vbox );

  gtk_box_pack_start ( GTK_BOX(vbox), menu_bar, FALSE, FALSE, 2 );
  gtk_widget_show ( menu_bar );

  button = gtk_button_new_with_label ( "press me" );
  g_signal_connect_swapped ( button, "event",  G_CALLBACK ( button_press ), menu );
  gtk_widget_show ( button );

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
