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
	global LangsCodesDictObject

	LangsCodesDictObject = {
		"af" : tr("Afrikaans"),
		"sq" : tr("Albanian"),
		"ar" : tr("Arabic"),
		"be" : tr("Belarusian"),
		"bg" : tr("Bulgarian"),
		"ca" : tr("Catalan"),
		"zh" : tr("Chinese"),
		"hz" : tr("Croatian"),
		"cs" : tr("Czech"),
		"da" : tr("Danish"),
		"nl" : tr("Dutch"),
		"en" : tr("English"),
		"et" : tr("Estonian"),
		"tl" : tr("Filipino"),
		"fi" : tr("Finnish"),
		"fr" : tr("French"),
		"gl" : tr("Galician"),
		"de" : tr("German"),
		"el" : tr("Greek"),
		"iw" : tr("Hebrew"),
		"hi" : tr("Hindi"),
		"hu" : tr("Hungarian"),
		"is" : tr("Icelandic"),
		"id" : tr("Indonesian"),
		"ga" : tr("Irish"),
		"it" : tr("Italian"),
		"ja" : tr("Japanese"),
		"ko" : tr("Korean"),
		"lv" : tr("Latvian"),
		"lt" : tr("Lithuanian"),
		"mk" : tr("Macedonian"),
		"ms" : tr("Malay"),
		"mt" : tr("Maltese"),
		"no" : tr("Norwegian"),
		"fa" : tr("Persian"),
		"pl" : tr("Polish"),
		"pt" : tr("Portuguese"),
		"ro" : tr("Romanian"),
		"ru" : tr("Russian"),
		"sr" : tr("Serbian"),
		"sk" : tr("Slovak"),
		"sl" : tr("Slovenian"),
		"es" : tr("Spanish"),
		"sw" : tr("Swahili"),
		"sv" : tr("Swedish"),
		"th" : tr("Thai"),
		"tr" : tr("Turkish"),
		"uk" : tr("Ukrainian"),
		"vi" : tr("Vietnamese"),
		"cy" : tr("Welsh"),
		"yi" : tr("Yiddish")
	}

	LangsListObject = []
	for langs_codes_dict_object_key in LangsCodesDictObject.keys() :
		LangsListObject.append({
				"name" : Qt.QString(LangsCodesDictObject[langs_codes_dict_object_key]),
				"code" : Qt.QString(langs_codes_dict_object_key)
			})
	sortLangsList(LangsListObject)


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

