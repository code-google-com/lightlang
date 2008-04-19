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
IconsDir = Config.Prefix+"/lib/xsl/icons/"

#####
class FindInTextPanel(Qt.QDockWidget) :
	def __init__(self, parent = None) :
		Qt.QDockWidget.__init__(self, parent)

		self.setObjectName("find_in_text_panel")

		self.setWindowTitle(self.tr("Search in translations"))
		self.setAllowedAreas(Qt.Qt.AllDockWidgetAreas)

		self.main_widget = Qt.QWidget()
		self.setWidget(self.main_widget)

		self.main_layout = Qt.QHBoxLayout()
		self.main_widget.setLayout(self.main_layout)

		#####

		self.line_edit = Qt.QLineEdit()
		self.line_edit.setFocus()
		self.main_layout.addWidget(self.line_edit)

		self.clear_line_edit_button = Qt.QToolButton()
		self.clear_line_edit_button.setIcon(Qt.QIcon(IconsDir+"clear_22.png"))
		self.clear_line_edit_button.setIconSize(Qt.QSize(16, 16))
		self.clear_line_edit_button.setEnabled(False)
		self.main_layout.addWidget(self.clear_line_edit_button)

		self.next_button = Qt.QToolButton()
		self.next_button.setIcon(Qt.QIcon(IconsDir+"down_22.png"))
		self.next_button.setIconSize(Qt.QSize(16, 16))
		self.next_button.setEnabled(False)
		self.main_layout.addWidget(self.next_button)

		self.previous_button = Qt.QToolButton()
		self.previous_button.setIcon(Qt.QIcon(IconsDir+"up_22.png"))
		self.previous_button.setIconSize(Qt.QSize(16, 16))
		self.previous_button.setEnabled(False)
		self.main_layout.addWidget(self.previous_button)

		#####

		self.connect(self.line_edit, Qt.SIGNAL("returnPressed()"), self.findNextRequest)
		self.connect(self.line_edit, Qt.SIGNAL("textChanged(const QString &)"), self.setStatus)

		self.connect(self.clear_line_edit_button, Qt.SIGNAL("clicked()"), self.clearLineEdit)

		self.connect(self.next_button, Qt.SIGNAL("clicked()"), self.findNextRequest)
		self.connect(self.previous_button, Qt.SIGNAL("clicked()"), self.findPreviousRequest)


	### Public ###

	def setFocus(self, reason = Qt.Qt.OtherFocusReason) :
		self.line_edit.setFocus(reason)
		self.line_edit.selectAll()


	### Private ###

	def findNextRequest(self) :
		word = self.line_edit.text()
		if word.simplified().isEmpty() :
			return
		self.findNextRequestSignal(word)

	def findPreviousRequest(self) :
		word = self.line_edit.text()
		if word.simplified().isEmpty() :
			return
		self.findPreviousRequestSignal(word)

	def setStatus(self, word) :
		if word.simplified().isEmpty() :
			self.clear_line_edit_button.setEnabled(False)

			self.next_button.setEnabled(False)
			self.previous_button.setEnabled(False)
		else :
			self.clear_line_edit_button.setEnabled(True)

			self.next_button.setEnabled(True)
			self.previous_button.setEnabled(True)

	def clearLineEdit(self) :
		self.line_edit.clear()
		self.line_edit.setFocus()


	### Signals ###

	def findNextRequestSignal(self, word) :
		self.emit(Qt.SIGNAL("findNextRequest(const QString &)"), word)

	def findPreviousRequestSignal(self, word) :
		self.emit(Qt.SIGNAL("findPreviousRequest(const QString &)"), word)
