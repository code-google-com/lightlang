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
LangsCodesDictObject = None


#####
def tr(str) :
	return Qt.QApplication.translate("@default", str)


##### Public #####
def langsList() :
	if LangsListObject == None :
		initLangsList()
	return LangsListObject


def langName(short_name) :
	if LangsCodesDictObject == None :
		initLangsList()

	if LangsCodesDictObject.has_key(str(short_name)) :
		return Qt.QString(LangsCodesDictObject[str(short_name)])
	else :
		return Qt.QString(short_name)


##### Private #####
def initLangsList() :
	global LangsListObject
	LangsListObject = [
		[ tr("Afrikaans"),	Qt.QString("af") ],
		[ tr("Albanian"),	Qt.QString("sq") ],
		[ tr("Arabic"),		Qt.QString("ar") ],
		[ tr("Belarusian"),	Qt.QString("be") ],
		[ tr("Bulgarian"),	Qt.QString("bg") ],
		[ tr("Catalan"),	Qt.QString("ca") ],
		[ tr("Chinese"),	Qt.QString("zh") ],
		[ tr("Croatian"),	Qt.QString("hr") ],
		[ tr("Czech"),		Qt.QString("cs") ],
		[ tr("Danish"),		Qt.QString("da") ],
		[ tr("Dutch"),		Qt.QString("nl") ],
		[ tr("English"),	Qt.QString("en") ],
		[ tr("Estonian"),	Qt.QString("et") ],
		[ tr("Filipino"),	Qt.QString("tl") ],
		[ tr("Finnish"),	Qt.QString("fi") ],
		[ tr("French"),		Qt.QString("fr") ],
		[ tr("Galician"),	Qt.QString("gl") ],
		[ tr("German"),		Qt.QString("de") ],
		[ tr("Greek"),		Qt.QString("el") ],
		[ tr("Hebrew"),		Qt.QString("iw") ],
		[ tr("Hindi"),		Qt.QString("hi") ],
		[ tr("Hungarian"),	Qt.QString("hu") ],
		[ tr("Icelandic"),	Qt.QString("is") ],
		[ tr("Indonesian"),	Qt.QString("id") ],
		[ tr("Irish"),		Qt.QString("ga") ],
		[ tr("Italian"),	Qt.QString("it") ],
		[ tr("Japanese"),	Qt.QString("ja") ],
		[ tr("Korean"),		Qt.QString("ko") ],
		[ tr("Latvian"),	Qt.QString("lv") ],
		[ tr("Lithuanian"),	Qt.QString("lt") ],
		[ tr("Macedonian"),	Qt.QString("mk") ],
		[ tr("Malay"),		Qt.QString("ms") ],
		[ tr("Maltese"),	Qt.QString("mt") ],
		[ tr("Norwegian"),	Qt.QString("no") ],
		[ tr("Persian"),	Qt.QString("fa") ],
		[ tr("Polish"),		Qt.QString("pl") ],
		[ tr("Portuguese"),	Qt.QString("pt") ],
		[ tr("Romanian"),	Qt.QString("ro") ],
		[ tr("Russian"),	Qt.QString("ru") ],
		[ tr("Serbian"),	Qt.QString("sr") ],
		[ tr("Slovak"),		Qt.QString("sk") ],
		[ tr("Slovenian"),	Qt.QString("sl") ],
		[ tr("Spanish"),	Qt.QString("es") ],
		[ tr("Swahili"),	Qt.QString("sw") ],
		[ tr("Swedish"),	Qt.QString("sv") ],
		[ tr("Thai"),		Qt.QString("th") ],
		[ tr("Turkish"),	Qt.QString("tr") ],
		[ tr("Ukrainian"),	Qt.QString("uk") ],
		[ tr("Vietnamese"),	Qt.QString("vi") ],
		[ tr("Welsh"),		Qt.QString("cy") ],
		[ tr("Yiddish"),	Qt.QString("yi") ]
		]
	sortLangsList(LangsListObject)

	global LangsCodesDictObject
	LangsCodesDictObject = {}
	for langs_list_object_item in LangsListObject :
		LangsCodesDictObject[str(langs_list_object_item[1])] = langs_list_object_item[0]


def sortLangsList(langs_list_object, left = None, right = None) :
	if left == right == None :
		left = 0
		right = len(langs_list_object) -1

	if left >= right :
		return

	i = j = left
	while j <= right :
		if langs_list_object[j][0] <= langs_list_object[right][0] :
			langs_list_object[i], langs_list_object[j] = langs_list_object[j], langs_list_object[i]
			i += 1
		j += 1

	sortLangsList(langs_list_object, left, i - 2)
	sortLangsList(langs_list_object, i, right)

