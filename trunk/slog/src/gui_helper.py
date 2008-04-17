# -*- mode: python; coding: utf-8; -*-

import gtk, gobject

def show_error(parent, message):
	dlg = gtk.MessageDialog(parent, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
								gtk.MESSAGE_WARNING, gtk.BUTTONS_CLOSE,	message)
	dlg.set_title("SLog")
	dlg.run()
	dlg.destroy()

def create_speed_button(stock):
		img = gtk.Image()
		img.set_from_stock(stock, gtk.ICON_SIZE_MENU)
		btn = gtk.Button()
		btn.add(img)
		return btn

def create_bold_label(text):
	label = gtk.Label()
	label.set_markup("<b>%s</b>" % text)
	label.show()
	return label

def change_cursor(cursor):
	for w in gtk.gdk.window_get_toplevels():
		w.set_cursor(cursor)

class ProgressDialog(gtk.Dialog):
	def __init__(self, parent, title, task):
		gtk.Dialog.__init__(self, title, parent, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
					(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL))

		self.__task = task
		self.__timeout = None

		self.set_border_width(8)
		self.set_size_request(300,100)
		
		self.task = gtk.Label()
		self.task.set_alignment(0.0, 0.0)
		self.vbox.pack_start(self.task)
		self.task.show()

		self.progress = gtk.ProgressBar()
		self.vbox.pack_start(self.progress, False)
		self.progress.show()
		
		self.set_task(task)

	def pulse(self):
		self.progress.pulse()

	def set_task(self, task):
		self.task.set_text(self.__task)
	
	def set_message(self, message):
		self.progress.set_text(message)

	def set_progress(self, progress):
		self.progress.set_fraction(progress/100.0)

