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


##### Public classes #####
class RadioButtonsMenu(Qt.QMenu) :
	def __init__(self, title, parent = None) :
		Qt.QMenu.__init__(self, title, parent)

		#####

		self._actions_list = []
		self._actions_group = Qt.QActionGroup(self)

		#####

		self.connect(self._actions_group, Qt.SIGNAL("triggered(QAction *)"), self.dataChangedSignal)


	### Public ###

	def data(self, index = -1) :
		if index < 0 :
			index = self.index()
		return self._actions_list[index].data()


	### Private ###

	def index(self) :
		for count in xrange(len(self._actions_list)) :
			if self._actions_list[count].isChecked() :
				return count

	def setIndex(self, index) :
		self._actions_list[index].setChecked(True)
		self.dataChangedSignal(self._actions_list[index])

	def addRadioButton(self, title, data) :
		action = Qt.QAction(title, self)
		action.setCheckable(True)
		action.setData(Qt.QVariant(data))

		self.addAction(action)
		self._actions_list.append(action)
		self._actions_group.addAction(action)


	### Signals ###

	def dataChangedSignal(self, action) :
		self.emit(Qt.SIGNAL("dataChanged(const QVariant &)"), action.data())

