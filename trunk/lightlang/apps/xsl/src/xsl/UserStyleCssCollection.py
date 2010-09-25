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
import UserStyleCss


##### Private objects #####
CollectionDictObject = {
	"dict_header_font" : {
		"bold_flag" : None,
		"italic_flag" : None,
		"large_flag" : None,
		"color" : None
	},
	"dict_header_background" : {
		"color" : None
	},
	"red_alert_background" : {
		"color" : None
	},
	"highlight_background" : {
		"color" : None,
		"opacity" : None
	},
	"transparent_frame_background" : {
		"color" : None,
		"opacity" : None
	}
}


##### Public methods #####
def dictHeaderFontBoldFlag() :
	return option("dict_header_font", "bold_flag")

def dictHeaderFontItalicFlag() :
	return option("dict_header_font", "italic_flag")

def dictHeaderFontLargeFlag() :
	return option("dict_header_font", "large_flag")

def dictHeaderFontColor() :
	return Qt.QColor(option("dict_header_font", "color"))

###

def dictHeaderBackgroundColor() :
	return Qt.QColor(option("dict_header_background", "color"))

###

def redAlertBackgroundColor() :
	return Qt.QColor(option("red_alert_background", "color"))

###

def highlightBackgroundColor() :
	return Qt.QColor(option("highlight_background", "color"))

def highlightBackgroundOpacity() :
	return option("highlight_background", "opacity")

###

def transparentFrameBackgroundColor() :
	return Qt.QColor(option("transparent_frame_background", "color"))

def transparentFrameBackgroundOpacity() :
	return option("transparent_frame_background", "opacity")


##### Private methods #####
def setOption(section_name, option_name, value) :
	if not CollectionDictObject.has_key(section_name) :
		CollectionDictObject[section_name] = {}
	CollectionDictObject[section_name][option_name] = value

def option(section_name, option_name) :
	if not CollectionDictObject.has_key(section_name) or not CollectionDictObject[section_name].has_key(option_name) :
		return None
	elif CollectionDictObject[section_name][option_name] == None :
		initCollection()
	return CollectionDictObject[section_name][option_name]

###

def initCollection() :
	setOption("dict_header_font", "bold_flag", False)
	setOption("dict_header_font", "italic_flag", False)
	setOption("dict_header_font", "large_flag", False)
	setOption("dict_header_font", "color", Qt.QColor())

	setOption("dict_header_background", "color", Qt.QColor())

	setOption("red_alert_background", "color", Qt.QColor())

	setOption("highlight_background", "color", Qt.QColor())
	setOption("highlight_background", "opacity", 255)

	setOption("transparent_frame_background", "color", Qt.QColor())
	setOption("transparent_frame_background", "opacity", 255)

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
					setOption(str(css_class_name), "bold_flag", ( css_option_value == "bold" ))
				elif css_option_name == "font-style" :
					setOption(str(css_class_name), "italic_flag", ( css_option_value == "italic" ))
				elif css_option_name == "font-size" :
					setOption(str(css_class_name), "large_flag", ( css_option_value == "large" ))
				elif css_option_name == "color" :
					setOption(str(css_class_name), "color", Qt.QColor(css_option_value))

			elif css_class_name == "dict_header_background" :
				if css_option_name == "background-color" :
					setOption(str(css_class_name), "color", Qt.QColor(css_option_value))

			elif css_class_name == "red_alert_background" :
				if css_option_name == "background-color" :
					setOption(str(css_class_name), "color", Qt.QColor(css_option_value))

			elif css_class_name == "highlight_background" :
				if css_option_name == "background-color" :
					if css_option_value == "from-palette" :
						setOption(str(css_class_name), "color", Qt.QApplication.palette().color(Qt.QPalette.Highlight))
					else :
						setOption(str(css_class_name), "color", Qt.QColor(css_option_value))
				if css_option_name == "opacity" :
					setOption(str(css_class_name), "opacity", ( css_option_value.toInt()[0] if css_option_value.toInt()[1] else 255 ))

			elif css_class_name == "transparent_frame_background" :
				if css_option_name == "background-color" :
					if css_option_value == "from-palette" :
						setOption(str(css_class_name), "color", Qt.QApplication.palette().color(Qt.QPalette.Window))
					else :
						setOption(str(css_class_name), "color", Qt.QColor(css_option_value))
				if css_option_name == "opacity" :
					setOption(str(css_class_name), "opacity", ( css_option_value.toInt()[0] if css_option_value.toInt()[1] else 255 ))

			css_option_pos = css_option_regexp.indexIn(css_class_body, css_option_pos + css_option_regexp.matchedLength())

		css_class_pos = css_class_regexp.indexIn(user_style_css, css_class_pos + css_class_regexp.matchedLength())

