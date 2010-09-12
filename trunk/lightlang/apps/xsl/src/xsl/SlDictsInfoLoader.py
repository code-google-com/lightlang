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
import IconsLoader
import LangsList


#####
AllDictsDir = Config.DataRootDir+"/sl/dicts/"

CaptionInfoTag = "Caption"
DirectionInfoTag = "Direction"
GroupInfoTag = "Group"
VersionInfoTag = "Version"
WordCountInfoTag = "WordCount"
FileSizeInfoTag = "FileSize"
AuthorInfoTag = "Author"
UrlInfoTag = "Url"
LicenseInfoTag = "License"
CopyrightInfoTag = "Copyright"
MiscInfoTag = "Misc"

AllTagsList = [
	CaptionInfoTag, DirectionInfoTag, GroupInfoTag, VersionInfoTag,
	WordCountInfoTag, FileSizeInfoTag, AuthorInfoTag, UrlInfoTag,
	LicenseInfoTag, CopyrightInfoTag, MiscInfoTag
]

#####
InfoDictObject = {}


#####
def tr(str) :
	return Qt.QApplication.translate("@default", str)


##### Public #####
def caption(dict_name) :
	return Qt.QString(infoByTag(CaptionInfoTag, dict_name))

def direction(dict_name) :
	return Qt.QString(infoByTag(DirectionInfoTag, dict_name))

def group(dict_name) :
	return Qt.QString(infoByTag(GroupInfoTag, dict_name))

def version(dict_name) :
	return Qt.QString(infoByTag(VersionInfoTag, dict_name))

def wordCount(dict_name) :
	return Qt.QString(infoByTag(WordCountInfoTag, dict_name))

def fileSize(dict_name) :
	return Qt.QString(infoByTag(FileSizeInfoTag, dict_name))

def author(dict_name) :
	return Qt.QString(infoByTag(AuthorInfoTag, dict_name))

def url(dict_name) :
	return Qt.QString(infoByTag(UrlInfoTag, dict_name))

def license(dict_name) :
	return Qt.QString(infoByTag(LicenseInfoTag, dict_name))

def copyright(dict_name) :
	return Qt.QString(infoByTag(CopyrightInfoTag, dict_name))

def miscInfo(dict_name) :
	return Qt.QString(infoByTag(MiscInfoTag, dict_name))


def infoByTag(tag, dict_name) :
	if not InfoDictObject.has_key(str(dict_name)) :
		loadInfo(dict_name)

	if InfoDictObject.has_key(str(dict_name)) and InfoDictObject[str(dict_name)].has_key(str(tag)) :
		return Qt.QString(InfoDictObject[str(dict_name)][str(tag)])
	return tr("Unavailable")


def clearInfo(dict_name = None) :
	global InfoDictObject

	if dict_name == None :
		InfoDictObject = {}
	else :
		if InfoDictObject.has_key(str(dict_name)) :
			InfoDictObject.pop(str(dict_name))


##### Private #####
def loadInfo(dict_name) :
	dict_name = str(dict_name)

	global InfoDictObject

	dict_file = Qt.QFile(AllDictsDir+dict_name)
	dict_file_stream = Qt.QTextStream(dict_file)
	if not dict_file.open(Qt.QIODevice.ReadOnly) :
		return

	InfoDictObject[dict_name] = {}
	for all_tags_list_item in AllTagsList :
		InfoDictObject[dict_name][all_tags_list_item] = Qt.QString()

	while not dict_file_stream.atEnd() :
		Qt.QCoreApplication.processEvents(Qt.QEventLoop.ExcludeUserInputEvents)
		line = dict_file_stream.readLine()

		if line.isEmpty() :
			continue
		if line[0] != "#" and line.contains("  ") :
			break

		if line[0] == "#" :
			line.remove(0, 1)
			line = line.trimmed()

			key = MiscInfoTag
			for key_item in InfoDictObject[dict_name].keys() :
				tag = Qt.QString(key_item+":")
				if line.startsWith(tag) :
					line = line.remove(0, tag.length()).simplified()
					key = key_item
					break

			if not InfoDictObject[dict_name][key].isEmpty() :
				InfoDictObject[dict_name][key].append("<br>")
			InfoDictObject[dict_name][key].append(line)

	dict_file.close()

	###

	InfoDictObject[dict_name][FileSizeInfoTag] = Qt.QString().setNum(dict_file.size() / 1024)

	direction_regexp = Qt.QRegExp("((..)-(..))")
	if direction_regexp.exactMatch(InfoDictObject[dict_name][DirectionInfoTag]) :
		icon_width = icon_height = Qt.QApplication.style().pixelMetric(Qt.QStyle.PM_SmallIconSize)
		InfoDictObject[dict_name][DirectionInfoTag] = (
			Qt.QString("<img src=\"%3\" width=\"%1\" height=\"%2\"> &#187; <img src=\"%4\" width=\"%1\" height=\"%2\">"
			"&nbsp;&nbsp;&nbsp;%5 &#187; %6 (%7)").arg(icon_width).arg(icon_height)
			.arg(IconsLoader.iconPath("flags/"+direction_regexp.cap(2)))
			.arg(IconsLoader.iconPath("flags/"+direction_regexp.cap(3)))
			.arg(LangsList.langName(direction_regexp.cap(2))).arg(LangsList.langName(direction_regexp.cap(3)))
			.arg(direction_regexp.cap(1)) )
		
	for key_item in InfoDictObject[dict_name].keys() :
		if InfoDictObject[dict_name][key_item].isEmpty() :
			InfoDictObject[dict_name][key_item] = tr("Unavailable")

