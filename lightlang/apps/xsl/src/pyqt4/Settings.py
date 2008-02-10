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
import Global

#####
MyIcon = Config.Prefix+"/lib/xsl/icons/xsl_16.png"
IconsDir = Config.Prefix+"/lib/xsl/icons/"

#####
class Settings(Qt.QObject) :
	def __init__(self, parent = None) :
		Qt.QObject.__init__(self, parent)

		self.common_lang = Qt.QString()

		self.common_http_proxy_type = 0
		self.common_http_proxy_server = Qt.QString()
		self.common_http_proxy_port = 1
		self.common_http_proxy_user = Qt.QString()
		self.common_http_proxy_passwd = Qt.QString()

		###

		self.sl_engine_show_time_flag = False

		###

		self.spy_delay = 100
		self.spy_show_translate_window_flag = True
		self.spy_auto_detect_window_flag = True

		###

		self.main_window_window_size = Qt.QSize(845, 650)
		self.main_window_window_position = Qt.QPoint(0, 0)
		self.main_window_is_visible_flag = True
		self.main_window_state = Qt.QByteArray()

		###

		self.tray_icon_is_visible_flag = True

		###

		self.dicts_manager_used_dicts_list = Qt.QStringList()

		###

		self.google_translate_panel_langpair_combobox_index = 0

		###

		self.history_panel_history_size = 100
		self.history_panel_history_list = Qt.QStringList()

		#####

		self.settings = Qt.QSettings(Const.Organizatonm Const.MyName)


	### Public ###

	def saveSettings(self) :
		self.settings.setValue("common/lang", Qt.QVariant(self.common_lang))

		self.settings.setValue("common/http_proxy_type", Qt.QVariant(self.common_http_proxy_type))
		self.settings.setValue("common/http_proxy_server", Qt.QVariant(self.common_http_proxy_type))
		self.settings.setValue("common/http_proxy_port", Qt.QVariant(self.common_http_proxy_port))
		self.settings.setValue("common/http_proxy_user", Qt.QVariant(self.common_http_proxy_user))
		self.settings.setValue("common/http_proxy_passwd", Qt.QVariant(self.common_http_proxy_passwd))

		self.settings.setValue("sl_engine/show_time_flag", Qt.QVariant(self.sl_engine_show_time_flag))

		self.settings.setValue("spy/delay", Qt.QVariant(self.spy_delay))
		self.settings.setValue("spy/show_translate_window_flag", Qt.QVariant(self.spy_show_translate_window_flag))
		self.settings.setValue("spy/auto_detect_window_flag", Qt.QVariant(self.spy_auto))

		self.settings.setValue("main_window/window_size", Qt.QVariant(self.main_window_window_size))
		self.settings.setValue("main_window/window_position", Qt.QVariant(self.main_window_window_position))
		self.settings.setValue("main_window/is_visible_flag", Qt.QVariant(self.main_window_is_visible_flag)
		self.settings.setValue("main_window/state", Qt.QVariant(self.main_window_state))

		self.settings.setValue("dicts_manager/used_dicts_list", Qt.QVariant(self.dicts_manager_used_dicts_list))

		self.settings.setValue("google_translate_panel/langpair_combobox_index",
			Qt.QVariant(self.google_translate_panel_langpair_combobox_index))

		self.settings.setValue("history_panel/history_size", Qt.QVariant(self.history_panel_history_size))
		self.settings.setValue("history_panel/history_list", Qt.QVariant(self.history_panel_history_list))
		

	def loadSettings(self) :
		self.common_lang = self.settings.value("common/lang", Qt.QVariant(Qt.QString())).toString()
		if self.common_lang.isEmpty() : pass
		lang = Qt.QLocale().name()
		lang.remove(lang.indexOf("_"), lang.length())
		

#####
class SettingsWindow(Qt.QDialog) :
	def __init__(self, parent = None) :
		Qt.QDialog.__init__(self, parent)

		self.setWindowTitle(self.tr("Settings"))
		self.setWindowIcon(Qt.QIcon(MyIcon))
		self.resize(550, 450)

		self.main_layout = Qt.QVBoxLayout()
		self.main_layout.setSpacing(0)
		self.setLayout(self.main_layout)

		self.section_browser_layout = Qt.QVBoxLayout()
		self.section_browser_layout.setSpacing(0)
		self.main_layout.addLayout(self.section_browser_layout)

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
