# -*- coding: utf8 -*-
#
# XSL - graphical interface for SL
# Copyright (C) 2007-2016 Devaev Maxim
#
# This file is part of XSL.
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.


import Qt
import Config
import Const
import EntitledMenu
try :
	import KeysGrabberThread
	import KeysGrabberThreadSingleton
except : pass


#####
MyIcon = Config.Prefix+"/lib/xsl/icons/xsl_16.png"
IconsDir = Config.Prefix+"/lib/xsl/icons/"


#####
def tr(str) :
	return Qt.QApplication.translate("@default", str)


#####
class TrayIcon(Qt.QSystemTrayIcon) :
	def __init__(self, parent = None) :
		Qt.QSystemTrayIcon.__init__(self, parent)

		self.setIcon(Qt.QIcon(IconsDir+"xsl_22.png"))
		self.setToolTip(tr("XSL - graphical interface for SL\nSpy is stopped"))

		#####

		try :
			self.keys_grabber_thread_singleton = KeysGrabberThreadSingleton.KeysGrabberThreadSingleton()
		except : pass

		self.tray_menu = EntitledMenu.EntitledMenu(Qt.QIcon(MyIcon), Const.Organization+" "+Const.MyName)

		self.start_spy_menu_action = self.tray_menu.addAction(Qt.QIcon(IconsDir+"start_spy_16.png"), tr("Start Spy"), self.startSpy)
		self.stop_spy_menu_action = self.tray_menu.addAction(Qt.QIcon(IconsDir+"stop_spy_16.png"), tr("Stop Spy"), self.stopSpy)
		self.stop_spy_menu_action.setEnabled(False)

		self.tray_menu.addSeparator()

		try :
			self.keys_grabber_thread_singleton.addHandler(KeysGrabberThread.Key_L, KeysGrabberThread.WinModifier,
				self.visibleChangeRequestSignal)
			self.tray_menu.addAction(Qt.QIcon(IconsDir+"window_16.png"), tr("Dictionary window"),
				self.visibleChangeRequestSignal, Qt.QKeySequence("Win+L"))
		except :
			self.tray_menu.addAction(Qt.QIcon(IconsDir+"window_16.png"), tr("Dictionary window"),
				self.visibleChangeRequestSignal)

		self.tray_menu.addSeparator()

		self.tray_menu.addAction(Qt.QIcon(IconsDir+"exit_16.png"), tr("Quit"), self.exit)
		self.setContextMenu(self.tray_menu)

		#####

		self.connect(self, Qt.SIGNAL("activated(QSystemTrayIcon::ActivationReason)"), self.act)


	### Public ###

	def spyStarted(self) :
		self.start_spy_menu_action.setEnabled(False)
		self.stop_spy_menu_action.setEnabled(True)

		self.setIcon(Qt.QIcon(IconsDir+"xsl+spy_22.png"))

		self.setToolTip(tr("XSL - graphical interface for SL\nSpy is running"))

	def spyStopped(self) :
		self.start_spy_menu_action.setEnabled(True)
		self.stop_spy_menu_action.setEnabled(False)

		self.setIcon(Qt.QIcon(IconsDir+"xsl_22.png"))

		self.setToolTip(tr("XSL - graphical interface for SL\nSpy is stopped"))


	### Private ###

	def startSpy(self) :
		self.spyStarted()
		self.startSpyRequestSignal()

	def stopSpy(self) :
		self.spyStopped()
		self.stopSpyRequestSignal()

	def act(self, reason) :
		if reason == Qt.QSystemTrayIcon.Trigger :
			self.visibleChangeRequestSignal()

	def exit(self) :
		self.exitRequestSignal()


	### Signals ###

	def startSpyRequestSignal(self) :
		self.emit(Qt.SIGNAL("startSpyRequest()"))

	def stopSpyRequestSignal(self) :
		self.emit(Qt.SIGNAL("stopSpyRequest()"))

	def visibleChangeRequestSignal(self) :
		self.emit(Qt.SIGNAL("visibleChangeRequest()"))

	def exitRequestSignal(self) :
		self.emit(Qt.SIGNAL("exitRequest()"))

