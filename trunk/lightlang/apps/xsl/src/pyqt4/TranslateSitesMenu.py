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
import Config
import Const
import TranslateSiteSAXHandler

#####
TranslateSitesDir = Config.Prefix+"/lib/xsl/trsites/"
IconsDir = Config.Prefix+"/lib/xsl/icons/"

#####
class TranslateSitesMenu(Qt.QMenu) :
	def __init__(self, title, parent = None) :
		Qt.QMenu.__init__(self, title, parent)

		self.actions_data_list = []

		self.createActions()

		#####

		self.connect(self, Qt.SIGNAL("triggered(QAction *)"), self.openSite)


	### Private ###

	def createActions(self) :
		translate_sites_dir = Qt.QDir(TranslateSitesDir)
		translate_sites_dir_name_filters = Qt.QStringList()
		translate_sites_dir_name_filters << "*.trsite" << "*.xml"
		translate_sites_dir.setNameFilters(translate_sites_dir_name_filters)
		translate_sites_dir.setFilter(Qt.QDir.Files)

		count = 0
		while count < translate_sites_dir.count() :
			trsite_file = Qt.QFile(TranslateSitesDir+translate_sites_dir[count])
			xml_input_source = Qt.QXmlInputSource(trsite_file)
			xml_reader = Qt.QXmlSimpleReader()
			xml_handler = TranslateSiteSAXHandler.TranslateSiteSAXHandler(self.addSite)
			xml_reader.setContentHandler(xml_handler)
			xml_reader.setErrorHandler(xml_handler)
			xml_reader.parse(xml_input_source)
			count += 1

	def addSite(self, site_title, site_description, site_icon_path, site_url) :
		if site_title.simplified().isEmpty() or site_url.simplified().isEmpty() :
			return

		if site_icon_path.simplified().isEmpty() :
			site_icon_path = IconsDir+"web_16.png"
		elif not Qt.QFile.exists(site_icon_path) :
			site_icon_path = IconsDir+"web_16.png"

		action = self.addAction(Qt.QIcon(site_icon_path), site_title)
		action.setStatusTip(site_description)

		self.actions_data_list.append(Qt.QString(site_url))
		index = len(self.actions_data_list) -1
		action.setData(Qt.QVariant(index))

	def openSite(self, action) :
		index = action.data().toInt()[0]
		site_url = self.actions_data_list[index]
		Qt.QDesktopServices.openUrl(Qt.QUrl(site_url))

