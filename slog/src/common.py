# -*- mode: python; coding: utf-8; -*-

import os

APP_NAME = "SLog"
VERSION = "0.9.2"
WEBSITE = "http://lightlang.org.ru"

LICENSE = """
SLog is a PyGTK-based GUI for the LightLang SL dictionary.
Copyright 2007 Nasyrov Renat <renatn@gmail.com>

This file is part of SLog.

SLog is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

SLog is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

along with SLog; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
"""

INSTALL_PREFIX = "/tmp/slog"

PIXMAP_DIR = os.path.join(INSTALL_PREFIX, "share", "pixmaps")
LOCALE_DIR = os.path.join(INSTALL_PREFIX, "share", "locale")
DATA_DIR   = os.path.join(INSTALL_PREFIX, "share", "slog")

LOGO_ICON = "slog.png"
LOGO_ICON_SPY = "slog_spy.png"

def get_icon(filename):
	return os.path.join(PIXMAP_DIR, filename)
