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
import Locale
import Settings
import IconsLoader
import TextBrowser
import TextSearchFrame
import TransparentFrame


#####
HtmlDocsDir = Config.DocsDir+"/lightlang/html/"


#####
class HelpBrowserWindow(Qt.QDialog) :
	def __init__(self, parent = None) :
		Qt.QDialog.__init__(self, parent)

		self.setObjectName("help_browser_window")

		self.setWindowTitle(tr("%1 Manual").arg(Const.Organization))
		self.setWindowIcon(IconsLoader.icon("xsl"))

		#####

		self._main_layout = Qt.QVBoxLayout()
		self._main_layout.setContentsMargins(0, 0, 0, 0)
		self._main_layout.setSpacing(0)
		self.setLayout(self._main_layout)

		#####

		index_file_path = HtmlDocsDir+Locale.mainLang()+"/index.html"
		if not Qt.QFile.exists(index_file_path) :
			index_file_path = HtmlDocsDir+"en/index.html"
		self._index_file_url = Qt.QUrl(index_file_path)

		#####

		self._text_browser = TextBrowser.TextBrowser()
		self._text_browser_layout = Qt.QHBoxLayout()
		self._text_browser_layout.setAlignment(Qt.Qt.AlignLeft|Qt.Qt.AlignTop)
		self._text_browser.setLayout(self._text_browser_layout)
		self._main_layout.addWidget(self._text_browser)

		###

		self._control_buttons_frame = TransparentFrame.TransparentFrame()
		self._control_buttons_frame_layout = Qt.QHBoxLayout()
		self._control_buttons_frame_layout.setContentsMargins(0, 0, 0, 0)
		self._control_buttons_frame.setLayout(self._control_buttons_frame_layout)
		self._text_browser_layout.addWidget(self._control_buttons_frame)

		self._backward_button = Qt.QToolButton()
		self._backward_button.setIcon(IconsLoader.icon("go-previous"))
		self._backward_button.setIconSize(Qt.QSize(22, 22))
		self._backward_button.setCursor(Qt.Qt.ArrowCursor)
		self._backward_button.setAutoRaise(True)
		self._backward_button.setEnabled(False)
		self._backward_button.setToolTip(tr("Backspace"))
		self._control_buttons_frame_layout.addWidget(self._backward_button)

		self._forward_button = Qt.QToolButton()
		self._forward_button.setIcon(IconsLoader.icon("go-next"))
		self._forward_button.setIconSize(Qt.QSize(22, 22))
		self._forward_button.setCursor(Qt.Qt.ArrowCursor)
		self._forward_button.setAutoRaise(True)
		self._forward_button.setEnabled(False)
		self._control_buttons_frame_layout.addWidget(self._forward_button)

		self._vertical_frame1 = Qt.QFrame()
		self._vertical_frame1.setFrameStyle(Qt.QFrame.VLine|Qt.QFrame.Sunken)
		self._control_buttons_frame_layout.addWidget(self._vertical_frame1)

		self._home_button = Qt.QToolButton()
		self._home_button.setIcon(IconsLoader.icon("go-home"))
		self._home_button.setIconSize(Qt.QSize(22, 22))
		self._home_button.setCursor(Qt.Qt.ArrowCursor)
		self._home_button.setAutoRaise(True)
		self._control_buttons_frame_layout.addWidget(self._home_button)

		self._control_buttons_frame.setFixedSize(self._control_buttons_frame_layout.minimumSize())

		###

		self._tools_buttons_frame = TransparentFrame.TransparentFrame()
		self._tools_buttons_frame_layout = Qt.QHBoxLayout()
		self._tools_buttons_frame_layout.setContentsMargins(0, 0, 0, 0)
		self._tools_buttons_frame.setLayout(self._tools_buttons_frame_layout)
		self._text_browser_layout.addWidget(self._tools_buttons_frame)

		self._show_text_search_frame_button = Qt.QToolButton()
		self._show_text_search_frame_button.setIcon(IconsLoader.icon("edit-find"))
		self._show_text_search_frame_button.setIconSize(Qt.QSize(22, 22))
		self._show_text_search_frame_button.setCursor(Qt.Qt.ArrowCursor)
		self._show_text_search_frame_button.setAutoRaise(True)
		self._show_text_search_frame_button.setToolTip(tr("Ctrl+F, /"))
		self._tools_buttons_frame_layout.addWidget(self._show_text_search_frame_button)

		self._tools_buttons_frame.setFixedSize(self._tools_buttons_frame_layout.minimumSize())

		###

		self._text_search_frame = TextSearchFrame.TextSearchFrame()
		self._text_search_frame.hide()
		self._main_layout.addWidget(self._text_search_frame)

		#####

		self.connect(self._text_search_frame, Qt.SIGNAL("findNextRequest(const QString &)"), self._text_browser.findNext)
		self.connect(self._text_search_frame, Qt.SIGNAL("findPreviousRequest(const QString &)"), self._text_browser.findPrevious)
		self.connect(self._text_search_frame, Qt.SIGNAL("instantSearchRequest(const QString &)"), self._text_browser.instantSearch)

		self.connect(self._text_browser, Qt.SIGNAL("backwardRequest()"), self._backward_button.animateClick)

		self.connect(self._backward_button, Qt.SIGNAL("clicked()"), self._text_browser.backward)
		self.connect(self._forward_button, Qt.SIGNAL("clicked()"), self._text_browser.forward)
		self.connect(self._home_button, Qt.SIGNAL("clicked()"), self.home)

		self.connect(self._show_text_search_frame_button, Qt.SIGNAL("clicked()"), self._text_search_frame.show)

		self.connect(self._text_browser, Qt.SIGNAL("showTextSearchFrameRequest()"), self._text_search_frame.show)
		self.connect(self._text_browser, Qt.SIGNAL("hideTextSearchFrameRequest()"), self._text_search_frame.hide)
		self.connect(self._text_browser, Qt.SIGNAL("setFoundRequest(bool)"), self._text_search_frame.setFound)
		self.connect(self._text_browser, Qt.SIGNAL("sourceChanged(const QUrl &)"), self.updateTitle)
		self.connect(self._text_browser, Qt.SIGNAL("backwardAvailable(bool)"), self.setBackwardButtonAvailable)
		self.connect(self._text_browser, Qt.SIGNAL("forwardAvailable(bool)"), self.setForwardButtonAvailable)


	### Public ###

	def saveSettings(self) :
		settings = Settings.settings()
		settings.setValue("help_browser_window/size", Qt.QVariant(self.size()))
		settings.setValue("help_browser_window/url", Qt.QVariant(self._text_browser.source()))

	def loadSettings(self) :
		settings = Settings.settings()
		self.resize(settings.value("help_browser_window/size", Qt.QVariant(Qt.QSize(800, 600))).toSize())
		self._text_browser.setSource(settings.value("help_browser_window/url", Qt.QVariant(self._index_file_url)).toUrl())

	###

	def show(self) :
		Qt.QDialog.show(self)
		self.raise_()
		self.activateWindow()
		self._text_browser.setFocus(Qt.Qt.OtherFocusReason)


	### Private ###

	def home(self) :
		self._text_browser.setSource(self._index_file_url)

	###

	def updateTitle(self) :
		self.setWindowTitle(tr("%1 Manual - %2").arg(Const.Organization).arg(self._text_browser.documentTitle()))

	###

	def setBackwardButtonAvailable(self, available) :
		if available :
			self._backward_button.setEnabled(True)
		else :
			self._backward_button.setEnabled(False)

	def setForwardButtonAvailable(self, available) :
		if available :
			self._forward_button.setEnabled(True)
		else :
			self._forward_button.setEnabled(False)


	### Handlers ###

	def keyPressEvent(self, event) :
		if event.key() != Qt.Qt.Key_Escape :
			Qt.QDialog.keyPressEvent(self, event)

