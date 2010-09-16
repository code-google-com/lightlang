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
import UserStyleCssCollection


#####
def tr(str) :
	return Qt.QApplication.translate("@default", str)


#####
class TransparentFrame(Qt.QFrame) :
	def __init__(self, parent = None) :
		Qt.QFrame.__init__(self, parent)

		self.setFrameShape(Qt.QFrame.Box)
		self.setFrameShadow(Qt.QFrame.Raised)

		#####

		self._color = UserStyleCssCollection.transparentFrameBackgroundColor()
		self._alpha = UserStyleCssCollection.transparentFrameBackgroundOpacity()

		#####

		self.setAlpha(self._alpha)


	### Private ###

	def setAlpha(self, alpha) :
		self.setStyleSheet(Qt.QString("QFrame {border: 1px solid gray; border-radius: 4px; background-color: rgb(%1, %2, %3, %4);}")
			.arg(self._color.red()).arg(self._color.green()).arg(self._color.blue()).arg(alpha))


	### Handlers ###

	def enterEvent(self, event) :
		self.setAlpha(255)
		Qt.QFrame.enterEvent(self, event)

	def leaveEvent(self, event) :
		self.setAlpha(self._alpha)
		Qt.QFrame.leaveEvent(self, event)

