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

#####
IFADir = Config.Prefix+"/lib/xsl/ifa/"
IconsDir = Config.Prefix+"/lib/xsl/icons/"

#####
class IFASAXHandler(Qt.QXmlDefaultHandler) :
	def __init__(self, new_app_handler) :
		Qt.QXmlDefaultHandler.__init__(self)

		self.new_app_handler = new_app_handler

		#####

		self.lang = Qt.QLocale().name()
		self.lang.remove(self.lang.indexOf("_"), self.lang.length())

		#####

		self.app_tag_flag = False
		self.title_tag_flag = False
		self.description_tag_flag = False
		self.icon_tag_flag = False
		self.path_tag_flag = False
		self.options_tag_flag = False
		self.precode_tag_flag = False
		self.postcode_tag_flag = False

		self.app_title = Qt.QString()
		self.app_title_lang = Qt.QString()
		self.app_description = Qt.QString()
		self.app_description_lang = Qt.QString()
		self.app_icon_path = Qt.QString()
		self.app_prog_path = Qt.QString()
		self.app_prog_options = Qt.QString()
		self.python_precode = Qt.QString()
		self.python_postcode = Qt.QString()


	### Private ###
	### Handlers ###
	def startElement(self, namespace_uri, local_name, name, attributes) :
		if name == "app" :
			self.app_tag_flag = True
			return True

		if self.app_tag_flag :
			if name == "title" :
				self.app_title_lang = attributes.value("lang")
				self.title_tag_flag = True
			elif name == "description" :
				self.app_description_lang = attributes.value("lang")
				self.description_tag_flag = True
			elif name == "icon" :
				self.icon_tag_flag = True
			elif name == "path" :
				self.path_tag_flag = True
			elif name == "options" :
				self.options_tag_flag = True
			elif name == "precode" and attributes.value("lang") == "python" :
				self.precode_tag_flag = True
			elif name == "postcode" and attributes.value("lang") == "python" :
				self.postcode_tag_flag = True
		return True

	def characters(self, str) :
		if str.simplified().isEmpty() :
			return True

		if self.app_tag_flag :
			if self.title_tag_flag :
				if self.app_title_lang == self.lang :
					self.app_title = str.simplified()
				if self.app_title.simplified().isEmpty() and self.app_title_lang.simplified().isEmpty() :
					self.app_title = str.simplified()
				return True
			elif self.description_tag_flag :
				if self.app_description_lang == self.lang :
					self.app_description = str.simplified()
				if self.app_description.simplified().isEmpty() and self.app_description_lang.simplified().isEmpty() :
					self.app_description = str.simplified()
				return True
			elif self.icon_tag_flag :
				self.app_icon_path = str.simplified()
				return True
			elif self.path_tag_flag :
				self.app_prog_path = str.simplified()
				return True
			elif self.options_tag_flag :
				self.app_prog_options = str.simplified()
				return True
			elif self.precode_tag_flag :
				self.python_precode = str.trimmed()
				return True
			elif self.postcode_tag_flag :
				self.python_postcode = str.trimmed()
				return True
		return True

	def endElement(self, namespace_uri, local_name, name) :
		if name == "app" :
			self.new_app_handler(self.app_title, self.app_description,
				self.app_icon_path, self.app_prog_path, self.app_prog_options,
				self.python_precode, self.python_postcode)

			self.app_title.clear()
			self.app_title_lang.clear()
			self.app_description.clear()
			self.app_description_lang.clear()
			self.app_icon_path.clear()
			self.app_prog_path.clear()
			self.app_prog_options.clear()
			self.python_precode.clear()
			self.python_postcode.clear()

			self.app_tag_flag = False
		elif name == "title" :
			self.title_tag_flag = False
		elif name == "description" :
			self.description_tag_flag = False
		elif name == "icon" :
			self.icon_tag_flag = False
		elif name == "path" :
			self.path_tag_flag = False
		elif name == "options" :
			self.options_tag_flag = False
		elif name == "precode" :
			self.precode_tag_flag = False
		elif name == "postcode" :
			self.postcode_tag_flag = False
		return True

	def fatalError(self, exception) :
		return True


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
			Qt.QCoreApplication.processEvents()
			ifa_file = Qt.QFile(IFADir+ifa_dir[count])
			xml_input_source = Qt.QXmlInputSource(ifa_file)
			xml_reader = Qt.QXmlSimpleReader()
			xml_handler = IFASAXHandler(self.addApp)
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
			Qt.QMessageBox.information(None, self.tr("IFA"),
				self.tr("This applications is already running"))
			return

		self.actions_data_list[index][5]()

		proc.start(app_prog_path+" "+app_prog_options)

	def execPrecode(self, index) :
		from Global import main
		instructions = self.actions_data_list[index][3].split("\n")
		count = 0
		while count < instructions.count() :
			Qt.QCoreApplication.processEvents()
			instruction = instructions[count].trimmed()
			if not instruction.simplified().isEmpty() :
				try :
					exec str(instruction)
				except :
					print >> sys.stderr, Const.MyName+": [exec] IFA exception: ignored"
			count += 1

	def execPostcode(self, index) :
		from Global import main
		instructions = self.actions_data_list[index][4].split("\n")
		count = 0
		while count < instructions.count() :
			Qt.QCoreApplication.processEvents()
			instruction = instructions[count].trimmed()
			if not instruction.simplified().isEmpty() :
				try :
					exec str(instruction)
				except :
					print >> sys.stderr, Const.MyName+": [exec] IFA exception: ignored"
			count += 1
