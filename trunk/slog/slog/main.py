# -*- mode: python; coding: utf-8; -*-
import sys
import os
import getopt
import dbus, _dbus_bindings as dbus_bindings

import slog.common as cmn

from slog.config import SlogConf
from slog.remote import Remote
from slog.MainWindow import MainWindow

def print_version():
	print "Version:", cmn.APP_NAME, cmn.VERSION
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

def main():
	
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

		app = MainWindow()
	except SystemExit:
		sys.exit()

	try:
		app.run()
	except KeyboardInterrupt:
		pass

