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

		self.mouse_selector = MouseSelector.MouseSelector()

		#####

		self.start_spy_menu_action = self.addAction(IconsLoader.icon("media-playback-start"), tr("Start Spy"), self.startSpy)
		self.stop_spy_menu_action = self.addAction(IconsLoader.icon("media-playback-stop"), tr("Stop Spy"), self.stopSpy)
		self.stop_spy_menu_action.setEnabled(False)

		self.addSeparator()

		self.show_translate_window_menu_action = self.addAction(tr("Show popup window"))
		self.show_translate_window_menu_action.setCheckable(True)

		self.auto_detect_window_menu_action = self.addAction(tr("Auto-detect window"))
		self.auto_detect_window_menu_action.setCheckable(True)

		try :
			self.keyboard_modifiers_menu = RadioButtonsMenu.RadioButtonsMenu(tr("Keyboard modifiers"))
			self.keyboard_modifiers_menu.setIcon(IconsLoader.icon("configure-shortcuts"))
			self.keyboard_modifiers_menu.addRadioButton(tr("No modifier"), Qt.QVariant(KeyboardModifiersTest.NoModifier))

			self.keyboard_modifiers_menu.addSeparator()

			self.keyboard_modifiers_menu.addRadioButton(tr("Left Ctrl"), Qt.QVariant(KeyboardModifiersTest.LeftCtrlModifier))
			self.keyboard_modifiers_menu.addRadioButton(tr("Left Alt"), Qt.QVariant(KeyboardModifiersTest.LeftAltModifier))
			self.keyboard_modifiers_menu.addRadioButton(tr("Left Shift"), Qt.QVariant(KeyboardModifiersTest.LeftShiftModifier))
			self.keyboard_modifiers_menu.addRadioButton(tr("Left Win"), Qt.QVariant(KeyboardModifiersTest.LeftWinModifier))

			self.keyboard_modifiers_menu.addSeparator()

			self.keyboard_modifiers_menu.addRadioButton(tr("Right Ctrl"), Qt.QVariant(KeyboardModifiersTest.RightCtrlModifier))
			self.keyboard_modifiers_menu.addRadioButton(tr("Right Alt"), Qt.QVariant(KeyboardModifiersTest.RightAltModifier))
			self.keyboard_modifiers_menu.addRadioButton(tr("Right Shift"), Qt.QVariant(KeyboardModifiersTest.RightShiftModifier))
			self.keyboard_modifiers_menu.addRadioButton(tr("Right Win"), Qt.QVariant(KeyboardModifiersTest.RightWinModifier))

			self.keyboard_modifiers_menu.setIndex(0)
			self.addMenu(self.keyboard_modifiers_menu)
		except :
			self.fictive_keyboard_modifiers_menu = Qt.QMenu(tr("Keyboard modifiers"))
			self.fictive_keyboard_modifiers_menu.setIcon(IconsLoader.icon("configure-shortcuts"))
			self.fictive_keyboard_modifiers_menu.setEnabled(False)
			self.addMenu(self.fictive_keyboard_modifiers_menu)

		self.addSeparator()

		self.translate_methods_menu = RadioButtonsMenu.RadioButtonsMenu(tr("Translate methods"))
		self.translate_methods_menu.setIcon(IconsLoader.icon("configure"))
		self.addMenu(self.translate_methods_menu)

		#####

		self.connect(self.mouse_selector, Qt.SIGNAL("selectionChanged(const QString &)"), self.translateRequestSignal)
		self.connect(self.mouse_selector, Qt.SIGNAL("selectionChanged(const QString &)"), self.showTranslateWindow)

		try :
			self.connect(self.keyboard_modifiers_menu, Qt.SIGNAL("dataChanged(const QVariant &)"),
				lambda data : self.mouse_selector.setModifier(data.toInt()[0]))
		except : pass


	### Public ###

	def addTranslateMethod(self, label, object_name, method_name) :
		signal_string = Qt.QString("%1__%2__translateRequest(const QString &)").arg(object_name).arg(method_name)
		self.translate_methods_menu.addRadioButton(label, Qt.QVariant(signal_string))
		return Qt.QString(signal_string)

	###

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

	def isRunning(self) :
		return self.mouse_selector.isRunning()

	### 

	def saveSettings(self) :
		settings = Settings.settings()
		settings.setValue("spy_menu/show_translate_window_flag", Qt.QVariant(self.show_translate_window_menu_action.isChecked()))
		settings.setValue("spy_menu/auto_detect_window_flag", Qt.QVariant(self.auto_detect_window_menu_action.isChecked()))
		settings.setValue("spy_menu/spy_is_running_flag", Qt.QVariant(self.mouse_selector.isRunning()))
		try :
			settings.setValue("spy_menu/keyboard_modifier_index", Qt.QVariant(self.keyboard_modifiers_menu.index()))
		except : pass
		settings.setValue("spy_menu/translate_method_index", Qt.QVariant(self.translate_methods_menu.index()))


	def loadSettings(self) :
		settings = Settings.settings()
		self.show_translate_window_menu_action.setChecked(settings.value("spy_menu/show_translate_window_flag", Qt.QVariant(True)).toBool())
		self.auto_detect_window_menu_action.setChecked(settings.value("spy_menu/auto_detect_window_flag", Qt.QVariant(True)).toBool())
		if settings.value("spy_menu/spy_is_running_flag", Qt.QVariant(False)).toBool() :
			self.startSpy()
		try :
			self.keyboard_modifiers_menu.setIndex(settings.value("spy_menu/keyboard_modifier_index", Qt.QVariant(0)).toInt()[0])
		except : pass
		self.translate_methods_menu.setIndex(settings.value("spy_menu/translate_method_index", Qt.QVariant(0)).toInt()[0])


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

	def translateRequestSignal(self, text) :
		self.emit(Qt.SIGNAL(self.translate_methods_menu.data().toString()), text)

	def showTranslateWindowRequestSignal(self) :
		self.emit(Qt.SIGNAL("showTranslateWindowRequest()"))

