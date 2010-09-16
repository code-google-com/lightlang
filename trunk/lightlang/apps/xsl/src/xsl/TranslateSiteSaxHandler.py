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
class TranslateSiteSaxHandler(Qt.QXmlDefaultHandler) :
	def __init__(self, new_site_handler) :
		Qt.QXmlDefaultHandler.__init__(self)

		#####

		self._new_site_handler = new_site_handler

		#####

		self._site_tag_flag = False
		self._title_tag_flag = False
		self._description_tag_flag = False
		self._icon_tag_flag = False
		self._url_tag_flag = False

		self._site_title = Qt.QString()
		self._site_title_lang = Qt.QString()
		self._site_description = Qt.QString()
		self._site_description_lang = Qt.QString()
		self._site_icon_name = Qt.QString()
		self._site_url = Qt.QString()


	### Private ###
	### Handlers ###

	def startElement(self, namespace_uri, local_name, name, attributes) :
		if name == "site" :
			self._site_tag_flag = True
			return True

		if self._site_tag_flag :
			if name == "title" :
				self._site_title_lang = attributes.value("lang")
				self._title_tag_flag = True
			elif name == "description" :
				self._site_description_lang = attributes.value("lang")
				self._description_tag_flag = True
			elif name == "icon" :
				self._icon_tag_flag = True
			elif name == "url" :
				self._url_tag_flag = True
		return True

	def characters(self, str) :
		if str.simplified().isEmpty() :
			return True

		if self._site_tag_flag :
			if self._title_tag_flag :
				if self._site_title_lang == Locale.mainLang() :
					self._site_title = str.simplified()
				if self._site_title.simplified().isEmpty() and self._site_title_lang.simplified().isEmpty() :
					self._site_title = str.simplified()
				return True
			elif self._description_tag_flag :
				if self._site_description_lang == Locale.mainLang() :
					self._site_description = str.simplified()
				if self._site_description.simplified().isEmpty() and self._site_description_lang.simplified().isEmpty() :
					self._site_description = str.simplified()
				return True
			elif self._icon_tag_flag :
				self._site_icon_name = str.simplified()
				return True
			elif self._url_tag_flag :
				self._site_url = str.simplified()
				return True
		return True

	def endElement(self, namespace_uri, local_name, name) :
		if name == "site" :
			self._new_site_handler(self._site_title, self._site_description, self._site_icon_name, self._site_url)

			for item in (self._site_title, self._site_title_lang, self._site_description,
				self._site_description_lang, self._site_icon_name, self._site_url ) :
				item.clear()

			self._site_tag_flag = False
		elif name == "title" :
			self._title_tag_flag = False
		elif name == "description" :
			self._description_tag_flag = False
		elif name == "icon" :
			self._icon_tag_flag = False
		elif name == "url" :
			self._url_tag_flag = False
		return True

	def fatalError(self, exception) :
		return True

