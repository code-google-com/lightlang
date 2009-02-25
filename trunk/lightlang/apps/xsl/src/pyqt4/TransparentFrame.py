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

#####
def tr(str) :
	return Qt.QApplication.translate("@default", str)

#####
TransparentAlpha = 180
NonTransparentAlpha = 255

#####
class TransparentFrame(Qt.QFrame) :
	def __init__(self, parent = None) :
		Qt.QFrame.__init__(self, parent)

		self.setFrameShape(Qt.QFrame.Box)
		self.setFrameShadow(Qt.QFrame.Raised)

		#####

		self.color = Qt.QApplication.palette().color(Qt.QPalette.Window)

		#####

		self.setAlpha(TransparentAlpha)


	### Private ###

	def setAlpha(self, a) :
		r = self.color.red()
		g = self.color.green()
		b = self.color.blue()

		try :
			self.setStyleSheet("QFrame {"
					"border: 1px solid gray;"
					"border-radius: 4px;"
					"background-color: rgb("+str(r)+", "+str(g)+", "+str(b)+", "+str(a)+");"
				"}")
		except : pass


	### Handlers ###

	def enterEvent(self, event) :
		self.setAlpha(NonTransparentAlpha)
		Qt.QFrame.enterEvent(self, event)

	def leaveEvent(self, event) :
		self.setAlpha(TransparentAlpha)
		Qt.QFrame.leaveEvent(self, event)

