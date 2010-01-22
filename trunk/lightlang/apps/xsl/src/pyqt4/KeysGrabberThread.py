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


##### Private #####
class KeysGrabberThreadPrivate(Qt.QThread) :
	def __init__(self, parent = None) :
		Qt.QThread.__init__(self, parent)

		#####

		self.is_stopped_flag = True

		self.hotkeys_list = []

		self.display = Xlib.display.Display()
		self.root = self.display.screen().root
		self.root.change_attributes(event_mask = Xlib.X.PropertyChangeMask|Xlib.X.KeyPressMask)

		#####

		self.connect(Qt.QApplication.instance(), Qt.SIGNAL("aboutToQuit()"), self.stop)


	### Public ###

	def addHotkey(self, object_name, key, modifier) :
		self.is_stopped_flag = True
		if not self.wait(100) :
			self.terminate()

		key = self.display.keysym_to_keycode(key)
		modifier = modifier & ~(Xlib.X.AnyModifier << 1)
		signal = Qt.QString("%1__%2__%3__globalHotkey()").arg(object_name).arg(key).arg(modifier)

		self.hotkeys_list.append([key, modifier, signal])
		self.root.grab_key(key, modifier, True, Xlib.X.GrabModeAsync, Xlib.X.GrabModeAsync)

		self.is_stopped_flag = False
		self.start()

		return signal


	### Private ###

	def run(self) :
		while not self.is_stopped_flag :
			event = self.root.display.next_event()
			if event.type != Xlib.X.KeyRelease :
				continue

			for hotkeys_list_item in self.hotkeys_list :
				if event.detail == hotkeys_list_item[0] and (event.state & hotkeys_list_item[1]) == hotkeys_list_item[1] :
					self.emit(Qt.SIGNAL(hotkeys_list_item[2]))

	def stop(self) :
		self.is_stopped_flag = True
		if not self.wait(100) :
			self.terminate()

		for hotkeys_list_item in self.hotkeys_list :
			self.root.ungrab_key(hotkeys_list_item[0], hotkeys_list_item[1])


##### Public #####
class KeysGrabberThread(KeysGrabberThreadPrivate) :
	keys_grabber_thread_private_object = None

	def __new__(self, parent = None) :
		if self.keys_grabber_thread_private_object == None :
			self.keys_grabber_thread_private_object = KeysGrabberThreadPrivate.__new__(self, parent)
		return self.keys_grabber_thread_private_object

