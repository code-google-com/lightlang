# -*- mode: python; coding: utf-8; -*

import os
import gtk, gtk.gdk as gdk
import gobject
import gtk.glade

from slog.common import *
from slog.config import SlogConf
import slog.gui_helper as ghlp

class PluginsView(gtk.HBox):
	def __init__(self, dialog, plugins):
		gtk.HBox.__init__(self, False, 0)

		self.dialog = dialog
		self.plugins = plugins

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

		self.pack_start(sw, True, True, 0)
		sw.show()

		vbox = gtk.VBox(False, 8)
		vbox.set_border_width(8)
		vbox.set_size_request(240, 200)

		label = ghlp.create_bold_label(_("Description:"))
		vbox.pack_start(label, False, False, 0)

		self.label_desc = gtk.Label()
		vbox.pack_start(self.label_desc, False, False, 0)

		label = ghlp.create_bold_label(_("Author:"))
		vbox.pack_start(label, False, False, 0)

		self.label_auth = gtk.Label()
		vbox.pack_start(self.label_auth, False, False, 0)

		label = ghlp.create_bold_label(_("Version:"))
		vbox.pack_start(label, False, False, 0)

		self.label_version = gtk.Label()
		vbox.pack_start(self.label_version, False, False, 0)

		self.btn_prop = gtk.Button(stock=gtk.STOCK_PROPERTIES)
		self.btn_prop.set_sensitive(False)
		self.btn_prop.connect("clicked", self.on_btn_prop_clicked, selection)
		vbox.pack_start(self.btn_prop, False, False, 0)

		self.pack_start(vbox, True, True, 0)
		vbox.show_all()

		gobject.idle_add(self.__load_plugins)

	def __load_plugins(self):
		for pname in self.plugins.get_available():
			plugin = self.plugins.get_plugin(pname)
			enabled = pname in SlogConf().get_enabled_plugins()

			iter = self.model.append()
			self.model.set(iter, 0, enabled, 1, plugin.plugin_name)

	def __get_selected_plugin(self, selection):
		model, iter = selection.get_selected()
		name = model.get_value(iter, 1)
		plugin = self.plugins.get_plugin(name)
		return plugin

	def on_btn_prop_clicked(self, widget, selection):
		plugin = self.__get_selected_plugin(selection)
		self.plugins.configure_plugin(plugin.plugin_name, self.dialog)

	def on_plugin_clicked(self, selection):
		plugin = self.__get_selected_plugin(selection)
		self.label_desc.set_text(plugin.plugin_description)
		self.label_auth.set_text(plugin.plugin_author)
		self.label_version.set_text(plugin.plugin_version)

		if plugin.plugin_name in self.plugins.get_enabled():
			config = self.plugins.is_configurable(plugin.plugin_name)
			self.btn_prop.set_sensitive(config)
		else:
			self.btn_prop.set_sensitive(False)

	def on_item_toggled(self, cell, path, model):
		l_iter = model.get_iter((int(path),))
		enabled, plugin_name = model.get(l_iter, 0, 1)
		enabled = not enabled
		model.set(l_iter, 0, enabled)
		if enabled:
			self.plugins.enable_plugin(plugin_name)
			config = self.plugins.is_configurable(plugin_name)
		else:
			config = False
			self.plugins.disable_plugin(plugin_name)
		self.btn_prop.set_sensitive(config)


class PrefsDialog():
	def __init__(self, parent, plugins):

		gladefile = os.path.join(DATA_DIR, "slog.glade")
		self.pref_glade = gtk.glade.XML(gladefile, "prefDialog", domain="slog")
		self.dialog = self.pref_glade.get_widget("prefDialog")
		
		self.conf = SlogConf()

		# Creating combobox for modifer keys
		model = gtk.ListStore(str)
		model.append(["Ctrl"])
		model.append(["Alt"])
		model.append(["Shift"])
		model.append(["Win"])
		model.append(["None"])
	
		combo_keys = self.pref_glade.get_widget("comboKeys")
		cell = gtk.CellRendererText()
		combo_keys.pack_start(cell, True)
		combo_keys.add_attribute(cell, "text", 0)
		combo_keys.set_model(model)
		combo_keys.set_active(self.conf.mod_key)
		combo_keys.connect("changed", self.on_modkey_changed)

		self.entry_proxy_host = self.pref_glade.get_widget("entryProxyHost")
		self.entry_proxy_port = self.pref_glade.get_widget("entryProxyPort")

		self.__setup_checkbox("chkSpyAutoStart", self.conf.spy_auto)
		self.__setup_checkbox("chkTrayExit", self.conf.tray_exit)
		self.__setup_checkbox("chkTrayInfo", self.conf.tray_info)
		self.__setup_checkbox("chkTrayStart", self.conf.tray_start)
		self.__setup_checkbox("chkProxyServer", self.conf.proxy)


		#plugins_page = PluginsView(self, plugins)
		#notebook.append_page(plugins_page, gtk.Label(_("Plugins")))
		#plugins_page.show()

	def run(self):
		self.dialog.run()

	def destroy(self):
		self.dialog.destroy()

	def __setup_checkbox(self, name, state):
		checkbox = self.pref_glade.get_widget(name)
		checkbox.connect("toggled", self.on_checkbox_toggled, name)
		if state != 0:
			checkbox.set_active(True)

	def on_modkey_changed(self, widget, data=None):
		idx = widget.get_active()
		self.conf.mod_key = idx

	def on_checkbox_toggled(self, widget, data=None):
		if widget.get_active():
			val = 1
		else:
			val = 0

		name = widget.get_name()
		if name == "chkTrayExit":
			self.conf.tray_exit = val
		elif name == "chkTrayInfo":
			self.conf.tray_info = val
		elif name == "chkTrayStart":
			self.conf.tray_start = val
		elif name == "chkSpyAutoStart":
			self.conf.spy_auto = val
		elif name == "chkProxyServer":
			self.conf.proxy = val

			enabled = widget.get_active()
			self.entry_proxy_host.set_sensitive(enabled)
			self.entry_proxy_port.set_sensitive(enabled)

