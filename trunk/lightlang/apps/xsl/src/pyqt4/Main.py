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
import sys
import os
import Config
import Const
import Locale
import TrayIcon
import MainWindow


#####
TrDir = Config.Prefix+"/lib/xsl/tr/"
MySplash = Config.Prefix+"/lib/xsl/pictures/xsl_splash.png"


#####
MainObject = None


#####
def tr(str) :
	return Qt.QApplication.translate("@default", str)


#####
class Main :
	def __init__(self, argv) :
		self.argv = argv


	### Public ###

	def run(self) :
		self.app = Qt.QApplication(self.argv)
		self.app.setQuitOnLastWindowClosed(False)

		self.lang = Locale.mainLang()

		self.translator = Qt.QTranslator()
		self.translator.load(TrDir+self.lang)
		self.app.installTranslator(self.translator)

		self.checkLockFile()

		#####

		self.splash_pixmap = Qt.QPixmap(MySplash)
		self.splash = Qt.QSplashScreen(self.splash_pixmap)
		if not self.app.isSessionRestored() :
			self.splash.show()

		self.app.processEvents()

		self.main_window = MainWindow.MainWindow()
		self.tray_icon = TrayIcon.TrayIcon()

		#####

		Qt.QObject.connect(self.app, Qt.SIGNAL("commitDataRequest(QSessionManager &)"), self.commitData)
		Qt.QObject.connect(self.app, Qt.SIGNAL("focusChanged(QWidget *, QWidget*)"), self.main_window.focusChanged)

		Qt.QObject.connect(self.main_window, Qt.SIGNAL("spyStarted()"), self.tray_icon.spyStarted)
		Qt.QObject.connect(self.main_window, Qt.SIGNAL("spyStopped()"), self.tray_icon.spyStopped)

		Qt.QObject.connect(self.tray_icon, Qt.SIGNAL("startSpyRequest()"), self.main_window.startSpy)
		Qt.QObject.connect(self.tray_icon, Qt.SIGNAL("stopSpyRequest()"), self.main_window.stopSpy)
		Qt.QObject.connect(self.tray_icon, Qt.SIGNAL("visibleChangeRequest()"), self.main_window.visibleChange)
		Qt.QObject.connect(self.tray_icon, Qt.SIGNAL("exitRequest()"), self.main_window.exit)

		#####

		self.main_window.load()
		self.tray_icon.show()

		self.splash.finish(self.main_window)

		#####

		global MainObject
		MainObject = self

		#####

		self.app.exec_()


	### Private ###

	def checkLockFile(self) :
		lock_file_name = Qt.QDir.tempPath()+"/"+Qt.QString(Const.MyName).toLower()+".lock"
		lock_file = Qt.QFile(lock_file_name)
		lock_file_stream = Qt.QTextStream(lock_file)

		if not lock_file.exists() :
			if not lock_file.open(Qt.QIODevice.WriteOnly) :
				print >> sys.stderr, Const.MyName+": cannot create lock file: ignored"
				return
			lock_file.close()

		if not lock_file.open(Qt.QIODevice.ReadOnly) :
			print >> sys.stderr, Const.MyName+": cannot open lock file: ignored"
			return

		old_pid = Qt.QString(lock_file_stream.readLine())
		if old_pid.length() and Qt.QDir("/proc/"+old_pid).exists() and not self.app.isSessionRestored() :
			Qt.QMessageBox.warning(None, Const.MyName,
				tr("%1 process is already running, kill old process and try again.\n"
					"If not, remove lock file \"%2\"").arg(Const.MyName).arg(lock_file_name))
			lock_file.close()
			sys.exit(1)

		lock_file.close()

		lock_file.open(Qt.QIODevice.WriteOnly|Qt.QIODevice.Truncate)
		lock_file_stream << os.getpid() << "\n";
		lock_file.close()

	###

	def commitData(self, session_manager) :
		if session_manager.allowsInteraction() :
			self.main_window.save()
			session_manager.setRestartHint(Qt.QSessionManager.RestartIfRunning)
		else :
			print >> sys.stderr, Const.MyName+": cannot save session: ignored"

