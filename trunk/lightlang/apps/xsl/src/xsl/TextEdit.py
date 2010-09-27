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
import IconsLoader


##### Public classes #####
class TextEdit(Qt.QTextEdit) :
	def __init__(self, parent = None) :
		Qt.QTextEdit.__init__(self, parent)

		self.setAcceptRichText(False)

		#####

		self._main_layout = Qt.QVBoxLayout()
		self._main_layout.setAlignment(Qt.Qt.AlignRight|Qt.Qt.AlignBottom)
		self._main_layout.setContentsMargins(0, 0, 0, 0)
		self._main_layout.setSpacing(0)
		self.setLayout(self._main_layout)

		#####

		self._clear_button = Qt.QToolButton(self)
		self._clear_button.setIcon(IconsLoader.icon("edit-clear-locationbar-rtl"))
		self._clear_button.setIconSize(Qt.QSize(16, 16))
		self._clear_button.setCursor(Qt.Qt.ArrowCursor)
		self._clear_button.setAutoRaise(True)
		self._clear_button.setEnabled(False)
		self._main_layout.addWidget(self._clear_button)

		#####

		self.connect(self, Qt.SIGNAL("textChanged()"), self.setStatusFromTextEdit)

		self.connect(self._clear_button, Qt.SIGNAL("clicked()"), self.clearTextEdit)


	### Private ###

	def clearTextEdit(self) :
		self.clear()
		self.setFocus(Qt.Qt.OtherFocusReason)

	def setStatusFromTextEdit(self) :
		self._clear_button.setEnabled(not self.toPlainText().simplified().isEmpty())


	### Signals ###

	def textAppliedSignal(self) :
		self.emit(Qt.SIGNAL("textApplied()"))


	### Handlers ###

	def keyPressEvent(self, event) :
		if event.key() in (Qt.Qt.Key_Return, Qt.Qt.Key_Enter) and event.modifiers() == Qt.Qt.ControlModifier :
			self.textAppliedSignal()
		else :
			Qt.QTextEdit.keyPressEvent(self, event)

