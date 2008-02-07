# -*- mode: python; coding: utf-8; -*-

import os
import sys
import imp

class PluginManager:
	def __init__(self):
		self.plugins = []

	def scan_for_plugins(self):

		plugins_dir = os.path.abspath("../plugins")

		for modname in os.listdir(plugins_dir):

			print "Modname:", modname

			path = os.path.join(plugins_dir, modname)

			print "Path:", path

			if "__init__.py" in os.listdir(path):

				(stream, path, desc) = imp.find_module("__init__", [path])
				try:
					mod = imp.load_module("__init__", stream, "__init__.py", desc)
				finally:
					stream.close()

				self.plugins.append(path)
				print mod.plugin_name



if __name__ == "__main__":
	p = PluginManager()
	p.scan_for_plugins()
	for plugin in p.plugins:
		print plugin
