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
import SLFind

#####
IconsDir = Config.Prefix+"/lib/xsl/icons/"

#####
class TranslateBrowser(Qt.QTextBrowser) :
	def __init__(self, parent = None) :
		Qt.QTextBrowser.__init__(self, parent)

		self.setOpenLinks(False)

		#####

		self.clipboard = Qt.QApplication.clipboard()

		self.find_sound = SLFind.FindSound()

		#####

		self.connect(self, Qt.SIGNAL("anchorClicked(const QUrl &)"), self.findFromAnchor)
		self.connect(self, Qt.SIGNAL("highlighted(const QString &)"), self.checkLink)


	### Private ###

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

	###

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

	def checkLink(self, word) :
		if word.startsWith("#s") :
                        word.remove(0, word.indexOf("_")+1)
                        word = word.simplified()
                        if word.isEmpty() :
                                return

			words_list = word.split(Qt.QRegExp("\\W+"), Qt.QString.SkipEmptyParts)
			if words_list.count() <= 1 :
				return

			count = 1
			while count < words_list.count() :
				if not self.find_sound.checkWord(words_list[0], words_list[count]) :
					self.statusChangedSignal(self.tr("Sound is not full"))
					return
				count += 1
		elif (word.startsWith("http:", Qt.Qt.CaseInsensitive) or
			word.startsWith("mailto:", Qt.Qt.CaseInsensitive)) :
			self.statusChangedSignal(word)


	### Signals ###

	def newTabRequestSignal(self) :
		self.emit(Qt.SIGNAL("newTabRequest()"))

	def uFindRequestSignal(self, word) :
		self.emit(Qt.SIGNAL("uFindRequest(const QString &)"), word)

	def cFindRequestSignal(self, word) :
		self.emit(Qt.SIGNAL("cFindRequest(const QString &)"), word)

	def showFindInTextFrameRequestSignal(self) :
		self.emit(Qt.SIGNAL("showFindInTextFrameRequest()"))

	def hideFindInTextFrameRequestSignal(self) :
		self.emit(Qt.SIGNAL("hideFindInTextFrameRequest()"))

	def statusChangedSignal(self, str) :
		self.emit(Qt.SIGNAL("statusChanged(const QString &)"), str)


	### Handlers ###

	def keyPressEvent(self, event) :
		if event.key() == Qt.Qt.Key_Escape :
			self.hideFindInTextFrameRequestSignal()
		elif event.key() == Qt.Qt.Key_Slash :
			self.showFindInTextFrameRequestSignal()

		Qt.QTextBrowser.keyPressEvent(self, event)

	def mousePressEvent(self, event) :
		if event.button() == Qt.Qt.MidButton :
			word = self.textCursor().selectedText().simplified()
			if word.isEmpty() :
				word = self.clipboard.text(Qt.QClipboard.Selection).simplified()
			if not word.isEmpty() :
				self.newTabRequestSignal()
				self.uFindRequestSignal(word)
		else :
			Qt.QTextBrowser.mousePressEvent(self, event)

	def contextMenuEvent(self, event) :
		context_menu = self.createStandardContextMenu()
		text_cursor = self.textCursor()
		if not text_cursor.selectedText().simplified().isEmpty() :
			context_menu.addSeparator()
			context_menu.addAction(self.tr("Search"), self.uFind)
			context_menu.addAction(self.tr("Expanded search"), self.cFind)
			context_menu.addSeparator()
			context_menu.addAction(self.tr("Search (in new tab)"), self.uFindInNewTab)
			context_menu.addAction(self.tr("Expanded search (in new tab)"), self.cFindInNewTab)
		context_menu.exec_(event.globalPos())
		

