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
import StartupLock
import UserStyleCss
import MainApplication
import TrayIcon
import MainWindow


#####
TrDir = Config.DataRootDir+"/xsl/tr/"
MySplash = Config.DataRootDir+"/xsl/pictures/xsl_splash.png"


#####
MainObject = None


#####
def tr(str) :
	return Qt.QApplication.translate("@default", str)


#####
class Main :
	def __init__(self, argv, no_splash_flag = False, no_tray_icon = False) :
		self.argv = argv
		self.no_splash_flag = no_splash_flag
		self.no_tray_icon = no_tray_icon


	### Public ###

	def run(self) :
		self.app = MainApplication.MainApplication(self.argv)
		self.app.setQuitOnLastWindowClosed(self.no_tray_icon)

		self.translator = Qt.QTranslator()
		self.translator.load(TrDir+Locale.mainLang())
		self.app.installTranslator(self.translator)

		self.app.setStyleSheet(UserStyleCss.userStyleCss())

		StartupLock.test()

		#####

		if not self.no_splash_flag :
			self.splash_pixmap = Qt.QPixmap(MySplash)
			self.splash = Qt.QSplashScreen(self.splash_pixmap)
			if not self.app.isSessionRestored() :
				self.splash.show()

		self.app.processEvents()

		self.main_window = MainWindow.MainWindow()
		self.tray_icon = TrayIcon.TrayIcon()

		#####

		Qt.QObject.connect(self.app, Qt.SIGNAL("focusChanged(QWidget *, QWidget*)"), self.main_window.focusChanged)
		Qt.QObject.connect(self.app, Qt.SIGNAL("saveSettingsRequest()"), self.main_window.save)

		Qt.QObject.connect(self.main_window, Qt.SIGNAL("spyStarted()"), self.tray_icon.spyStarted)
		Qt.QObject.connect(self.main_window, Qt.SIGNAL("spyStopped()"), self.tray_icon.spyStopped)

		Qt.QObject.connect(self.tray_icon, Qt.SIGNAL("startSpyRequest()"), self.main_window.startSpy)
		Qt.QObject.connect(self.tray_icon, Qt.SIGNAL("stopSpyRequest()"), self.main_window.stopSpy)
		Qt.QObject.connect(self.tray_icon, Qt.SIGNAL("visibleChangeRequest()"), self.main_window.visibleChange)
		Qt.QObject.connect(self.tray_icon, Qt.SIGNAL("exitRequest()"), self.main_window.exit)

		#####

		self.main_window.load()
		if not self.no_tray_icon :
			self.tray_icon.show()

		if not self.no_splash_flag :
			self.splash.finish(self.main_window)

		#####

		global MainObject
		MainObject = self

		#####

		self.app.exec_()

