# -*- mode: python; coding: utf-8; -*-

import os
import gtk, gobject
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


class MainWindow(gtk.Window):

	def __init__(self, parent=None):
		gtk.Window.__init__(self)
		try:
			self.set_screen(parent.get_screen())
		except AttributeError:
			self.connect('destroy', lambda *w: gtk.main_quit())
	
		self.conf = SlogConf()

		# Translation stuff
		try:
			gettext.install("slog", LOCALE_DIR, unicode=1)
		except:
			pass
		gettext.textdomain("slog")

		# Create tray icon 
		self.status_icon = gtk.status_icon_new_from_file(get_icon("slog.png"))
		self.status_icon.set_tooltip(APP_NAME)
		self.status_icon.connect("popup-menu", self.on_tray_popup)
		self.status_icon.connect("activate", self.on_tray_clicked)

		# Create main window
		self.tooltips = gtk.Tooltips()
		self.notebook = MyNotebook()

		self.set_icon_from_file(get_icon("slog.png"))
		self.set_border_width(1)
		self.set_title("%s %s" % (APP_NAME, VERSION))
		self.set_size_request(396, 256)

		(width, height) = self.conf.get_size()
		(left, top) = self.conf.get_pos()
		if left != 0 or top != 0:
			self.move(left, top)
		self.set_default_size(width, height)

		self.connect("delete_event", self.delete_event)
		self.connect("destroy", self.destroy)

		# Create Actions
		self.uimanager = gtk.UIManager()
		self.set_data("ui-manager", self.uimanager)
		self.uimanager.insert_action_group(self.__create_action_group(), 0)
		self.add_accel_group(self.uimanager.get_accel_group())

		try:
			uimanagerid = self.uimanager.add_ui_from_string(ui_info)
		except gobject.GError, msg:
			print "building menus failed: %s" % msg

		vbox = gtk.VBox(False, 4)
		self.add(vbox)

		menubar = self.uimanager.get_widget("/MenuBar")
		vbox.pack_start(menubar, False, False, 0)

		self.hpaned = gtk.HPaned()
		vbox.pack_start(self.hpaned, True, True, 0)

		self.sidebar = SideBar()

		self.hpaned.add1(self.sidebar)
		self.hpaned.add2(self.notebook)
		self.new_translate_page()

		self.statusbar = gtk.Statusbar()
		self.context_id = self.statusbar.get_context_id("slog")
		vbox.pack_start(self.statusbar, False, False, 0)

		if self.conf.tray_start == 0:
			self.show_all()

		if self.conf.spy_auto == 1:
			self.spy_action.activate()

		#gobject.idle_add(self.__load_plugins)
		self.__load_plugins()

	def __load_plugins(self):
		self.plugin_manager = PluginManager()
		self.plugin_manager.scan_for_plugins()

		list_enabled = self.conf.get_enabled_plugins()
		for plugin in self.plugin_manager.get_available():

			while gtk.events_pending():
				gtk.main_iteration(False)

			if plugin not in list_enabled:
				continue
				
			view = self.plugin_manager.enable_plugin(plugin)
			view.connect("translate_it", self.on_translate)
			view.connect("changed", self.on_status_changed)
			self.sidebar.append_page(plugin, view)
			view.show_all()
		
		self.spy = Spy()

		self.sidebar.set_active(self.conf.get_engine())

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
		n.set_icon_from_pixbuf(gtk.gdk.pixbuf_new_from_file_at_size(get_icon("slog.png"), 48, 48))
		return n


	#################
	# GUI Callbacks #
	#################

	def delete_event(self, widget, data=None):
		if self.conf.tray_exit != 0:
			self.destroy(widget, data)

		if self.conf.tray_info != 0:
			n = self.__create_notify(APP_NAME, "Close in system tray")
			if not n.show():
				print "Failed to send notification"

		self.hide()
		return True

	def destroy(self, widget, data=None):
		(width, height) = self.get_size()
		(left, top) = self.get_position()
		self.conf.set_size(width, height)
		self.conf.set_pos(left, top)
		self.conf.set_engine(self.sidebar.get_active())
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
		dialog = PrefsDialog(self, self.plugin_manager)
		dialog.run()
		dialog.destroy()

	def on_dicts_manage_activate(self, widget, data=None):
		dialog = DictsDialog(self)
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
		menu = self.uimanager.get_widget("/TrayMenu")
		menu.popup(None, None, gtk.status_icon_position_menu, event_button, event_time, self.status_icon)

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
		if self.get_property("visible"):
			self.hide()
		else:
			self.app_show()

	def app_show(self):
		self.show_all()
		gobject.idle_add(self.window_present_and_focus)

	def window_present_and_focus(self):
		self.present()
		self.grab_focus()

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
