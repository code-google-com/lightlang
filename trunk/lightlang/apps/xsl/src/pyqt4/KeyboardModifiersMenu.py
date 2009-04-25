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
import User
import KeyboardModifiers


#####
def tr(str) :
	return Qt.QApplication.translate("@default", str)


#####
class KeyboardModifiersMenu(Qt.QMenu) :
	def __init__(self, title, parent = None) :
		Qt.QMenu.__init__(self, title, parent)

		#####

		self.actions_list = []
		self.actions_group = Qt.QActionGroup(self)

		#####

		self.addModifier(tr("Left Ctrl"), KeyboardModifiers.LeftCtrlModifier)
		self.addModifier(tr("Left Alt"), KeyboardModifiers.LeftAltModifier)
		self.addModifier(tr("Left Shift"), KeyboardModifiers.LeftShiftModifier)
		self.addModifier(tr("Left Win"), KeyboardModifiers.LeftWinModifier)
		self.addSeparator()
		self.addModifier(tr("Right Ctrl"), KeyboardModifiers.RightCtrlModifier)
		self.addModifier(tr("Right Alt"), KeyboardModifiers.RightAltModifier)
		self.addModifier(tr("Right Shift"), KeyboardModifiers.RightShiftModifier)
		self.addModifier(tr("Right Win"), KeyboardModifiers.RightWinModifier)
		self.addSeparator()
		self.addModifier(tr("No modifier"), KeyboardModifiers.NoModifier)

		#####

		self.connect(self.actions_group, Qt.SIGNAL("triggered(QAction *)"), self.modifierChangedSignal)

		#####

		self.setIndex(0)


	### Public ###

	def saveSettings(self) :
		settings = User.settings()
		settings.setValue("keyboard_modifiers_menu/modifier_index", Qt.QVariant(self.index()))

	def loadSettings(self) :
		settings = User.settings()
		self.setIndex(settings.value("keyboard_modifiers_menu/modifier_index", Qt.QVariant(0)).toInt()[0])


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

