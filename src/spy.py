# -*- mode: python; coding: utf-8; -*-

import gtk, gtk.gdk as gdk
import gobject
import re
import threading

import libsl
from slog.config import SlogConf
from slog.TransPanel import TransView

class Spy:
	def __init__(self):
		self.timer = 0;
		self.prev_selection = ""
		self.clipboard = gtk.clipboard_get(gdk.SELECTION_PRIMARY)
		self.conf = SlogConf()
		self.spy_view = None

	#Thread function
	def __fuzzy_search(self, word):
		all_lines = []
		used_dicts = self.conf.get_spy_dicts()
		for dic in used_dicts:
			filename = self.conf.get_dic_path(dic)
			lines = libsl.find_word(word, libsl.SL_FIND_FUZZY, filename)
			if lines != []:
				html = []
				html.append(libsl.get_dict_html_block(filename))
				html.append("<dl>")
				for item in lines:
					html.append("<li><a href='%s|%s'>%s</a></li>" % (dic, item, item))
				html.append("</dl>")
				all_lines.append("".join(html))

			# Cancelled..
			if not self.spy_view.get_property("visible"):
				return

		translate = "<body>%s</body>" % ("".join(all_lines))
		gobject.idle_add(self.spy_view.set_translate, word, translate)

	def __get_translate(self, word):
		all_lines = []
		used_dicts = self.conf.get_spy_dicts()
		for dic in used_dicts:
			filename = self.conf.get_dic_path(dic)
			lines = libsl.find_word(word, libsl.SL_FIND_MATCH, filename)
			if lines != []:
				all_lines.append("".join(lines))
		return all_lines

	def __on_clipboard_text_received(self, clipboard, text, data):
		if text is None:
			return

		selection = text.lower().strip()
		if selection == "" or selection == self.prev_selection:
			return
		self.prev_selection = selection

		#TODO: remove characters like , . ;
		word = selection
		all_lines = self.__get_translate(word)

		if len(all_lines) == 0:
			translate = """
				<body>This word not found.<br/>
				<span style='color:#4c4c4c; font-size:80%'>Searching similar words...</span>
				</body>"""
			thread = threading.Thread(target = self.__fuzzy_search, args = (word, ))
			thread.start()
		else:
			translate = "<body>%s</body>" % ("".join(all_lines))

		self.spy_view.set_translate(word, translate)
		self.spy_view.popup()

	def __on_timer_timeout(self):
		if self.timer == 0:
			return False

		display = gdk.display_get_default()
		screen, x, y, mask = display.get_pointer()
		mask = mask & ((1<<13)-1)

		if mask & self.conf.get_mod_key():
			if self.spy_view.get_property("visible") is False:
				self.clipboard.request_text(self.__on_clipboard_text_received)
		else:
			if self.spy_view.get_property("visible"):
				self.spy_view.hide()

		return True

	def __on_url_click(self, view, url, type_):
		dic, word = url.split("|")

		filename = self.conf.get_dic_path(dic)
		lines = libsl.find_word(word, libsl.SL_FIND_MATCH, filename)

		translate = "<body>%s</body>" % ("".join(lines))
		self.spy_view.set_translate(word, translate)

	def start(self):
		self.spy_view = SpyView()
		self.spy_view.set_url_callback(self.__on_url_click)
		self.clipboard.set_text("")
		self.prev_selection = ""
		self.timer = gobject.timeout_add(300, self.__on_timer_timeout)

	def stop(self):
		self.timer = 0
		self.spy_view.destroy()

class SpyView(gtk.Window):
	def __init__(self):
		gtk.Window.__init__(self, gtk.WINDOW_POPUP)

		self.set_app_paintable(True)
		self.set_resizable(False)
		self.set_size_request(320, 240)
		self.set_name("gtk-tooltips")
		self.connect("expose_event", self.__on_expose_event)

		self.__tv = TransView()
		self.add(self.__tv)
		self.__tv.show()

	def __on_expose_event(self, window, event):
		w, h = window.size_request()
		window.style.paint_flat_box(window.window, gtk.STATE_NORMAL, gtk.SHADOW_OUT,
									None, window, "tooltip", 0, 0, w, h)
		return False

	def __get_pos(self):
		display = gdk.display_get_default()
		screen, x, y, mask = display.get_pointer()
		w = screen.get_width()
		h = screen.get_height()

		if (x + 320 + 5) > w:
			x = (w - 320 - 8)

		if (y + 240 + 5) > h:
			y = (y - 240 - 2)

		return (x+8), (y+2)

	def set_url_callback(self, callback):
		self.__tv.htmlview.connect("url-clicked", callback)

	def set_translate(self, word, translate):
		self.__tv.set_translate(word, translate)

	def popup(self):
		x, y = self.__get_pos()
		self.move(x, y)
		self.show()