#####
class FindInTextFrame(Qt.QFrame) :
	def __init__(self, parent = None) :
		Qt.QFrame.__init__(self, parent)

		self.setFrameShape(Qt.QFrame.Box)

		self.main_layout = Qt.QHBoxLayout()
		self.main_layout.setContentsMargins(2, 2, 2, 2)
		self.setLayout(self.main_layout)

		#####

		self.close_button = Qt.QToolButton()
		self.close_button.setIcon(Qt.QIcon(IconsDir+"close_22.png"))
		self.close_button.setIconSize(Qt.QSize(16, 16))
		self.main_layout.addWidget(self.close_button)

		self.vertical_frame1 = Qt.QFrame()
		self.vertical_frame1.setFrameStyle(Qt.QFrame.VLine|Qt.QFrame.Sunken)
		self.vertical_frame1.setMinimumSize(22, 22)
		self.main_layout.addWidget(self.vertical_frame1)

		self.line_edit_label = Qt.QLabel(self.tr("Search:"))
		self.main_layout.addWidget(self.line_edit_label)

		self.line_edit = Qt.QLineEdit()
		self.line_edit.setFocus(Qt.Qt.OtherFocusReason)
		self.main_layout.addWidget(self.line_edit)

		self.clear_line_edit_button = Qt.QToolButton()
		self.clear_line_edit_button.setIcon(Qt.QIcon(IconsDir+"clear_22.png"))
		self.clear_line_edit_button.setIconSize(Qt.QSize(16, 16))
		self.clear_line_edit_button.setEnabled(False)
		self.main_layout.addWidget(self.clear_line_edit_button)

		self.vertical_frame2 = Qt.QFrame()
		self.vertical_frame2.setFrameStyle(Qt.QFrame.VLine|Qt.QFrame.Sunken)
		self.main_layout.addWidget(self.vertical_frame2)

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

		self.line_edit_default_palette = Qt.QPalette(self.line_edit.palette()) # construct new palette :-)
		self.line_edit_red_alert_palette = Qt.QPalette()
		self.line_edit_red_alert_palette.setColor(Qt.QPalette.Base, Qt.QColor(255, 110, 110, 255))

		#####

		self.connect(self.close_button, Qt.SIGNAL("clicked()"), self.hide)

		self.connect(self.line_edit, Qt.SIGNAL("returnPressed()"), self.next_button.animateClick)
		self.connect(self.line_edit, Qt.SIGNAL("textChanged(const QString &)"), self.setStatus)
		self.connect(self.line_edit, Qt.SIGNAL("textChanged(const QString &)"), self.instantSearchRequest)

		self.connect(self.clear_line_edit_button, Qt.SIGNAL("clicked()"), self.clearLineEdit)

		self.connect(self.next_button, Qt.SIGNAL("clicked()"), self.findNextRequest)

		self.connect(self.previous_button, Qt.SIGNAL("clicked()"), self.findPreviousRequest)


	### Public ###

	def setFocus(self, reason = Qt.Qt.OtherFocusReason) :
		self.line_edit.setFocus(reason)
		self.line_edit.selectAll()

	def setLineEditRedAlertPalette(self) :
		self.line_edit.setPalette(self.line_edit_red_alert_palette)

	def setLineEditDefaultPalette(self) :
		self.line_edit.setPalette(self.line_edit_default_palette)


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

	def instantSearchRequest(self, word) :
		self.instantSearchRequestSignal(word)

	def setStatus(self) :
		if self.line_edit.text().simplified().isEmpty() :
			self.clear_line_edit_button.setEnabled(False)

			self.next_button.setEnabled(False)
			self.previous_button.setEnabled(False)
		else :
			self.clear_line_edit_button.setEnabled(True)

			self.next_button.setEnabled(True)
			self.previous_button.setEnabled(True)

	def clearLineEdit(self) :
		self.line_edit.clear()
		self.line_edit.setFocus(Qt.Qt.OtherFocusReason)


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


