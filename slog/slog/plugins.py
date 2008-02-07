# -*- mode: python; coding: utf-8; -*-

import os
import sys
import imp

class PluginManager:
	def __init__(self):
		self.plugins = []

	def scan_for_plugins(self):
		plugins_dir = "../plugins"
		path = os.path.abspath(plugins_dir)
		print path
		os.chdir(path)
		print "Current:", os.getcwd()
		for modname in os.listdir(plugins_dir):
			path = os.path.join(plugins_dir, modname)
			self.plugins.append(path)
			if "__init__.py" in os.listdir(path):
				mod = __import__(modname, globals(), locals(), [""])
				print mod.plugin_name



if __name__ == "__main__":
	p = PluginManager()
	p.scan_for_plugins()
	for plugin in p.plugins:
		print plugin
