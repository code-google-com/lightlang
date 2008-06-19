#!/usr/bin/env python

import os
import shutil

from distutils.core import setup
from distutils import cmd
from distutils.command.install import install as _install
from distutils.command.install_data import install_data as _install_data

APP_NAME = "SLog"
VERSION = "0.9.2"
WEBSITE = "http://lightlang.org.ru"

# Thanks to Iain Nicol for code to save the location for installed prefix
# At runtime, we need to know where we installed the data to.

class write_data_install_path(cmd.Command):
	description = 'saves the data installation path for access at runtime'
    
	def initialize_options(self):
		self.prefix = None
		self.lib_build_dir = None

	def finalize_options(self):
		self.set_undefined_options('install',
			('prefix', 'prefix')
		)
		self.set_undefined_options('build',
			('build_lib', 'lib_build_dir')
		)

	def __replace_value(self, filename, token, value):
		fp = open(filename, "r")
		text = fp.read()
		fp.close()
		text = text.replace(token, value)
		fp = open(filename, "w")
		fp.write(text)
		fp.close()

	def run(self):
		filename = os.path.join(self.lib_build_dir,	"slog", "common.py")
		self.__replace_value(filename, "@prefix@", self.prefix)

	def get_outputs(self): return []

class unwrite_data_install_path(cmd.Command):
	description = 'undoes write_data_install_path'

	def initialize_options(self):
		self.lib_build_dir = None

	def finalize_options(self):
		self.set_undefined_options('build',
			('build_lib', 'lib_build_dir')
		)

	def run(self):
		dest = os.path.join(self.lib_build_dir,
			'slog', 'common.py')
		shutil.copyfile('src/common.py', dest)

	def get_outputs(self): return []

class install(_install):
	sub_commands = [('write_data_install_path', None)] + \
		_install.sub_commands + [('unwrite_data_install_path', None)]
	def run(self):
		_install.run(self)

cmdclass = {
	'install': install,
	'write_data_install_path': write_data_install_path,
	'unwrite_data_install_path': unwrite_data_install_path,
}

data = [
		('share/applications', ['data/slog.desktop']),
		('share/pixmaps', ['data/icons/slog.png', 'data/icons/slog_spy.png']),
		('share/locale/ru/LC_MESSAGES', ['po/slog.mo'])
]

for o in os.walk("plugins"):
	path = o[0]
	if not path.count("/.") and not path.count("\\."):
		items = o[2]
		for x in range(len(items)):
			items[x] = path + "/" + items[x]
			data.append(("share/slog/" + path, items))

setup(
	name = 'slog',
	version= VERSION,
	url = WEBSITE,
	author = 'Nasyrov Renat',
	author_email = 'renatn@gmail.com',
	description = 'SLog is a PyGTK-based GUI for the LightLang SL',
	license = 'GPL',
	requires=['gtk (>=2.10.0)', 'pynotify'],
	scripts = ['bin/slog'],
	packages = ['slog'],
	py_modules = ['libsl', 'htmltextview'],
	package_dir = {"": "lib", "slog" : "src"},
	data_files = data,
    cmdclass=cmdclass
	)
