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

import sys
import Qt
import Config
import Const


#####
def tr(str) :
	return Qt.QApplication.translate("@default", str)


#####
class MainApplication(Qt.QApplication) :
	def __init__(self, argv) :
		Qt.QApplication.__init__(self, argv)


	### Private ###

	def commitData(self, session_manager) :
		if session_manager.allowsInteraction() :
			self.saveSettingsRequestSignal()
			session_manager.setRestartHint(Qt.QSessionManager.RestartIfRunning)
			session_manager.release()
		else :
			print >> sys.stderr, Const.MyName+": cannot save session: ignored"


	### Signals ###

	def saveSettingsRequestSignal(self) :
		self.emit(Qt.SIGNAL("saveSettingsRequest()"))

