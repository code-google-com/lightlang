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
LocaleObject = None


#####
def tr(str) :
	return Qt.QApplication.translate("@default", str)


##### Public #####
def locale() :
	if LocaleObject == None :
		initLocale()
	return LocaleObject

def mainLang() :
	if LocaleObject == None :
		initLocale()

	lang = LocaleObject.name()
	lang.remove(lang.indexOf("_"), lang.length())

	if lang.simplified().isEmpty() :
		lang = "en"

	return Qt.QString(lang)


def docsLang() :
	if LocaleObject == None :
		initLocale()

	lang = LocaleObject.name()
	lang.remove(lang.indexOf("_"), lang.length())

	if not lang.simplified().isEmpty() :
		help_dir = Qt.QDir(Config.Prefix+"/share/doc/lightlang/html/"+lang)
		if not help_dir.exists() :
			lang = "en"
	else :
		lang = "en"

	return Qt.QString(lang)


##### Private #####
def initLocale() :
	global LocaleObject
	LocaleObject = Qt.QLocale()

