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

			print "Path:", path

			if "__init__.py" in os.listdir(path):
			
				print "Modname:", modname

				(stream, path, desc) = imp.find_module("__init__", [path])
				try:
					mod = imp.load_module("__init__", stream, "__init__.py", desc)
				finally:
					stream.close()

				self.plugins[mod.plugin_name] = mod
				print "Name:", mod.plugin_name

	def enable_plugin(self, name):
		plugin = self.plugins[name]
		return plugin.enable()

