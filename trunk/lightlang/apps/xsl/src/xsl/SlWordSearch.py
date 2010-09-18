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


##### Private constants #####
Sl = Config.BinsDir+"/sl"
AllDictsDir = Config.DataRootDir+"/sl/dicts/"

UsuallySearchOption = "-u"
WordCombinationsSearchOption = "-c"
ListSearchOption = "-l"
IllDefinedSearchOption = "-i"


##### Public classes #####
class SlWordSearch(Qt.QObject) :
	def __init__(self, parent = None) :
		Qt.QObject.__init__(self, parent)

		#####

		self._proc = Qt.QProcess()
		self._proc.setReadChannelMode(Qt.QProcess.MergedChannels)
		self._proc.setReadChannel(Qt.QProcess.StandardOutput)

		self._proc_block_flag = False
		self._proc_kill_flag = False

		self._proc_args = Qt.QStringList()

		self._proc_output = Qt.QByteArray()

		self._dicts_list = Qt.QStringList()

		###

		self._info_item_regexp = Qt.QRegExp("<font class=\"info_font\">(.*)</font>")
		self._info_item_regexp.setMinimal(True)

		self._caption_item_regexp = Qt.QRegExp("<font class=\"dict_header_font\">(.*)</font>")
		self._caption_item_regexp.setMinimal(True)

		self._word_item_regexp = Qt.QRegExp("<a href=.*>(.*)</a>")
		self._word_item_regexp.setMinimal(True)

		#####

		self._replaces_dict = {
			"<font class=\"info_font\">This word is not found</font>" : tr("<font class=\"info_font\">This word is not found</font>"),
			"<font class=\"info_font\">No dict is connected</font>" : tr("<font class=\"info_font\">No dict is connected</font>")
		}

		#####

		self.connect(self._proc, Qt.SIGNAL("error(QProcess::ProcessError)"), self.processError)
		self.connect(self._proc, Qt.SIGNAL("finished(int, QProcess::ExitStatus)"), self.processFinished)
		self.connect(self._proc, Qt.SIGNAL("stateChanged(QProcess::ProcessState)"), self.processStateChenged)
		self.connect(self._proc, Qt.SIGNAL("readyReadStandardOutput()"), self.setText)


	### Public ###

	def uFind(self, word) :
		self.find(word, UsuallySearchOption)

	def cFind(self, word) :
		self.find(word, WordCombinationsSearchOption)

	def lFind(self, word) :
		self.find(word, ListSearchOption)

	def iFind(self, word) :
		self.find(word, IllDefinedSearchOption)

	def setDictsList(self, dicts_list) :
		self._dicts_list = dicts_list


	### Private ###

	def find(self, word, option) :
		word = word.simplified().toLower()
		if word.isEmpty() :
			return

		if self._proc.state() in (Qt.QProcess.Starting, Qt.QProcess.Running) :
			self.setText()
			self._proc_kill_flag = True
			self._proc.kill()

		self.processStartedSignal()

		self.clearRequestSignal()

		self._proc_output.clear()

		self._proc_args.clear()
		self._proc_args << "--output-format=html" << "--use-css=no" << "--use-list="+self._dicts_list.join("|") << option << word

		while self._proc_block_flag :
			self._proc.waitForFinished()
		self._proc_kill_flag = False
		self._proc.start(Sl, self._proc_args)

	###

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
		elif error_code == Qt.QProcess.WriteError and not self._proc_kill_flag :
			Qt.QMessageBox.warning(None, Const.MyName,
				tr("Error while writing data into the search process"),
				Qt.QMessageBox.Yes)
		elif error_code == Qt.QProcess.ReadError and not self._proc_kill_flag :
			Qt.QMessageBox.warning(None, Const.MyName,
				tr("Error while reading data from the search process"),
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
		self.processFinishedSignal()

	def processStateChenged(self, state) :
		self._proc_block_flag = ( state in (Qt.QProcess.Starting, Qt.QProcess.Running) )

	def setText(self) :
		self._proc_output.append(self._proc.readAllStandardOutput())

		text = Qt.QString.fromLocal8Bit(str(self._proc_output))

		for replaces_dict_key in self._replaces_dict.keys() :
			text.replace(replaces_dict_key, self._replaces_dict[replaces_dict_key])

		if self._proc_args[3] in (UsuallySearchOption, WordCombinationsSearchOption) :
			self.textChangedSignal(text)
		else :
			list = Qt.QStringList()

			parts_list = text.split("<table border=\"0\" width=\"100%\">")

			#####

			if parts_list.count() == 1 :
				info_item_pos = self._info_item_regexp.indexIn(text, 0)
				while info_item_pos != -1 :
					list << "{{"+self._info_item_regexp.cap(1)+"}}"
					info_item_pos = self._info_item_regexp.indexIn(text, info_item_pos +
						self._info_item_regexp.matchedLength())

				if list.count() == 0 :
					list << "{{"+text+"}}"

			###

			parts_list_count = 1
			while parts_list_count < parts_list.count() :
				if self._caption_item_regexp.indexIn(parts_list[parts_list_count]) < 0 :
					parts_list_count += 1
					continue

				list << "[["+self._caption_item_regexp.cap(1)+"]]"

				word_item_pos = self._word_item_regexp.indexIn(parts_list[parts_list_count], 0)
				while word_item_pos != -1 :
					list << self._word_item_regexp.cap(1)
					word_item_pos = self._word_item_regexp.indexIn(parts_list[parts_list_count], word_item_pos +
						self._word_item_regexp.matchedLength())

				parts_list_count += 1

			#####

			self.listChangedSignal(list)


	### Signals ###

	def processStartedSignal(self) :
		self.emit(Qt.SIGNAL("processStarted()"))

	def processFinishedSignal(self) :
		self.emit(Qt.SIGNAL("processFinished()"))

	def clearRequestSignal(self) :
		self.emit(Qt.SIGNAL("clearRequest()"))

	def textChangedSignal(self, text) :
		self.emit(Qt.SIGNAL("textChanged(const QString &)"), text)

	def listChangedSignal(self, list) :
		self.emit(Qt.SIGNAL("listChanged(const QStringList &)"), list)

