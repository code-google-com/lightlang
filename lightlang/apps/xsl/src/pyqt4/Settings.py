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

#####
MyIcon = Config.Prefix+"/lib/xsl/icons/xsl_16.png"
IconsDir = Config.Prefix+"/lib/xsl/icons/"

class SLEngineSettingsPage(Qt.QWidget) :
	def __init__(self, parent = None) :
		Qt.QWidget.__init__(self, parent)


	### Public ###

	def apply(self) : pass
	def reset(self) : pass
	def saveSettings(self) : pass
	def loadSettings(self) : pass

#####
class HistorySettingsPage(Qt.QWidget) :
	def __init__(self, parent = None) :
		Qt.QWidget.__init__(self, parent)


	### Public ###

	def apply(self) : pass
	def reset(self) : pass
	def saveSettings(self) : pass
	def loadSettings(self) : pass

#####
class NetworkSettingsPage(Qt.QWidget) :
	def __init__(self, parent = None) :
		Qt.QWidget.__init__(self, parent)

		self.main_layout = Qt.QVBoxLayout()
		self.setLayout(self.main_layout)

		self.http_proxy_type_group = Qt.QGroupBox(self.tr("HTTP-Proxy type"))
		self.http_proxy_type_group_layout = Qt.QVBoxLayout()
		self.http_proxy_type_group.setLayout(self.http_proxy_type_group_layout)
		self.main_layout.addWidget(self.http_proxy_type_group)

		self.http_proxy_settings_layout = Qt.QGridLayout()
		self.main_layout.addLayout(self.http_proxy_settings_layout)

		#####

		self.http_proxy_type_no_proxy_radiobutton = Qt.QRadioButton(self.tr("No proxy"))
		self.http_proxy_type_group_layout.addWidget(self.http_proxy_type_no_proxy_radiobutton)

		self.http_proxy_type_http_proxy = Qt.QRadioButton(self.tr("HTTP proxy"))
		self.http_proxy_type_group_layout.addWidget(self.http_proxy_type_http_proxy)

		self.http_proxy_type_socks5_proxy = Qt.QRadioButton(self.tr("SOCKS5 proxy"))
		self.http_proxy_type_group_layout.addWidget(self.http_proxy_type_socks5_proxy)

		self.http_proxy_server_label = Qt.QLabel(self.tr("Server: "))
		self.http_proxy_settings_layout.addWidget(self.http_proxy_server_label, 0, 0)

		self.http_proxy_server_line_edit = Qt.QLineEdit()
		self.http_proxy_settings_layout.addWidget(self.http_proxy_server_line_edit, 0, 1)

		self.http_proxy_port_label = Qt.QLabel(self.tr("Port:"))
		self.http_proxy_settings_layout.addWidget(self.http_proxy_port_label, 1, 0)

		self.http_proxy_port_spinbox = Qt.QSpinBox()
		self.http_proxy_port_spinbox.setRange(1, 32768)
		self.http_proxy_settings_layout.addWidget(self.http_proxy_port_spinbox, 1, 1)

		self.http_proxy_user_name_label = Qt.QLabel(self.tr("User name:"))
		self.http_proxy_settings_layout.addWidget(self.http_proxy_user_name_label, 2, 0)

		self.http_proxy_user_name_line_edit = Qt.QLineEdit()
		self.http_proxy_settings_layout.addWidget(self.http_proxy_user_name_line_edit, 2, 1)

		self.http_proxy_user_passwd_label = Qt.QLabel(self.tr("Password:"))
		self.http_proxy_settings_layout.addWidget(self.http_proxy_user_passwd_label, 3, 0)

		self.http_proxy_user_passwd_line_edit = Qt.QLineEdit()
		self.http_proxy_user_passwd_line_edit.setEchoMode(Qt.QLineEdit.Password)
		self.http_proxy_settings_layout.addWidget(self.http_proxy_user_passwd_line_edit, 3, 1)

		self.main_layout.addStretch()


	### Public ###

	def apply(self) : pass
	def reset(self) : pass
	def saveSettings(self) : pass
	def loadSettings(self) : pass

