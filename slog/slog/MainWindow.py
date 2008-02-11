# -*- mode: python; coding: utf-8; -*-

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
import pygtk
pygtk.require('2.0')

import sys, os
import gtk, gobject
import dbus, dbus.service, dbus.mainloop.glib
import pynotify
import gettext

from slog.TransPanel import TransView
from slog.PrefsDialog import PrefsDialog
from slog.DictsDialog import DictsDialog
from slog.MyNotebook import MyNotebook
from slog.SideBar import SideBar
from slog.slengine import SLView
from slog.google import GoogleView
from slog.config import SlogConf
from slog.dict_client import DCView
from slog.spy import Spy
from slog.plugins import PluginManager

LOGO_ICON = "slog.png"
LOGO_ICON_SPY = "slog_spy.png"

ui_info = \
'''<ui>
		<menubar name="MenuBar">
			<menu action="FileMenu">
				<menuitem action="NewTab"/>
				<separator/>
				<menuitem action="Preferences"/>
				<separator/>
				<menuitem action="Close"/>
				<menuitem action="Quit"/>
			</menu>
			<menu action="ToolsMenu">
				<menuitem action="DictMng"/>
				<menuitem action="Spy"/>
			</menu>
			<menu action="HelpMenu">
				<menuitem action="About"/>
			</menu>
		</menubar>
		<toolbar name="ToolBar">
		</toolbar>
		<popup name="TrayMenu">
			<menuitem action="Spy"/>
			<separator/>
			<menuitem action="Quit"/>
		</popup>
</ui>'''

