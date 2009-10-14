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
import TranslateBrowser
import TextSearchFrame


#####
IconsDir = Config.Prefix+"/lib/xsl/icons/"


#####
def tr(str) :
	return Qt.QApplication.translate("@default", str)


#####
class TabbedTranslateBrowser(Qt.QWidget) :
	def __init__(self, parent = None) :
		Qt.QWidget.__init__(self, parent)

		#####

		self.main_layout = Qt.QVBoxLayout()
		self.main_layout.setContentsMargins(0, 0, 0, 0)
		self.main_layout.setSpacing(0)
		self.setLayout(self.main_layout)

		#####

		self.shred_lock_flag = False

		self.single_translate_browsers = []

		self.tmp_text_cursor = Qt.QTextCursor()

		#####

		self.tab_widget = Qt.QTabWidget()
		try : # FIXME: Qt-4.5
			self.tab_widget.setTabsClosable(True)
		except : pass
		self.main_layout.addWidget(self.tab_widget)

		self.add_tab_button = Qt.QToolButton()
		self.add_tab_button.setIcon(Qt.QIcon(IconsDir+"add_22.png"))
		self.add_tab_button.setIconSize(Qt.QSize(16, 16))
		self.add_tab_button.setCursor(Qt.Qt.ArrowCursor)
		self.add_tab_button.setAutoRaise(True)
		self.tab_widget.setCornerWidget(self.add_tab_button, Qt.Qt.TopLeftCorner)

		self.remove_tab_button = Qt.QToolButton()
		self.remove_tab_button.setIcon(Qt.QIcon(IconsDir+"remove_22.png"))
		self.remove_tab_button.setIconSize(Qt.QSize(16, 16))
		self.remove_tab_button.setCursor(Qt.Qt.ArrowCursor)
		self.remove_tab_button.setAutoRaise(True)
		self.tab_widget.setCornerWidget(self.remove_tab_button, Qt.Qt.TopRightCorner)

		self.text_search_frame = TextSearchFrame.TextSearchFrame()
		self.text_search_frame.hide()
		self.main_layout.addWidget(self.text_search_frame)

		#####

		self.connect(self.add_tab_button, Qt.SIGNAL("clicked()"), self.addTab)
		self.connect(self.remove_tab_button, Qt.SIGNAL("clicked()"), self.removeTab)

		self.connect(self.tab_widget, Qt.SIGNAL("currentChanged(int)"), self.tabChangedSignal)
		try : # FIXME: Qt-4.5
			self.connect(self.tab_widget, Qt.SIGNAL("tabCloseRequested(int)"), self.removeTab)
		except : pass

		self.connect(self.text_search_frame, Qt.SIGNAL("findNextRequest(const QString &)"), self.findNext)
		self.connect(self.text_search_frame, Qt.SIGNAL("findPreviousRequest(const QString &)"), self.findPrevious)
		self.connect(self.text_search_frame, Qt.SIGNAL("instantSearchRequest(const QString &)"), self.instantSearch)

		#####

		self.addTab()


	### Public ###

	def setShredLock(self, shred_lock_flag) :
		self.shred_lock_flag = shred_lock_flag

	def showTextSearchFrame(self) :
		self.text_search_frame.show()
		self.text_search_frame.setFocus()

	def hideTextSearchFrame(self) :
		self.text_search_frame.hide()

	###

	def addTab(self) :
		self.single_translate_browsers.append(TranslateBrowser.TranslateBrowser())
		index = len(self.single_translate_browsers) -1

		self.connect(self.single_translate_browsers[index], Qt.SIGNAL("newTabRequest()"), self.addTab)
		self.connect(self.single_translate_browsers[index], Qt.SIGNAL("uFindRequest(const QString &)"), self.uFindRequestSignal)
		self.connect(self.single_translate_browsers[index], Qt.SIGNAL("cFindRequest(const QString &)"), self.cFindRequestSignal)
		self.connect(self.single_translate_browsers[index], Qt.SIGNAL("showTextSearchFrameRequest()"), self.showTextSearchFrame)
		self.connect(self.single_translate_browsers[index], Qt.SIGNAL("hideTextSearchFrameRequest()"), self.hideTextSearchFrame)
		self.connect(self.single_translate_browsers[index], Qt.SIGNAL("statusChanged(const QString &)"), self.statusChangedSignal)
		self.connect(self.single_translate_browsers[index], Qt.SIGNAL("setTextSearchFrameLineEditRedAlertPaletteRequest()"),
			self.text_search_frame.setLineEditRedAlertPalette)
		self.connect(self.single_translate_browsers[index], Qt.SIGNAL("setTextSearchFrameLineEditDefaultPaletteRequest()"),
			self.text_search_frame.setLineEditDefaultPalette)

		self.single_translate_browsers[index].setText(tr("<font class=\"info_font\">Empty</font>"))
		self.tab_widget.addTab(self.single_translate_browsers[index], tr("(Untitled)"))
		self.tab_widget.setCurrentIndex(index)

		self.tabChangedSignal()

	def removeTab(self, index = -1) :
		if self.shred_lock_flag :
			return

		index = ( self.tab_widget.currentIndex() if index < 0 else index )

		self.tab_widget.removeTab(index)
		self.single_translate_browsers.pop(index)

		if self.tab_widget.count() == 0 :
			self.addTab()

		self.tabChangedSignal()

	###

	def count(self) :
		return self.tab_widget.count()

	def currentIndex(self) :
		return self.tab_widget.currentIndex()

	###

	def setText(self, index, text) :
		self.single_translate_browsers[index].setText(text)

	def setCaption(self, index, word) :
		self.tab_widget.setTabText(index, word)

	###

	def text(self, index = -1) :
		index = ( self.tab_widget.currentIndex() if index < 0 else index )
		return self.single_translate_browsers[index].text()

	def caption(self, index = -1) :
		index = ( self.tab_widget.currentIndex() if index < 0 else index )
		return self.tab_widget.tabText(index)

	def browser(self, index = -1) :
		index = ( self.tab_widget.currentIndex() if index < 0 else index )
		return self.single_translate_browsers[index]

	def document(self, index = -1) :
		index = ( self.tab_widget.currentIndex() if index < 0 else index )
		return self.single_translate_browsers[index].document()

	###

	def clearPage(self, index = -1) :
		if self.shred_lock_flag :
			return

		index = ( self.tab_widget.currentIndex() if index < 0 else index )
		self.single_translate_browsers[index].setText(tr("<font class=\"info_font\">Empty</font>"))
		self.tab_widget.setTabText(index, tr("(Untitled)"))

	def clearAll(self) :
		if self.shred_lock_flag :
			return

		count = self.count()
		while count > 0 :
			self.removeTab(0)
			count -= 1

		self.text_search_frame.hide()
		self.text_search_frame.clear()

	def clear(self, index = -1) :
		if self.shred_lock_flag :
			return

		index = ( self.tab_widget.currentIndex() if index < 0 else index )
		self.single_translate_browsers[index].clear()
		self.tab_widget.setTabText(index, Qt.QString())

	###

	def zoomIn(self, index = -1, range = 1) :
		index = ( self.tab_widget.currentIndex() if index < 0 else index )
		self.single_translate_browsers[index].zoomIn(range)

	def zoomOut(self, index = -1, range = 1) :
		index = ( self.tab_widget.currentIndex() if index < 0 else index )
		self.single_translate_browsers[index].zoomOut(range)

	def zoomNormal(self, index = -1) :
		index = ( self.tab_widget.currentIndex() if index < 0 else index )
		self.single_translate_browsers[index].zoomNormal()


	### Private ###

	def findNext(self, word) :
		index = self.currentIndex()
		self.single_translate_browsers[index].findNext(word)

	def findPrevious(self, word) :
		index = self.currentIndex()
		self.single_translate_browsers[index].findPrevious(word)

	def instantSearch(self, word) :
		index = self.currentIndex()
		self.single_translate_browsers[index].instantSearch(word)


	### Signals ###

	def tabChangedSignal(self) :
		self.emit(Qt.SIGNAL("tabChanged(int)"), self.tab_widget.currentIndex())

	def uFindRequestSignal(self, word) :
		self.emit(Qt.SIGNAL("uFindRequest(const QString &)"), word)

	def cFindRequestSignal(self, word) :
		self.emit(Qt.SIGNAL("cFindRequest(const QString &)"), word)

	def statusChangedSignal(self, str) :
		self.emit(Qt.SIGNAL("statusChanged(const QString &)"), str)


	### Handlers ###

	def mouseDoubleClickEvent(self, event) :
		self.addTab()

