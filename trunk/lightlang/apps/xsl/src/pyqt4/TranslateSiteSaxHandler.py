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
import Locale


#####
def tr(str) :
	return Qt.QApplication.translate("@default", str)


#####
class TranslateSiteSaxHandler(Qt.QXmlDefaultHandler) :
	def __init__(self, new_site_handler) :
		Qt.QXmlDefaultHandler.__init__(self)

		#####

		self.new_site_handler = new_site_handler

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
				if self.site_title_lang == Locale.mainLang() :
					self.site_title = str.simplified()
				if self.site_title.simplified().isEmpty() and self.site_title_lang.simplified().isEmpty() :
					self.site_title = str.simplified()
				return True
			elif self.description_tag_flag :
				if self.site_description_lang == Locale.mainLang() :
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

