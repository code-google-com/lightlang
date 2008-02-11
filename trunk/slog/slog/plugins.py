# -*- mode: python; coding: utf-8; -*-

import os
import sys
import imp

class PluginManager:
	def __init__(self):
		self.plugins = {}

	def scan_for_plugins(self, data_dir):

		plugins_dir = os.path.join(data_dir, "plugins")

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

	def enable_plugin(self, name):
		plugin = self.plugins[name]
		return plugin.enable()

