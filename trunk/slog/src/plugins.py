# -*- mode: python; coding: utf-8; -*-

import os
import sys
import imp
import gtk

class PluginManager(object):
	def __init__(self):
		self.plugins = {}
		self.enabled_plugins = {}
		self.plugin_dirs = []
		self.callbacks = []

	def __fire_changed(self):
		for callback in self.callbacks():
			callback()

	def add_plugin_dir(self, directory):
		self.plugin_dirs.append(directory)
		sys.path.append(directory)
	
	def scan_for_plugins(self):
		""" Search installed plugins in the directory and 
			try loaded him
		"""
		for folder in self.plugin_dirs:
			for modname in os.listdir(folder):
				path = os.path.join(folder, modname)
				if "__init__.py" in os.listdir(path):
					filename = os.path.join(path, "__init__.py")
					mod = __import__(modname, globals(), locals(), [''])
					mod.slog_init(path)
					self.plugins[mod.plugin_name] = mod

	def get_available(self):
		""" Возвращает список установленных плагинов
		"""
		return self.plugins.keys()

	def get_enabled(self):
		""" Возвращает список подключенных плагинов
		"""
		return self.enabled_plugins.keys()

	def get_plugin(self, name):
		""" Возвращает плагин по имени
		"""
		return self.plugins[name]

	def get_nth_plugin(self, number):
		""" Возвращает подключенный плагин по номеру
		"""
		name = self.enabled_plugins.keys()[number]
		return self.enabled_plugins[name]

	def get_enabled_plugin(self, name):
		return self.enabled_plugins[name]

	def enable_plugin(self, name):
		""" Подключает плагин
		"""
		plugin = self.plugins[name]
		self.enabled_plugins[name] = plugin.enable()
		return self.enabled_plugins[name]

	def disable_plugin(self, name):
		""" Отключает плагин
		"""
		del self.enabled_plugins[name]

	def configure_plugin(self, name, window):
		plugin = self.enabled_plugins[name]
		plugin.configure(window)

	def is_configurable(self, name):
		plugin = self.enabled_plugins[name]
		return ("configure" in dir(plugin))

	def connect(self, callback):
		self.callbacks.append(callback)

class PluginView(object):

	def __init__(self, gui, plugin_manager):
		self.plugin_manager = plugin_manager
		self.plugin_manager.connect(self.on_plugins_changed)
		self.radio_group = None

		self.sidebar = gui.get_widget("sideBar")

		self.menu = gtk.Menu()
		gui.get_widget("menuItemView").set_submenu(self.menu)

		self.accel_group = gtk.AccelGroup()
		gui.get_widget("mainWindow").add_accel_group(self.accel_group)
	
	def __create_plugin_menuitem(self, title, index):
		menu_item = gtk.RadioMenuItem(self.radio_group, title)

		if index < 10:
			hotkey = ord(str(index))
			menu_item.add_accelerator("activate", self.accel_group, hotkey, gtk.gdk.MOD1_MASK, gtk.ACCEL_VISIBLE)

		menu_item.connect("activate", self.on_menuitem_view_activate, index-1)
		
		self.radio_group = menu_item

		return menu_item
	
	def add_plugin(self, title, module):
		index = len(self.menu.get_children()) + 1

		panel = module.get_panel()
		self.sidebar.append_page(panel)
			
		menu_item = self.__create_plugin_menuitem(title, index)
		self.menu.append(menu_item)
		menu_item.show()

	def set_active(self, index):
		self.menu.set_active(index)
		m = self.menu.get_active()
		m.set_active(True)

	def get_active(self):
		return self.sidebar.get_current_page()

	def get_model(self):
		return self.plugin_manager

	def on_menuitem_view_activate(self, widget, data):
		""" Обработчик события активизации плагина, в
			параметре <data> передается номер элемента.
		"""
		print "Index:", data
		self.sidebar.set_current_page(data)
		plugin = self.plugin_manager.get_nth_plugin(data)
		plugin.grab_focus()

	def clear_sidebar(self, sidebar):
		count = sidebar.get_n_pages()
		for i in range(count):
			sidebar.remove_page(-1)

	def clear_menu(self, menu):
		children = menu.get_children()
		for c in children:
			menu.remove(c)
			del c

	def update(self):
		self.clear_sidebar(self.sidebar)
		self.clear_menu(self.menu)

		for plugin_name in self.plugin_manager.get_enabled():
			module = self.plugin_manager.get_enabled_plugin(plugin_name)
			self.add_plugin(plugin_name, module)

	def on_plugins_changed(self):
		print "Changed"

