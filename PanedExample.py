import gi
import sqlparse

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Pango

settings = Gtk.Settings.get_default()
settings.set_property("gtk-theme-name", "Adwaita")
settings.set_property("gtk-application-prefer-dark-theme", False)


class MyWindow(Gtk.ApplicationWindow):
    def __init__(self, app):
        Gtk.Window.__init__(self, title="Separator Example", application=app)

        hpaned = Gtk.Paned(orientation=Gtk.Orientation.VERTICAL)
                

        self.frame_sql_query = self.create_sql_frame()
        self.frame_res_query = self.create_res_frame()

        hpaned.add1(self.frame_sql_query)
        hpaned.add2(self.frame_res_query)

        self.maximize()
        self.add(hpaned)

    def create_res_frame(self):
        frame_res_query = Gtk.Frame.new(None)                        
        return frame_res_query

    def create_text_view(self):
        textview = Gtk.TextView()
        self.textbuffer = textview.get_buffer()
        self.textbuffer.set_text("SELECT CAMPO1, CAMPO2, CAMPO3, CAMPO4 FROM SYSIBM.TABLES WHERE TABLE_NAME = 'XXX' AND COLUMN_NAME = 'YY';")
        self.tag_bold = self.textbuffer.create_tag("bold", weight=Pango.Weight.BOLD)
        self.tag_italic = self.textbuffer.create_tag("italic", style=Pango.Style.ITALIC)

        monospace = self.textbuffer.create_tag("orange_bg", family="monospace")
        size = self.textbuffer.create_tag("font_size", size=12000)

        start = self.textbuffer.get_start_iter()
        end = self.textbuffer.get_end_iter()
        self.textbuffer.apply_tag(monospace, start, end)
        self.textbuffer.apply_tag(size, start, end)
        return textview

    def create_scroll_window(self):        
        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.set_hexpand(True)
        scrolledwindow.set_vexpand(True)
        textview = self.create_text_view()
        scrolledwindow.add(textview)
        return scrolledwindow

    def create_sql_frame_grid(self):
        grid = Gtk.Grid.new()
        btn_formatear = Gtk.Button.new_with_label("Formatear")
        btn_ejecutar = Gtk.Button.new_with_label("Ejecutar")
        scrolled_window = self.create_scroll_window()

        start = self.textbuffer.get_start_iter()
        end = self.textbuffer.get_end_iter()
        text = self.textbuffer.get_text(start, end, False)
        btn_formatear.connect("button-press-event", self.do_button, text)

        grid.attach(btn_formatear, 0, 0, 1, 1)
        grid.attach(btn_ejecutar, 1, 0, 1, 1)
        grid.attach(scrolled_window, 0, 1, 2, 1)
        return grid

    def do_button(self, btn, event, value):
        print(value)
        formatted_value = sqlparse.format(value, reindent=True, keyword_case='upper')
        print(formatted_value)
        self.textbuffer.set_text(formatted_value)


    def create_sql_frame(self):
        frame_sql_query = Gtk.Frame.new(None)
        grid = self.create_sql_frame_grid()

        frame_sql_query.add(grid)
        return frame_sql_query


class MyApplication(Gtk.Application):
    def __init__(self):
        Gtk.Application.__init__(self)

    def do_activate(self):
        win = MyWindow(self)
        win.show_all()
