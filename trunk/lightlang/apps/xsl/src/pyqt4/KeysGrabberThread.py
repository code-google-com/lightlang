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
Key_F1 = Xlib.XK.XK_F1
Key_F2 = Xlib.XK.XK_F2
Key_F3 = Xlib.XK.XK_F3
Key_F4 = Xlib.XK.XK_F4
Key_F5 = Xlib.XK.XK_F5
Key_F6 = Xlib.XK.XK_F6
Key_F7 = Xlib.XK.XK_F7
Key_F8 = Xlib.XK.XK_F8
Key_F9 = Xlib.XK.XK_F9
Key_F10 = Xlib.XK.XK_F10
Key_F11 = Xlib.XK.XK_F11
Key_F12 = Xlib.XK.XK_F12
CtrlModifier = Xlib.X.ControlMask
ShiftModifier = Xlib.X.ShiftMask


#####
def tr(str) :
	return Qt.QApplication.translate("@default", str)


#####
class KeysGrabberThread(Qt.QThread) :
	def __init__(self, parent = None) :
		Qt.QThread.__init__(self, parent)

		#####

		self.functions_list = []

		self.display = Xlib.display.Display()
		self.root = self.display.screen().root
		self.root.change_attributes(event_mask = Xlib.X.PropertyChangeMask|Xlib.X.KeyPressMask)

		#####

		self.connect(Qt.QApplication.instance(), Qt.SIGNAL("aboutToQuit()"), self.stop)


	### Public ###

	def addFunction(self, key, modifier, function) :
		self.exit(0)

		key = self.display.keysym_to_keycode(key)
		self.functions_list.append([key, modifier, function])
		self.root.grab_key(key, modifier, True, Xlib.X.GrabModeAsync, Xlib.X.GrabModeAsync)

		self.start()


	### Private ###

	def run(self) :
		while True :
			try :
				event = self.root.display.next_event()
				if event.type != Xlib.X.KeyRelease :
					continue

				has_right_function_flag = False

				for function in self.functions_list :
					if ( event.detail == function[0] and (event.state & function[1]) == function[1] and
						function[1] != Xlib.X.AnyModifier ) :
						has_right_function_flag = True
						function[2]()

				if not has_right_function_flag :
					for function in self.functions_list :
						if event.detail == function[0] and function[1] == Xlib.X.AnyModifier :
							function[2]()
			except : pass

	def stop(self) :
		self.exit(0)

		for function in self.functions_list :
			self.root.ungrab_key(function[0], function[1])

