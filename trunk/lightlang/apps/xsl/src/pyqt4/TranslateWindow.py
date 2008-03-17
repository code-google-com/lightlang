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
import SLFind
import Config
import Const

#####
IconsDir = Config.Prefix+"/lib/xsl/icons/"

#####
class TranslateWindow(Qt.QDialog) :
	def __init__(self, parent = None) :
		Qt.QDialog.__init__(self, parent)

		self.setWindowFlags(Qt.Qt.Popup)
		self.resize(550, 400)

		self.main_layout = Qt.QVBoxLayout()
		self.main_layout.setMargin(0)
		self.main_layout.setSpacing(0)
		self.setLayout(self.main_layout)

		self.caption_layout = Qt.QHBoxLayout()
		self.caption_layout.setMargin(0)
		self.caption_layout.setSpacing(0)
		self.main_layout.addLayout(self.caption_layout)

		#####

		self.cursor = Qt.QCursor()
		self.desktop_widget = Qt.QDesktopWidget()

		self.find_sound = SLFind.FindSound()

		#####

		self.caption_label = Qt.QLabel()
		self.caption_layout.addWidget(self.caption_label)

		self.caption_layout.addStretch()

		self.close_button = Qt.QToolButton()
		self.close_button.setIcon(Qt.QIcon(IconsDir+"hide_22.png"))
		self.close_button.setIconSize(Qt.QSize(16, 16))
		self.close_button.setFixedSize(Qt.QSize(22, 22))
		self.caption_layout.addWidget(self.close_button)

		self.text_browser = Qt.QTextBrowser()
		try : # FIXME with PyQt-4.3
			self.text_browser.setOpenLinks(False)
		except : pass
		self.main_layout.addWidget(self.text_browser)

		#####

		self.connect(self.close_button, Qt.SIGNAL("clicked()"), self.hide)
		self.connect(self.text_browser, Qt.SIGNAL("anchorClicked(const QUrl &)"), self.findFromAnchor)


	### Public ###

	def setCaption(self, str) :
		self.caption_label.setText("<em><strong><font color=\"#494949\">"
			"&nbsp;&nbsp;&nbsp;"+str+"</font></strong></em>")

	def setText(self, text) :
		self.text_browser.setHtml(text)

	def clear(self) :
		self.text_browser.clear()

	def showUnderCursor(self) :
		cursor_position = Qt.QCursor.pos()
		if cursor_position.x() + 550 > self.desktop_widget.width() :
			x_window_position = self.desktop_widget.width() - 550
		else :
			x_window_position = cursor_position.x()
		if cursor_position.y() + 400 > self.desktop_widget.height() :
			y_window_position = self.desktop_widget.height() - 400
		else :
			y_window_position = cursor_position.y()
		window_position = Qt.QPoint(x_window_position, y_window_position)
		self.resize(550, 400)
		self.move(window_position)
		self.show()


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
