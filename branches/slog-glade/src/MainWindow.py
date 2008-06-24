# -*- mode: python; coding: utf-8; -*-

import os
import gtk, gobject
import gtk.glade
import pynotify
import gettext

from slog.common import *
from slog.TransPanel import TransView
from slog.PrefsDialog import PrefsDialog
from slog.DictsDialog import DictsDialog
from slog.MyNotebook import MyNotebook
from slog.SideBar import SideBar
from slog.config import SlogConf
from slog.spy import Spy
from slog.plugins import PluginManager
from slog.remote import SLogDBus

class MainWindow():

	def __init__(self):
		self.conf = SlogConf()

		# Translation stuff
		try:
			gettext.install("slog", LOCALE_DIR, unicode=1)
		except:
			pass
		gettext.textdomain("slog")

		gladefile = os.path.join(DATA_DIR, "slog.glade")

		# Create tray icon 
		tray_glade = gtk.glade.XML(gladefile, "trayMenu", domain="slog")
		tray_glade.signal_autoconnect(self)
		self.tray_menu = tray_glade.get_widget("trayMenu")

		self.status_icon = gtk.status_icon_new_from_file(get_icon("slog.png"))
		self.status_icon.set_tooltip(APP_NAME)
		self.status_icon.connect("popup-menu", self.on_tray_popup)
		self.status_icon.connect("activate", self.on_tray_clicked)

		# Create main window
		self.wtree = gtk.glade.XML(gladefile, "mainWindow", domain="slog")
		self.wtree.signal_autoconnect(self)
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

		self.hpaned = self.wtree.get_widget("hPaned")
		self.hpaned.set_position(self.conf.paned)
		self.tooltips = gtk.Tooltips()
		self.notebook = MyNotebook()
		self.sidebar = SideBar()

		self.hpaned.add1(self.sidebar)
		self.hpaned.add2(self.notebook)
		self.new_translate_page()

		self.statusbar = self.wtree.get_widget("statusBar")
		self.context_id = self.statusbar.get_context_id("slog")

		if self.conf.tray_start == 0:
			self.window.show_all()

		#if self.conf.spy_auto == 1:
		#	self.spy_action.activate()

		self.window.add_events(gtk.gdk.KEY_PRESS_MASK)
		gobject.idle_add(self.__load_plugins)

	def __load_plugins(self):
		self.plugin_manager = PluginManager()
		self.plugin_manager.scan_for_plugins()

		list_enabled = self.conf.get_enabled_plugins()
		for plugin in self.plugin_manager.get_available():

			if plugin not in list_enabled:
				continue

			view = self.plugin_manager.enable_plugin(plugin)
			view.connect("translate_it", self.on_translate)
			view.connect("changed", self.on_status_changed)
			self.sidebar.append_page(plugin, view)
			view.show_all()

			while gtk.events_pending():
				gtk.main_iteration(False)

		self.spy = Spy()

		self.sidebar.set_active(self.conf.get_engine())

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
			n = self.__create_notify(APP_NAME, "Close in system tray")
			if not n.show():
				print "Failed to send notification"

		self.window.hide()
		return True

	def on_window_exit(self, widget, data=None):
		(width, height) = self.window.get_size()
		(left, top) = self.window.get_position()
		self.conf.paned = self.hpaned.get_position()
		self.conf.set_size(width, height)
		self.conf.set_pos(left, top)
		self.conf.set_engine(self.sidebar.get_active())
		self.conf.save()
		gtk.main_quit()

	def on_press_hotkey(self, widget, event):
		# Process hotkey like <Alt>-1,2,3,...
		if event.keyval in (49, 50, 51):
			if event.state & gtk.gdk.MOD1_MASK:
				engine = (event.keyval - 49)
				self.sidebar.set_active(engine)

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
		dialog.connect ("response", lambda d, r: d.destroy())
		dialog.show()

	def on_tray_clicked(self, args):
		self.window_toggle()

	def on_tray_popup(self, icon, event_button, event_time):
		self.tray_menu.popup(None, None, gtk.status_icon_position_menu, event_button, event_time, self.status_icon)

	#Thread safe update
	def __set_translate(self, word, translate, newtab=False):
		if newtab:
			self.new_translate_page()

		tv = self.notebook.get_page()
		tv.set_translate(word, translate)

	# Activated by Translate Engine
	def on_translate(self, word, translate, newtab=False):
		gobject.idle_add(self.__set_translate, word, translate, newtab)

	def on_status_changed(self, msg):
		self.statusbar.pop(self.context_id);
		self.statusbar.push(self.context_id, msg)

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

	def new_translate_page(self, event=None):
		label = gtk.Label()
		tv = TransView(label)
		self.notebook.add_page(label, tv)

	def run(self):
		self.ipc = SLogDBus(self)
		if not pynotify.init("SLog Notification"):
			print "Failed init python-notify module"

		gobject.threads_init()
		gtk.gdk.threads_enter()
		gtk.main()
		gtk.gdk.threads_leave()