#####
class SettingsWindow(Qt.QDialog) :
	def __init__(self, parent = None) :
		Qt.QDialog.__init__(self, parent)

		self.setWindowTitle(self.tr("Settings"))
		self.setWindowIcon(Qt.QIcon(MyIcon))
		self.resize(500, 400)

		self.main_layout = Qt.QHBoxLayout()
		self.main_layout.setMargin(0)
		self.main_layout.setSpacing(0)
		self.setLayout(self.main_layout)

		self.pages_browser_layout = Qt.QVBoxLayout()
		self.pages_browser_layout.setMargin(0)
		self.pages_browser_layout.setSpacing(0)
		self.main_layout.addLayout(self.pages_browser_layout)

		self.controls_layout = Qt.QVBoxLayout()
		self.main_layout.addLayout(self.controls_layout)

		self.pages_stack_layout = Qt.QVBoxLayout()
		self.controls_layout.addLayout(self.pages_stack_layout)

		self.control_buttons_layout = Qt.QHBoxLayout()
		self.control_buttons_layout.setMargin(6)
		self.control_buttons_layout.setSpacing(6)
		self.controls_layout.addLayout(self.control_buttons_layout)

		#####

		self.pages_browser = Qt.QListWidget()
		self.pages_browser.setViewMode(Qt.QListView.IconMode)
		self.pages_browser.setIconSize(Qt.QSize(64, 64))
		self.pages_browser.setMovement(Qt.QListView.Static)
		self.pages_browser.setMaximumWidth(96)
		self.pages_browser.setSpacing(10)
		self.pages_browser_layout.addWidget(self.pages_browser)

		self.pages_stack = Qt.QStackedWidget()
		self.pages_stack_layout.addWidget(self.pages_stack)

		self.control_buttons_layout.addStretch()

		self.cancel_button = Qt.QPushButton(self.tr("Cancel"))
		self.control_buttons_layout.addWidget(self.cancel_button)

		self.ok_button = Qt.QPushButton(self.tr("OK"))
		self.control_buttons_layout.addWidget(self.ok_button)

		#####

		self.sl_engine_settings_page_button = Qt.QListWidgetItem(self.pages_browser)
		self.sl_engine_settings_page_button.setIcon(Qt.QIcon(IconsDir+"sl_engine_64.png"))
		self.sl_engine_settings_page_button.setText(self.tr("SL Engine"))
		self.sl_engine_settings_page_button.setTextAlignment(Qt.Qt.AlignHCenter)
		self.sl_engine_settings_page_button.setFlags(Qt.Qt.ItemIsSelectable|Qt.Qt.ItemIsEnabled)
		self.sl_engine_settings_page = SLEngineSettingsPage()
		self.pages_stack.addWidget(self.sl_engine_settings_page)

		self.history_settings_page_button = Qt.QListWidgetItem(self.pages_browser)
		self.history_settings_page_button.setIcon(Qt.QIcon(IconsDir+"history_64.png"))
		self.history_settings_page_button.setText(self.tr("History"))
		self.history_settings_page_button.setTextAlignment(Qt.Qt.AlignHCenter)
		self.history_settings_page_button.setFlags(Qt.Qt.ItemIsSelectable|Qt.Qt.ItemIsEnabled)
		self.history_settings_page = HistorySettingsPage()
		self.pages_stack.addWidget(self.history_settings_page)

		self.network_settings_page_button = Qt.QListWidgetItem(self.pages_browser)
		self.network_settings_page_button.setIcon(Qt.QIcon(IconsDir+"network_settings_64.png"))
		self.network_settings_page_button.setText(self.tr("Network"))
		self.network_settings_page_button.setTextAlignment(Qt.Qt.AlignHCenter)
		self.network_settings_page_button.setFlags(Qt.Qt.ItemIsSelectable|Qt.Qt.ItemIsEnabled)
		self.network_settings_page = NetworkSettingsPage()
		self.pages_stack.addWidget(self.network_settings_page)

		#####

		self.connect(self.pages_browser, Qt.SIGNAL("currentItemChanged(QListWidgetItem *, QListWidgetItem *)"),
			self.changePage)

		self.connect(self.cancel_button, Qt.SIGNAL("clicked()"), self.sl_engine_settings_page.reset)
		self.connect(self.cancel_button, Qt.SIGNAL("clicked()"), self.history_settings_page.reset)
		self.connect(self.cancel_button, Qt.SIGNAL("clicked()"), self.network_settings_page.reset)
		self.connect(self.cancel_button, Qt.SIGNAL("clicked()"), self.reject)

		self.connect(self.ok_button, Qt.SIGNAL("clicked()"), self.sl_engine_settings_page.apply)
		self.connect(self.ok_button, Qt.SIGNAL("clicked()"), self.history_settings_page.apply)
		self.connect(self.ok_button, Qt.SIGNAL("clicked()"), self.network_settings_page.apply)
		self.connect(self.ok_button, Qt.SIGNAL("clicked()"), self.settingsChangedSignal)
		self.connect(self.ok_button, Qt.SIGNAL("clicked()"), self.accept)


	### Public ###

	def saveSettings(self) :
		self.sl_engine_settings_page.saveSettings()
		self.history_settings_page.saveSettings()
		self.network_settings_page.saveSettings()

	def loadSettings(self) :
		self.sl_engine_settings_page.loadSettings()
		self.history_settings_page.loadSettings()
		self.network_settings_page.loadSettings()

	###

	def show(self) :
		self.sl_engine_settings_page.reset()
		self.history_settings_page.reset()
		self.network_settings_page.reset()

		Qt.QWidget.show(self)

	### Private ###

	def changePage(self, current, previous) :
		if current == None :
			current = previous

		self.pages_stack.setCurrentIndex(self.pages_browser.row(current))


	### Signals ###

	def settingsChangedSignal(self) :
		self.emit(Qt.SIGNAL("settingsChanged()"))
