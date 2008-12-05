# -*- mode: python; coding: utf-8; -*-

import os
import sys
import gtk, gobject

from slog.TransPanel import TransView
import slog.gui_helper as ghlp

class PluginManager(object):
	def __init__(self):
		self.plugins = {}
		self.enabled_plugins = {}
		self.plugin_dirs = []
		self.callbacks = []

	def __fire_changed(self, state, plugin_name, module):
		for callback in self.callbacks:
			callback(state, plugin_name, module)

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
		list_names = self.enabled_plugins.keys()
		if number < 0 or number >= len(list_names):
			return None
		name = list_names[number]
		return self.enabled_plugins[name]

	def get_enabled_plugin(self, name):
		return self.enabled_plugins[name]

	def get_plugin_num(self, name):
		i = 0
		for plugin_name in self.enabled_plugins.keys():
			if plugin_name == name:
				return i
			i += 1
		return -1

	def enable_plugin(self, name):
		""" Подключает плагин
		"""
		plugin = self.plugins[name]
		module = plugin.enable()
		self.enabled_plugins[name] = module
		self.__fire_changed(1, name, module)

	def disable_plugin(self, name):
		""" Отключает плагин
		"""
		module = self.enabled_plugins[name]
		del self.enabled_plugins[name]
		self.__fire_changed(0, name, module)

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
		self.plugin_model = plugin_manager
		self.plugin_model.connect(self.on_plugins_changed)
		self.radio_group = None

		gui.signal_autoconnect({
				"on_next_plugin_activate" : self.on_nextprev_plugin_activate,
				"on_prev_plugin_activate" : self.on_nextprev_plugin_activate
				})

		self.notebook = gui.get_widget("noteBook")
		self.notebook.remove_page(0)
		self.new_translate_page()
		self.notebook.connect("button-press-event", self.on_notebook_pressed)

		self.sidebar = gui.get_widget("sideBar")
		self.plugins_menu = gui.get_widget("menuItemView")

		self.accel_group = gtk.AccelGroup()
		gui.get_widget("mainWindow").add_accel_group(self.accel_group)

		self.menuitem_cut = gui.get_widget("menuitem_cut")
		self.menuitem_cut.connect("activate", self.on_menuitem_cut_activate)

		self.statusbar = gui.get_widget("statusBar")
		self.context_id = self.statusbar.get_context_id("slog")
	
	def __create_plugin_menuitem(self, title, index):
		menu_item = gtk.RadioMenuItem(self.radio_group, title)

		hotkey = None
		if index < 9:
			a = "<Alt>%d" % (index + 1)
			keyval, modmask = gtk.accelerator_parse(a)
			menu_item.add_accelerator("activate", self.accel_group, keyval, modmask, gtk.ACCEL_VISIBLE)
			
		menu_item.connect("toggled", self.on_menuitem_view_activate, index)
		self.radio_group = menu_item
		return menu_item

	def load(self, plugins):
		self.sidebar.remove_page(0)
		for plugin in self.plugin_manager.get_available():

			if plugin not in list_enabled:
				continue

			module = self.plugin_manager.enable_plugin(plugin)
			module.connect("changed", self.on_status_changed)
			
			while gtk.events_pending():
				gtk.main_iteration(False)

	
	def add_plugin(self, child, title):
		self.sidebar.append_page(child)
		index = self.sidebar.get_n_pages() - 1
		m = self.__create_plugin_menuitem(title, index)
		self.plugins_menu.get_submenu().append(m)
		m.show()

	def set_active(self, index):
		""" Устанавливает плагин по номеру index текущим """
		menu = self.plugins_menu.get_submenu()
		menu_item = menu.get_children()[index+3]
		menu_item.set_active(True)

	def get_active(self):
		return self.sidebar.get_current_page()

	def get_model(self):
		return self.plugin_model

	def clear_menu(self, menu):
		children = menu.get_children()
		for c in children:
			menu.remove(c)
			del c

	def refresh_menu_plugins(self):
		menu = self.plugins_menu.get_submenu()
		self.clear_menu(menu)

		index = 0
		for plugin_name in self.plugin_model.get_enabled():
			m = self.__create_plugin_menuitem(plugin_name, index)
			self.plugins_menu.get_submenu().append(m)
			m.show()
			index += 1

		self.set_active(0)

	def new_translate_page(self, event=None):
		""" Добавляет новую вкладку с окном перевода
		"""
		label = gtk.Label()
		tv = TransView(label)
		self.notebook.append_page(tv)
		header = ghlp.create_tab_header(label, tv, self.on_close_tab_clicked)
		self.notebook.set_tab_label(tv, header)
		tv.show()
		self.notebook.next_page()

	def on_plugins_changed(self, event, name, module):
		panel = module.get_panel()
		if event == 0:
			index = self.sidebar.page_num(panel)
			self.sidebar.remove_page(index)
			self.refresh_menu_plugins()
			del module
		else:
			self.add_plugin(panel, name)
			module.connect("translate_it", self.on_translate)
			module.connect("changed", self.on_status_changed)

	def on_nextprev_plugin_activate(self, widget, data=None):
		group = self.radio_group.get_group()
		for n, item in enumerate(group):
			if item.get_active() == True:
				self.set_active(n)
				break
				
	def on_menuitem_cut_activate(self, widget, data=None):
		number = self.get_active()
		module = self.plugin_model.get_nth_plugin(number)
		if module != None:
			module.clear()

	def on_menuitem_view_activate(self, widget, data=None):
		""" Обработчик события активизации плагина, в
			параметре <data> передается номер элемента.
		"""
		module = self.plugin_model.get_nth_plugin(data)
		if module != None:
			self.sidebar.set_current_page(data)
			module.grab_focus()

	def on_notebook_pressed(self, widget, event, data=None):
		""" Обработчик события двойного клика на панели вкладок
		"""
		if event.button == 1 and event.type == gtk.gdk._2BUTTON_PRESS:
			self.new_translate_page()

	def on_close_tab_clicked(self, widget, page):
		# Always show one tab		
		if self.notebook.get_n_pages() == 1:
			page.clear()
			return

		idx = self.notebook.page_num(page)
		self.notebook.remove_page(idx)
		page.destroy()

	#Thread safe update
	def __set_translate(self, word, translate, newtab=False):
		if newtab:
			self.new_translate_page()

		index = self.notebook.get_current_page()
		tv = self.notebook.get_nth_page(index)
		tv.set_translate(word, translate)

	# Activated by Translate Engine
	def on_translate(self, word, translate, newtab=False):
		gobject.idle_add(self.__set_translate, word, translate, newtab)

	def on_status_changed(self, msg):
		self.statusbar.pop(self.context_id);
		self.statusbar.push(self.context_id, msg)

