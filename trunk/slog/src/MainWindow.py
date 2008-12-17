# -*- mode: python; coding: utf-8; -*-

import os
import gtk, gobject
import gtk.glade
import pynotify

from slog.common import *
from slog.PrefsDialog import PrefsDialog
from slog.DictsDialog import DictsDialog
from slog.config import SlogConf
from slog.spy import Spy
from slog.plugins import PluginManager
from slog.plugins import PluginView
from slog.remote import SLogDBus
import slog.gui_helper as ghlp

class MainWindow(object):

	def __init__(self):
		self.conf = SlogConf()

		gladefile = os.path.join(DATA_DIR, "slog.glade")
		self.wtree = gtk.glade.XML(gladefile, domain="slog")
		self.wtree.signal_autoconnect(self)

		# Create tray icon 
		self.status_icon = gtk.status_icon_new_from_file(get_icon("slog.png"))
		self.status_icon.set_tooltip(APP_NAME)
		self.status_icon.connect("popup-menu", self.on_tray_popup)
		self.status_icon.connect("activate", self.on_tray_clicked)

		# Create main window
		self.window = self.wtree.get_widget("mainWindow")
		self.window.set_icon_from_file(get_icon("slog.png"))
		self.window.set_title("%s %s" % (APP_NAME, VERSION))
		self.window.set_size_request(396, 256)

		# Restore window settings
		(width, height) = self.conf.get_size()
		(left, top) = self.conf.get_pos()
		if left != 0 or top != 0:
			self.window.move(left, top)
		self.window.set_default_size(width, height)

		self.wtree.get_widget("hPaned").set_position(self.conf.paned)
		self.sidebar = self.wtree.get_widget("sideBar")

		#Create Spy object
		self.spy = Spy()
		mb_menuitem_spy = self.wtree.get_widget("menuItemSpy1")
		tray_menuitem_spy = self.wtree.get_widget("menuItemSpy2")
		self.spy_action = gtk.ToggleAction("Spy", "_Spy", "Spy Service", None)
		self.spy_action.connect("activate", self.on_spy_clicked)
		self.spy_action.connect_proxy(tray_menuitem_spy)
		self.spy_action.connect_proxy(mb_menuitem_spy)

		if self.conf.tray_start == 0:
			self.window.show_all()

		if self.conf.spy_auto == 1:
			self.spy_action.activate()

		plugin_dir = os.path.join(DATA_DIR, "plugins")
		self.plugin_manager = PluginManager()
		self.plugin_manager.add_plugin_dir(plugin_dir)
		self.plugin_manager.scan_for_plugins()
		self.plugin_view = PluginView(self.wtree, self.plugin_manager)

		self.__load_plugins()

	def __load_plugins(self):

		list_enabled = self.conf.get_enabled_plugins()
		if list_enabled == []:
			return

		self.sidebar.remove_page(0)
		for plugin in self.plugin_manager.get_available():
			if plugin not in list_enabled:
				continue

			self.plugin_manager.enable_plugin(plugin)
			
			while gtk.events_pending():
				gtk.main_iteration(False)

		self.plugin_view.set_active(self.conf.get_engine())

	def __create_notify(self, title, message, timeout=3000):
		n = pynotify.Notification(title, message)
		n.attach_to_status_icon(self.status_icon)
		n.set_urgency(pynotify.URGENCY_NORMAL)
		n.set_timeout(timeout)
		n.set_icon_from_pixbuf(gtk.gdk.pixbuf_new_from_file_at_size(get_icon("slog.png"), 48, 48))
		return n

	#################
	# GUI Callbacks #
	#################

	def on_window_closed(self, widget, data=None):
		if self.conf.tray_exit != 0:
			self.window.destroy(widget, data)

		if self.conf.tray_info != 0:
			n = self.__create_notify(APP_NAME, "Closed to system tray")
			if not n.show():
				print "Warning: Failed to show notification"

		self.window.hide()
		return True

	def on_window_exit(self, widget, data=None):
		(width, height) = self.window.get_size()
		(left, top) = self.window.get_position()
		self.conf.paned = self.wtree.get_widget("hPaned").get_position()
		self.conf.set_size(width, height)
		self.conf.set_pos(left, top)
		self.conf.set_engine(self.plugin_view.get_active_engine())
		self.conf.save()
		gtk.main_quit()

	def on_spy_clicked(self, widget):
		if widget.get_active():
			self.status_icon.set_from_file(get_icon("slog_spy.png"))
			self.spy.start()
		else:
			self.status_icon.set_from_file(get_icon("slog.png"))
			self.spy.stop()

	def on_preferences_activate(self, widget, data=None):
		dialog = PrefsDialog(self.window, self.plugin_manager)
		dialog.run()
		dialog.destroy()

	def on_dicts_manage_activate(self, widget, data=None):
		dialog = DictsDialog(self.window)
		dialog.run()
		dialog.destroy()

	def on_about_activate(self, action):
		dialog = gtk.AboutDialog()
		dialog.set_name(APP_NAME)
		dialog.set_logo(gtk.gdk.pixbuf_new_from_file(get_icon("slog.png")))
		dialog.set_copyright("\302\251 Copyright 2007,2008 Renat Nasyrov (renatn@gmail.com)")
		dialog.set_website(WEBSITE)
		dialog.set_version(VERSION)
		dialog.set_license(LICENSE)
		dialog.connect("response", lambda d, r: d.destroy())
		dialog.show()

	def on_tray_clicked(self, args):
		self.window_toggle()

	def on_tray_popup(self, icon, event_button, event_time):
		tray_menu = self.wtree.get_widget("trayMenu")
		tray_menu.popup(None, None, gtk.status_icon_position_menu, event_button, event_time, self.status_icon)

	###########
	# Private #
	###########

	def window_toggle(self):
		if self.window.get_property("visible"):
			self.window.hide()
		else:
			self.window.show_all()
			gobject.idle_add(self.window_present_and_focus)

	def window_present_and_focus(self):
		self.window.present()
		self.window.grab_focus()

	def run(self):
		self.ipc = SLogDBus(self)
		if not pynotify.init("SLog Notification"):
			print "Failed init python-notify module"

		gobject.threads_init()
		gtk.gdk.threads_enter()
		gtk.main()
		gtk.gdk.threads_leave()

