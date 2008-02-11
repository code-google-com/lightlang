# -*- mode: python; coding: utf-8; -*-

import os
import sys
import imp

from slog.config import SlogConf

class PluginManager:
	def __init__(self):
		self.plugins = {}
		self.conf = SlogConf()
		
	def scan_for_plugins(self):
		plugins_dir = os.path.join(self.conf.get_data_dir(), "plugins")

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

		enabled = self.conf.get_enabled_plugins()
		if name not in enabled:
			enabled.append(name)
			self.conf.enabled_plugins = ":".join(enabled)

		return plugin.enable()

