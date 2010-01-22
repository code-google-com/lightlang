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
DictHeaderFontBoldFlagObject = None
DictHeaderFontItalicFlagObject = None
DictHeaderFontLargeFlagObject = None
DictHeaderFontColorObject = None

DictHeaderBackgroundColorObject = None

RedAlertBackgroundColorObject = None

SearchSelectionBackgroundColorObject = None


#####
def tr(str) :
	return Qt.QApplication.translate("@default", str)


##### Public #####
def dictHeaderFontBoldFlag() :
	if DictHeaderFontBoldFlagObject == None :
		initDictHeaderFont()
	return DictHeaderFontBoldFlagObject

def dictHeaderFontItalicFlag() :
	if DictHeaderFontItalicFlagObject == None :
		initDictHeaderFont()
	return DictHeaderFontItalicFlagObject

def dictHeaderFontLargeFlag() :
	if DictHeaderFontLargeFlagObject == None :
		initDictHeaderFont()
	return DictHeaderFontLargeFlagObject

def dictHeaderFontColor() :
	if DictHeaderFontColorObject == None :
		initDictHeaderFont()
	return Qt.QColor(DictHeaderFontColorObject)

###

def dictHeaderBackgroundColor() :
	if DictHeaderBackgroundColorObject == None :
		initDictHeaderBackground()
	return Qt.QColor(DictHeaderBackgroundColorObject)

###

def redAlertBackgroundColor() :
	if RedAlertBackgroundColorObject == None :
		initRedAlertBackground()
	return Qt.QColor(RedAlertBackgroundColorObject)

###

def searchSelectionBackgroundColor() :
	if SearchSelectionBackgroundColorObject == None :
		initSearchSelectionBackground()
	return Qt.QColor(SearchSelectionBackgroundColorObject)


##### Private #####
def initDictHeaderFont() :
	global DictHeaderFontBoldFlagObject
	global DictHeaderFontItalicFlagObject
	global DictHeaderFontLargeFlagObject
	global DictHeaderFontColorObject

	DictHeaderFontBoldFlagObject = False
	DictHeaderFontItalicFlagObject = False
	DictHeaderFontLargeFlagObject = False
	DictHeaderFontColorObject = Qt.QColor()

	user_style_css = UserStyleCss.userStyleCss()
	dict_header_font_regexp = Qt.QRegExp("\\.dict_header_font\\s+\\{(([^(\\{|\\})])*"
		"(color:\\s*(#\\w{6});([^(\\{|\\})])*)?)\\}")
	dict_header_font_regexp.setMinimal(True)
	dict_header_font_pos = dict_header_font_regexp.indexIn(user_style_css)
	while dict_header_font_pos != -1 :
		DictHeaderFontBoldFlagObject = dict_header_font_regexp.cap(1).contains("bold")
		DictHeaderFontItalicFlagObject = dict_header_font_regexp.cap(1).contains("italic")
		DictHeaderFontLargeFlagObject = dict_header_font_regexp.cap(1).contains("large")
		DictHeaderFontColorObject = Qt.QColor(dict_header_font_regexp.cap(4))

		dict_header_font_pos = dict_header_font_regexp.indexIn(user_style_css,
			dict_header_font_pos + dict_header_font_regexp.matchedLength())

def initDictHeaderBackground() :
	global DictHeaderBackgroundColorObject

	DictHeaderBackgroundColorObject = Qt.QColor()

	user_style_css = UserStyleCss.userStyleCss()
	dict_header_background_regexp = Qt.QRegExp("\\.dict_header_background\\s+\\{([^(\\{|\\})])*"
		"background-color:\\s*(#\\w{6});([^(\\{|\\})])*\\}")
	dict_header_background_regexp.setMinimal(True)
	dict_header_background_pos = dict_header_background_regexp.indexIn(user_style_css)
	while dict_header_background_pos != -1 :
		DictHeaderBackgroundColorObject = Qt.QColor(dict_header_background_regexp.cap(2))

		dict_header_background_pos = dict_header_background_regexp.indexIn(user_style_css,
			dict_header_background_pos + dict_header_background_regexp.matchedLength())

def initRedAlertBackground() :
	global RedAlertBackgroundColorObject

	RedAlertBackgroundColorObject = Qt.QColor()

	user_style_css = UserStyleCss.userStyleCss()
	red_alert_background_regexp = Qt.QRegExp("\\.red_alert_background\\s+\\{([^(\\{|\\})])*"
		"background-color:\\s*(#\\w{6});([^(\\{|\\})])*\\}")
	red_alert_background_regexp.setMinimal(True)
	red_alert_background_pos = red_alert_background_regexp.indexIn(user_style_css)
	while red_alert_background_pos != -1 :
		RedAlertBackgroundColorObject = Qt.QColor(red_alert_background_regexp.cap(2))

		red_alert_background_pos = red_alert_background_regexp.indexIn(user_style_css,
			red_alert_background_pos + red_alert_background_regexp.matchedLength())

def initSearchSelectionBackground() :
	global SearchSelectionBackgroundColorObject

	SearchSelectionBackgroundColorObject = Qt.QColor()

	user_style_css = UserStyleCss.userStyleCss()
	search_selection_background_regexp = Qt.QRegExp("\\.search_selection_background\\s+\\{([^(\\{|\\})])*"
		"background-color:\\s*(#\\w{6});([^(\\{|\\})])*\\}")
	search_selection_background_regexp.setMinimal(True)
	search_selection_background_pos = search_selection_background_regexp.indexIn(user_style_css)
	while search_selection_background_pos != -1 :
		SearchSelectionBackgroundColorObject = Qt.QColor(search_selection_background_regexp.cap(2))

		search_selection_background_pos = search_selection_background_regexp.indexIn(user_style_css,
			search_selection_background_pos + search_selection_background_regexp.matchedLength())

