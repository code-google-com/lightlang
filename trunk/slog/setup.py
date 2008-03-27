#!/usr/bin/env python

import os

from src.common import *
from distutils.core import setup

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
	requires=['gtk (>=2.10.0)', 'pynotify', 'gtkhtml2'],
	scripts = ['bin/slog'],
	packages = ['slog'],
	py_modules = ['libsl'],
	package_dir = {"": "libsl", "slog" : "src"},
	data_files = data
	)
