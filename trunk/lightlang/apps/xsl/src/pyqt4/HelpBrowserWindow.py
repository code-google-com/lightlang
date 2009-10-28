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
import TextBrowser
import TextSearchFrame
import TransparentFrame


#####
MyIcon = Config.Prefix+"/lib/xsl/icons/xsl_16.png"
IconsDir = Config.Prefix+"/lib/xsl/icons/"

HtmlDocsDir = Config.Prefix+"/share/doc/lightlang/html/"


#####
def tr(str) :
	return Qt.QApplication.translate("@default", str)


#####
class HelpBrowserWindow(Qt.QDialog) :
	def __init__(self, parent = None) :
		Qt.QDialog.__init__(self, parent)

		self.setObjectName("help_browser_window")

		self.setWindowTitle(tr("%1 Manual").arg(Const.Organization))
		self.setWindowIcon(Qt.QIcon(MyIcon))

		#####

		self.main_layout = Qt.QVBoxLayout()
		self.main_layout.setContentsMargins(0, 0, 0, 0)
		self.main_layout.setSpacing(0)
		self.setLayout(self.main_layout)

		#####

		index_file_path = HtmlDocsDir+Locale.mainLang()+"/index.html"
		if not Qt.QFile.exists(index_file_path) :
			index_file_path = HtmlDocsDir+"en/index.html"
		self.index_file_url = Qt.QUrl(index_file_path)

		#####

		self.text_browser = TextBrowser.TextBrowser()
		self.text_browser_layout = Qt.QHBoxLayout()
		self.text_browser_layout.setAlignment(Qt.Qt.AlignLeft|Qt.Qt.AlignTop)
		self.text_browser.setLayout(self.text_browser_layout)
		self.main_layout.addWidget(self.text_browser)

		###

		self.control_buttons_frame = TransparentFrame.TransparentFrame()
		self.control_buttons_frame_layout = Qt.QHBoxLayout()
		self.control_buttons_frame_layout.setContentsMargins(0, 0, 0, 0)
		self.control_buttons_frame.setLayout(self.control_buttons_frame_layout)
		self.text_browser_layout.addWidget(self.control_buttons_frame)

		self.backward_button = Qt.QToolButton()
		self.backward_button.setIcon(Qt.QIcon(IconsDir+"left_22.png"))
		self.backward_button.setIconSize(Qt.QSize(22, 22))
		self.backward_button.setCursor(Qt.Qt.ArrowCursor)
		self.backward_button.setAutoRaise(True)
		self.backward_button.setEnabled(False)
		self.backward_button.setToolTip(tr("Backspace"))
		self.control_buttons_frame_layout.addWidget(self.backward_button)

		self.forward_button = Qt.QToolButton()
		self.forward_button.setIcon(Qt.QIcon(IconsDir+"right_22.png"))
		self.forward_button.setIconSize(Qt.QSize(22, 22))
		self.forward_button.setCursor(Qt.Qt.ArrowCursor)
		self.forward_button.setAutoRaise(True)
		self.forward_button.setEnabled(False)
		self.control_buttons_frame_layout.addWidget(self.forward_button)

		self.vertical_frame1 = Qt.QFrame()
		self.vertical_frame1.setFrameStyle(Qt.QFrame.VLine|Qt.QFrame.Sunken)
		self.control_buttons_frame_layout.addWidget(self.vertical_frame1)

		self.home_button = Qt.QToolButton()
		self.home_button.setIcon(Qt.QIcon(IconsDir+"home_22.png"))
		self.home_button.setIconSize(Qt.QSize(22, 22))
		self.home_button.setCursor(Qt.Qt.ArrowCursor)
		self.home_button.setAutoRaise(True)
		self.control_buttons_frame_layout.addWidget(self.home_button)

		self.control_buttons_frame.setFixedSize(self.control_buttons_frame_layout.minimumSize())

		###

		self.tools_buttons_frame = TransparentFrame.TransparentFrame()
		self.tools_buttons_frame_layout = Qt.QHBoxLayout()
		self.tools_buttons_frame_layout.setContentsMargins(0, 0, 0, 0)
		self.tools_buttons_frame.setLayout(self.tools_buttons_frame_layout)
		self.text_browser_layout.addWidget(self.tools_buttons_frame)

		self.show_text_search_frame_button = Qt.QToolButton()
		self.show_text_search_frame_button.setIcon(Qt.QIcon(IconsDir+"search_22.png"))
		self.show_text_search_frame_button.setIconSize(Qt.QSize(22, 22))
		self.show_text_search_frame_button.setCursor(Qt.Qt.ArrowCursor)
		self.show_text_search_frame_button.setAutoRaise(True)
		self.show_text_search_frame_button.setToolTip(tr("Ctrl+F, /"))
		self.tools_buttons_frame_layout.addWidget(self.show_text_search_frame_button)

		self.tools_buttons_frame.setFixedSize(self.tools_buttons_frame_layout.minimumSize())

		###

		self.text_search_frame = TextSearchFrame.TextSearchFrame()
		self.text_search_frame.hide()
		self.main_layout.addWidget(self.text_search_frame)

		#####

		self.connect(self.text_search_frame, Qt.SIGNAL("findNextRequest(const QString &)"), self.text_browser.findNext)
		self.connect(self.text_search_frame, Qt.SIGNAL("findPreviousRequest(const QString &)"), self.text_browser.findPrevious)
		self.connect(self.text_search_frame, Qt.SIGNAL("instantSearchRequest(const QString &)"), self.text_browser.instantSearch)

		self.connect(self.text_browser, Qt.SIGNAL("backwardRequest()"), self.backward_button.animateClick)

		self.connect(self.backward_button, Qt.SIGNAL("clicked()"), self.text_browser.backward)
		self.connect(self.forward_button, Qt.SIGNAL("clicked()"), self.text_browser.forward)
		self.connect(self.home_button, Qt.SIGNAL("clicked()"), self.home)

		self.connect(self.show_text_search_frame_button, Qt.SIGNAL("clicked()"), self.text_search_frame.show)
		self.connect(self.show_text_search_frame_button, Qt.SIGNAL("clicked()"), self.text_search_frame.setFocus)

		self.connect(self.text_browser, Qt.SIGNAL("showTextSearchFrameRequest()"), self.text_search_frame.show)
		self.connect(self.text_browser, Qt.SIGNAL("showTextSearchFrameRequest()"), self.text_search_frame.setFocus)
		self.connect(self.text_browser, Qt.SIGNAL("hideTextSearchFrameRequest()"), self.text_search_frame.hide)
		self.connect(self.text_browser, Qt.SIGNAL("setTextSearchFrameLineEditRedAlertPaletteRequest()"),
			self.text_search_frame.setLineEditRedAlertPalette)
		self.connect(self.text_browser, Qt.SIGNAL("setTextSearchFrameLineEditDefaultPaletteRequest()"),
			self.text_search_frame.setLineEditDefaultPalette)
		self.connect(self.text_browser, Qt.SIGNAL("sourceChanged(const QUrl &)"), self.updateTitle)
		self.connect(self.text_browser, Qt.SIGNAL("backwardAvailable(bool)"), self.setBackwardButtonAvailable)
		self.connect(self.text_browser, Qt.SIGNAL("forwardAvailable(bool)"), self.setForwardButtonAvailable)


	### Public ###

	def saveSettings(self) :
		settings = Settings.settings()
		settings.setValue("help_browser_window/size", Qt.QVariant(self.size()))
		settings.setValue("help_browser_window/url", Qt.QVariant(self.text_browser.source()))

	def loadSettings(self) :
		settings = Settings.settings()
		self.resize(settings.value("help_browser_window/size", Qt.QVariant(Qt.QSize(800, 600))).toSize())
		self.text_browser.setSource(settings.value("help_browser_window/url", Qt.QVariant(self.index_file_url)).toUrl())

	###

	def show(self) :
		Qt.QDialog.show(self)
		self.raise_()
		self.activateWindow()
		self.text_browser.setFocus(Qt.Qt.OtherFocusReason)


	### Private ###

	def home(self) :
		self.text_browser.setSource(self.index_file_url)

	###

	def updateTitle(self) :
		self.setWindowTitle(tr("%1 Manual - %2").arg(Const.Organization).arg(self.text_browser.documentTitle()))

	###

	def setBackwardButtonAvailable(self, available) :
		if available :
			self.backward_button.setEnabled(True)
		else :
			self.backward_button.setEnabled(False)

	def setForwardButtonAvailable(self, available) :
		if available :
			self.forward_button.setEnabled(True)
		else :
			self.forward_button.setEnabled(False)


	### Handlers ###

	def keyPressEvent(self, event) :
		if event.key() != Qt.Qt.Key_Escape :
			Qt.QDialog.keyPressEvent(self, event)

