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
import FictiveButtonEventFilter


#####
def tr(str) :
	return Qt.QApplication.translate("@default", str)


#####
class EntitledMenu(Qt.QMenu) :
	def __init__(self, icon = None, text = None, parent = None) :
		Qt.QMenu.__init__(self, parent)

		if icon != None and text != None :
			self.addCaption(icon, text)


	### Public ###

	def addCaption(self, icon, text, before_action = None) :
		button_action = Qt.QAction(self)
		button_action_font = button_action.font()
		button_action_font.setBold(True)
		button_action.setFont(button_action_font)
		button_action.setIcon(icon)
		button_action.setText(text)

		fictive_action = Qt.QWidgetAction(self)
		fictive_button = Qt.QToolButton()
		fictive_button.installEventFilter(FictiveButtonEventFilter.FictiveButtonEventFilter(self))
		fictive_button.setDefaultAction(button_action)
		fictive_button.setDown(True)
		fictive_button.setToolButtonStyle(Qt.Qt.ToolButtonTextBesideIcon)
		fictive_button.click()
		fictive_action.setDefaultWidget(fictive_button)
		fictive_action.setEnabled(False)
		fictive_button.setEnabled(True)

		self.insertAction(before_action, fictive_action)

		return fictive_action

