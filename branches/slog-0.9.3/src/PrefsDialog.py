# -*- mode: python; coding: utf-8; -*

import os
import gtk, gtk.gdk as gdk
import gobject
import gtk.glade

from slog.common import *
from slog.config import SlogConf
import slog.gui_helper as ghlp

class PrefsDialog():
	def __init__(self, parent, plugins):

		self.__plugins = plugins

		gladefile = os.path.join(DATA_DIR, "slog.glade")
		self.wtree = gtk.glade.XML(gladefile, "prefDialog", domain="slog")
		self.wtree.signal_autoconnect(self)
		self.dialog = self.wtree.get_widget("prefDialog")
		self.dialog.set_transient_for(parent)
		
		self.conf = SlogConf()

		# Creating combobox for modifer keys
		model = gtk.ListStore(str)
		model.append(["Ctrl"])
		model.append(["Alt"])
		model.append(["Shift"])
		model.append(["Win"])
		model.append(["None"])
	
		combo_keys = self.wtree.get_widget("comboKeys")
		cell = gtk.CellRendererText()
		combo_keys.pack_start(cell, True)
		combo_keys.add_attribute(cell, "text", 0)
		combo_keys.set_model(model)
		combo_keys.set_active(self.conf.mod_key)

		self.entry_proxy_host = self.wtree.get_widget("entryProxyHost")
		self.entry_proxy_host.set_text(self.conf.proxy_host)
		self.entry_proxy_port = self.wtree.get_widget("entryProxyPort")
		self.entry_proxy_port.set_value(self.conf.proxy_port)

		self.__setup_checkbox("chkSpyAutoStart", self.conf.spy_auto)
		self.__setup_checkbox("chkTrayExit", self.conf.tray_exit)
		self.__setup_checkbox("chkTrayInfo", self.conf.tray_info)
		self.__setup_checkbox("chkTrayStart", self.conf.tray_start)
		self.__setup_checkbox("chkProxyServer", self.conf.proxy)

		self.plugins_model = gtk.ListStore(bool, str)
		treeview = self.wtree.get_widget("tablePlugins")
		treeview.set_model(self.plugins_model)

		renderer = gtk.CellRendererToggle()
		renderer.connect('toggled', self.on_item_toggled, self.plugins_model)
		column = gtk.TreeViewColumn(_("Enabled"), renderer, active=0)
		column.set_sizing(gtk.TREE_VIEW_COLUMN_FIXED)
		column.set_fixed_width(64)
		treeview.append_column(column)

		column = gtk.TreeViewColumn(_("Name"), gtk.CellRendererText(), text=1)
		treeview.append_column(column)

		self.__selection = treeview.get_selection()
		self.__selection.connect("changed", self.on_plugin_clicked)

		gobject.idle_add(self.__load_plugins)

	def __load_plugins(self):
		for pname in self.__plugins.get_available():
			plugin = self.__plugins.get_plugin(pname)
			enabled = pname in self.__plugins.get_enabled()

			it = self.plugins_model.append()
			self.plugins_model.set(it, 0, enabled, 1, plugin.plugin_name)

	def __get_selected_plugin(self):
		model, iter = self.__selection.get_selected()
		name = model.get_value(iter, 1)
		plugin = self.__plugins.get_plugin(name)
		return plugin

	def __setup_checkbox(self, name, state):
		checkbox = self.wtree.get_widget(name)
		checkbox.connect("toggled", self.on_checkbox_toggled, name)
		if state != 0:
			checkbox.set_active(True)

	def on_btnPluginProps_clicked(self, widget, data=None):
		plugin = self.__get_selected_plugin()
		self.__plugins.configure_plugin(plugin.plugin_name, self.dialog)

	def on_plugin_clicked(self, selection):
		plugin = self.__get_selected_plugin()
		self.wtree.get_widget("labelPluginDescr").set_text(plugin.plugin_description)
		self.wtree.get_widget("labelPluginAuthor").set_text(plugin.plugin_author)
		self.wtree.get_widget("labelPluginVersion").set_text(plugin.plugin_version)

		if plugin.plugin_name in self.__plugins.get_enabled():
			config = self.__plugins.is_configurable(plugin.plugin_name)
			self.wtree.get_widget("btnPluginProps").set_sensitive(config)
		else:
			self.wtree.get_widget("btnPluginProps").set_sensitive(False)

	def on_item_toggled(self, cell, path, model):
		""" Обработчик события нажатия на компонент CheckButton 
			в таблице плагинов.
		"""
		l_iter = model.get_iter((int(path),))
		enabled, plugin_name = model.get(l_iter, 0, 1)
		enabled = not enabled
		model.set(l_iter, 0, enabled)
		is_config = False

		if enabled:
			self.__plugins.enable_plugin(plugin_name)
			is_config = self.__plugins.is_configurable(plugin_name)
		else:
			self.__plugins.disable_plugin(plugin_name)

		self.wtree.get_widget("btnPluginProps").set_sensitive(is_config)

		list_enabled = self.__plugins.get_enabled()
		self.conf.enabled_plugins = ":".join(list_enabled)

	def on_comboKeys_changed(self, widget, data=None):
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

	def on_proxyhost_changed(self, widget, data=None):
		self.conf.proxy_host = widget.get_text()

	def on_proxyport_changed(self, widget, data=None):
		self.conf.proxy_port = widget.get_value_as_int()

	def run(self):
		self.dialog.run()

	def destroy(self):
		self.dialog.destroy()
