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
import UserStyleCss


#####
def tr(str) :
	return Qt.QApplication.translate("@default", str)


#####
class UserStyleCssCollectionBase(Qt.QObject) :
	def __init__(self, parent = None) :
		Qt.QObject.__init__(self, parent)

		#####

		self.user_style_css = UserStyleCss.userStyleCss()

		#####

		self.dict_header_font_bold_flag = None
		self.dict_header_font_italic_flag = None
		self.dict_header_font_large_flag = None
		self.dict_header_font_color = None

		###

		self.dict_header_background_color = None

		###

		self.red_alert_background_color = None

		#####

		self.parseUserStyleCss()


	### Public ###

	def dictHeaderFontBoldFlag(self) :
		return self.dict_header_font_bold_flag

	def dictHeaderFontItalicFlag(self) :
		return self.dict_header_font_italic_flag

	def dictHeaderFontLargeFlag(self) :
		return self.dict_header_font_large_flag

	def dictHeaderFontColor(self) :
		return ( Qt.QColor(self.dict_header_font_color) if self.dict_header_font_color != None else None )

	###

	def dictHeaderBackgroundColor(self) :
		return ( Qt.QColor(self.dict_header_background_color) if self.dict_header_background_color != None else None )

	###

	def redAlertBackgroundColor(self) :
		return Qt.QColor(self.red_alert_background_color)


	### Private ###

	def parseUserStyleCss(self) :
		self.parseDictHeaderFont()
		self.parseDictHeaderBackground()
		self.parseRedAlertBackground()

	###

	def parseDictHeaderFont(self) :
		dict_header_font_regexp = Qt.QRegExp("\\.dict_header_font\\s+\\{(([^(\\{|\\})])*"
			"(color:\\s*(#\\w{6});([^(\\{|\\})])*)?)\\}")
		dict_header_font_regexp.setMinimal(True)
		dict_header_font_pos = dict_header_font_regexp.indexIn(self.user_style_css)
		while dict_header_font_pos != -1 :
			self.dict_header_font_bold_flag = dict_header_font_regexp.cap(1).contains("bold")
			self.dict_header_font_italic_flag = dict_header_font_regexp.cap(1).contains("italic")
			self.dict_header_font_large_flag = dict_header_font_regexp.cap(1).contains("large")
			if not dict_header_font_regexp.cap(4).isEmpty() :
				self.dict_header_font_color = Qt.QColor(dict_header_font_regexp.cap(4))

			dict_header_font_pos = dict_header_font_regexp.indexIn(self.user_style_css, dict_header_font_pos +
				dict_header_font_regexp.matchedLength())

	def parseDictHeaderBackground(self) :
		dict_header_background_regexp = Qt.QRegExp("\\.dict_header_background\\s+\\{([^(\\{|\\})])*"
			"background-color:\\s*(#\\w{6});([^(\\{|\\})])*\\}")
		dict_header_background_regexp.setMinimal(True)
		dict_header_background_pos = dict_header_background_regexp.indexIn(self.user_style_css)
		while dict_header_background_pos != -1 :
			if not dict_header_background_regexp.cap(2).isEmpty() :
				self.dict_header_background_color = Qt.QColor(dict_header_background_regexp.cap(2))

			dict_header_background_pos = dict_header_background_regexp.indexIn(self.user_style_css, dict_header_background_pos +
				dict_header_background_regexp.matchedLength())

	def parseRedAlertBackground(self) :
		red_alert_background_regexp = Qt.QRegExp("\\.red_alert_background\\s+\\{([^(\\{|\\})])*"
			"background-color:\\s*(#\\w{6});([^(\\{|\\})])*\\}")
		red_alert_background_regexp.setMinimal(True)
		red_alert_background_pos = red_alert_background_regexp.indexIn(self.user_style_css)
		while red_alert_background_pos != -1 :
			if not red_alert_background_regexp.cap(2).isEmpty() :
				self.red_alert_background_color = Qt.QColor(red_alert_background_regexp.cap(2))

			red_alert_background_pos = red_alert_background_regexp.indexIn(self.user_style_css, red_alert_background_pos +
				red_alert_background_regexp.matchedLength())

