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


import sys

import Qt
import Config
import Const
import Locale


##### Public classes #####
class IfaSaxHandler(Qt.QXmlDefaultHandler) :
	def __init__(self, new_app_handler) :
		Qt.QXmlDefaultHandler.__init__(self)

		#####

		self._new_app_handler = new_app_handler

		#####

		self._app_tag_flag = False
		self._title_tag_flag = False
		self._description_tag_flag = False
		self._icon_tag_flag = False
		self._path_tag_flag = False
		self._options_tag_flag = False
		self._precode_tag_flag = False
		self._postcode_tag_flag = False

		self._app_title = Qt.QString()
		self._app_title_lang = Qt.QString()
		self._app_description = Qt.QString()
		self._app_description_lang = Qt.QString()
		self._app_icon_name = Qt.QString()
		self._app_prog_path = Qt.QString()
		self._app_prog_options = Qt.QString()
		self._python_precode = Qt.QString()
		self._python_postcode = Qt.QString()


	### Private ###
	### Handlers ###
	def startElement(self, namespace_uri, local_name, name, attributes) :
		if name == "app" :
			self._app_tag_flag = True
			return True

		if self._app_tag_flag :
			if name == "title" :
				self._app_title_lang = attributes.value("lang")
				self._title_tag_flag = True
			elif name == "description" :
				self._app_description_lang = attributes.value("lang")
				self._description_tag_flag = True
			elif name == "icon" :
				self._icon_tag_flag = True
			elif name == "path" :
				self._path_tag_flag = True
			elif name == "options" :
				self._options_tag_flag = True
			elif name == "precode" and attributes.value("lang") == "python" :
				self._precode_tag_flag = True
			elif name == "postcode" and attributes.value("lang") == "python" :
				self._postcode_tag_flag = True
		return True

	def characters(self, str) :
		if str.simplified().isEmpty() :
			return True

		if self._app_tag_flag :
			if self._title_tag_flag :
				if self._app_title_lang == Locale.mainLang() :
					self._app_title = str.simplified()
				if self._app_title.simplified().isEmpty() and self._app_title_lang.simplified().isEmpty() :
					self._app_title = str.simplified()
				return True
			elif self._description_tag_flag :
				if self._app_description_lang == Locale.mainLang() :
					self._app_description = str.simplified()
				if self._app_description.simplified().isEmpty() and self._app_description_lang.simplified().isEmpty() :
					self._app_description = str.simplified()
				return True
			elif self._icon_tag_flag :
				self._app_icon_name = str.simplified()
				return True
			elif self._path_tag_flag :
				self._app_prog_path = str.simplified()
				return True
			elif self._options_tag_flag :
				self._app_prog_options = str.simplified()
				return True
			elif self._precode_tag_flag :
				self._python_precode = str.trimmed()
				return True
			elif self._postcode_tag_flag :
				self._python_postcode = str.trimmed()
				return True
		return True

	def endElement(self, namespace_uri, local_name, name) :
		if name == "app" :
			self._new_app_handler(self._app_title, self._app_description, self._app_icon_name,
				self._app_prog_path, self._app_prog_options, self._python_precode, self._python_postcode)

			for item in ( self._app_title, self._app_title_lang, self._app_description, self._app_description_lang, self._app_icon_name,
				self._app_prog_path, self._app_prog_options, self._python_precode, self._python_postcode ) :
				item.clear()

			self._app_tag_flag = False
		elif name == "title" :
			self._title_tag_flag = False
		elif name == "description" :
			self._description_tag_flag = False
		elif name == "icon" :
			self._icon_tag_flag = False
		elif name == "path" :
			self._path_tag_flag = False
		elif name == "options" :
			self._options_tag_flag = False
		elif name == "precode" :
			self._precode_tag_flag = False
		elif name == "postcode" :
			self._postcode_tag_flag = False
		return True

	def fatalError(self, exception) :
		return True

