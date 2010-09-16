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


#####
Sl = Config.BinsDir+"/sl"
AllSoundsDir = Config.DataRootDir+"/sl/sounds/"
AudioPostfix = ".ogg"

SoundSearchOption = "-s"


#####
class SlSoundSearch(Qt.QObject) :
	def __init__(self, parent = None) :
		Qt.QObject.__init__(self, parent)

		#####

		self._proc = Qt.QProcess()

		self._proc_block_flag = False
		self._proc_kill_flag = False

		self._proc_args = Qt.QStringList()

		self._all_sounds_dir = Qt.QDir(AllSoundsDir)

		#####

		self.connect(self._proc, Qt.SIGNAL("error(QProcess::ProcessError)"), self.processError)
		self.connect(self._proc, Qt.SIGNAL("finished(int, QProcess::ExitStatus)"), self.processFinished)
		self.connect(self._proc, Qt.SIGNAL("stateChanged(QProcess::ProcessState)"), self.processStateChenged)


	### Public ###

	def find(self, word) :
		word = word.simplified().toLower()
		if word.isEmpty() :
			return

		if self._proc.state() in (Qt.QProcess.Starting, Qt.QProcess.Running) :
			self._proc_kill_flag = True
			self._proc.kill()

		self._proc_args.clear()
		self._proc_args << SoundSearchOption << word

		while self._proc_block_flag :
			self._proc.waitForFinished()
		self._proc_kill_flag = False
		self._proc.start(Sl, self._proc_args)

	def checkWord(self, lang, word) :
		word = word.simplified().toLower()
		if word.isEmpty() :
			return

		return Qt.QFile.exists(AllSoundsDir+lang+"/"+word[0]+"/"+word+AudioPostfix)


	### Private ###

	def processError(self, error_code) :
		if error_code == Qt.QProcess.FailedToStart and not self._proc_kill_flag :
			Qt.QMessageBox.warning(None, Const.MyName,
				tr("An error occured when creating the search process"),
				Qt.QMessageBox.Yes)
		elif error_code == Qt.QProcess.Crashed and not self._proc_kill_flag :
			Qt.QMessageBox.warning(None, Const.MyName,
				tr("Error of the search process"),
				Qt.QMessageBox.Yes)
		elif error_code == Qt.QProcess.Timedout and not self._proc_kill_flag :
			Qt.QMessageBox.warning(None, Const.MyName,
				tr("Connection lost with search process"),
				Qt.QMessageBox.Yes)
		elif not self._proc_kill_flag :
			Qt.QMessageBox.warning(None, Const.MyName,
				tr("Unknown error occured while executing the search process"),
				Qt.QMessageBox.Yes)

	def processFinished(self, exit_code) :
		if exit_code and not self._proc_kill_flag :
			Qt.QMessageBox.warning(None, Const.MyName,
				tr("Error of the search process"),
				Qt.QMessageBox.Yes)

	def processStateChenged(self, state) :
		self._proc_block_flag = ( state in (Qt.QProcess.Starting, Qt.QProcess.Running) )

