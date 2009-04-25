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
import Xlib
import Xlib.display
import Config
import Const


#####
LeftCtrlModifier = 133
LeftAltModifier = 256
LeftShiftModifier = 194
LeftWinModifier = 451
RightCtrlModifier = 421
RightAltModifier = 449
RightShiftModifier = 230
RightWinModifier = 452
NoModifier = -1


#####
Display = None


#####
def tr(str) :
	return Qt.QApplication.translate("@default", str)


#####
def checkModifier(modifier) :
	if Display == None :
		initDisplay()

	if modifier == NoModifier :
		return True

	keymap = Display.query_keymap()
	keys = []

	for count1 in range(0, len(keymap)) :
		Qt.QCoreApplication.processEvents()
		for count2 in range(0, 32) :
			keys.append(int(keymap[count1] & (1 << count2)))

	if keys[modifier] != 0 :
		return True
	else :
		return False


#####
def initDisplay() :
	global Display
	Display = Xlib.display.Display()

