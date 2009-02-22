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

from PyQt4 import Qt
import Config
import Const
try : # optional requires python-xlib
	import Xlib
	import Xlib.display
	PythonXlibExistsFlag = True
except :
	PythonXlibExistsFlag = False
	print Const.MyName+": python-xlib is not found, please, install it"
import MouseSelector
import KeyboardModifierMenu

#####
IconsDir = Config.Prefix+"/lib/xsl/icons/"

#####
def tr(str) :
	return Qt.QApplication.translate("@default", str)

#####
class SpyMenu(Qt.QMenu) :
	def __init__(self, title, parent = None) :
		Qt.QObject.__init__(self, title, parent)

		self.mouse_selector = MouseSelector.MouseSelector()

		#####

		self.start_spy_menu_action = self.addAction(Qt.QIcon(IconsDir+"start_spy_16.png"),
			tr("Start Spy"), self.startSpy)
		self.stop_spy_menu_action = self.addAction(Qt.QIcon(IconsDir+"stop_spy_16.png"),
			tr("Stop Spy"), self.stopSpy)
		self.stop_spy_menu_action.setEnabled(False)
		self.addSeparator()
		self.show_translate_window_menu_action = self.addAction(tr("Show popup window"))
		self.show_translate_window_menu_action.setCheckable(True)
		self.auto_detect_window_menu_action = self.addAction(tr("Auto-detect window"))
		self.auto_detect_window_menu_action.setCheckable(True)
		self.addSeparator()
		self.keyboard_modifier_menu = KeyboardModifierMenu.KeyboardModifierMenu(tr("Keyboard modifier"))
		self.keyboard_modifier_menu.setIcon(Qt.QIcon(IconsDir+"keys_16.png"))
		self.addMenu(self.keyboard_modifier_menu)

		#####

		self.connect(self.mouse_selector, Qt.SIGNAL("selectionChanged(const QString &)"), self.uFindRequestSignal)
		self.connect(self.mouse_selector, Qt.SIGNAL("selectionChanged(const QString &)"), self.showTranslateWindow)

		self.connect(self.keyboard_modifier_menu, Qt.SIGNAL("modifierChanged(int)"),
			self.mouse_selector.setModifier)


	### Public ###

	def startSpy(self) :
		self.mouse_selector.start()

		self.start_spy_menu_action.setEnabled(False)
		self.stop_spy_menu_action.setEnabled(True)

		self.statusChangedSignal(tr("Spy is running"))

		self.spyStartedSignal()

	def stopSpy(self) :
		self.mouse_selector.stop()

		self.start_spy_menu_action.setEnabled(True)
		self.stop_spy_menu_action.setEnabled(False)

		self.statusChangedSignal(tr("Spy is stopped"))

		self.spyStoppedSignal()

	### 

	def saveSettings(self) :
		settings = Qt.QSettings(Const.Organization, Const.MyName)
		settings.setValue("spy_menu/show_translate_window_flag",
			Qt.QVariant(self.show_translate_window_menu_action.isChecked()))
		settings.setValue("spy_menu/auto_detect_window_flag",
			Qt.QVariant(self.auto_detect_window_menu_action.isChecked()))
		settings.setValue("spy_menu/spy_is_running_flag",
			Qt.QVariant(self.stop_spy_menu_action.isEnabled()))

		self.keyboard_modifier_menu.saveSettings()


	def loadSettings(self) :
		settings = Qt.QSettings(Const.Organization, Const.MyName)
		self.show_translate_window_menu_action.setChecked(settings.value("spy_menu/show_translate_window_flag",
			Qt.QVariant(True)).toBool())
		self.auto_detect_window_menu_action.setChecked(settings.value("spy_menu/auto_detect_window_flag",
			Qt.QVariant(True)).toBool())
		if settings.value("spy_menu/spy_is_running_flag", Qt.QVariant(False)).toBool() :
			self.startSpy()

		self.keyboard_modifier_menu.loadSettings()


	### Private ###

	def showTranslateWindow(self) :
		if self.show_translate_window_menu_action.isChecked() :
			if self.auto_detect_window_menu_action.isChecked() :
				if Qt.QApplication.activeWindow() == None :
					self.showTranslateWindowRequestSignal()
			else :
				self.showTranslateWindowRequestSignal()


	### Signals ###

	def spyStartedSignal(self) :
		self.emit(Qt.SIGNAL("spyStarted()"))

	def spyStoppedSignal(self) :
		self.emit(Qt.SIGNAL("spyStopped()"))

	def statusChangedSignal(self, text) :
		self.emit(Qt.SIGNAL("statusChanged(const QString &)"), text)

	def uFindRequestSignal(self, word) :
		self.emit(Qt.SIGNAL("uFindRequest(const QString &)"), word)

	def showTranslateWindowRequestSignal(self) :
		self.emit(Qt.SIGNAL("showTranslateWindowRequest()"))

