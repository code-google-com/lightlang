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

#####
TrSitesDir = Config.Prefix+"/lib/xsl/trsites/"
IconsDir = Config.Prefix+"/lib/xsl/icons/"

#####
class TrSiteSAXHandler(Qt.QXmlDefaultHandler) :
	def __init__(self, new_site_handler) :
		Qt.QXmlDefaultHandler.__init__(self)

		self.new_site_handler = new_site_handler

		#####

		self.lang = Qt.QLocale().name()
		self.lang.remove(self.lang.indexOf("_"), self.lang.length())

		#####

		self.site_tag_flag = False
		self.title_tag_flag = False
		self.description_tag_flag = False
		self.icon_tag_flag = False
		self.url_tag_flag = False

		self.site_title = Qt.QString()
		self.site_title_lang = Qt.QString()
		self.site_description = Qt.QString()
		self.site_description_lang = Qt.QString()
		self.site_icon_path = Qt.QString()
		self.site_url = Qt.QString()


	### Private ###
	### Handlers ###

	def startElement(self, namespace_uri, local_name, name, attributes) :
		if name == "site" :
			self.site_tag_flag = True
			return True

		if self.site_tag_flag :
			if name == "title" :
				self.site_title_lang = attributes.value("lang")
				self.title_tag_flag = True
			elif name == "description" :
				self.site_description_lang = attributes.value("lang")
				self.description_tag_flag = True
			elif name == "icon" :
				self.icon_tag_flag = True
			elif name == "url" :
				self.url_tag_flag = True
		return True

	def characters(self, str) :
		if str.simplified().isEmpty() :
			return True

		if self.site_tag_flag :
			if self.title_tag_flag :
				if self.site_title_lang == self.lang :
					self.site_title = str.simplified()
				if self.site_title.simplified().isEmpty() and self.site_title_lang.simplified().isEmpty() :
					self.site_title = str.simplified()
				return True
			elif self.description_tag_flag :
				if self.site_description_lang == self.lang :
					self.site_description = str.simplified()
				if self.site_description.simplified().isEmpty() and self.site_description_lang.simplified().isEmpty() :
					self.site_description = str.simplified()
				return True
			elif self.icon_tag_flag :
				self.site_icon_path = str.simplified()
				return True
			elif self.url_tag_flag :
				self.site_url = str.simplified()
				return True
		return True

	def endElement(self, namespace_uri, local_name, name) :
		if name == "site" :
			self.new_site_handler(self.site_title, self.site_description, self.site_icon_path, self.site_url)

			self.site_title.clear()
			self.site_title_lang.clear()
			self.site_description.clear()
			self.site_description_lang.clear()
			self.site_icon_path.clear()
			self.site_url.clear()

			self.site_tag_flag = False
		elif name == "title" :
			self.title_tag_flag = False
		elif name == "description" :
			self.description_tag_flag = False
		elif name == "icon" :
			self.icon_tag_flag = False
		elif name == "url" :
			self.url_tag_flag = False
		return True

	def fatalError(self, exception) :
		return True


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
		trsites_dir = Qt.QDir(TrSitesDir)
		trsites_dir_name_filters = Qt.QStringList()
		trsites_dir_name_filters << "*.trsite" << "*.xml"
		trsites_dir.setNameFilters(trsites_dir_name_filters)
		trsites_dir.setFilter(Qt.QDir.Files)

		count = 0
		while count < trsites_dir.count() :
			Qt.QCoreApplication.processEvents()
			trsite_file = Qt.QFile(TrSitesDir+trsites_dir[count])
			xml_input_source = Qt.QXmlInputSource(trsite_file)
			xml_reader = Qt.QXmlSimpleReader()
			xml_handler = TrSiteSAXHandler(self.addSite)
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
