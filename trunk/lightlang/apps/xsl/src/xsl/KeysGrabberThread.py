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


import Xlib.display
import Xlib.XK
import Xlib.X

import Qt
import Config
import Const


##### Public constants #####
Key_L = Xlib.XK.XK_L
Key_F1 = Xlib.XK.XK_F1

CtrlModifier = Xlib.X.ControlMask
AltModifier = Xlib.X.Mod1Mask
ShiftModifier = Xlib.X.ShiftMask
WinModifier = Xlib.X.Mod4Mask


##### Public classes #####
class KeysGrabberThread(KeysGrabberThreadPrivate) :
	_keys_grabber_thread_private_object = None

	def __new__(self, parent = None) :
		if self._keys_grabber_thread_private_object == None :
			self._keys_grabber_thread_private_object = KeysGrabberThreadPrivate.__new__(self, parent)
			KeysGrabberThreadPrivate.__init__(self._keys_grabber_thread_private_object, parent)
		return self._keys_grabber_thread_private_object

	def __init__(self, parent = None) :
		pass


##### Private classes #####
class KeysGrabberThreadPrivate(Qt.QThread) :
	def __init__(self, parent = None) :
		Qt.QThread.__init__(self, parent)

		#####

		self._is_stopped_flag = True

		self._hotkeys_list = []

		self._display = Xlib.display.Display()
		self._root = self._display.screen().root
		self._root.change_attributes(event_mask = Xlib.X.PropertyChangeMask|Xlib.X.KeyPressMask)

		#####

		self.connect(Qt.QApplication.instance(), Qt.SIGNAL("aboutToQuit()"), self.stop)


	### Public ###

	def addHotkey(self, object_name, key, modifier) :
		self._is_stopped_flag = True
		if not self.wait(100) :
			self.terminate()

		key = self._display.keysym_to_keycode(key)
		modifier = modifier & ~(Xlib.X.AnyModifier << 1)
		signal_string = Qt.QString("%1__%2__%3__globalHotkey()").arg(object_name).arg(key).arg(modifier)

		self._hotkeys_list.append({ "key" : key, "modifier" : modifier, "signal_string" : signal_string })
		self._root.grab_key(key, modifier, True, Xlib.X.GrabModeAsync, Xlib.X.GrabModeAsync)

		self._is_stopped_flag = False
		self.start()

		return Qt.QString(signal_string)


	### Private ###

	def run(self) :
		while not self._is_stopped_flag :
			event = self._root.display.next_event()
			if event.type != Xlib.X.KeyRelease :
				continue

			for hotkeys_list_item in self._hotkeys_list :
				if ( (event.state & hotkeys_list_item["modifier"]) == hotkeys_list_item["modifier"] and
					event.detail == hotkeys_list_item["key"] ) :
					self.emit(Qt.SIGNAL(hotkeys_list_item["signal_string"]))

	def stop(self) :
		self._is_stopped_flag = True
		if not self.wait(100) :
			self.terminate()

		for hotkeys_list_item in self._hotkeys_list :
			self._root.ungrab_key(hotkeys_list_item["key"], hotkeys_list_item["modifier"])