#####
class TextBrowser(Qt.QWidget) :
	def __init__(self, parent = None) :
		Qt.QWidget.__init__(self, parent)

		self.main_layout = Qt.QVBoxLayout()
		self.main_layout.setContentsMargins(0, 0, 0, 0)
		self.main_layout.setSpacing(0)
		self.setLayout(self.main_layout)

		#####

		self.shred_lock_flag = False

		self.translate_browsers = []

		self.tmp_text_cursor = Qt.QTextCursor()

		###

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

		self.find_in_text_frame = FindInTextFrame()
		self.find_in_text_frame.setVisible(False)
		self.main_layout.addWidget(self.find_in_text_frame)

		#####

		self.connect(self.add_tab_button, Qt.SIGNAL("clicked()"), self.addTab)
		self.connect(self.remove_tab_button, Qt.SIGNAL("clicked()"), self.removeTab)

		self.connect(self.tab_widget, Qt.SIGNAL("currentChanged(int)"), self.tabChangedSignal)

		self.connect(self.find_in_text_frame, Qt.SIGNAL("findNextRequest(const QString &)"), self.findNext)
		self.connect(self.find_in_text_frame, Qt.SIGNAL("findPreviousRequest(const QString &)"), self.findPrevious)
		self.connect(self.find_in_text_frame, Qt.SIGNAL("instantSearchRequest(const QString &)"), self.instantSearch)

		#####

		self.addTab()


	### Public ###

	def setShredLock(self, shred_lock_flag) :
		self.shred_lock_flag = shred_lock_flag

	def showFindInTextFrame(self) :
		self.find_in_text_frame.setVisible(True)
		self.find_in_text_frame.setFocus()

	def hideFindInTextFrame(self) :
		self.find_in_text_frame.setVisible(False)

	###

	def addTab(self) :
		self.translate_browsers.append(TranslateBrowser())
		index = len(self.translate_browsers) -1
		#
		self.connect(self.translate_browsers[index], Qt.SIGNAL("newTabRequest()"), self.addTab)
		self.connect(self.translate_browsers[index], Qt.SIGNAL("uFindRequest(const QString &)"), self.uFindRequestSignal)
		self.connect(self.translate_browsers[index], Qt.SIGNAL("cFindRequest(const QString &)"), self.cFindRequestSignal)
		self.connect(self.translate_browsers[index], Qt.SIGNAL("showFindInTextFrameRequest()"), self.showFindInTextFrame)
		self.connect(self.translate_browsers[index], Qt.SIGNAL("hideFindInTextFrameRequest()"), self.hideFindInTextFrame)
		self.connect(self.translate_browsers[index], Qt.SIGNAL("statusChanged(const QString &)"), self.statusChangedSignal)
		#
		self.translate_browsers[index].setHtml(self.tr("<em>Empty</em>"))
		self.tab_widget.addTab(self.translate_browsers[index], self.tr("(Untitled)"))
		self.tab_widget.setCurrentIndex(index)
		self.tabChangedSignal()

	def removeTab(self, index = -1) :
		if self.shred_lock_flag :
			return

		if self.tab_widget.count() == 1 :
			self.translate_browsers[0].setHtml(self.tr("<em>Empty</em>"))
			self.tab_widget.setTabText(0, self.tr("(Untitled)"))
		else :
			if index == -1 :
				index = self.tab_widget.currentIndex()
			self.tab_widget.removeTab(index)
			self.translate_browsers.pop(index)
		self.tabChangedSignal()

	###

	def count(self) :
		return self.tab_widget.count()

	def currentIndex(self) :
		return self.tab_widget.currentIndex()

	###

	def setText(self, index, text) :
		self.translate_browsers[index].setHtml(text)

	def setCaption(self, index, word) :
		self.tab_widget.setTabText(index, word)

	###

	def text(self, index = -1) :
		if index == -1 :
			index = self.tab_widget.currentIndex()
		return self.translate_browsers[index].toHtml()

	def caption(self, index = -1) :
		if index == -1 :
			index = self.tab_widget.currentIndex()
		return self.tab_widget.tabText(index)

	def browser(self, index = -1) :
		if index == -1 :
			index = self.tab_widget.currentIndex()
		return self.translate_browsers[index]

	def document(self, index = -1) :
		if index == -1 :
			index = self.tab_widget.currentIndex()
		return self.translate_browsers[index].document()

	###

	def clearPage(self, index = -1) :
		if self.shred_lock_flag :
			return

		if index == -1 :
			index = self.tab_widget.currentIndex()
		self.translate_browsers[index].setHtml(self.tr("<em>Empty</em>"))
		self.tab_widget.setTabText(index, self.tr("(Untitled)"))

	def clearAll(self) :
		if self.shred_lock_flag :
			return

		while self.count() != 1 :
			self.removeTab(0)
		self.clearPage(0)

	def clear(self, index = -1) :
		if self.shred_lock_flag :
			return

		if index == -1 :
			index = self.tab_widget.currentIndex()
		self.translate_browsers[index].clear()
		self.tab_widget.setTabText(index, Qt.QString())

	###

	def zoomIn(self, index = -1, range = 1) :
		if index == -1 :
			index = self.tab_widget.currentIndex()
		self.translate_browsers[index].zoomIn(range)

	def zoomOut(self, index = -1, range = 1) :
		if index == -1 :
			index = self.tab_widget.currentIndex()
		self.translate_browsers[index].zoomOut(range)


	### Private ###

	def findNext(self, word) :
		self.find(word)

	def findPrevious(self, word) :
		self.find(word, True)

	def find(self, word, backward_flag = False) :
		index = self.currentIndex()
		browser = self.browser(index)
		document = self.document(index)
		text_cursor = browser.textCursor()

		if text_cursor.hasSelection() and backward_flag :
			text_cursor.setPosition(text_cursor.anchor(), Qt.QTextCursor.MoveAnchor)

		if not backward_flag :
			new_text_cursor = document.find(word, text_cursor)
			if new_text_cursor.isNull() :
				new_text_cursor = text_cursor
				self.statusChangedSignal(self.tr("Not found"))
		else :
			new_text_cursor = document.find(word, text_cursor, Qt.QTextDocument.FindBackward)
			if new_text_cursor.isNull() :
				new_text_cursor = text_cursor
				self.statusChangedSignal(self.tr("Not found"))

		browser.setTextCursor(new_text_cursor)

	def instantSearch(self, word) : # Thanks :-)
		index = self.currentIndex()

		if word.isEmpty() :
			my_text_cursor = self.tmp_text_cursor = self.translate_browsers[index].textCursor()
		else :
			my_text_cursor = self.translate_browsers[index].textCursor()

		my_text_cursor.setPosition(my_text_cursor.selectionStart(), Qt.QTextCursor.MoveAnchor)
		self.translate_browsers[index].setTextCursor(my_text_cursor)

		my_text_cursor = self.translate_browsers[index].document().find(word, my_text_cursor)

		if my_text_cursor.isNull() and not word.isEmpty() :
			my_text_cursor = self.translate_browsers[index].document().find(word, False)
			if my_text_cursor.isNull() :
				self.find_in_text_frame.setLineEditRedAlertPalette()
				self.tmp_text_cursor.setPosition(self.tmp_text_cursor.selectionStart(), Qt.QTextCursor.MoveAnchor)
				self.translate_browsers[index].setTextCursor(self.tmp_text_cursor)
			else :
				self.tmp_text_cursor = my_text_cursor
				self.translate_browsers[index].setTextCursor(my_text_cursor)
		elif not my_text_cursor.isNull() :
			self.tmp_text_cursor = my_text_cursor
			self.translate_browsers[index].setTextCursor(my_text_cursor)
			self.find_in_text_frame.setLineEditDefaultPalette()
		else :
			self.find_in_text_frame.setLineEditDefaultPalette()


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
