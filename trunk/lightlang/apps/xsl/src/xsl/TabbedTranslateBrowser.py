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
import TranslateBrowser
import TextSearchFrame


##### Public classes #####
class TabbedTranslateBrowser(Qt.QWidget) :
	def __init__(self, parent = None) :
		Qt.QWidget.__init__(self, parent)

		#####

		self._main_layout = Qt.QVBoxLayout()
		self._main_layout.setContentsMargins(0, 0, 0, 0)
		self._main_layout.setSpacing(0)
		self.setLayout(self._main_layout)

		#####

		self._shred_lock_flag = False

		self._translate_browsers_list = []
		self._old_index = -1

		self._tmp_text_cursor = Qt.QTextCursor()

		#####

		self._tab_widget = Qt.QTabWidget()
		self._tab_widget.setTabsClosable(True)
		self._main_layout.addWidget(self._tab_widget)

		self._add_tab_button = Qt.QToolButton()
		self._add_tab_button.setIcon(IconsLoader.icon("tab-new"))
		self._add_tab_button.setIconSize(Qt.QSize(16, 16))
		self._add_tab_button.setCursor(Qt.Qt.ArrowCursor)
		self._add_tab_button.setAutoRaise(True)
		self._tab_widget.setCornerWidget(self._add_tab_button, Qt.Qt.TopLeftCorner)

		self._remove_tab_button = Qt.QToolButton()
		self._remove_tab_button.setIcon(IconsLoader.icon("tab-close"))
		self._remove_tab_button.setIconSize(Qt.QSize(16, 16))
		self._remove_tab_button.setCursor(Qt.Qt.ArrowCursor)
		self._remove_tab_button.setAutoRaise(True)
		self._tab_widget.setCornerWidget(self._remove_tab_button, Qt.Qt.TopRightCorner)

		self._text_search_frame = TextSearchFrame.TextSearchFrame()
		self._text_search_frame.hide()
		self._main_layout.addWidget(self._text_search_frame)

		#####

		self.connect(self._add_tab_button, Qt.SIGNAL("clicked()"), self.addTab)
		self.connect(self._remove_tab_button, Qt.SIGNAL("clicked()"), self.removeTab)

		self.connect(self._tab_widget, Qt.SIGNAL("currentChanged(int)"), self.tabChanged)
		self.connect(self._tab_widget, Qt.SIGNAL("tabCloseRequested(int)"), self.removeTab)

		self.connect(self._text_search_frame, Qt.SIGNAL("findNextRequest(const QString &)"), self.findNext)
		self.connect(self._text_search_frame, Qt.SIGNAL("findPreviousRequest(const QString &)"), self.findPrevious)
		self.connect(self._text_search_frame, Qt.SIGNAL("instantSearchRequest(const QString &)"), self.instantSearch)

		#####

		self.addTab()


	### Public ###

	def setShredLock(self, shred_lock_flag) :
		self._shred_lock_flag = shred_lock_flag

	def showTextSearchFrame(self) :
		self._text_search_frame.show()

	def hideTextSearchFrame(self) :
		self._text_search_frame.hide()

	###

	def addTab(self) :
		self._translate_browsers_list.append(TranslateBrowser.TranslateBrowser())
		index = len(self._translate_browsers_list) - 1

		self.connect(self._translate_browsers_list[index], Qt.SIGNAL("newTabRequest()"), self.addTab)
		self.connect(self._translate_browsers_list[index], Qt.SIGNAL("uFindRequest(const QString &)"), self.uFindRequestSignal)
		self.connect(self._translate_browsers_list[index], Qt.SIGNAL("cFindRequest(const QString &)"), self.cFindRequestSignal)
		self.connect(self._translate_browsers_list[index], Qt.SIGNAL("statusChanged(const QString &)"), self.statusChangedSignal)
		self.connect(self._translate_browsers_list[index], Qt.SIGNAL("showTextSearchFrameRequest()"), self._text_search_frame.show)
		self.connect(self._translate_browsers_list[index], Qt.SIGNAL("hideTextSearchFrameRequest()"), self._text_search_frame.hide)
		self.connect(self._translate_browsers_list[index], Qt.SIGNAL("setFoundRequest(bool)"), self._text_search_frame.setFound)

		self._translate_browsers_list[index].setText(tr("<font class=\"info_font\">Empty</font>"))
		self._tab_widget.addTab(self._translate_browsers_list[index], tr("(Untitled)"))
		self._tab_widget.setCurrentIndex(index)

	def removeTab(self, index = -1) :
		if self._shred_lock_flag :
			return

		index = ( self._tab_widget.currentIndex() if index < 0 else index )

		self._tab_widget.removeTab(index)
		self._translate_browsers_list.pop(index)

		if self._tab_widget.count() == 0 :
			self.addTab()

	###

	def count(self) :
		return self._tab_widget.count()

	def currentIndex(self) :
		return self._tab_widget.currentIndex()

	###

	def setText(self, index, text) :
		self._translate_browsers_list[index].setText(text)

	def setCaption(self, index, word) :
		self._tab_widget.setTabText(index, word)

	###

	def text(self, index = -1) :
		index = ( self._tab_widget.currentIndex() if index < 0 else index )
		return self._translate_browsers_list[index].text()

	def caption(self, index = -1) :
		index = ( self._tab_widget.currentIndex() if index < 0 else index )
		return self._tab_widget.tabText(index)

	def browser(self, index = -1) :
		index = ( self._tab_widget.currentIndex() if index < 0 else index )
		return self._translate_browsers_list[index]

	def document(self, index = -1) :
		index = ( self._tab_widget.currentIndex() if index < 0 else index )
		return self._translate_browsers_list[index].document()

	###

	def clearPage(self, index = -1) :
		if self._shred_lock_flag :
			return

		index = ( self._tab_widget.currentIndex() if index < 0 else index )
		self._translate_browsers_list[index].setText(tr("<font class=\"info_font\">Empty</font>"))
		self._tab_widget.setTabText(index, tr("(Untitled)"))

	def clearAll(self) :
		if self._shred_lock_flag :
			return

		for count in xrange(self.count()) :
			self.removeTab(0)

		self._text_search_frame.hide()
		self._text_search_frame.clear()

	def clear(self, index = -1) :
		if self._shred_lock_flag :
			return

		index = ( self._tab_widget.currentIndex() if index < 0 else index )
		self._translate_browsers_list[index].clear()
		self._tab_widget.setTabText(index, Qt.QString())

	def clearSpecials(self, index = -1) :
		if self._shred_lock_flag :
			return

		index = ( self._tab_widget.currentIndex() if index < 0 else index )
		self._translate_browsers_list[index].clearSpecials()

	###

	def zoomIn(self, index = -1, range = 1) :
		index = ( self._tab_widget.currentIndex() if index < 0 else index )
		self._translate_browsers_list[index].zoomIn(range)

	def zoomOut(self, index = -1, range = 1) :
		index = ( self._tab_widget.currentIndex() if index < 0 else index )
		self._translate_browsers_list[index].zoomOut(range)

	def zoomNormal(self, index = -1) :
		index = ( self._tab_widget.currentIndex() if index < 0 else index )
		self._translate_browsers_list[index].zoomNormal()


	### Private ###

	def findNext(self, word) :
		index = self.currentIndex()
		self._translate_browsers_list[index].findNext(word)

	def findPrevious(self, word) :
		index = self.currentIndex()
		self._translate_browsers_list[index].findPrevious(word)

	def instantSearch(self, word) :
		index = self.currentIndex()
		self._translate_browsers_list[index].instantSearch(word)

	###

	def tabChanged(self, index) :
		self._translate_browsers_list[self._old_index].clearSpecials()
		self._old_index = index
		self.tabChangedSignal(index)


	### Signals ###

	def tabChangedSignal(self, index) :
		self.emit(Qt.SIGNAL("tabChanged(int)"), index)

	def uFindRequestSignal(self, word) :
		self.emit(Qt.SIGNAL("uFindRequest(const QString &)"), word)

	def cFindRequestSignal(self, word) :
		self.emit(Qt.SIGNAL("cFindRequest(const QString &)"), word)

	def statusChangedSignal(self, status) :
		self.emit(Qt.SIGNAL("statusChanged(const QString &)"), status)


	### Handlers ###

	def mouseDoubleClickEvent(self, event) :
		self.addTab()