class MainWindow:

	def __init__(self, slog_prefix=sys.prefix):
		self.name = "SLog"
	
		self.conf = SlogConf()
		self.conf.prefix = slog_prefix

		# Translation stuff
		locale_path = os.path.join(slog_prefix, "share", "locale")
		try:
			gettext.install("slog", locale_path, unicode=1)
		except:
			pass
		gettext.textdomain("slog")

		self.spy = Spy()

		# Create tray icon 
		self.status_icon = gtk.status_icon_new_from_file(self.get_icon(LOGO_ICON))
		self.status_icon.set_tooltip(self.name)
		self.status_icon.connect("popup-menu", self.on_tray_popup)
		self.status_icon.connect("activate", self.on_tray_clicked)

		# Create main window
		self.tooltips = gtk.Tooltips()
		self.notebook = MyNotebook()

		self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		self.window.set_icon_from_file(self.get_icon(LOGO_ICON))
		self.window.set_border_width(1)
		self.window.set_title("%s %s" % (self.name, __version__))
		self.window.set_size_request(396, 256)

		(width, height) = self.conf.get_size()
		(left, top) = self.conf.get_pos()
		if left != 0 or top != 0:
			self.window.move(left, top)
		self.window.set_default_size(width, height)

		self.window.connect("delete_event", self.delete_event)
		self.window.connect("destroy", self.destroy)

		# Create Actions
		self.uimanager = gtk.UIManager()
		self.window.set_data("ui-manager", self.uimanager)
		self.uimanager.insert_action_group(self.__create_action_group(), 0)
		self.window.add_accel_group(self.uimanager.get_accel_group())

		try:
			uimanagerid = self.uimanager.add_ui_from_string(ui_info)
		except gobject.GError, msg:
			print "building menus failed: %s" % msg

		vbox = gtk.VBox(False, 4)
		self.window.add(vbox)

		menubar = self.uimanager.get_widget("/MenuBar")
		vbox.pack_start(menubar, False, False, 0)

		self.hpaned = gtk.HPaned()
		vbox.pack_start(self.hpaned, True, True, 0)

		self.sidebar = SideBar()

		plugin_mananer = PluginManager()
		plugin_mananer.scan_for_plugins(self.conf.get_data_dir())

		view = SLView()
		view.connect("translate_it", self.on_translate)
		view.connect("changed", self.on_status_changed)
		self.sidebar.append_page("LightLang", view)

		view = plugin_mananer.enable_plugin("Google Translate")
		view.connect("translate_it", self.on_translate)
		view.connect("changed", self.on_status_changed)
		self.sidebar.append_page("Google Translate", view)

		view = DCView()
		view.connect("translate_it", self.on_translate)
		view.connect("changed", self.on_status_changed)
		self.sidebar.append_page("DICT client", view)

		self.sidebar.set_active(self.conf.get_engine())

		self.hpaned.add1(self.sidebar)
		self.hpaned.add2(self.notebook)
		self.new_translate_page()

		self.statusbar = gtk.Statusbar()
		self.context_id = self.statusbar.get_context_id("slog")
		vbox.pack_start(self.statusbar, False, False, 0)

		self.window.show_all()

	def __create_action_group(self):
		entries = (
			("FileMenu", None, _("_File")),
			("ToolsMenu", None, _("_Tools")),
			("HelpMenu", None, _("_Help")),
			("NewTab",  gtk.STOCK_NEW, _("New _Tab"), "<control>T", "NewTab", self.new_translate_page),
			("Preferences",  gtk.STOCK_PREFERENCES, _("_Preferences"), None,
									"Preferences", self.on_preferences_activate),
			("Close",  gtk.STOCK_CLOSE, _("_Close"), "<control>W", "Close", self.delete_event),
			("Quit",  gtk.STOCK_QUIT, _("_Quit"), "<control>Q", "Quit", self.destroy),
			("DictMng", gtk.STOCK_PROPERTIES, _("_Manage dictionaries"), "<control>D", "Manage dictionaries", \
						self.on_dicts_manage_activate),
			("About", gtk.STOCK_ABOUT,	_("_About..."), None, "About", self.on_about_activate),
		)

		self.spy_action = gtk.ToggleAction("Spy", "_Spy", "Spy service", None)
		self.spy_action.connect("toggled", self.on_spy_clicked)

		action_group = gtk.ActionGroup("AppWindowActions")
		action_group.add_actions(entries)
		action_group.add_action_with_accel(self.spy_action, "<control>S")
		return action_group

	def __create_notify(self, title, message, timeout=3000):
		n = pynotify.Notification(title, message)
		n.attach_to_status_icon(self.status_icon)
		n.set_urgency(pynotify.URGENCY_NORMAL)
		n.set_timeout(timeout)
		n.set_icon_from_pixbuf(gtk.gdk.pixbuf_new_from_file_at_size(self.get_icon(LOGO_ICON), 48, 48))
		return n

	def get_icon(self, filename):
		path = self.conf.get_pixmap_dir()
		return os.path.join(path, filename)

	#################
	# GUI Callbacks #
	#################

	def delete_event(self, widget, data=None):
		if self.conf.tray_exit != 0:
			self.destroy(widget, data)

		if self.conf.tray_info != 0:
			n = self.__create_notify(self.name, "Close in system tray")
			if not n.show():
				print "Failed to send notification"

		self.window.hide()
		return True

	def destroy(self, widget, data=None):
		(width, height) = self.window.get_size()
		(left, top) = self.window.get_position()
		self.conf.set_size(width, height)
		self.conf.set_pos(left, top)
		self.conf.set_engine(self.sidebar.get_active())
		self.conf.save()
		gtk.main_quit()

	def on_spy_clicked(self, widget):
		if widget.get_active():
			self.status_icon.set_from_file(self.get_icon(LOGO_ICON_SPY))
			self.spy.start()
		else:
			self.status_icon.set_from_file(self.get_icon(LOGO_ICON))
			self.spy.stop()

	def on_preferences_activate(self, widget, data=None):
		dialog = PrefsDialog(self.window)
		dialog.run()
		dialog.destroy()

	def on_dicts_manage_activate(self, widget, data=None):
		dialog = DictsDialog(self.window)
		dialog.run()
		dialog.destroy()

	def on_about_activate(self, action):
		dialog = gtk.AboutDialog()
		dialog.set_name(self.name)
		dialog.set_logo(gtk.gdk.pixbuf_new_from_file(self.get_icon(LOGO_ICON)))
		dialog.set_copyright("\302\251 Copyright 2007 Renat Nasyrov (renatn@gmail.com)")
		dialog.set_website("http://lightlang.org.ru/")
		dialog.set_version(__version__)
		dialog.set_license(__license__)
		dialog.connect ("response", lambda d, r: d.destroy())
		dialog.show()

	def on_tray_clicked(self, args):
		self.window_toggle()

	def on_tray_popup(self, icon, event_button, event_time):
		menu = self.uimanager.get_widget("/TrayMenu")
		menu.popup(None, None, gtk.status_icon_position_menu, event_button, event_time, self.status_icon)

	# Activated by Translate Engine
	def on_translate(self, word, translate):
		tv = self.notebook.get_page()
		tv.set_translate(word, translate)

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
			self.app_show()

	def app_show(self):
		self.window.show_all()
		gobject.idle_add(self.window_present_and_focus)

	def window_present_and_focus(self):
		self.window.present()
		self.window.grab_focus()

	def new_translate_page(self, args=None):
		label = gtk.Label()
		tv = TransView(label)
		self.notebook.add_page(label, tv)

	def run(self):
		if not pynotify.init("SLog Notification"):
			print "Failed init python-notify module"
		gtk.main()

class SLogDBus(dbus.service.Object, MainWindow):

	def __init__(self, bus_name, obj_path, slog_prefix):
		dbus.service.Object.__init__(self, bus_name, obj_path)
		MainWindow.__init__(self, slog_prefix)

	@dbus.service.method("org.LightLang.SLogInterface")
	def dbus_spy_toggle(self):
		self.spy_action.activate()

	@dbus.service.method("org.LightLang.SLogInterface")
	def toggle(self):
		self.window_toggle()

	@dbus.service.method("org.LightLang.SLogInterface")
	def show(self):
		self.window.hide()
		self.app_show()

