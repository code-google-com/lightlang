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
import sys
import Config
import Const
import IFASAXHandler

#####
IFADir = Config.Prefix+"/lib/xsl/ifa/"
IconsDir = Config.Prefix+"/lib/xsl/icons/"

#####
def tr(str) :
	return Qt.QApplication.translate("@default", str)

#####
class IFAMenu(Qt.QMenu) :
	def __init__(self, title, parent=None) :
		Qt.QMenu.__init__(self, title, parent)

		self.actions_data_list = []

		self.createActions()

		#####

		self.connect(self, Qt.SIGNAL("triggered(QAction *)"), self.launchApp)


	### Private ###

	def createActions(self) :
		ifa_dir = Qt.QDir(IFADir)
		ifa_dir_name_filters = Qt.QStringList()
		ifa_dir_name_filters << "*.ifa" << "*.xml"
		ifa_dir.setNameFilters(ifa_dir_name_filters)
		ifa_dir.setFilter(Qt.QDir.Files)

		count = 0
		while count < ifa_dir.count() :
			ifa_file = Qt.QFile(IFADir+ifa_dir[count])
			xml_input_source = Qt.QXmlInputSource(ifa_file)
			xml_reader = Qt.QXmlSimpleReader()
			xml_handler = IFASAXHandler.IFASAXHandler(self.addApp)
			xml_reader.setContentHandler(xml_handler)
			xml_reader.setErrorHandler(xml_handler)
			xml_reader.parse(xml_input_source)
			count += 1

	def addApp(self, app_title, app_description, app_icon_path, app_prog_path,
		app_prog_options, python_precode, python_postcode) :

		if app_title.simplified().isEmpty() or app_prog_path.simplified().isEmpty() :
			return

		if app_icon_path.simplified().isEmpty() :
			app_icon_path = IconsDir+"exec_16.png"
		elif not Qt.QFile.exists(app_icon_path) :
			app_icon_path = IconsDir+"exec_16.png"

		action = self.addAction(Qt.QIcon(app_icon_path), app_title)
		action.setStatusTip(app_description)

		self.actions_data_list.append([])
		index = len(self.actions_data_list) -1
		self.actions_data_list[index] = [
			Qt.QString(app_prog_path), Qt.QString(app_prog_options), Qt.QProcess(),
			Qt.QString(python_precode), Qt.QString(python_postcode),
			lambda : self.execPrecode(index), lambda : self.execPostcode(index)]

		action.setData(Qt.QVariant(index))

		if not Qt.QFile.exists(app_prog_path) :
			action.setEnabled(False)

		#####

		self.connect(self.actions_data_list[index][2], Qt.SIGNAL("finished(int, QProcess::ExitStatus)"),
			self.actions_data_list[index][6])

	def launchApp(self, action) :
		index = action.data().toInt()[0]
		app_prog_path = self.actions_data_list[index][0]
		app_prog_options = self.actions_data_list[index][1]
		proc = self.actions_data_list[index][2]

		#####

		if proc.state() == Qt.QProcess.Starting or proc.state() == Qt.QProcess.Running :
			Qt.QMessageBox.information(None, tr("IFA"),
				tr("This applications is already running"))
			return

		self.actions_data_list[index][5]()

		proc.start(app_prog_path+" "+app_prog_options)

	def execPrecode(self, index) :
		from Global import main
		instructions = self.actions_data_list[index][3].split("\n", Qt.QString.SkipEmptyParts)
		count = 0
		while count < instructions.count() :
			instruction = instructions[count].trimmed()
			if not instruction.simplified().isEmpty() :
				try :
					exec str(instruction)
				except :
					print >> sys.stderr, Const.MyName+": [exec] IFA exception: ignored"
			count += 1

	def execPostcode(self, index) :
		from Global import main
		instructions = self.actions_data_list[index][4].split("\n", Qt.QString.SkipEmptyParts)
		count = 0
		while count < instructions.count() :
			instruction = instructions[count].trimmed()
			if not instruction.simplified().isEmpty() :
				try :
					exec str(instruction)
				except :
					print >> sys.stderr, Const.MyName+": [exec] IFA exception: ignored"
			count += 1

