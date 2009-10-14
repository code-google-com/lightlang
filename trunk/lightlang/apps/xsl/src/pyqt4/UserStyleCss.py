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


#####
UserStyleCssName = "user-style.css"


#####
UserStyleCssObject = None


#####
def tr(str) :
	return Qt.QApplication.translate("@default", str)


##### Public #####
def userStyleCss() :
	if UserStyleCssObject == None :
		initUserStyleCss()

	return Qt.QString(UserStyleCssObject)


##### Private #####
def initUserStyleCss() :
	my_name = Qt.QString(Const.MyName).toLower()

	if not Qt.QDir(Qt.QDir.homePath()+"/."+my_name).exists() :
		Qt.QDir.home().mkdir("."+my_name)

	user_style_css_file = Qt.QFile(Qt.QDir.homePath()+"/."+my_name+"/"+UserStyleCssName)
	user_style_css_file_stream = Qt.QTextStream(user_style_css_file)

	global UserStyleCssObject
	if user_style_css_file.open(Qt.QIODevice.ReadOnly) :
		UserStyleCssObject = "\n"+user_style_css_file_stream.readAll()+"\n"
		UserStyleCssObject.remove(Qt.QRegExp("/\\*([^*]|\\*[^/]|\\n)*\\*/"))
	else :
		UserStyleCssObject = Qt.QString("\n")

