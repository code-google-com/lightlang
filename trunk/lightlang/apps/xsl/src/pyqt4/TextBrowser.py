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
import UserStyleCss
import ChromeScrollBar


#####
def tr(str) :
	return Qt.QApplication.translate("@default", str)


#####
class TextBrowser(Qt.QTextBrowser) :
	def __init__(self, parent = None) :
		Qt.QTextBrowser.__init__(self, parent)

		self.setOpenExternalLinks(True)
		self.setUndoRedoEnabled(True)

		#####

		self.zoom_count = 0

		self.highlight_color = Qt.QApplication.palette().color(Qt.QPalette.Highlight)
		self.highlight_color.setAlpha(100)
		self.user_style_css = UserStyleCss.userStyleCss()
		# setSource() dont accept user-style.css

		#####

		self.chrome_scroll_bar = ChromeScrollBar.ChromeScrollBar()
		self.setVerticalScrollBar(self.chrome_scroll_bar)

		#####

		self.connect(self, Qt.SIGNAL("highlighted(const QString &)"), self.setCursorInfo)
		self.connect(self, Qt.SIGNAL("sourceChanged(const QUrl &)"), self.chrome_scroll_bar.clearHighlight)


	### Public ###

	def setText(self, text) :
		self.clearSpecials()

		index = text.indexOf("</style>")
		if index >= 0 :
			text = Qt.QString(text).insert(index, self.user_style_css)
		else :
			text = Qt.QString("<html><head><style>%1</style></head><body>%2</body></html>").arg(self.user_style_css).arg(text)
		self.setHtml(text)

	def text(self) :
		self.clearSpecials()
		return self.toHtml()

	###

	def document(self) :
		self.clearSpecials()
		return Qt.QTextBrowser.document(self)

	###

	def clear(self) :
		self.clearSpecials()
		Qt.QTextBrowser.clear(self)

	def clearSpecials(self) :
		if Qt.QTextBrowser.document(self).isModified() :
			Qt.QTextBrowser.document(self).undo()
		self.chrome_scroll_bar.clearHighlight()

	###

	def zoomIn(self, range = 1) :
		if -5 <= self.zoom_count + range <= 5 :
			Qt.QTextBrowser.zoomIn(self, range)
			self.zoom_count += range

	def zoomOut(self, range = 1) :
		if -5 <= self.zoom_count - range <= 5 :
			Qt.QTextBrowser.zoomOut(self, range)
			self.zoom_count -= range

	def zoomNormal(self) :
		if self.zoom_count > 0 :
			self.zoomOut(self.zoom_count)
		elif self.zoom_count < 0 :
			self.zoomIn(-self.zoom_count)

	###

	def findNext(self, word) :
		self.findWord(word)

	def findPrevious(self, word) :
		self.findWord(word, True)

	def findWord(self, word, backward_flag = False) :
		if not Qt.QTextBrowser.document(self).isModified() :
			self.instantSearch(word)

		text_cursor = self.textCursor()

		if text_cursor.hasSelection() and backward_flag :
			text_cursor.setPosition(text_cursor.anchor(), Qt.QTextCursor.MoveAnchor)

		if not backward_flag :
			new_text_cursor = Qt.QTextBrowser.document(self).find(word, text_cursor)
			if new_text_cursor.isNull() :
				new_text_cursor = text_cursor
				self.statusChangedSignal(tr("Not found"))
		else :
			new_text_cursor = Qt.QTextBrowser.document(self).find(word, text_cursor, Qt.QTextDocument.FindBackward)
			if new_text_cursor.isNull() :
				new_text_cursor = text_cursor
				self.statusChangedSignal(tr("Not found"))

		self.setTextCursor(new_text_cursor)

	def instantSearch(self, word) :
		word_found_flag = False

		if Qt.QTextBrowser.document(self).isModified() :
			Qt.QTextBrowser.document(self).undo()
			self.setFoundRequestSignal(True)
		self.chrome_scroll_bar.clearHighlight()

		if word.isEmpty() :
			self.setFoundRequestSignal(True)
			return

		highlight_cursor = Qt.QTextCursor(Qt.QTextBrowser.document(self))
		cursor = Qt.QTextCursor(Qt.QTextBrowser.document(self))

		plain_format = Qt.QTextCharFormat(highlight_cursor.charFormat())
		color_format = Qt.QTextCharFormat(highlight_cursor.charFormat())
		color_format.setBackground(self.highlight_color)

		cursor.beginEditBlock()

		while (not highlight_cursor.isNull()) and (not highlight_cursor.atEnd()) :
			Qt.QCoreApplication.processEvents(Qt.QEventLoop.ExcludeUserInputEvents)
			highlight_cursor = Qt.QTextBrowser.document(self).find(word, highlight_cursor)
			if not highlight_cursor.isNull() :
				word_found_flag = True
				highlight_cursor.movePosition(Qt.QTextCursor.Right, Qt.QTextCursor.KeepAnchor, 0)
				highlight_cursor.mergeCharFormat(color_format)
				self.chrome_scroll_bar.addHighlight(highlight_cursor.position(), Qt.QTextBrowser.document(self).characterCount())

		cursor.endEditBlock()

		self.setFoundRequestSignal(word_found_flag)
		if word_found_flag :
			self.chrome_scroll_bar.drawHighlight()
		else :
			self.chrome_scroll_bar.clearHighlight()


	### Private ###

	def setCursorInfo(self, str) :
		if not str.simplified().isEmpty() :
			if str.startsWith("http:", Qt.Qt.CaseInsensitive) or str.startsWith("mailto:", Qt.Qt.CaseInsensitive) :
				Qt.QToolTip.showText(Qt.QCursor.pos(), str)


	### Signals ###

	def showTextSearchFrameRequestSignal(self) :
		self.emit(Qt.SIGNAL("showTextSearchFrameRequest()"))

	def hideTextSearchFrameRequestSignal(self) :
		self.emit(Qt.SIGNAL("hideTextSearchFrameRequest()"))

	def setFoundRequestSignal(self, found_flag) :
		self.emit(Qt.SIGNAL("setFoundRequest(bool)"), found_flag)

	def statusChangedSignal(self, str) :
		self.emit(Qt.SIGNAL("statusChanged(const QString &)"), str)

	def backwardRequestSignal(self) :
		self.emit(Qt.SIGNAL("backwardRequest()"))


	### Handlers ###

	def keyPressEvent(self, event) :
		if event.key() == Qt.Qt.Key_Escape :
			self.hideTextSearchFrameRequestSignal()
		elif event.key() == Qt.Qt.Key_Slash or (event.key() == Qt.Qt.Key_F and event.modifiers() == Qt.Qt.ControlModifier) :
			self.showTextSearchFrameRequestSignal()
		elif event.key() == Qt.Qt.Key_Backspace :
			self.backwardRequestSignal()
			return

		Qt.QTextBrowser.keyPressEvent(self, event)

