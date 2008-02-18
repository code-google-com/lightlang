# -*- mode: python; coding: utf-8; -*-
import sys
import os
import getopt
import dbus, _dbus_bindings as dbus_bindings

__app_name__ = "SLog"
__version__ = "0.9.2"

__license__ = """
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

from slog.remote import Remote
from slog.config import SlogConf
from slog.MainWindow import MainWindow

class SLogDBus(dbus.service.Object):

	def __init__(self, bus_name, obj_path):
		self.window = MainWindow()
		dbus.service.Object.__init__(self, bus_name, obj_path)

	@dbus.service.method("org.LightLang.SLogInterface")
	def dbus_spy_toggle(self):
		self.window.spy_action.activate()

	@dbus.service.method("org.LightLang.SLogInterface")
	def toggle(self):
		self.window.window_toggle()

	@dbus.service.method("org.LightLang.SLogInterface")
	def show(self):
		self.window.hide()
		self.window.app_show()

	def run(self):
		self.window.run()

def print_version():
	print "Version:", __app_name__, __version__
	print "Website: http://lightlang.org.ru/"

def print_usage():
	print_version()
	print ""
	print "Usage: slog [OPTION]"
	print ""
	print "Options" + ":"
	print "  -h, --help        " + "Show this help and exit"
	print "  -v, --version     " + "Show version information and exit"
	print "  -r, --remote cmd  " + "Execute remote command: [toggle, spy-toggle, show]"
	print

def main(prefix=sys.prefix):
	
	# Process command line
	try:
		opts, args = getopt.getopt(sys.argv[1:], "hvr:", ["help", "version", "remote="])
	except getopt.GetoptError:
		self.print_usage()
		sys.exit(1)

	if opts != []:
		for o, a in opts:
			if o in ("-h", "--help"):
				print_usage()
			elif o in ("-v", "--version"):
				print_version()
			elif o in ("-r", "--remote"):
				try:
					remote = Remote()
					remote.execute(a)
				except dbus.DBusException, err:
					print >> sys.stderr, err
					sys.exit(1)
		sys.exit()

	try:
		dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
		bus = dbus.SessionBus()
	
		#Check double running	
		retval = bus.request_name("org.LightLang.SLog", dbus_bindings.NAME_FLAG_DO_NOT_QUEUE)
		if retval in (dbus_bindings.REQUEST_NAME_REPLY_PRIMARY_OWNER, dbus_bindings.REQUEST_NAME_REPLY_ALREADY_OWNER):
			pass
		elif retval in (dbus_bindings.REQUEST_NAME_REPLY_EXISTS, dbus_bindings.REQUEST_NAME_REPLY_IN_QUEUE):
			remote = Remote()
			remote.execute("show")
			sys.exit()

		conf = SlogConf()
		conf.prefix = prefix
		name = dbus.service.BusName("org.LightLang.SLog", bus)
		app = SLogDBus(bus, "/SLog")
	except SystemExit:
		sys.exit()

	try:
		app.run()
	except KeyboardInterrupt:
		pass

