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
try : # Optional python-xlib requires
	import KeyboardModifiers
except : pass


#####
def tr(str) :
	return Qt.QApplication.translate("@default", str)


#####
class MouseSelector(Qt.QObject) :
	def __init__(self, parent = None) :
		Qt.QObject.__init__(self, parent)

		#####

		self.clipboard = Qt.QApplication.clipboard()
		self.old_selection = Qt.QString()

		self.timer = Qt.QTimer()
		self.timer.setInterval(300)

		try :
			self.modifier = KeyboardModifiers.LeftCtrlModifier
		except : pass

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

		try :
			if not KeyboardModifiers.checkModifier(self.modifier) :
				return
		except : pass

		self.selectionChangedSignal(word)


	### Signals ###

	def selectionChangedSignal(self, word) :
		self.emit(Qt.SIGNAL("selectionChanged(const QString &)"), word)

