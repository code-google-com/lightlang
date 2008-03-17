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
Emblem = Config.Prefix+"/lib/xsl/pictures/emblem.png"
IconsDir = Config.Prefix+"/lib/xsl/icons/"

IndexPage = Config.Prefix+"/share/doc/lightlang/html/"+lang+"/index.html"

#####
class HelpBrowser(Qt.QDialog) :
	def __init__(self, parent = None) :
		Qt.QDialog.__init__(self, parent)

		self.setWindowTitle(self.tr("%1 Manual").arg(Const.Organization))
		self.setWindowIcon(Qt.QIcon(MyIcon))
		self.resize(750, 550)

		self.main_layout = Qt.QVBoxLayout()
		self.setLayout(self.main_layout)

		self.buttons_layout = Qt.QHBoxLayout()
		self.main_layout.addLayout(self.buttons_layout)

		#####

		self.previous_button = Qt.QToolButton()
		self.previous_button.setIcon(Qt.QIcon(IconsDir+"left_22.png"))
		self.previous_button.setIconSize(Qt.QSize(22, 22))
		self.previous_button.setEnabled(False)
		self.buttons_layout.addWidget(self.previous_button)

		self.next_button = Qt.QToolButton()
		self.next_button.setIcon(Qt.QIcon(IconsDir+"right_22.png"))
		self.next_button.setIconSize(Qt.QSize(22, 22))
		self.next_button.setEnabled(False)
		self.buttons_layout.addWidget(self.next_button)

		self.vertical_frame1 = Qt.QFrame()
		self.vertical_frame1.setFrameStyle(Qt.QFrame.VLine|Qt.QFrame.Sunken)
		self.buttons_layout.addWidget(self.vertical_frame1)

		self.home_button = Qt.QToolButton()
		self.home_button.setIcon(Qt.QIcon(IconsDir+"home_22.png"))
		self.home_button.setIconSize(Qt.QSize(22, 22))
		self.buttons_layout.addWidget(self.home_button)

		self.vertical_frame2 = Qt.QFrame()
		self.vertical_frame2.setFrameStyle(Qt.QFrame.VLine|Qt.QFrame.Sunken)
		self.buttons_layout.addWidget(self.vertical_frame2)

		self.reload_button = Qt.QToolButton()
		self.reload_button.setIcon(Qt.QIcon(IconsDir+"reload_22.png"))
		self.reload_button.setIconSize(Qt.QSize(22, 22))
		self.buttons_layout.addWidget(self.reload_button)

		self.buttons_layout.addStretch()

		self.link_label = Qt.QLabel()
		self.buttons_layout.addWidget(self.link_label)

		self.text_browser = Qt.QTextBrowser()
		self.text_browser.setOpenExternalLinks(True)
		self.main_layout.addWidget(self.text_browser)

		#####

		self.connect(self.previous_button, Qt.SIGNAL("clicked()"), self.previous)
		self.connect(self.next_button, Qt.SIGNAL("clicked()"), self.next)
		self.connect(self.home_button, Qt.SIGNAL("clicked()"), self.home)
		self.connect(self.reload_button, Qt.SIGNAL("clicked()"), self.reload)

		self.connect(self.text_browser, Qt.SIGNAL("highlighted(const QString &)"), self.updateLinkLabel)
		self.connect(self.text_browser, Qt.SIGNAL("sourceChanged(const QUrl &)"), self.updateTitle)
		self.connect(self.text_browser, Qt.SIGNAL("backwardAvailable(bool)"), self.checkPreviousButton)
		self.connect(self.text_browser, Qt.SIGNAL("forwardAvailable(bool)"), self.checkNextButton)

		#####

		self.home()


	### Private ###

	def home(self) :
		self.text_browser.setSource(Qt.QUrl(IndexPage))
		self.text_browser.clearHistory()
		self.previous_button.setEnabled(False)
		self.next_button.setEnabled(False)

	def previous(self) :
		self.text_browser.backward()

	def next(self) :
		self.text_browser.forward()

	def reload(self) :
		self.text_browser.reload()

	###

	def updateLinkLabel(self, str) :
		self.link_label.setText("<em><font color=\"#494949\">"
			"&nbsp;&nbsp;&nbsp;"+str+"</font></em>")

	def updateTitle(self) :
		self.setWindowTitle(self.tr("%1 Manual - %2").arg(Const.Organization)
			.arg(self.text_browser.documentTitle()))

	###

	def checkPreviousButton(self, available) :
		if available :
			self.previous_button.setEnabled(True)
		else :
			self.previous_button.setEnabled(False)

	def checkNextButton(self, available) :
		if available :
			self.next_button.setEnabled(True)
		else :
			self.next_button.setEnabled(False)

#####
class About(Qt.QDialog) :
	def __init__(self, parent = None) :
		Qt.QDialog.__init__(self, parent)

		self.setWindowTitle(self.tr("About %1").arg(Const.MyName))
		self.setWindowIcon(Qt.QIcon(MyIcon))

		self.main_layout = Qt.QVBoxLayout()
		self.setLayout(self.main_layout)

		self.icon_label_layout = Qt.QHBoxLayout()
		self.icon_label_layout.setAlignment(Qt.Qt.AlignHCenter)
		self.main_layout.addLayout(self.icon_label_layout)

		self.text_label_layout = Qt.QHBoxLayout()
		self.main_layout.addLayout(self.text_label_layout)

		self.ok_button_layout = Qt.QHBoxLayout()
		self.ok_button_layout.setAlignment(Qt.Qt.AlignHCenter)
		self.main_layout.addLayout(self.ok_button_layout)

		###

		self.icon_label = Qt.QLabel()
		self.icon_label.setPixmap(Qt.QPixmap(IconsDir+"xsl_128.png"))
		self.icon_label_layout.addWidget(self.icon_label)

		self.text_label = Qt.QLabel(self.tr("<center><h3>XSL - the graphical interface for SL</h3></center>"
			"All the programs of the <strong>LightLang</strong> package are distributable, according<br>"
			"to the license <strong>GPLv2</strong>. For details visit <em>License agreement</em> of the<br>"
			"<strong>LightLang</strong> manual.<br>"
			"<br>"
			"Author of the <strong>LightLang</strong> package:<br>"
			"&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<em>Devaev Maxim</em><br>"
			"Thanks to:<br>"
			"&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<em>Baburina Elisabeth</em><br>"
			"Valuable assistants:<br>"
			"&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<em>Vladimir Fomkin</em><br>"
			"&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<em>Tihonov Sergey</em><br>"
			"Translators:<br>"
			"&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<em>Kirill Nebogin</em><br>"
			"<br>"
			"<em>Copyright &copy; 2007-2016 Devaev Maxim"
			" (<a href=\"mailto:mdevaev@gmail.com?subject=LightLang\">mdevaev@gmail.com</a>)</em>"))
		self.text_label.setOpenExternalLinks(True)
		self.text_label_layout.addWidget(self.text_label)

		self.ok_button = Qt.QPushButton(self.tr("OK"))
		self.ok_button_layout.addWidget(self.ok_button)

		###

		self.connect(self.ok_button, Qt.SIGNAL("clicked()"), self.accept)
