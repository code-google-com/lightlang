# -*- mode: python; coding: utf-8; -*-

import gtk, gobject

class SideBar(gtk.VBox):
	def __init__(self):
		gtk.VBox.__init__(self, False, 4)

		self.tabs = []
		self.notebook = gtk.Notebook()
		self.notebook.set_show_tabs(False)
		self.pack_start(self.notebook, True, True, 0)

		self.combo_box = gtk.combo_box_new_text()
		self.combo_box.connect("changed", self.on_engine_selected)
		self.pack_start(self.combo_box, False, True, 0)

	def append_page(self, title, view):
		self.combo_box.append_text(title)
		self.notebook.append_page(view)
		self.tabs.append(view)

	def on_engine_selected(self, widget, data=None):
		index = widget.get_active()
		self.notebook.set_current_page(index)
		view = self.tabs[index]
		view.grab_focus()

	def get_active(self):
		return self.combo_box.get_active()

	def set_active(self, index):
		self.combo_box.set_active(index)


