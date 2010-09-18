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
import Settings
import sys
import os


##### Private constants #####
ProcDir = "/proc/"
LockFilePostfix = ".lock"


##### Public methods #####
def test() :
	lock_file_path = Settings.settingsPath()+"/"+Qt.QString(Const.MyName).toLower()+LockFilePostfix
	lock_file = Qt.QFile(lock_file_path)
	lock_file_stream = Qt.QTextStream(lock_file)

	if not lock_file.exists() :
		if not lock_file.open(Qt.QIODevice.WriteOnly|Qt.QIODevice.Truncate) :
			print >> sys.stderr, Const.MyName+": cannot create lock file: ignored"
			return
		lock_file.close()

	if not lock_file.open(Qt.QIODevice.ReadOnly) :
		print >> sys.stderr, Const.MyName+": cannot open lock file: ignored"
		return

	old_pid = Qt.QString(lock_file_stream.readLine())
	if old_pid.length() and Qt.QDir(ProcDir+old_pid).exists() and not Qt.QApplication.instance().isSessionRestored() :
		Qt.QMessageBox.warning(None, Const.MyName,
			tr("Oops, %1 process is already running, kill old process and try again.\n"
				"If not, remove lock file \"%2\"").arg(Const.MyName).arg(lock_file_path))
		lock_file.close()
		sys.exit(1)
		return

	lock_file.close()

	lock_file.open(Qt.QIODevice.WriteOnly|Qt.QIODevice.Truncate)
	lock_file_stream << os.getpid() << "\n";
	lock_file.close()

