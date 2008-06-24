# -*- mode: python; coding: utf-8; -*-

import gtk

class MyNotebook(gtk.Notebook):
	def __init__(self):
		gtk.Notebook.__init__(self)
		self.tabs = []
	
	def __create_tab_header(self, label, page):
		hbox = gtk.HBox(False, 2)
		hbox.pack_start(label, False, False);

		img = gtk.Image()
		img.set_from_stock(gtk.STOCK_CLOSE, gtk.ICON_SIZE_MENU)
		close = gtk.Button()
		close.set_focus_on_click(False)
		close.set_relief(gtk.RELIEF_NONE)
		close.add(img)
		close.connect("clicked", self.on_close_tab_clicked, page)

		hbox.pack_start(close, False, False);
		hbox.show_all()
		return hbox

	def on_close_tab_clicked(self, widget, page):

		# Always show one tab		
		if len(self.tabs) == 1:
			return

		idx = self.page_num(page)
		self.remove_page(idx)
		self.tabs.remove(page)
		page.destroy()

	def add_page(self, label, page):
		self.append_page(page)
		self.tabs.append(page)
		page.show()

		header = self.__create_tab_header(label, page)
		self.set_tab_label(page, header)
		self.next_page()

	def get_page(self):
		return self.tabs[self.get_current_page()]

