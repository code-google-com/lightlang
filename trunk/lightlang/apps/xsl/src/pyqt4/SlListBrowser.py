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
IconsDir = Config.Prefix+"/lib/xsl/icons/"


#####
def tr(str) :
	return Qt.QApplication.translate("@default", str)


#####
class SlListBrowser(Qt.QListWidget) :
	def __init__(self, parent = None) :
		Qt.QListWidget.__init__(self, parent)

		self.setFocusPolicy(Qt.Qt.NoFocus)

		#####

		self.last_word = Qt.QString()

		#####

		self.connect(self, Qt.SIGNAL("itemActivated(QListWidgetItem *)"), self.uFind)


	### Public ###

	def setText(self, text) :
		text = Qt.QString(text)

		self.clear()

		###

		parts_list = text.split("<table border=\"0\" width=\"100%\">")

		if parts_list.count() == 1 :
			em_item_regexp = Qt.QRegExp("<em>(.*)</em>")
			em_item_regexp.setMinimal(True)

			em_item_pos = em_item_regexp.indexIn(text, 0)
			while em_item_pos != -1 :
				em_item = Qt.QListWidgetItem(em_item_regexp.cap(1))
				em_item.setFlags(Qt.Qt.NoItemFlags)
				self.addItem(em_item)
				em_item_pos = em_item_regexp.indexIn(text, em_item_pos + em_item_regexp.matchedLength())

			if self.count() == 0 :
				default_item = Qt.QListWidgetItem(text)
				default_item.setFlags(Qt.Qt.NoItemFlags)
				self.addItem(default_item)

		caption_item_regexp = Qt.QRegExp("<td bgcolor=\"(.*)\"><h2 align=\"center\"><em>(.*)</em>")
		caption_item_regexp.setMinimal(True)

		word_item_regexp = Qt.QRegExp("<a href=.*>(.*)</a>")
		word_item_regexp.setMinimal(True)

		parts_list_count = 1
		while parts_list_count < parts_list.count() :
			if caption_item_regexp.indexIn(parts_list[parts_list_count]) < 0 :
				parts_list_count += 1
				continue

			caption_item = Qt.QListWidgetItem(caption_item_regexp.cap(2))

			caption_item_font = caption_item.font()
			caption_item_font.setBold(True)
			caption_item_font.setItalic(True)
			if caption_item_font.pixelSize() > 0 :
				caption_item_font.setPixelSize(caption_item_font.pixelSize() +1)
			elif caption_item_font.pointSize() > 0 :
				caption_item_font.setPointSize(caption_item_font.pointSize() +1)

			caption_item_foreground_brush = caption_item.foreground()
			caption_item_foreground_brush.setStyle(Qt.Qt.SolidPattern)

			caption_item_background_brush = caption_item.background()
			caption_item_background_brush.setStyle(Qt.Qt.SolidPattern)
			caption_item_background_brush.setColor(Qt.QColor(caption_item_regexp.cap(1)))

			caption_item.setFlags(Qt.Qt.NoItemFlags)
			caption_item.setTextAlignment(Qt.Qt.AlignHCenter|Qt.Qt.AlignVCenter)
			caption_item.setFont(caption_item_font)
			caption_item.setForeground(caption_item_foreground_brush)
			caption_item.setBackground(caption_item_background_brush)

			self.addItem(caption_item)

			###

			word_item_pos = word_item_regexp.indexIn(parts_list[parts_list_count], 0)
			while word_item_pos != -1 :
				self.addItem(word_item_regexp.cap(1))
				word_item_pos = word_item_regexp.indexIn(parts_list[parts_list_count],
					word_item_pos + word_item_regexp.matchedLength())

			###

			parts_list_count += 1


	### Private ###

	def uFind(self, item) :
		if item.flags() == Qt.Qt.NoItemFlags :
			return

		word = item.text().simplified()
		if word.isEmpty() :
			return
		self.uFindRequestSignal(word)

	def uFindInNewTab(self) :
		if self.last_word.isEmpty() :
			return
		self.uFindInNewTabRequestSignal(self.last_word)

	def cFindInNewTab(self) :
		if self.last_word.isEmpty() :
			return
		self.cFindInNewTabRequestSignal(self.last_word)


	### Signals ###

	def uFindRequestSignal(self, word) :
		self.emit(Qt.SIGNAL("uFindRequest(const QString &)"), word)

	def uFindInNewTabRequestSignal(self, word) :
		self.emit(Qt.SIGNAL("uFindInNewTabRequest(const QString &)"), word)

	def cFindInNewTabRequestSignal(self, word) :
		self.emit(Qt.SIGNAL("cFindInNewTabRequest(const QString &)"), word)


	### Handlers ###

	def contextMenuEvent(self, event) :
		item = self.itemAt(event.pos())
		if item == None :
			return

		if item.flags() == Qt.Qt.NoItemFlags :
			return

		self.last_word = item.text().simplified()
		if not self.last_word.isEmpty() :
			context_menu = Qt.QMenu()
			context_menu.addAction(tr("Search (in new tab)"), self.uFindInNewTab)
			context_menu.addAction(tr("Expanded search (in new tab)"), self.cFindInNewTab)
			context_menu.exec_(event.globalPos())

