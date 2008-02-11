#!/usr/bin/env python

import os

from distutils.core import setup
from slog.MainWindow import __version__ as VERSION

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
	url = 'http://lightlang.org.ru',
	author = 'Nasyrov Renat',
	author_email = 'renatn@gmail.com',
	description = 'SLog is a PyGTK-based GUI for the LightLang SL',
	license = 'GPL',
	requires=['gtk (>=2.10.0)', 'pynotify', 'gtkhtml2'],
	scripts = ['bin/slog'],
	packages = ['slog'],
	data_files = data
	)
