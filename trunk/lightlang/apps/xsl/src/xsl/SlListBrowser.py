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
import ListBrowser


##### Public classes #####
class SlListBrowser(ListBrowser.ListBrowser) :
	def __init__(self, parent = None) :
		ListBrowser.ListBrowser.__init__(self, parent)

		self.setFocusPolicy(Qt.Qt.NoFocus)

		#####

		self._last_word = Qt.QString()

		#####

		self.connect(self, Qt.SIGNAL("itemActivated(QListWidgetItem *)"), self.uFind)


	### Private ###

	def uFind(self, item) :
		if item.flags() == Qt.Qt.NoItemFlags :
			return

		word = item.text().simplified()
		if word.isEmpty() :
			return
		self.uFindRequestSignal(word)

	def uFindInNewTab(self) :
		if self._last_word.isEmpty() :
			return
		self.uFindInNewTabRequestSignal(self._last_word)

	def cFindInNewTab(self) :
		if self._last_word.isEmpty() :
			return
		self.cFindInNewTabRequestSignal(self._last_word)


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

		self._last_word = item.text().simplified()
		if not self._last_word.isEmpty() :
			context_menu = Qt.QMenu()
			context_menu.addAction(tr("Search (in new tab)"), self.uFindInNewTab)
			context_menu.addAction(tr("Expanded search (in new tab)"), self.cFindInNewTab)
			context_menu.exec_(event.globalPos())

