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
import Xlib.display
import Xlib.XK
import Config
import Const


#####
LeftCtrlModifier = Xlib.XK.XK_Control_L
LeftAltModifier = Xlib.XK.XK_Alt_L
LeftShiftModifier = Xlib.XK.XK_Shift_L
LeftWinModifier = Xlib.XK.XK_Super_L
RightCtrlModifier = Xlib.XK.XK_Control_R
RightAltModifier = Xlib.XK.XK_Alt_R
RightShiftModifier = Xlib.XK.XK_Shift_R
RightWinModifier = Xlib.XK.XK_Super_R
NoModifier = -1


#####
DisplayObject = None


#####
def tr(str) :
	return Qt.QApplication.translate("@default", str)


#####
def checkModifier(modifier) :
	if DisplayObject == None :
		initDisplay()

	if modifier == NoModifier :
		return True

	keymap = DisplayObject.query_keymap()
	keycode = DisplayObject.keysym_to_keycode(modifier)

	return 1 & (keymap[keycode / 8] >> (keycode & 7))


#####
def initDisplay() :
	global DisplayObject
	DisplayObject = Xlib.display.Display()

