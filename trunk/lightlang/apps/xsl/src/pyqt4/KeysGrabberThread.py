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
import Xlib.X
import Config
import Const


#####
Key_L = Xlib.XK.XK_L
Key_F1 = Xlib.XK.XK_F1
CtrlModifier = Xlib.X.ControlMask
AltModifier = Xlib.X.Mod1Mask
ShiftModifier = Xlib.X.ShiftMask
WinModifier = Xlib.X.Mod4Mask


#####
def tr(str) :
	return Qt.QApplication.translate("@default", str)


#####
class KeysGrabberThread(Qt.QThread) :
	def __init__(self, parent = None) :
		Qt.QThread.__init__(self, parent)

		#####

		self.handlers_list = []

		self.display = Xlib.display.Display()
		self.root = self.display.screen().root
		self.root.change_attributes(event_mask = Xlib.X.PropertyChangeMask|Xlib.X.KeyPressMask)

		#####

		self.connect(Qt.QApplication.instance(), Qt.SIGNAL("aboutToQuit()"), self.stop)


	### Public ###

	def addHandler(self, key, modifier, handler) :
		self.exit(0)

		key = self.display.keysym_to_keycode(key)
		modifier = modifier & ~(Xlib.X.AnyModifier << 1)

		self.handlers_list.append([key, modifier, handler])
		self.root.grab_key(key, modifier, True, Xlib.X.GrabModeAsync, Xlib.X.GrabModeAsync)

		self.start()


	### Private ###

	def run(self) :
		while True :
			event = self.root.display.next_event()
			if event.type != Xlib.X.KeyRelease :
				continue

			for handlers_list_item in self.handlers_list :
				if event.detail == handlers_list_item[0] and (event.state & handlers_list_item[1]) == handlers_list_item[1] :
					handlers_list_item[2]()

	def stop(self) :
		self.exit(0)

		for handlers_list_item in self.handlers_list :
			self.root.ungrab_key(handlers_list_item[0], handlers_list_item[1])

