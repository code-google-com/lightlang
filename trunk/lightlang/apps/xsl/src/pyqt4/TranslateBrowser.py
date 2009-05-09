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
import TextBrowser
import FindSoundInSL


#####
def tr(str) :
	return Qt.QApplication.translate("@default", str)


#####
class TranslateBrowser(TextBrowser.TextBrowser) :
	def __init__(self, parent = None) :
		TextBrowser.TextBrowser.__init__(self, parent)

		self.setOpenExternalLinks(False)
		self.setOpenLinks(False)

		#####

		self.find_sound = FindSoundInSL.FindSoundInSL()

		self.clipboard = Qt.QApplication.clipboard()

		#####

		self.connect(self, Qt.SIGNAL("anchorClicked(const QUrl &)"), self.findFromAnchor)


	### Private ###

	def uFind(self) :
		word = self.textCursor().selectedText().simplified()
		if not word.isEmpty() :
			self.uFindRequestSignal(word)

	def uFindInNewTab(self) :
		word = self.textCursor().selectedText().simplified()
		if not word.isEmpty() :
			self.newTabRequestSignal()
			self.uFindRequestSignal(word)

	def cFind(self) :
		word = self.textCursor().selectedText().simplified()
		if not word.isEmpty() :
			self.cFindRequestSignal(word)

	def cFindInNewTab(self) :
		word = self.textCursor().selectedText().simplified()
		if not word.isEmpty() :
			self.newTabRequestSignal()
			self.cFindRequestSignal(word)

	###

	def findFromAnchor(self, url) :
		word = url.toString()
		if word.startsWith("#s") :
			word.remove(0, word.indexOf("_")+1)
			word = word.simplified()
			if word.isEmpty() :
				return
			self.find_sound.find(word)
		elif (word.startsWith("http:", Qt.Qt.CaseInsensitive) or 
			word.startsWith("mailto:", Qt.Qt.CaseInsensitive)) :
			Qt.QDesktopServices.openUrl(url)


	### Signals ###

	def newTabRequestSignal(self) :
		self.emit(Qt.SIGNAL("newTabRequest()"))

	def uFindRequestSignal(self, word) :
		self.emit(Qt.SIGNAL("uFindRequest(const QString &)"), word)

	def cFindRequestSignal(self, word) :
		self.emit(Qt.SIGNAL("cFindRequest(const QString &)"), word)


	### Handlers ###

	def setCursorInfo(self, str) :
		if not str.simplified().isEmpty() :
			if str.startsWith("#s") :
				str.remove(0, str.indexOf("_") +1)
				str = str.simplified()
				if str.isEmpty() :
					return

				words_list = str.split(Qt.QRegExp("\\W+"), Qt.QString.SkipEmptyParts)
				if words_list.count() <= 1 :
					return

				count = 1
				while count < words_list.count() :
					if not self.find_sound.checkWord(words_list[0], words_list[count]) :
						Qt.QToolTip.showText(Qt.QCursor.pos(), tr("Sound is not full"))
						return
					count += 1
			elif (str.startsWith("http:", Qt.Qt.CaseInsensitive) or
				str.startsWith("mailto:", Qt.Qt.CaseInsensitive)) :
				Qt.QToolTip.showText(Qt.QCursor.pos(), str)

	###

	def mousePressEvent(self, event) :
		if event.button() == Qt.Qt.MidButton :
			word = self.textCursor().selectedText().simplified()
			if word.isEmpty() :
				word = self.clipboard.text(Qt.QClipboard.Selection).simplified()
			if not word.isEmpty() :
				self.newTabRequestSignal()
				self.uFindRequestSignal(word)
		else :
			TextBrowser.TextBrowser.mousePressEvent(self, event)

	def contextMenuEvent(self, event) :
		context_menu = self.createStandardContextMenu()
		text_cursor = self.textCursor()
		if not text_cursor.selectedText().simplified().isEmpty() :
			context_menu.addSeparator()
			context_menu.addAction(tr("Search"), self.uFind)
			context_menu.addAction(tr("Expanded search"), self.cFind)
			context_menu.addSeparator()
			context_menu.addAction(tr("Search (in new tab)"), self.uFindInNewTab)
			context_menu.addAction(tr("Expanded search (in new tab)"), self.cFindInNewTab)
		context_menu.exec_(event.globalPos())

