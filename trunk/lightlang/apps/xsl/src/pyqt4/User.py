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


from PyQt4 import Qt
import Config
import Const


#####
SettingsPostfix = ".conf"


#####
Settings = None


#####
def tr(str) :
	return Qt.QApplication.translate("@default", str)


##### Public #####
def settings() :
	if Settings == None :
		initSettings()
	return Settings


def settingsPath() :
	if Settings == None :
		initSettings()

	user_settings_file_name = Settings.fileName()

	index = user_settings_file_name.lastIndexOf("/")
	if index >= 0 :
		user_settings_dir_path = user_settings_file_name.left(index)
	else :
		user_settings_dir_path = Qt.QString()

	return user_settings_dir_path


##### Private #####
def initSettings() :
	global Settings

	myname = Qt.QString(Const.MyName).toLower()

	user_settings_dir = Qt.QDir(Qt.QDir.homePath()+"/."+myname)
	if not user_settings_dir.exists() :
		Qt.QDir.home().mkdir("."+myname)

	Settings = Qt.QSettings(Qt.QDir.homePath()+"/."+myname+"/"+myname+SettingsPostfix, Qt.QSettings.IniFormat)

