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
class TextBrowser(Qt.QTextBrowser) :
	def __init__(self, parent = None) :
		Qt.QTextBrowser.__init__(self, parent)

		self.setOpenExternalLinks(True)


	### Public ###

	def setText(self, text) :
		self.setHtml(text)

	def text(self) :
		return self.toHtml()

	###

	def findNext(self, word) :
		self.findWord(word)

	def findPrevious(self, word) :
		self.findWord(word, True)

	def findWord(self, word, backward_flag = False) :
		text_cursor = self.textCursor()

		if text_cursor.hasSelection() and backward_flag :
			text_cursor.setPosition(text_cursor.anchor(), Qt.QTextCursor.MoveAnchor)

		if not backward_flag :
			new_text_cursor = self.document().find(word, text_cursor)
			if new_text_cursor.isNull() :
				new_text_cursor = text_cursor
				self.statusChangedSignal(self.tr("Not found"))
		else :
			new_text_cursor = self.document().find(word, text_cursor, Qt.QTextDocument.FindBackward)
			if new_text_cursor.isNull() :
				new_text_cursor = text_cursor
				self.statusChangedSignal(self.tr("Not found"))

		self.setTextCursor(new_text_cursor)

	def instantSearch(self, word) :
		if word.isEmpty() :
			my_text_cursor = self.tmp_text_cursor = self.textCursor()
		else :
			my_text_cursor = self.textCursor()

		my_text_cursor.setPosition(my_text_cursor.selectionStart(), Qt.QTextCursor.MoveAnchor)
		self.setTextCursor(my_text_cursor)

		my_text_cursor = self.document().find(word, my_text_cursor)

		if my_text_cursor.isNull() and not word.isEmpty() :
			my_text_cursor = self.document().find(word, False)
			if my_text_cursor.isNull() :
				self.setFindInTextFrameLineEditRedAlertPaletteSignal()
				self.tmp_text_cursor.setPosition(self.tmp_text_cursor.selectionStart(), Qt.QTextCursor.MoveAnchor)
				self.setTextCursor(self.tmp_text_cursor)
			else :
				self.tmp_text_cursor = my_text_cursor
				self.setTextCursor(my_text_cursor)
		elif not my_text_cursor.isNull() :
			self.tmp_text_cursor = my_text_cursor
			self.setTextCursor(my_text_cursor)
			self.setFindInTextFrameLineEditDefaultPaletteSignal()
		else :
			self.setFindInTextFrameLineEditDefaultPaletteSignal()



	### Private ###
	### Signals ###

	def showFindInTextFrameRequestSignal(self) :
		self.emit(Qt.SIGNAL("showFindInTextFrameRequest()"))

	def hideFindInTextFrameRequestSignal(self) :
		self.emit(Qt.SIGNAL("hideFindInTextFrameRequest()"))

	def setFindInTextFrameLineEditRedAlertPaletteSignal(self) :
		self.emit(Qt.SIGNAL("setFindInTextFrameLineEditRedAlertPaletteRequest()"))

	def setFindInTextFrameLineEditDefaultPaletteSignal(self) :
		self.emit(Qt.SIGNAL("setFindInTextFrameLineEditDefaultPaletteRequest()"))

	def statusChangedSignal(self, str) :
		self.emit(Qt.SIGNAL("statusChanged(const QString &)"), str)


	### Handlers ###

	def keyPressEvent(self, event) :
		if event.key() == Qt.Qt.Key_Escape :
			self.hideFindInTextFrameRequestSignal()
		elif event.key() == Qt.Qt.Key_Slash :
			self.showFindInTextFrameRequestSignal()

		Qt.QTextBrowser.keyPressEvent(self, event)

