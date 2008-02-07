#!/usr/bin/env python

from distutils.core import setup
from slog.MainWindow import __version__ as VERSION

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
	data_files = [
			('share/applications', ['data/slog.desktop']),
			('share/pixmaps', ['data/icons/slog.png', 'data/icons/slog_spy.png']),
			('share/locale/ru/LC_MESSAGES', ['po/slog.mo'])
		]
	)
