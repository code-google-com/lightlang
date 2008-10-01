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
import sys
import Config
import Const
try : # optional requires python-xlib
	import Xlib
	import Xlib.display
	PythonXlibExistsFlag = True
except :
	PythonXlibExistsFlag = False
	print Const.MyName+": python-xlib is not found, please, install it"

#####
SL = Config.Prefix+"/bin/sl"
IconsDir = Config.Prefix+"/lib/xsl/icons/"

LeftCtrlModifier = 133
LeftAltModifier = 256
LeftShiftModifier = 194
LeftWinModifier = 451
RightCtrlModifier = 421
RightAltModifier = 449
RightShiftModifier = 230
RightWinModifier = 452
NoModifier = -1

#####
class MouseSelector(Qt.QObject) :
	def __init__(self, parent = None) :
		Qt.QObject.__init__(self, parent)

		self.clipboard = Qt.QApplication.clipboard()
		self.old_selection = Qt.QString()

		self.timer = Qt.QTimer()
		self.timer.setInterval(300)

		if PythonXlibExistsFlag :
			self.display = Xlib.display.Display()

		self.modifier = LeftCtrlModifier

		#####

		self.connect(self.timer, Qt.SIGNAL("timeout()"), self.checkSelection)


	### Public ###

	def start(self) :
		self.clipboard.setText(Qt.QString(""), Qt.QClipboard.Selection)
		self.old_selection.clear()
		self.timer.start()

	def stop(self) :
		self.timer.stop()

	def setModifier(self, modifier) :
		self.modifier = modifier


	### Private ###

	def checkSelection(self) :
		word = self.clipboard.text(Qt.QClipboard.Selection)
		word = word.simplified()
		if word.isEmpty() :
			return
		word = word.toLower()

		if word == self.old_selection :
			return
		self.old_selection = word

		# TODO: add mouse-buttons checks
		if not self.checkModifier() :
			return

		self.selectionChangedSignal(word)

	def checkModifier(self) :
		if not PythonXlibExistsFlag :
			return True

		if self.modifier == NoModifier :
			return True

		keymap = self.display.query_keymap()
		keys = []

		for count1 in range(0, len(keymap)) :
			Qt.QCoreApplication.processEvents()
			for count2 in range(0, 32) :
				keys.append(int(keymap[count1] & (1 << count2)))

		if keys[self.modifier] != 0 :
			return True
		else :
			return False


	### Signals ###

	def selectionChangedSignal(self, word) :
		self.emit(Qt.SIGNAL("selectionChanged(const QString &)"), word)


#####
class KeyboardModifierMenu(Qt.QMenu) :
	def __init__(self, title, parent = None) :
		Qt.QMenu.__init__(self, title, parent)

		self.actions_list = []
		self.actions_group = Qt.QActionGroup(self)

		###

		self.addModifier(self.tr("Left Ctrl"), LeftCtrlModifier)
		self.addModifier(self.tr("Left Alt"), LeftAltModifier)
		self.addModifier(self.tr("Left Shift"), LeftShiftModifier)
		self.addModifier(self.tr("Left Win"), LeftWinModifier)
		self.addSeparator()
		self.addModifier(self.tr("Right Ctrl"), RightCtrlModifier)
		self.addModifier(self.tr("Right Alt"), RightAltModifier)
		self.addModifier(self.tr("Right Shift"), RightShiftModifier)
		self.addModifier(self.tr("Right Win"), RightWinModifier)
		self.addSeparator()
		self.addModifier(self.tr("No modifier"), NoModifier)

		#####

		self.connect(self.actions_group, Qt.SIGNAL("triggered(QAction *)"), self.modifierChangedSignal)

		#####

		self.setIndex(0)

		if not PythonXlibExistsFlag :
			self.setTitle(self.tr("No modifiers available"))
			self.setEnabled(False)


	### Public ###

	def saveSettings(self) :
		settings = Qt.QSettings(Const.Organization, Const.MyName)
		settings.setValue("modifier_menu/modifier_index", Qt.QVariant(self.index()))

	def loadSettings(self) :
		settings = Qt.QSettings(Const.Organization, Const.MyName)
		self.setIndex(settings.value("modifier_menu/modifier_index", Qt.QVariant(0)).toInt()[0])


	### Private ###

	def index(self) :
		count = 0
		while count < len(self.actions_list) :
			if self.actions_list[count].isChecked() :
				return count
			count += 1

	def setIndex(self, index) :
		self.actions_list[index].setChecked(True)
		self.modifierChangedSignal(self.actions_list[index])

	def addModifier(self, title, modifier) :
		action = Qt.QAction(title, self)
		action.setCheckable(True)
		action.setData(Qt.QVariant(modifier))

		self.addAction(action)
		self.actions_list.append(action)
		self.actions_group.addAction(action)


	### Signals ###

	def modifierChangedSignal(self, action) :
		modifier = action.data().toInt()[0]
		self.emit(Qt.SIGNAL("modifierChanged(int)"), modifier)


#####
class SpyMenu(Qt.QMenu) :
	def __init__(self, title, parent = None) :
		Qt.QObject.__init__(self, title, parent)

		self.mouse_selector = MouseSelector()

		#####

		self.start_spy_menu_action = self.addAction(Qt.QIcon(IconsDir+"start_spy_16.png"),
			self.tr("Start Spy"), self.startSpy)
		self.stop_spy_menu_action = self.addAction(Qt.QIcon(IconsDir+"stop_spy_16.png"),
			self.tr("Stop Spy"), self.stopSpy)
		self.stop_spy_menu_action.setEnabled(False)
		self.addSeparator()
		self.show_translate_window_menu_action = self.addAction(self.tr("Show popup window"))
		self.show_translate_window_menu_action.setCheckable(True)
		self.auto_detect_window_menu_action = self.addAction(self.tr("Auto-detect window"))
		self.auto_detect_window_menu_action.setCheckable(True)
		self.addSeparator()
		self.keyboard_modifier_menu = KeyboardModifierMenu(self.tr("Keyboard modifier"))
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

		self.statusChangedSignal(self.tr("Spy is running"))

		self.spyStartedSignal()

	def stopSpy(self) :
		self.mouse_selector.stop()

		self.start_spy_menu_action.setEnabled(True)
		self.stop_spy_menu_action.setEnabled(False)

		self.statusChangedSignal(self.tr("Spy is stopped"))

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
