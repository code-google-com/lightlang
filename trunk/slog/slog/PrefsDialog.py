# -*- mode: python; coding: utf-8; -*-

import os
import gtk, gtk.gdk as gdk
import gobject

from slog.config import SlogConf
import slog.gui_helper as ghlp

class PrefsDialog(gtk.Dialog):
	def __init__(self, parent, plugins):
		gtk.Dialog.__init__(self, _("Preferences"), parent,
								gtk.DIALOG_MODAL, (gtk.STOCK_CLOSE, gtk.RESPONSE_OK))

		self.conf = SlogConf()
		self.plugins = plugins

		notebook = gtk.Notebook()
		self.vbox.pack_start(notebook, True, True, 0)

		main_page = self.__create_main_page()
		notebook.append_page(main_page, gtk.Label(_("Main")))
		main_page.show()

		plugins_page = self.__create_plugins_page()
		notebook.append_page(plugins_page, gtk.Label(_("Plugins")))
		plugins_page.show()

		notebook.show()

		gobject.idle_add(self.__load_plugins)

	def __create_main_page(self):
		vbox = gtk.VBox()

		# SL stuff
		hbox = gtk.HBox(False, 0)
		hbox.set_border_width(4)
		vbox.pack_start(hbox, False, True, 0)

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
		frame = self.__create_hig_frame(_("Service Spy"))
		vbox.pack_start(frame, False, True, 0)

		hbox = gtk.HBox(False, 0)
		hbox.set_border_width(4)
		frame.add(hbox)

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
		hbox.pack_start(cmb_keys, True, False, 0)

		hbox.show_all()

		# Tray icon stuff
		frame = self.__create_hig_frame(_("System Tray"))
		vbox.pack_start(frame, False, True, 0)

		vbox_tray = gtk.VBox(False, 8)
		vbox_tray.set_border_width(8)
		
		check_box = self.__create_check_box(_("Terminate instead of minimizing to tray icon"), self.conf.tray_exit, "tray_exit")
		vbox_tray.pack_start(check_box, False, True, 0)

		check_box = self.__create_check_box(_("Notify when minimizing to tray icon"), self.conf.tray_info, "tray_info")
		vbox_tray.pack_start(check_box, False, True, 0)

		check_box = self.__create_check_box(_("Start in tray"), self.conf.tray_start, "tray_start")
		vbox_tray.pack_start(check_box, False, True, 0)

		frame.add(vbox_tray)
		vbox_tray.show_all()

		return vbox

	def __create_hig_frame(self, title):
		label = self.__create_bold_label(title)
		frame = gtk.Frame()
		frame.set_shadow_type(gtk.SHADOW_NONE)
		frame.set_label_widget(label)
		frame.show()
		return frame

	def __create_bold_label(self, text):
		label = gtk.Label()
		label.set_markup("<b>%s</b>" % text)
		label.show()
		return label

	def __create_check_box(self, text, state, name):
		check_box = gtk.CheckButton(text)
		check_box.connect("toggled", self.on_checkbox_toggled, name)
		if state != 0:
			check_box.set_active(True)
		return check_box

	def __create_plugins_page(self):
		hbox = gtk.HBox()

		sw = gtk.ScrolledWindow()
		sw.set_shadow_type(gtk.SHADOW_IN)
		sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)

		self.model = gtk.ListStore(gobject.TYPE_BOOLEAN, gobject.TYPE_STRING)
		treeview = gtk.TreeView(self.model)
		treeview.set_rules_hint(True)
		treeview.set_size_request(260, 200)
		selection = treeview.get_selection()
		selection.connect("changed", self.on_plugin_clicked)

		renderer = gtk.CellRendererToggle()
		renderer.connect('toggled', self.on_item_toggled, self.model)
		column = gtk.TreeViewColumn(_("Enabled"), renderer, active=0)
		column.set_sizing(gtk.TREE_VIEW_COLUMN_FIXED)
		column.set_fixed_width(64)
		treeview.append_column(column)

		column = gtk.TreeViewColumn(_("Name"), gtk.CellRendererText(), text=1)
		treeview.append_column(column)

		sw.add(treeview)
		treeview.show()
		
		hbox.pack_start(sw, True, True, 0)
		sw.show()

		vbox = gtk.VBox(False, 8)
		vbox.set_border_width(8)
		vbox.set_size_request(240, 200)
		
		label = self.__create_bold_label(_("Description:"))
		vbox.pack_start(label, False, False, 0)

		self.label_desc = gtk.Label()
		vbox.pack_start(self.label_desc, False, False, 0)

		label = self.__create_bold_label(_("Author:"))
		vbox.pack_start(label, False, False, 0)

		self.label_auth = gtk.Label()
		vbox.pack_start(self.label_auth, False, False, 0)

		label = self.__create_bold_label(_("Version:"))
		vbox.pack_start(label, False, False, 0)

		self.label_version = gtk.Label()
		vbox.pack_start(self.label_version, False, False, 0)

		self.btn_prop = gtk.Button(stock=gtk.STOCK_PROPERTIES)
		self.btn_prop.set_sensitive(False)
		self.btn_prop.connect("clicked", self.on_btn_prop_clicked, selection)
		vbox.pack_start(self.btn_prop, False, False, 0)

		hbox.pack_start(vbox, True, True, 0)
		vbox.show_all()

		return hbox

	def __load_plugins(self):
		for pname in self.plugins.get_available():
			plugin = self.plugins.get_plugin(pname)
			enabled = pname in self.conf.get_enabled_plugins()

			iter = self.model.append()
			self.model.set(iter, 0, enabled, 1, plugin.plugin_name)

	def __get_selected_plugin(self, selection):
		model, iter = selection.get_selected()
		name = model.get_value(iter, 1)
		plugin = self.plugins.get_plugin(name)
		return plugin

	def on_btn_prop_clicked(self, widget, selection):
		plugin = self.__get_selected_plugin(selection)
		plugin.configure(self)

	def on_plugin_clicked(self, selection):
		plugin = self.__get_selected_plugin(selection)
		self.label_desc.set_text(plugin.plugin_description)
		self.label_auth.set_text(plugin.plugin_author)
		self.label_version.set_text(plugin.plugin_version)

		if plugin.plugin_configurable:
			self.btn_prop.set_sensitive(True)
		else:
			self.btn_prop.set_sensitive(False)

	def on_item_toggled(self, cell, path, model):
		l_iter = model.get_iter((int(path),))
		enabled, plugin = model.get(l_iter, 0, 1)
		enabled = not enabled
		model.set(l_iter, 0, enabled)
		if enabled:
			self.plugins.enable_plugin(plugin)
		else:
			self.plugins.disable_plugin(plugin)

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
		elif data == "tray_start":
			self.conf.tray_start = val

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

