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
import IconsLoader
import LineEdit


#####
class TextSearchFrame(Qt.QFrame) :
	def __init__(self, parent = None) :
		Qt.QFrame.__init__(self, parent)

		self.setFrameShape(Qt.QFrame.Box)

		#####

		self._main_layout = Qt.QHBoxLayout()
		self._main_layout.setContentsMargins(3, 0, 3, 0)
		self.setLayout(self._main_layout)

		#####

		self._close_button = Qt.QToolButton()
		self._close_button.setIcon(IconsLoader.icon("dialog-cancel"))
		self._close_button.setIconSize(Qt.QSize(16, 16))
		self._main_layout.addWidget(self._close_button)

		self._vertical_frame1 = Qt.QFrame()
		self._vertical_frame1.setFrameStyle(Qt.QFrame.VLine|Qt.QFrame.Sunken)
		self._vertical_frame1.setMinimumSize(22, 22)
		self._main_layout.addWidget(self._vertical_frame1)

		self._line_edit_label = Qt.QLabel(tr("Search:"))
		self._main_layout.addWidget(self._line_edit_label)

		self._line_edit = LineEdit.LineEdit()
		self._main_layout.addWidget(self._line_edit)

		self._vertical_frame2 = Qt.QFrame()
		self._vertical_frame2.setFrameStyle(Qt.QFrame.VLine|Qt.QFrame.Sunken)
		self._main_layout.addWidget(self._vertical_frame2)

		self._next_button = Qt.QToolButton()
		self._next_button.setIcon(IconsLoader.icon("go-down"))
		self._next_button.setIconSize(Qt.QSize(16, 16))
		self._next_button.setEnabled(False)
		self._main_layout.addWidget(self._next_button)

		self._previous_button = Qt.QToolButton()
		self._previous_button.setIcon(IconsLoader.icon("go-up"))
		self._previous_button.setIconSize(Qt.QSize(16, 16))
		self._previous_button.setEnabled(False)
		self._main_layout.addWidget(self._previous_button)

		#####

		self._line_edit_default_palette = Qt.QPalette(self._line_edit.palette())

		self._line_edit_red_alert_palette = Qt.QPalette()
		if UserStyleCssCollection.redAlertBackgroundColor().isValid() :
			self._line_edit_red_alert_palette.setColor(Qt.QPalette.Base, UserStyleCssCollection.redAlertBackgroundColor())

		#####

		self.connect(self._close_button, Qt.SIGNAL("clicked()"), self.hide)

		self.connect(self._line_edit, Qt.SIGNAL("returnPressed()"), self._next_button.animateClick)
		self.connect(self._line_edit, Qt.SIGNAL("textChanged(const QString &)"), self.setStatusFromLineEdit)
		self.connect(self._line_edit, Qt.SIGNAL("textChanged(const QString &)"), self.instantSearchRequest)

		self.connect(self._next_button, Qt.SIGNAL("clicked()"), self.findNextRequest)

		self.connect(self._previous_button, Qt.SIGNAL("clicked()"), self.findPreviousRequest)


	### Public ###

	def show(self) :
		Qt.QFrame.show(self)
		self.raise_()
		self.setFocus()

	def setFocus(self, reason = Qt.Qt.OtherFocusReason) :
		self._line_edit.setFocus(reason)
		self._line_edit.selectAll()

	###

	def setFound(self, found_flag) :
		self._line_edit.setPalette(self._line_edit_default_palette if found_flag else self._line_edit_red_alert_palette)

	###

	def clear(self) :
		self._line_edit.clear()


	### Private ###

	def findNextRequest(self) :
		word = self._line_edit.text()
		if word.simplified().isEmpty() :
			return
		self.findNextRequestSignal(word)

	def findPreviousRequest(self) :
		word = self._line_edit.text()
		if word.simplified().isEmpty() :
			return
		self.findPreviousRequestSignal(word)

	def instantSearchRequest(self, word) :
		self.instantSearchRequestSignal(word)

	###

	def setStatusFromLineEdit(self, word) :
		line_edit_empty_flag = word.simplified().isEmpty()
		self._next_button.setEnabled(not line_edit_empty_flag)
		self._previous_button.setEnabled(not line_edit_empty_flag)


	### Signals ###

	def findNextRequestSignal(self, word) :
		self.emit(Qt.SIGNAL("findNextRequest(const QString &)"), word)

	def findPreviousRequestSignal(self, word) :
		self.emit(Qt.SIGNAL("findPreviousRequest(const QString &)"), word)

	def instantSearchRequestSignal(self, word) :
		self.emit(Qt.SIGNAL("instantSearchRequest(const QString &)"), word)


	### Handlers ###

	def keyPressEvent(self, event) :
		if event.key() == Qt.Qt.Key_Escape :
			self.hide()
		Qt.QFrame.keyPressEvent(self, event)

	def hideEvent(self, event) :
		self.instantSearchRequestSignal(Qt.QString())
		Qt.QFrame.hideEvent(self, event)

	def closeEvent(self, event) :
		self.instantSearchRequestSignal(Qt.QString())
		Qt.QFrame.closeEvent(self, event)

