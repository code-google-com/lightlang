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
SettingsPostfix = ".conf"


#####
SettingsObject = None


##### Public #####
def settings() :
	if SettingsObject == None :
		initSettings()
	return SettingsObject


def settingsPath() :
	if SettingsObject == None :
		initSettings()

	user_settings_file_path = SettingsObject.fileName()

	index = user_settings_file_path.lastIndexOf("/")
	return ( user_settings_file_path.left(index) if index >= 0 else Qt.QString() )


##### Private #####
def initSettings() :
	my_name = Qt.QString(Const.MyName).toLower()

	if not Qt.QDir(Qt.QDir.homePath()+"/."+my_name).exists() :
		Qt.QDir.home().mkdir("."+my_name)

	global SettingsObject
	SettingsObject = Qt.QSettings(Qt.QDir.homePath()+"/."+my_name+"/"+my_name+SettingsPostfix, Qt.QSettings.IniFormat)

