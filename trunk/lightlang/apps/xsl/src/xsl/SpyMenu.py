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
import Settings
import IconsLoader
import MouseSelector
import RadioButtonsMenu
try :
	import KeyboardModifiersTest
except : pass


#####
def tr(str) :
	return Qt.QApplication.translate("@default", str)


#####
class SpyMenu(Qt.QMenu) :
	def __init__(self, title, parent = None) :
		Qt.QObject.__init__(self, title, parent)

		self.setObjectName("spy_menu")

		#####

		self._mouse_selector = MouseSelector.MouseSelector()

		#####

		self._start_spy_menu_action = self.addAction(IconsLoader.icon("media-playback-start"), tr("Start Spy"), self.startSpy)
		self._stop_spy_menu_action = self.addAction(IconsLoader.icon("media-playback-stop"), tr("Stop Spy"), self.stopSpy)
		self._stop_spy_menu_action.setEnabled(False)

		self.addSeparator()

		self._show_translate_window_menu_action = self.addAction(tr("Show popup window"))
		self._show_translate_window_menu_action.setCheckable(True)

		self._auto_detect_window_menu_action = self.addAction(tr("Auto-detect window"))
		self._auto_detect_window_menu_action.setCheckable(True)

		try :
			self._keyboard_modifiers_menu = RadioButtonsMenu.RadioButtonsMenu(tr("Keyboard modifiers"))
			self._keyboard_modifiers_menu.setIcon(IconsLoader.icon("configure-shortcuts"))
			self._keyboard_modifiers_menu.addRadioButton(tr("No modifier"), Qt.QVariant(KeyboardModifiersTest.NoModifier))

			self._keyboard_modifiers_menu.addSeparator()

			self._keyboard_modifiers_menu.addRadioButton(tr("Left Ctrl"), Qt.QVariant(KeyboardModifiersTest.LeftCtrlModifier))
			self._keyboard_modifiers_menu.addRadioButton(tr("Left Alt"), Qt.QVariant(KeyboardModifiersTest.LeftAltModifier))
			self._keyboard_modifiers_menu.addRadioButton(tr("Left Shift"), Qt.QVariant(KeyboardModifiersTest.LeftShiftModifier))
			self._keyboard_modifiers_menu.addRadioButton(tr("Left Win"), Qt.QVariant(KeyboardModifiersTest.LeftWinModifier))

			self._keyboard_modifiers_menu.addSeparator()

			self._keyboard_modifiers_menu.addRadioButton(tr("Right Ctrl"), Qt.QVariant(KeyboardModifiersTest.RightCtrlModifier))
			self._keyboard_modifiers_menu.addRadioButton(tr("Right Alt"), Qt.QVariant(KeyboardModifiersTest.RightAltModifier))
			self._keyboard_modifiers_menu.addRadioButton(tr("Right Shift"), Qt.QVariant(KeyboardModifiersTest.RightShiftModifier))
			self._keyboard_modifiers_menu.addRadioButton(tr("Right Win"), Qt.QVariant(KeyboardModifiersTest.RightWinModifier))

			self._keyboard_modifiers_menu.setIndex(0)
			self.addMenu(self._keyboard_modifiers_menu)
		except :
			self._fictive_keyboard_modifiers_menu = Qt.QMenu(tr("Keyboard modifiers"))
			self._fictive_keyboard_modifiers_menu.setIcon(IconsLoader.icon("configure-shortcuts"))
			self._fictive_keyboard_modifiers_menu.setEnabled(False)
			self.addMenu(self._fictive_keyboard_modifiers_menu)

		self.addSeparator()

		self._translate_methods_menu = RadioButtonsMenu.RadioButtonsMenu(tr("Translate methods"))
		self._translate_methods_menu.setIcon(IconsLoader.icon("configure"))
		self.addMenu(self._translate_methods_menu)

		#####

		self.connect(self._mouse_selector, Qt.SIGNAL("selectionChanged(const QString &)"), self.translateRequestSignal)
		self.connect(self._mouse_selector, Qt.SIGNAL("selectionChanged(const QString &)"), self.showTranslateWindow)

		try :
			self.connect(self._keyboard_modifiers_menu, Qt.SIGNAL("dataChanged(const QVariant &)"),
				lambda data : self._mouse_selector.setModifier(data.toInt()[0]))
		except : pass


	### Public ###

	def addTranslateMethod(self, label, object_name, method_name) :
		signal_string = Qt.QString("%1__%2__translateRequest(const QString &)").arg(object_name).arg(method_name)
		self._translate_methods_menu.addRadioButton(label, Qt.QVariant(signal_string))
		return Qt.QString(signal_string)

	###

	def startSpy(self) :
		self._mouse_selector.start()

		self._start_spy_menu_action.setEnabled(False)
		self._stop_spy_menu_action.setEnabled(True)

		self.statusChangedSignal(tr("Spy is running"))

		self.spyStartedSignal()

	def stopSpy(self) :
		self._mouse_selector.stop()

		self._start_spy_menu_action.setEnabled(True)
		self._stop_spy_menu_action.setEnabled(False)

		self.statusChangedSignal(tr("Spy is stopped"))

		self.spyStoppedSignal()

	def isRunning(self) :
		return self._mouse_selector.isRunning()

	### 

	def saveSettings(self) :
		settings = Settings.settings()
		settings.setValue("spy_menu/show_translate_window_flag", Qt.QVariant(self._show_translate_window_menu_action.isChecked()))
		settings.setValue("spy_menu/auto_detect_window_flag", Qt.QVariant(self._auto_detect_window_menu_action.isChecked()))
		settings.setValue("spy_menu/spy_is_running_flag", Qt.QVariant(self._mouse_selector.isRunning()))
		try :
			settings.setValue("spy_menu/keyboard_modifier_index", Qt.QVariant(self._keyboard_modifiers_menu.index()))
		except : pass
		settings.setValue("spy_menu/translate_method_index", Qt.QVariant(self._translate_methods_menu.index()))

	def loadSettings(self) :
		settings = Settings.settings()
		self._show_translate_window_menu_action.setChecked(settings.value("spy_menu/show_translate_window_flag", Qt.QVariant(True)).toBool())
		self._auto_detect_window_menu_action.setChecked(settings.value("spy_menu/auto_detect_window_flag", Qt.QVariant(True)).toBool())
		if settings.value("spy_menu/spy_is_running_flag", Qt.QVariant(False)).toBool() :
			self.startSpy()
		try :
			self._keyboard_modifiers_menu.setIndex(settings.value("spy_menu/keyboard_modifier_index", Qt.QVariant(0)).toInt()[0])
		except : pass
		self._translate_methods_menu.setIndex(settings.value("spy_menu/translate_method_index", Qt.QVariant(0)).toInt()[0])


	### Private ###

	def showTranslateWindow(self) :
		if self._show_translate_window_menu_action.isChecked() :
			if self._auto_detect_window_menu_action.isChecked() :
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

	def translateRequestSignal(self, text) :
		self.emit(Qt.SIGNAL(self._translate_methods_menu.data().toString()), text)

	def showTranslateWindowRequestSignal(self) :
		self.emit(Qt.SIGNAL("showTranslateWindowRequest()"))

