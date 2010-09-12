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
import IconsLoader
import TranslateSiteSaxHandler


#####
TranslateSitesSubdir = "trsites/"
TranslateSitesSystemDir = Config.DataRootDir+"/xsl/"+TranslateSitesSubdir


#####
def tr(str) :
	return Qt.QApplication.translate("@default", str)


#####
class TranslateSitesMenu(Qt.QMenu) :
	def __init__(self, title, parent = None) :
		Qt.QMenu.__init__(self, title, parent)

		self.setObjectName("translate_sites_menu")

		#####

		self.actions_data_list = []

		#####

		self.connect(self, Qt.SIGNAL("triggered(QAction *)"), self.openSite)


	### Public ###

	def saveSettings(self) :
		pass

	def loadSettings(self) :
		self.createActions()


	### Private ###

	def createActions(self) :
		translate_sites_file_name_filtes = Qt.QStringList()
		translate_sites_file_name_filtes << "*.trsite" << "*.xml"

		translate_sites_system_dir = Qt.QDir(TranslateSitesSystemDir)
		translate_sites_system_dir.setSorting(Qt.QDir.Name)
		translate_sites_system_dir.setNameFilters(translate_sites_file_name_filtes)
		translate_sites_system_dir.setFilter(Qt.QDir.Files)
		translate_sites_system_dir_entry_list = translate_sites_system_dir.entryList()
		translate_sites_system_dir_entry_list.replaceInStrings(Qt.QRegExp("^(.*)$"), TranslateSitesSystemDir+"\\1")

		translate_sites_user_dir = Qt.QDir(Settings.settingsPath()+"/"+TranslateSitesSubdir)
		translate_sites_user_dir.setSorting(Qt.QDir.Name)
		translate_sites_user_dir.setNameFilters(translate_sites_file_name_filtes)
		translate_sites_user_dir.setFilter(Qt.QDir.Files)
		translate_sites_user_dir_entry_list = translate_sites_user_dir.entryList()
		translate_sites_user_dir_entry_list.replaceInStrings(Qt.QRegExp("^(.*)$"), Settings.settingsPath()+"/"+TranslateSitesSubdir+"\\1")

		translate_sites_files_list = Qt.QStringList()
		translate_sites_files_list << translate_sites_system_dir_entry_list << translate_sites_user_dir_entry_list

		if translate_sites_files_list.count() == 0 :
			self.setEnabled(False)
			return

		count = 0
		while count < translate_sites_files_list.count() :
			translate_site_file = Qt.QFile(translate_sites_files_list[count])
			xml_input_source = Qt.QXmlInputSource(translate_site_file)
			xml_reader = Qt.QXmlSimpleReader()
			xml_handler = TranslateSiteSaxHandler.TranslateSiteSaxHandler(self.addSite)
			xml_reader.setContentHandler(xml_handler)
			xml_reader.setErrorHandler(xml_handler)
			xml_reader.parse(xml_input_source)
			count += 1

	def addSite(self, site_title, site_description, site_icon_name, site_url) :
		if site_title.simplified().isEmpty() or site_url.simplified().isEmpty() :
			return

		action = self.addAction(IconsLoader.icon(site_icon_name, "applications-internet"), site_title)
		action.setStatusTip(site_description)

		self.actions_data_list.append(Qt.QUrl(site_url))
		index = len(self.actions_data_list) - 1
		action.setData(Qt.QVariant(index))

	def openSite(self, action) :
		index = action.data().toInt()[0]
		Qt.QDesktopServices.openUrl(self.actions_data_list[index])

