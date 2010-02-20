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
			{ "name" : tr("Afrikaans"),	"code" : Qt.QString("af") },
			{ "name" : tr("Albanian"),	"code" : Qt.QString("sq") },
			{ "name" : tr("Arabic"),	"code" : Qt.QString("ar") },
			{ "name" : tr("Belarusian"),	"code" : Qt.QString("be") },
			{ "name" : tr("Bulgarian"),	"code" : Qt.QString("bg") },
			{ "name" : tr("Catalan"),	"code" : Qt.QString("ca") },
			{ "name" : tr("Chinese"),	"code" : Qt.QString("zh") },
			{ "name" : tr("Croatian"),	"code" : Qt.QString("hr") },
			{ "name" : tr("Czech"),		"code" : Qt.QString("cs") },
			{ "name" : tr("Danish"),	"code" : Qt.QString("da") },
			{ "name" : tr("Dutch"),		"code" : Qt.QString("nl") },
			{ "name" : tr("English"),	"code" : Qt.QString("en") },
			{ "name" : tr("Estonian"),	"code" : Qt.QString("et") },
			{ "name" : tr("Filipino"),	"code" : Qt.QString("tl") },
			{ "name" : tr("Finnish"),	"code" : Qt.QString("fi") },
			{ "name" : tr("French"),	"code" : Qt.QString("fr") },
			{ "name" : tr("Galician"),	"code" : Qt.QString("gl") },
			{ "name" : tr("German"),	"code" : Qt.QString("de") },
			{ "name" : tr("Greek"),		"code" : Qt.QString("el") },
			{ "name" : tr("Hebrew"),	"code" : Qt.QString("iw") },
			{ "name" : tr("Hindi"),		"code" : Qt.QString("hi") },
			{ "name" : tr("Hungarian"),	"code" : Qt.QString("hu") },
			{ "name" : tr("Icelandic"),	"code" : Qt.QString("is") },
			{ "name" : tr("Indonesian"),	"code" : Qt.QString("id") },
			{ "name" : tr("Irish"),		"code" : Qt.QString("ga") },
			{ "name" : tr("Italian"),	"code" : Qt.QString("it") },
			{ "name" : tr("Japanese"),	"code" : Qt.QString("ja") },
			{ "name" : tr("Korean"),	"code" : Qt.QString("ko") },
			{ "name" : tr("Latvian"),	"code" : Qt.QString("lv") },
			{ "name" : tr("Lithuanian"),	"code" : Qt.QString("lt") },
			{ "name" : tr("Macedonian"),	"code" : Qt.QString("mk") },
			{ "name" : tr("Malay"),		"code" : Qt.QString("ms") },
			{ "name" : tr("Maltese"),	"code" : Qt.QString("mt") },
			{ "name" : tr("Norwegian"),	"code" : Qt.QString("no") },
			{ "name" : tr("Persian"),	"code" : Qt.QString("fa") },
			{ "name" : tr("Polish"),	"code" : Qt.QString("pl") },
			{ "name" : tr("Portuguese"),	"code" : Qt.QString("pt") },
			{ "name" : tr("Romanian"),	"code" : Qt.QString("ro") },
			{ "name" : tr("Russian"),	"code" : Qt.QString("ru") },
			{ "name" : tr("Serbian"),	"code" : Qt.QString("sr") },
			{ "name" : tr("Slovak"),	"code" : Qt.QString("sk") },
			{ "name" : tr("Slovenian"),	"code" : Qt.QString("sl") },
			{ "name" : tr("Spanish"),	"code" : Qt.QString("es") },
			{ "name" : tr("Swahili"),	"code" : Qt.QString("sw") },
			{ "name" : tr("Swedish"),	"code" : Qt.QString("sv") },
			{ "name" : tr("Thai"),		"code" : Qt.QString("th") },
			{ "name" : tr("Turkish"),	"code" : Qt.QString("tr") },
			{ "name" : tr("Ukrainian"),	"code" : Qt.QString("uk") },
			{ "name" : tr("Vietnamese"),	"code" : Qt.QString("vi") },
			{ "name" : tr("Welsh"),		"code" : Qt.QString("cy") },
			{ "name" : tr("Yiddish"),	"code" : Qt.QString("yi") }
		]
	sortLangsList(LangsListObject)

	global LangsCodesDictObject
	LangsCodesDictObject = {}
	for langs_list_object_item in LangsListObject :
		LangsCodesDictObject[str(langs_list_object_item["code"])] = langs_list_object_item["name"]


def sortLangsList(langs_list_object, left = None, right = None) :
	if left == right == None :
		left = 0
		right = len(langs_list_object) - 1

	if left >= right :
		return

	i = j = left
	while j <= right :
		if langs_list_object[j]["name"] <= langs_list_object[right]["name"] :
			langs_list_object[i], langs_list_object[j] = langs_list_object[j], langs_list_object[i]
			i += 1
		j += 1

	sortLangsList(langs_list_object, left, i - 2)
	sortLangsList(langs_list_object, i, right)

