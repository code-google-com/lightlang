#!/usr/bin/env python
# -*- mode: python; coding: utf-8 -*-

import gettext
import gtk.glade

from slog.common import *

# Translation stuff
domain = "slog"
gtk.glade.bindtextdomain(domain, LOCALE_DIR)
gtk.glade.textdomain(domain)
gettext.bindtextdomain(domain, LOCALE_DIR)
gettext.textdomain(domain)
gettext.install(domain, LOCALE_DIR, unicode=1)
