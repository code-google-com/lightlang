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

HighlightBackgroundColorObject = None
HighlightBackgroundOpacityObject = None


#####
def tr(str) :
	return Qt.QApplication.translate("@default", str)


##### Public #####
def dictHeaderFontBoldFlag() :
	if DictHeaderFontBoldFlagObject == None :
		initUserStyleCssCollection()
	return DictHeaderFontBoldFlagObject

def dictHeaderFontItalicFlag() :
	if DictHeaderFontItalicFlagObject == None :
		initUserStyleCssCollection()
	return DictHeaderFontItalicFlagObject

def dictHeaderFontLargeFlag() :
	if DictHeaderFontLargeFlagObject == None :
		initUserStyleCssCollection()
	return DictHeaderFontLargeFlagObject

def dictHeaderFontColor() :
	if DictHeaderFontColorObject == None :
		initUserStyleCssCollection()
	return Qt.QColor(DictHeaderFontColorObject)

###

def dictHeaderBackgroundColor() :
	if DictHeaderBackgroundColorObject == None :
		initUserStyleCssCollection()
	return Qt.QColor(DictHeaderBackgroundColorObject)

###

def redAlertBackgroundColor() :
	if RedAlertBackgroundColorObject == None :
		initUserStyleCssCollection()
	return Qt.QColor(RedAlertBackgroundColorObject)

###

def highlightBackgroundColor() :
	if HighlightBackgroundColorObject == None :
		initUserStyleCssCollection()
	return Qt.QColor(HighlightBackgroundColorObject)

def highlightBackgroundOpacity() :
	if HighlightBackgroundOpacityObject == None :
		initUserStyleCssCollection()
	return HighlightBackgroundOpacityObject


##### Private #####
def initUserStyleCssCollection() :
	global DictHeaderFontBoldFlagObject
	global DictHeaderFontItalicFlagObject
	global DictHeaderFontLargeFlagObject
	global DictHeaderFontColorObject

	global DictHeaderBackgroundColorObject

	global RedAlertBackgroundColorObject

	global HighlightBackgroundColorObject
	global HighlightBackgroundOpacityObject

	###

	DictHeaderFontBoldFlagObject = False
	DictHeaderFontItalicFlagObject = False
	DictHeaderFontLargeFlagObject = False
	DictHeaderFontColorObject = False

	DictHeaderBackgroundColorObject = Qt.QColor()

	RedAlertBackgroundColorObject = Qt.QColor()

	HighlightBackgroundColorObject = Qt.QColor()
	HighlightBackgroundOpacityObject = 255

	###

	user_style_css = UserStyleCss.userStyleCss().remove(Qt.QRegExp("\\s"))

	css_class_regexp = Qt.QRegExp("\\.([^(\\{|\\})]*)\\{([^(\\{|\\})]*)\\}")
	css_class_regexp.setMinimal(True)

	css_option_regexp = Qt.QRegExp("([^(\\{|\\})]*):([^(\\{|\\})]*);")
	css_option_regexp.setMinimal(True)

	css_class_pos = css_class_regexp.indexIn(user_style_css)
	while css_class_pos != -1 :
		css_class_name = css_class_regexp.cap(1)
		css_class_body = css_class_regexp.cap(2)

		css_option_pos = css_option_regexp.indexIn(css_class_body)
		while css_option_pos != -1 :
			css_option_name = css_option_regexp.cap(1)
			css_option_value = css_option_regexp.cap(2)

			if css_class_name == "dict_header_font" :
				if css_option_name == "font-weight" :
					DictHeaderFontBoldFlagObject = ( True if css_option_value == "bold" else False )
				elif css_option_name == "font-style" :
					DictHeaderFontItalicFlagObject = ( True if css_option_value == "italic" else False )
				elif css_option_name == "font-size" :
					DictHeaderFontLargeFlagObject = ( True if css_option_value == "large" else False )
				elif css_option_name == "color" :
					DictHeaderFontColorObject = Qt.QColor(css_option_value)

			elif css_class_name == "dict_header_background" :
				if css_option_name == "background-color" :
					DictHeaderBackgroundColorObject = Qt.QColor(css_option_value)

			elif css_class_name == "red_alert_background" :
				if css_option_name == "background-color" :
					RedAlertBackgroundColorObject = Qt.QColor(css_option_value)

			elif css_class_name == "highlight_background" :
				if css_option_name == "background-color" :
					HighlightBackgroundColorObject = Qt.QColor(css_option_value)
				if css_option_name == "opacity" :
					HighlightBackgroundOpacityObject = ( css_option_value.toInt()[0] if css_option_value.toInt()[0] else 255 )

			css_option_pos = css_option_regexp.indexIn(css_class_body, css_option_pos + css_option_regexp.matchedLength())

		css_class_pos = css_class_regexp.indexIn(user_style_css, css_class_pos + css_class_regexp.matchedLength())

