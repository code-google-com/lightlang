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
class TextEdit(Qt.QTextEdit) :
	def __init__(self, parent = None) :
		Qt.QTextEdit.__init__(self, parent)

		self.setAcceptRichText(False)


	### Signals ###

	def translateRequestSignal(self) :
		self.emit(Qt.SIGNAL("translateRequest()"))


	### Handlers ###

	def keyPressEvent(self, event) :
		if ( (event.key() == Qt.Qt.Key_Return or event.key() == Qt.Qt.Key_Enter) and
			event.modifiers() == Qt.Qt.ControlModifier ) :
			self.translateRequestSignal()
		else :
			Qt.QTextEdit.keyPressEvent(self, event)

