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


#####
def tr(str) :
	return Qt.QApplication.translate("@default", str)


#####
class CenteredWindow(Qt.QWidget) :
	def __init__(self, parent = None) :
		Qt.QWidget.__init__(self, parent)


	### Public ###

	def show(self) :
		x_window_position = (Qt.QApplication.desktop().width() - self.width()) / 2
		x_window_position = ( 0 if x_window_position < 0 else x_window_position )
		y_window_position = (Qt.QApplication.desktop().height() - self.height()) / 2
		y_window_position = ( 0 if y_window_position < 0 else y_window_position )
		self.move(Qt.QPoint(x_window_position, y_window_position))

		Qt.QWidget.show(self)
		self.raise_()
		self.activateWindow()

