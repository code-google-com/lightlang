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
from KeysGrabberThreadBase import *


#####
def tr(str) :
	return Qt.QApplication.translate("@default", str)


#####
class KeysGrabberThread(KeysGrabberThreadBase) :
	keys_grabber_thread_base_object = None

	def __new__(self, parent = None) :
		if self.keys_grabber_thread_base_object == None :
			self.keys_grabber_thread_base_object = KeysGrabberThreadBase.__new__(self, parent)
		return self.keys_grabber_thread_base_object

