# -*- mode: python; coding: utf-8; -*-

import os
import gtk, gtk.gdk as gdk

from slog.config import SlogConf
import slog.gui_helper as ghlp

class PrefsDialog(gtk.Dialog):
	def __init__(self, parent):
		gtk.Dialog.__init__(self, _("Preferences"), parent,
								gtk.DIALOG_MODAL, (gtk.STOCK_CLOSE, gtk.RESPONSE_OK))

		self.conf = SlogConf()

		# SL stuff
		hbox = gtk.HBox(False, 0)
		hbox.set_border_width(4)
		self.vbox.pack_start(hbox, False, True, 0)

		label = gtk.Label("SL_PREFIX:")
		self.sl_prefix = gtk.Entry()
		self.sl_prefix.set_text(self.conf.sl_prefix)
		self.sl_prefix.connect("focus-out-event", self.on_focus_out)

		btn_browse = gtk.Button("...")
		btn_browse.connect("clicked", self.on_browse_clicked)

		hbox.pack_start(label, False, True, 4)
		hbox.pack_start(self.sl_prefix, True, True, 4)
		hbox.pack_start(btn_browse, False, False, 0)
		hbox.show_all()

		# Spy stuff
		hbox = gtk.HBox(False, 0)
		hbox.set_border_width(4)
		self.vbox.pack_start(hbox, False, True, 0)

		label = gtk.Label("Spy modifier key:")
		cmb_keys = gtk.combo_box_new_text()
		cmb_keys.append_text("Ctrl")
		cmb_keys.append_text("Alt")
		cmb_keys.append_text("Shift")
		cmb_keys.append_text("Win")
		cmb_keys.append_text("None")
		cmb_keys.set_active(self.conf.mod_key)
		cmb_keys.connect("changed", self.on_modkey_changed)
		
		hbox.pack_start(label, False, True, 4)
		hbox.pack_start(cmb_keys, True, True, 0)

		hbox.show_all()

		# Tray icon stuff
		check_box = gtk.CheckButton(_("Terminate instead of minimizing to tray icon"))
		if self.conf.tray_exit != 0:
			check_box.set_active(True)
		check_box.connect("toggled", self.on_checkbox_toggled, "tray_exit")
		self.vbox.pack_start(check_box, False, True, 0)
		check_box.show()

		check_box = gtk.CheckButton(_("Notify when minimizing to tray icon"))
		check_box.connect("toggled", self.on_checkbox_toggled, "tray_info")
		if self.conf.tray_info != 0:
			check_box.set_active(True)
		self.vbox.pack_start(check_box, False, True, 0)
		check_box.show()

	def on_focus_out(self, widget, data=None):
		path = widget.get_text()
		if not os.path.exists(path):
			ghlp.show_error(self, _("Path not exists!"))
		
		self.conf.sl_prefix = path
		return False
	
	def on_modkey_changed(self, widget, data=None):
		idx = widget.get_active()
		self.conf.mod_key = idx
		ghlp.show_error(self, _("Need SLog restart"))

	def on_checkbox_toggled(self, widget, data):
		if widget.get_active():
			val = 1		
		else:
			val = 0

		if data == "tray_exit":
			self.conf.tray_exit = val
		elif data == "tray_info":
			self.conf.tray_info = val

	def on_browse_clicked(self, widget, data=None):
		chooser = gtk.FileChooserDialog("Open..", None, gtk.FILE_CHOOSER_ACTION_OPEN,
							(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OPEN, gtk.RESPONSE_OK))

		sl_filter = gtk.FileFilter()
		sl_filter.set_name("SL execute")
		sl_filter.add_pattern("sl")
		chooser.add_filter(sl_filter)

		if os.path.exists(self.conf.sl_prefix):
			chooser.set_current_folder(self.conf.sl_prefix)

		response = chooser.run()
		if response == gtk.RESPONSE_OK:
			sl_path = chooser.get_filenames()[0]
			sl_prefix = sl_path.split("/bin/sl")[0]
			self.sl_prefix.set_text(sl_prefix)

		chooser.destroy()

