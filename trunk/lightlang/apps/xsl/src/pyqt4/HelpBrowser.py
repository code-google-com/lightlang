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
class HelpTextBrowser(TextBrowser.TextBrowser) :
	def __init__(self, parent = None) :
		TextBrowser.TextBrowser.__init__(self, parent)

		self.connect(self, Qt.SIGNAL("highlighted(const QString &)"), self.setCursorInfo)


	### Public ###

	def home(self) :
		self.setSource(Qt.QUrl(IndexPage))

	def previous(self) :
		self.backward()

	def next(self) :
		self.forward()


	### Private ###

	def setCursorInfo(self, str) :
		if not str.simplified().isEmpty() :
			if (str.startsWith("http:", Qt.Qt.CaseInsensitive) or
				str.startsWith("mailto:", Qt.Qt.CaseInsensitive)) :
				Qt.QToolTip.showText(Qt.QCursor.pos(), str)


	### Signals ###

	def previousRequestSignal(self) :
		self.emit(Qt.SIGNAL("previousRequest()"))


	### Handlers ###

	def keyPressEvent(self, event) :
		if event.key() == Qt.Qt.Key_Backspace :
			self.previousRequestSignal()
		else :
			TextBrowser.TextBrowser.keyPressEvent(self, event)


#####
class HelpBrowser(Qt.QWidget) :
	def __init__(self, parent = None) :
		Qt.QWidget.__init__(self, parent)

		self.setWindowTitle(self.tr("%1 Manual").arg(Const.Organization))
		self.setWindowIcon(Qt.QIcon(MyIcon))
		self.resize(800, 600)

		self.main_layout = Qt.QVBoxLayout()
		self.main_layout.setContentsMargins(0, 0, 0, 0)
		self.main_layout.setSpacing(0)
		self.setLayout(self.main_layout)

		#####

		self.help_text_browser = HelpTextBrowser()
		self.help_text_browser_layout = Qt.QHBoxLayout()
		self.help_text_browser_layout.setAlignment(Qt.Qt.AlignLeft|Qt.Qt.AlignTop)
		self.help_text_browser.setLayout(self.help_text_browser_layout)
		self.main_layout.addWidget(self.help_text_browser)

		self.control_buttons_frame = Qt.QFrame()
		self.control_buttons_frame.setFrameShape(Qt.QFrame.Box)
		self.control_buttons_frame.setFrameShadow(Qt.QFrame.Raised)
		color = Qt.QApplication.palette().color(Qt.QPalette.Window)
		r = color.red(); g = color.green(); b = color.blue()
		try :
			self.control_buttons_frame.setStyleSheet("QFrame {"
					"border: 1px solid gray;"
					"border-radius: 4px;"
					"background-color: rgb("+str(r)+", "+str(g)+", "+str(b)+", 180);"
				"}")
		except : pass
		self.control_buttons_frame_layout = Qt.QHBoxLayout()
		self.control_buttons_frame_layout.setContentsMargins(0, 0, 0, 0)
		self.control_buttons_frame.setLayout(self.control_buttons_frame_layout)
		self.help_text_browser_layout.addWidget(self.control_buttons_frame)

		self.previous_button = Qt.QToolButton()
		self.previous_button.setIcon(Qt.QIcon(IconsDir+"left_22.png"))
		self.previous_button.setIconSize(Qt.QSize(22, 22))
		self.previous_button.setCursor(Qt.Qt.ArrowCursor)
		self.previous_button.setAutoRaise(True)
		self.previous_button.setEnabled(False)
		self.control_buttons_frame_layout.addWidget(self.previous_button)

		self.next_button = Qt.QToolButton()
		self.next_button.setIcon(Qt.QIcon(IconsDir+"right_22.png"))
		self.next_button.setIconSize(Qt.QSize(22, 22))
		self.next_button.setCursor(Qt.Qt.ArrowCursor)
		self.next_button.setAutoRaise(True)
		self.next_button.setEnabled(False)
		self.control_buttons_frame_layout.addWidget(self.next_button)

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
		self.find_in_text_frame.setVisible(False)
		self.main_layout.addWidget(self.find_in_text_frame)

		#####

		self.connect(self.help_text_browser, Qt.SIGNAL("showFindInTextFrameRequest()"), self.find_in_text_frame.show)
		self.connect(self.help_text_browser, Qt.SIGNAL("showFindInTextFrameRequest()"), self.find_in_text_frame.setFocus)
		self.connect(self.help_text_browser, Qt.SIGNAL("hideFindInTextFrameRequest()"), self.find_in_text_frame.hide)
		self.connect(self.help_text_browser, Qt.SIGNAL("setFindInTextFrameLineEditRedAlertPaletteRequest()"),
			self.find_in_text_frame.setLineEditRedAlertPalette)
		self.connect(self.help_text_browser, Qt.SIGNAL("setFindInTextFrameLineEditDefaultPaletteRequest()"),
			self.find_in_text_frame.setLineEditDefaultPalette)

		self.connect(self.find_in_text_frame, Qt.SIGNAL("findNextRequest(const QString &)"), self.help_text_browser.findNext)
		self.connect(self.find_in_text_frame, Qt.SIGNAL("findPreviousRequest(const QString &)"), self.help_text_browser.findPrevious)
		self.connect(self.find_in_text_frame, Qt.SIGNAL("instantSearchRequest(const QString &)"), self.help_text_browser.instantSearch)

		self.connect(self.help_text_browser, Qt.SIGNAL("previousRequest()"), self.previous_button.animateClick)

		self.connect(self.previous_button, Qt.SIGNAL("clicked()"), self.help_text_browser.previous)
		self.connect(self.next_button, Qt.SIGNAL("clicked()"), self.help_text_browser.next)
		self.connect(self.home_button, Qt.SIGNAL("clicked()"), self.help_text_browser.home)

		self.connect(self.help_text_browser, Qt.SIGNAL("sourceChanged(const QUrl &)"), self.updateTitle)
		self.connect(self.help_text_browser, Qt.SIGNAL("backwardAvailable(bool)"), self.setPreviousButtonAvailable)
		self.connect(self.help_text_browser, Qt.SIGNAL("forwardAvailable(bool)"), self.setNextButtonAvailable)

		#####

		self.help_text_browser.home()


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

	def updateTitle(self) :
		self.setWindowTitle(self.tr("%1 Manual - %2").arg(Const.Organization)
			.arg(self.help_text_browser.documentTitle()))

	###

	def setPreviousButtonAvailable(self, available) :
		if available :
			self.previous_button.setEnabled(True)
		else :
			self.previous_button.setEnabled(False)

	def setNextButtonAvailable(self, available) :
		if available :
			self.next_button.setEnabled(True)
		else :
			self.next_button.setEnabled(False)


