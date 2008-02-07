# -*- mode: python; coding: utf-8; -*-

import gtk

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

