# -*- coding: utf8 -*-
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
import SLFind

#####
IconsDir = Config.Prefix+"/lib/xsl/icons/"

#####
class TextBrowser(Qt.QWidget) :
	def __init__(self, parent = None) :
		Qt.QWidget.__init__(self, parent)

		self.main_layout = Qt.QVBoxLayout()
		self.main_layout.setMargin(0)
		self.main_layout.setSpacing(0)
		self.setLayout(self.main_layout)

		#####

		self.find_sound = SLFind.FindSound()

		#####

		self.text_browsers = []

		self.tab_widget = Qt.QTabWidget()
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

		#####

		self.connect(self.add_tab_button, Qt.SIGNAL("clicked()"), self.addTab)
		self.connect(self.remove_tab_button, Qt.SIGNAL("clicked()"), self.removeTab)

		self.connect(self.tab_widget, Qt.SIGNAL("currentChanged(int)"), self.tabChangedSignal)

		#####

		self.addTab()


	### Public ###

	def addTab(self) :
		self.text_browsers.append(Qt.QTextBrowser())
		index = len(self.text_browsers) -1
		try : # FIXME with PyQt-4.3
			self.text_browsers[index].setOpenLinks(False)
		except : pass
		self.text_browsers[index].setHtml(self.tr("<em>Empty</em>"))
		self.connect(self.text_browsers[index],	Qt.SIGNAL("anchorClicked(const QUrl &)"), self.findFromAnchor)
		self.tab_widget.addTab(self.text_browsers[index], self.tr("(Untitled)"))
		self.tab_widget.setCurrentIndex(index)
		self.tabChangedSignal()

	def removeTab(self, index = -1) :
		if self.tab_widget.count() == 1 :
			self.text_browsers[0].setHtml(self.tr("<em>Empty</em>"))
			self.tab_widget.setTabText(0, self.tr("(Untitled)"))
		else :
			if index == -1 :
				index = self.tab_widget.currentIndex()
			self.tab_widget.removeTab(index)
			self.text_browsers.pop(index)
		self.tabChangedSignal()

	###

	def count(self) :
		return self.tab_widget.count()

	def currentIndex(self) :
		return self.tab_widget.currentIndex()

	###

	def setText(self, index, text) :
		self.text_browsers[index].setHtml(text)

	def setCaption(self, index, word) :
		self.tab_widget.setTabText(index, word)

	###

	def text(self, index = -1) :
		if index == -1 :
			index = self.tab_widget.currentIndex()
		return self.text_browsers[index].toHtml()

	def caption(self, index = -1) :
		if index == -1 :
			index = self.tab_widget.currentIndex()
		return self.tab_widget.tabText(index)

	def browser(self, index = -1) :
		if index == -1 :
			index = self.tab_widget.currentIndex()
		return self.text_browsers[index]

	def document(self, index = -1 ) :
		if index == -1 :
			index = self.tab_widget.currentIndex()
		return self.text_browsers[index].document()

	###

	def clearPage(self, index = -1) :
		if index == -1 :
			index = self.tab_widget.currentIndex()
		self.text_browsers[index].setHtml(self.tr("<em>Empty</em>"))
		self.tab_widget.setTabText(index, self.tr("(Untitled)"))

	def clearAll(self) :
		while self.count() != 1 :
			Qt.QCoreApplication.processEvents()
			self.removeTab(0)
		self.clearPage(0)

	def clear(self, index = -1) :
		if index == -1 :
			index = self.tab_widget.currentIndex()
		self.text_browsers[index].clear()
		self.tab_widget.setTabText(index, Qt.QString())

	###

	def findNext(self, index, word) :
		return self.text_browsers[index].find(word)

	def findPrevious(self, index, word) :
		return self.text_browsers[index].find(word, Qt.QTextDocument.FindBackward)

	###

	def zoomIn(self, index = -1, range = 1) :
		if index == -1 :
			index = self.tab_widget.currentIndex()
		self.text_browsers[index].zoomIn(range)

	def zoomOut(self, index = -1, range = 1) :
		if index == -1 :
			index = self.tab_widget.currentIndex()
		self.text_browsers[index].zoomOut(range)


	### Private ###

	def findFromAnchor(self, url) :
		word = url.toString()
		if word.startsWith("#s") :
			word.remove(0, word.indexOf("_")+1)
			word = word.simplified()
			if word.isEmpty() :
				return
			self.find_sound.find(word)
		elif word.startsWith("http://", Qt.Qt.CaseInsensitive) :
			Qt.QDesktopServices.openUrl(url)


	### Signals ###

	def tabChangedSignal(self) :
		self.emit(Qt.SIGNAL("tabChanged(int)"), self.tab_widget.currentIndex())


	### Events ###

	def mouseDoubleClickEvent(self, event) :
		self.addTab()
