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


##### Public classes #####
class HorizontalGrabWidget(Qt.QWidget) :
	def __init__(self, parent = None) :
		Qt.QWidget.__init__(self, parent)

		self.setFixedWidth(self.style().pixelMetric(Qt.QStyle.PM_ToolBarHandleExtent))


	### Private ###
	### Handlers ###

	def enterEvent(self, event) :
		self.setCursor(Qt.Qt.SizeAllCursor)
		Qt.QWidget.enterEvent(self, event)

	def leaveEvent(self, event) :
		self.setCursor(Qt.Qt.ArrowCursor)
		Qt.QWidget.leaveEvent(self, event)

	###

	def paintEvent(self, event) :
		style_painter = Qt.QStylePainter(self)
		option = Qt.QStyleOption()
		option.initFrom(self)
		option.state |= Qt.QStyle.State_Horizontal
		style_painter.drawPrimitive(Qt.QStyle.PE_IndicatorToolBarHandle, option)

