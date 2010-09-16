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
import IconsLoader


#####
class LineEdit(Qt.QLineEdit) :
	def __init__(self, parent = None) :
		Qt.QLineEdit.__init__(self, parent)

		#####

		self._main_layout = Qt.QHBoxLayout()
		self._main_layout.setAlignment(Qt.Qt.AlignRight)
		self._main_layout.setContentsMargins(0, 0, 1, 0)
		self._main_layout.setSpacing(0)
		self.setLayout(self._main_layout)

		#####

		self._clear_button = Qt.QToolButton()
		self._clear_button.setIcon(IconsLoader.icon("edit-clear-locationbar-rtl"))
		self._clear_button.setIconSize(Qt.QSize(16, 16))
		self._clear_button.setCursor(Qt.Qt.ArrowCursor)
		self._clear_button.setAutoRaise(True)
		self._clear_button.setEnabled(False)
		self._main_layout.addWidget(self._clear_button)

		self.setTextMargins(0, 0, 22, 0)

		#####

		self.connect(self, Qt.SIGNAL("textChanged(const QString &)"), self.setStatusFromLineEdit)

		self.connect(self._clear_button, Qt.SIGNAL("clicked()"), self.clearLineEdit)


	### Private ###

	def clearLineEdit(self) :
		self.clear()
		self.setFocus(Qt.Qt.OtherFocusReason)

	def setStatusFromLineEdit(self, word) :
		self._clear_button.setEnabled(not word.simplified().isEmpty())

