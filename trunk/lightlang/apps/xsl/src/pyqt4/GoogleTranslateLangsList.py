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
LangsListObject = None


#####
def tr(str) :
	return Qt.QApplication.translate("@default", str)


##### Public #####
def langsList() :
	if LangsListObject == None :
		initLangsList()
	return LangsListObject


##### Private #####
def initLangsList() :
	global LangsListObject
	LangsListObject = [
		[ tr("Albanian"),		Qt.QVariant("sq") ],
		[ tr("Arabic"),			Qt.QVariant("ar") ],
		[ tr("Bulgarian"),		Qt.QVariant("bg") ],
		[ tr("Catalan"),		Qt.QVariant("ca") ],
		[ tr("Chinese (Simplified)"),	Qt.QVariant("zh-CN") ],
		[ tr("Chinese (Traditional)"),	Qt.QVariant("zh-TW") ],
		[ tr("Croatian"),		Qt.QVariant("hr") ],
		[ tr("Czech"),			Qt.QVariant("cs") ],
		[ tr("Danish"),			Qt.QVariant("da") ],
		[ tr("Dutch"),			Qt.QVariant("nl") ],
		[ tr("English"),		Qt.QVariant("en") ],
		[ tr("Estonian"),		Qt.QVariant("et") ],
		[ tr("Filipino"),		Qt.QVariant("tl") ],
		[ tr("Finnish"),		Qt.QVariant("fi") ],
		[ tr("French"),			Qt.QVariant("fr") ],
		[ tr("Galician"),		Qt.QVariant("gl") ],
		[ tr("German"),			Qt.QVariant("de") ],
		[ tr("Greek"),			Qt.QVariant("el") ],
		[ tr("Hebrew"),			Qt.QVariant("iw") ],
		[ tr("Hindi"),			Qt.QVariant("hi") ],
		[ tr("Hungarian"),		Qt.QVariant("hu") ],
		[ tr("Indonesian"),		Qt.QVariant("id") ],
		[ tr("Italian"),		Qt.QVariant("it") ],
		[ tr("Japanese"),		Qt.QVariant("ja") ],
		[ tr("Korean"),			Qt.QVariant("ko") ],
		[ tr("Latvian"),		Qt.QVariant("lv") ],
		[ tr("Lithuanian"),		Qt.QVariant("lt") ],
		[ tr("Maltese"),		Qt.QVariant("mt") ],
		[ tr("Norwegian"),		Qt.QVariant("no") ],
		[ tr("Polish"),			Qt.QVariant("pl") ],
		[ tr("Portuguese"),		Qt.QVariant("pt") ],
		[ tr("Romanian"),		Qt.QVariant("ro") ],
		[ tr("Russian"),		Qt.QVariant("ru") ],
		[ tr("Serbian"),		Qt.QVariant("sr") ],
		[ tr("Slovak"),			Qt.QVariant("sk") ],
		[ tr("Slovenian"),		Qt.QVariant("sl") ],
		[ tr("Spanish"),		Qt.QVariant("es") ],
		[ tr("Swedish"),		Qt.QVariant("sv") ],
		[ tr("Thai"),			Qt.QVariant("th") ],
		[ tr("Turkish"),		Qt.QVariant("tr") ],
		[ tr("Ukrainian"),		Qt.QVariant("uk") ],
		[ tr("Vietnamese"),		Qt.QVariant("vi") ]
		]
	sortLangsList(LangsListObject)


def sortLangsList(langs_list, left = None, right = None) :
	if left == right == None :
		left = 0
		right = len(langs_list) -1

	if left >= right :
		return

	i = j = left
	while j <= right :
		if langs_list[j][0] <= langs_list[right][0] :
			langs_list[i], langs_list[j] = langs_list[j], langs_list[i]
			i += 1
		j += 1

	sortLangsList(langs_list, left, i - 2)
	sortLangsList(langs_list, i, right)

