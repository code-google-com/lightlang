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
import TextBrowser
import FindInTextFrame
import TransparentFrame

#####
lang = Qt.QLocale().name()
lang.remove(lang.indexOf("_"), lang.length())

if not lang.simplified().isEmpty() :
	help_dir = Qt.QDir(Config.Prefix+"/share/doc/lightlang/html/"+lang)
	if not help_dir.exists() :
		lang = "en"
else :
	lang = "en"

#####
MyIcon = Config.Prefix+"/lib/xsl/icons/xsl_16.png"
IconsDir = Config.Prefix+"/lib/xsl/icons/"

IndexPage = Config.Prefix+"/share/doc/lightlang/html/"+lang+"/index.html"

#####
def tr(str) :
	return Qt.QApplication.translate("@default", str)

#####
class HelpBrowser(Qt.QWidget) :
	def __init__(self, parent = None) :
		Qt.QWidget.__init__(self, parent)

		self.setWindowTitle(tr("%1 Manual").arg(Const.Organization))
		self.setWindowIcon(Qt.QIcon(MyIcon))
		self.resize(800, 600)

		self.main_layout = Qt.QVBoxLayout()
		self.main_layout.setContentsMargins(0, 0, 0, 0)
		self.main_layout.setSpacing(0)
		self.setLayout(self.main_layout)

		#####

		self.text_browser = TextBrowser.TextBrowser()
		self.text_browser_layout = Qt.QHBoxLayout()
		self.text_browser_layout.setAlignment(Qt.Qt.AlignLeft|Qt.Qt.AlignTop)
		self.text_browser.setLayout(self.text_browser_layout)
		self.main_layout.addWidget(self.text_browser)

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

		self.find_in_text_frame = FindInTextFrame.FindInTextFrame()
		self.find_in_text_frame.hide()
		self.main_layout.addWidget(self.find_in_text_frame)

		#####

		self.connect(self.text_browser, Qt.SIGNAL("showFindInTextFrameRequest()"), self.find_in_text_frame.show)
		self.connect(self.text_browser, Qt.SIGNAL("showFindInTextFrameRequest()"), self.find_in_text_frame.setFocus)
		self.connect(self.text_browser, Qt.SIGNAL("hideFindInTextFrameRequest()"), self.find_in_text_frame.hide)
		self.connect(self.text_browser, Qt.SIGNAL("setFindInTextFrameLineEditRedAlertPaletteRequest()"),
			self.find_in_text_frame.setLineEditRedAlertPalette)
		self.connect(self.text_browser, Qt.SIGNAL("setFindInTextFrameLineEditDefaultPaletteRequest()"),
			self.find_in_text_frame.setLineEditDefaultPalette)

		self.connect(self.find_in_text_frame, Qt.SIGNAL("findNextRequest(const QString &)"), self.text_browser.findNext)
		self.connect(self.find_in_text_frame, Qt.SIGNAL("findPreviousRequest(const QString &)"), self.text_browser.findPrevious)
		self.connect(self.find_in_text_frame, Qt.SIGNAL("instantSearchRequest(const QString &)"), self.text_browser.instantSearch)

		self.connect(self.text_browser, Qt.SIGNAL("backwardRequest()"), self.backward_button.animateClick)

		self.connect(self.backward_button, Qt.SIGNAL("clicked()"), self.text_browser.backward)
		self.connect(self.forward_button, Qt.SIGNAL("clicked()"), self.text_browser.forward)
		self.connect(self.home_button, Qt.SIGNAL("clicked()"), self.home)

		self.connect(self.text_browser, Qt.SIGNAL("sourceChanged(const QUrl &)"), self.updateTitle)
		self.connect(self.text_browser, Qt.SIGNAL("backwardAvailable(bool)"), self.setBackwardButtonAvailable)
		self.connect(self.text_browser, Qt.SIGNAL("forwardAvailable(bool)"), self.setForwardButtonAvailable)

		#####

		self.home()


	### Public ###

	def show(self) :
		x_window_position = (Qt.QApplication.desktop().width() - self.width()) / 2
		if x_window_position < 0 :
			x_window_position = 0
		y_window_position = (Qt.QApplication.desktop().height() - self.height()) / 2
		if y_window_position < 0 :
			y_window_position = 0

		self.move(Qt.QPoint(x_window_position, y_window_position))

		Qt.QWidget.show(self)
		self.raise_()
		self.activateWindow()


	### Private ###

	def home(self) :
		self.text_browser.setSource(Qt.QUrl(IndexPage))

	def updateTitle(self) :
		self.setWindowTitle(tr("%1 Manual - %2").arg(Const.Organization)
			.arg(self.text_browser.documentTitle()))

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


