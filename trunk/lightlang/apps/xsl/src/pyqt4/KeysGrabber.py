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
import Xlib.display
import Xlib.XK
import Xlib.X

#####
def tr(str) :
	return Qt.QApplication.translate("@default", str)


#####
class KeysGrabber(Qt.QThread) :
	def __init__(self) :
		Qt.QThread.__init__(self)

		#####

		self.functions_list = []

		self.display = Xlib.display.Display()
		self.root = self.display.screen().root
		self.root.change_attributes(event_mask=Xlib.X.PropertyChangeMask|Xlib.X.KeyPressMask)

		#####

		self.connect(Qt.qApp, Qt.SIGNAL("aboutToQuit()"), lambda : self.exit(0))


	### Public ###

	def addFunction(self, keysym, modifier_mask, function) :
		self.exit(0)

		keycode = self.display.keysym_to_keycode(getattr(Xlib.XK, keysym))

		if modifier_mask == None :
			modifier_mask = -1
		else :
			modifier_mask = getattr(Xlib.X, modifier_mask)

		self.functions_list.append([keycode, modifier_mask, function])

		self.root.grab_key(self.functions_list[len(self.functions_list) -1][0], Xlib.X.AnyModifier,
			True, Xlib.X.GrabModeAsync, Xlib.X.GrabModeAsync)

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
					if event.detail == function[0] and (event.state & function[1]) == function[1] and function[1] != -1 :
						has_right_function_flag = True
						function[2]()

				if not has_right_function_flag :
					for function in self.functions_list :
						if event.detail == function[0] and function[1] == -1 :
							function[2]()
			except : pass

