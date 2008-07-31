# -*- mode: python; coding: utf-8; -*-

import os
import sys
import imp

class PluginManager:
	def __init__(self):
		self.plugins = {}
		self.enabled_plugins = {}
		self.plugins_dirs = []

	def add_plugin_dir(self, directory):
		self.plugins_dirs.append(directory)
	
	def scan_for_plugins(self):
		""" Search installed plugins in the directory and 
			try loaded him
		"""
		for folder in self.plugins_dirs:
			for modname in os.listdir(folder):
				path = os.path.join(folder, modname)
				if "__init__.py" in os.listdir(path):
					filename = os.path.join(path, "__init__.py")
					(stream, path_mod, desc) = imp.find_module("__init__", [path])
					try:
						mod = imp.load_module(modname, stream, filename, desc)
					finally:
						stream.close()

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

