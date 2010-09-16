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
import Config
import Const
import Settings
import IconsLoader
import IfaSaxHandler


#####
IfaSubdir = "ifa/"
IfaSystemDir = Config.DataRootDir+"/xsl/"+IfaSubdir


#####
class IfaMenu(Qt.QMenu) :
	def __init__(self, title, parent = None) :
		Qt.QMenu.__init__(self, title, parent)

		self.setObjectName("ifa_menu")

		#####

		self._actions_data_list = []

		#####

		self.connect(self, Qt.SIGNAL("triggered(QAction *)"), self.launchApp)


	### Public ###

	def saveSettings(self) :
		pass

	def loadSettings(self) :
		self.createActions()


	### Private ###

	def createActions(self) :
		ifa_file_name_filtes = Qt.QStringList()
		ifa_file_name_filtes << "*.ifa" << "*.xml"

		ifa_system_dir = Qt.QDir(IfaSystemDir)
		ifa_system_dir.setSorting(Qt.QDir.Name)
		ifa_system_dir.setNameFilters(ifa_file_name_filtes)
		ifa_system_dir.setFilter(Qt.QDir.Files)
		ifa_system_dir_entry_list = ifa_system_dir.entryList()
		ifa_system_dir_entry_list.replaceInStrings(Qt.QRegExp("^(.*)$"), IfaSystemDir+"\\1")

		ifa_user_dir = Qt.QDir(Settings.settingsPath()+"/"+IfaSubdir)
		ifa_user_dir.setSorting(Qt.QDir.Name)
		ifa_user_dir.setNameFilters(ifa_file_name_filtes)
		ifa_user_dir.setFilter(Qt.QDir.Files)
		ifa_user_dir_entry_list = ifa_user_dir.entryList()
		ifa_user_dir_entry_list.replaceInStrings(Qt.QRegExp("^(.*)$"), Settings.settingsPath()+"/"+IfaSubdir+"\\1")

		ifa_files_list = Qt.QStringList()
		ifa_files_list << ifa_system_dir_entry_list << ifa_user_dir_entry_list

		if ifa_files_list.count() == 0 :
			self.setEnabled(False)
			return

		count = 0
		while count < ifa_files_list.count() :
			ifa_file = Qt.QFile(ifa_files_list[count])
			xml_input_source = Qt.QXmlInputSource(ifa_file)
			xml_reader = Qt.QXmlSimpleReader()
			xml_handler = IfaSaxHandler.IfaSaxHandler(self.addApp)
			xml_reader.setContentHandler(xml_handler)
			xml_reader.setErrorHandler(xml_handler)
			xml_reader.parse(xml_input_source)
			count += 1

	def addApp(self, app_title, app_description, app_icon_name, app_prog_path,
		app_prog_options, python_precode, python_postcode) :

		if app_title.simplified().isEmpty() or app_prog_path.simplified().isEmpty() :
			return

		action = self.addAction(IconsLoader.icon(app_icon_name, "system-run"), app_title)
		action.setStatusTip(app_description)

		index = len(self._actions_data_list)
		self._actions_data_list.append({
				"path" : Qt.QString(app_prog_path),
				"options" : Qt.QString(app_prog_options),
				"process" : Qt.QProcess(),
				"python_precode" : Qt.QString(python_precode),
				"python_postcode" : Qt.QString(python_postcode),
				"exec_precode" : ( lambda : self.execPrecode(index) ),
				"exec_postcode" : ( lambda : self.execPostcode(index) )
			})

		action.setData(Qt.QVariant(index))

		if not Qt.QFile.exists(app_prog_path) :
			action.setEnabled(False)

		###

		self.connect(self._actions_data_list[index]["process"], Qt.SIGNAL("finished(int, QProcess::ExitStatus)"),
			self._actions_data_list[index]["exec_postcode"])

	def launchApp(self, action) :
		index = action.data().toInt()[0]

		if ( self._actions_data_list[index]["process"].state() == Qt.QProcess.Starting or
			self._actions_data_list[index]["process"].state() == Qt.QProcess.Running ) :
			Qt.QMessageBox.information(None, tr("IFA"),
				tr("This applications is already running"))
			return

		self._actions_data_list[index]["exec_precode"]()

		self._actions_data_list[index]["process"].start(self._actions_data_list[index]["path"]+" "+self._actions_data_list[index]["options"])

	def execPrecode(self, index) :
		from Main import MainObject as main
		instructions = self._actions_data_list[index]["python_precode"].split("\n", Qt.QString.SkipEmptyParts)
		count = 0
		while count < instructions.count() :
			instruction = instructions[count].trimmed()
			if not instruction.simplified().isEmpty() :
				try :
					exec str(instruction)
				except Exception, err1 :
					print >> sys.stderr, Const.MyName+": IFA instruction \""+str(instruction)+"\": "+str(err1)
			count += 1

	def execPostcode(self, index) :
		from Main import MainObject as main
		instructions = self._actions_data_list[index]["python_postcode"].split("\n", Qt.QString.SkipEmptyParts)
		count = 0
		while count < instructions.count() :
			instruction = instructions[count].trimmed()
			if not instruction.simplified().isEmpty() :
				try :
					exec str(instruction)
				except Exception, err1 :
					print >> sys.stderr, Const.MyName+": IFA instruction \""+str(instruction)+"\": "+str(err1)
			count += 1

