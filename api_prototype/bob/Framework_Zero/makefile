ALL = gui
all: $(ALL)

# This is how pkg_config would be defined automatically
pkg_config = `pkg-config --cflags --libs gtk+-2.0`

# This alternate syntax is from the man page, but doesn't work in this context
# pkg_config = $(pkg-config --cflags --libs gtk+-2.0)

# This is what it happens to be on a particular machine
#pkg_config = -pthread -I/usr/include/gtk-2.0 -I/usr/lib/x86_64-linux-gnu/gtk-2.0/include -I/usr/include/gio-unix-2.0/ \
#             -I/usr/include/cairo -I/usr/include/pango-1.0 -I/usr/include/atk-1.0 -I/usr/include/cairo \
#             -I/usr/include/pixman-1 -I/usr/include/libpng12 -I/usr/include/gdk-pixbuf-2.0 -I/usr/include/libpng12 \
#             -I/usr/include/pango-1.0 -I/usr/include/harfbuzz -I/usr/include/pango-1.0 -I/usr/include/glib-2.0 \
#             -I/usr/lib/x86_64-linux-gnu/glib-2.0/include -I/usr/include/freetype2 -lgtk-x11-2.0 -lgdk-x11-2.0 \
#             -lpangocairo-1.0 -latk-1.0 -lcairo -lgdk_pixbuf-2.0 -lgio-2.0 -lpangoft2-1.0 -lpango-1.0 -lgobject-2.0 \
#             -lglib-2.0 -lfontconfig -lfreetype


gui: gui.c makefile
	gcc gui.c -o gui $(pkg_config)

.PHONY: clean
clean:
	rm -f $(ALL)
	rm -f core
	rm -f *.o *.so
	rm -f *.pyc
	rm -f *~

test:
	./gui
