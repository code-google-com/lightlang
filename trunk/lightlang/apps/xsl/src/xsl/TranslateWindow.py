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
import Utils
import Settings
import UserStyleCss
import IconsLoader
import PopupWindow
import TextSearchFrame
import TranslateBrowser


##### Public classes #####
class TranslateWindow(PopupWindow.PopupWindow) :
	def __init__(self, parent = None) :
		PopupWindow.PopupWindow.__init__(self, parent)

		self.setObjectName("translate_window")

		#####

		self._main_layout = Qt.QVBoxLayout()
		self._main_layout.setContentsMargins(0, 0, 0, 0)
		self._main_layout.setSpacing(0)
		self.setLayout(self._main_layout)

		self._caption_frame = Qt.QFrame(self)
		self._caption_frame.setMouseTracking(True)
		self._caption_frame.setFrameShape(Qt.QFrame.Box)
		self._caption_frame.setFrameShadow(Qt.QFrame.Raised)
		if self.font().pixelSize() > 0 :
			self._caption_frame.setMaximumHeight((self.font().pixelSize()) * 4)
		elif self.font().pointSize() > 0 :
			self._caption_frame.setMaximumHeight((self.font().pointSize()) * 4)
		else :
			self._caption_frame.setMaximumHeight(40)
		self._main_layout.addWidget(self._caption_frame)

		self._caption_frame_layout = Qt.QHBoxLayout()
		self._caption_frame_layout.setContentsMargins(20, 1, 2, 1)
		self._caption_frame_layout.setSpacing(1)
		self._caption_frame.setLayout(self._caption_frame_layout)

		#####

		self._caption_label = Qt.QLabel(self)
		self._caption_label.setTextFormat(Qt.Qt.RichText)
		self._caption_label.setWordWrap(True)
		self._caption_frame_layout.addWidget(self._caption_label)

		self._close_button = Qt.QToolButton(self)
		self._close_button.setIcon(IconsLoader.icon("dialog-cancel"))
		self._close_button.setIconSize(Qt.QSize(16, 16))
		self._close_button.setFixedSize(Qt.QSize(16, 16))
		self._close_button.setCursor(Qt.Qt.ArrowCursor)
		self._close_button.setAutoRaise(True)
		self._caption_frame_layout.addWidget(self._close_button)

		self._translate_browser = TranslateBrowser.TranslateBrowser(self)
		self._main_layout.addWidget(self._translate_browser)

		self._text_search_frame = TextSearchFrame.TextSearchFrame(self)
		self._text_search_frame.hide()
		self._main_layout.addWidget(self._text_search_frame)

		#####

		self.connect(self._close_button, Qt.SIGNAL("clicked()"), self.close)

		self.connect(self._translate_browser, Qt.SIGNAL("showTextSearchFrameRequest()"), self._text_search_frame.show)
		self.connect(self._translate_browser, Qt.SIGNAL("hideTextSearchFrameRequest()"), self._text_search_frame.hide)
		self.connect(self._translate_browser, Qt.SIGNAL("setFoundRequest(bool)"), self._text_search_frame.setFound)
		self.connect(self._translate_browser, Qt.SIGNAL("newTabRequest()"), self.newTabRequestSignal)
		self.connect(self._translate_browser, Qt.SIGNAL("uFindRequest(const QString &)"), self.uFindRequestSignal)
		self.connect(self._translate_browser, Qt.SIGNAL("cFindRequest(const QString &)"), self.cFindRequestSignal)

		self.connect(self._text_search_frame, Qt.SIGNAL("findNextRequest(const QString &)"), self._translate_browser.findNext)
		self.connect(self._text_search_frame, Qt.SIGNAL("findPreviousRequest(const QString &)"), self._translate_browser.findPrevious)
		self.connect(self._text_search_frame, Qt.SIGNAL("instantSearchRequest(const QString &)"), self._translate_browser.instantSearch)

		self.connect(self._close_button, Qt.SIGNAL("clicked()"), self.close)


	### Public ###

	def setCaption(self, caption) :
		self._caption_label.setText(Utils.styledHtml(UserStyleCss.userStyleCss(), caption))

	def setText(self, text) :
		self._translate_browser.setText(text)

	def clear(self) :
		self._translate_browser.clear()

	###

	def saveSettings(self) :
		settings = Settings.settings()
		settings.setValue("translate_window/size", Qt.QVariant(self.size()))

	def loadSettings(self) :
		settings = Settings.settings()
		self.resize(settings.value("translate_window/size", Qt.QVariant(Qt.QSize(550, 400))).toSize())

	###

	def setFocus(self, reason = Qt.Qt.OtherFocusReason) :
		self._translate_browser.setFocus(reason)

	def show(self) :
		self._text_search_frame.hide()
		PopupWindow.PopupWindow.show(self)


	### Private ###
	### Signals ###

	def newTabRequestSignal(self) :
		self.emit(Qt.SIGNAL("newTabRequest()"))

	def uFindRequestSignal(self, word) :
		self.emit(Qt.SIGNAL("uFindRequest(const QString &)"), word)

	def cFindRequestSignal(self, word) :
		self.emit(Qt.SIGNAL("cFindRequest(const QString &)"), word)


