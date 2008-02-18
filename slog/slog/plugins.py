# -*- mode: python; coding: utf-8; -*-

import os
import sys
import imp

from slog.config import SlogConf
from slog.common import DATA_DIR

class PluginManager:
	def __init__(self):
		self.plugins = {}
		self.enabled_plugins = {}
		self.conf = SlogConf()
		
	def __sync_config(self):
		list_enabled = self.get_enabled()
		self.conf.enabled_plugins = ":".join(list_enabled)

	def scan_for_plugins(self):
		plugins_dir = os.path.join(DATA_DIR, "plugins")

		for modname in os.listdir(plugins_dir):
			path = os.path.join(plugins_dir, modname)
			if "__init__.py" in os.listdir(path):
				filename = os.path.join(path, "__init__.py")
				(stream, path, desc) = imp.find_module("__init__", [path])
				try:
					mod = imp.load_module(modname, stream, filename, desc)
				finally:
					stream.close()

				self.plugins[mod.plugin_name] = mod

	def get_available(self):
		return self.plugins.keys()

	def get_enabled(self):
		return self.enabled_plugins.keys()

	def get_plugin(self, name):
		return self.plugins[name]

	def enable_plugin(self, name):
		plugin = self.plugins[name]
		self.enabled_plugins[name] = plugin.enable()
		self.__sync_config()
		return self.enabled_plugins[name]

	def disable_plugin(self, name):
		del self.enabled_plugins[name]
		self.__sync_config()

	def configure_plugin(self, name, window):
		plugin = self.enabled_plugins[name]
		plugin.configure(window)

	def is_configurable(self, name):
		plugin = self.enabled_plugins[name]
		return ("configure" in dir(plugin))


