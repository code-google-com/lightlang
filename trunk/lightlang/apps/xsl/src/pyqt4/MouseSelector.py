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
try : # optional requires python-xlib
	import Xlib
	import Xlib.display
	PythonXlibExistsFlag = True
except :
	PythonXlibExistsFlag = False
	print Const.MyName+": python-xlib is not found, please, install it"

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
def tr(str) :
	return Qt.QApplication.translate("@default", str)

#####
class MouseSelector(Qt.QObject) :
	def __init__(self, parent = None) :
		Qt.QObject.__init__(self, parent)

		self.clipboard = Qt.QApplication.clipboard()
		self.old_selection = Qt.QString()

		self.timer = Qt.QTimer()
		self.timer.setInterval(300)

		if PythonXlibExistsFlag :
			self.display = Xlib.display.Display()

		self.modifier = LeftCtrlModifier

		#####

		self.connect(self.timer, Qt.SIGNAL("timeout()"), self.checkSelection)


	### Public ###

	def start(self) :
		self.clipboard.setText(Qt.QString(""), Qt.QClipboard.Selection)
		self.old_selection.clear()
		self.timer.start()

	def stop(self) :
		self.timer.stop()

	def setModifier(self, modifier) :
		self.modifier = modifier


	### Private ###

	def checkSelection(self) :
		word = self.clipboard.text(Qt.QClipboard.Selection)
		word = word.simplified()
		if word.isEmpty() :
			return
		word = word.toLower()

		if word == self.old_selection :
			return
		self.old_selection = word

		# TODO: add mouse-buttons checks
		if not self.checkModifier() :
			return

		self.selectionChangedSignal(word)

	def checkModifier(self) :
		if not PythonXlibExistsFlag :
			return True

		if self.modifier == NoModifier :
			return True

		keymap = self.display.query_keymap()
		keys = []

		for count1 in range(0, len(keymap)) :
			Qt.QCoreApplication.processEvents()
			for count2 in range(0, 32) :
				keys.append(int(keymap[count1] & (1 << count2)))

		if keys[self.modifier] != 0 :
			return True
		else :
			return False


	### Signals ###

	def selectionChangedSignal(self, word) :
		self.emit(Qt.SIGNAL("selectionChanged(const QString &)"), word)

