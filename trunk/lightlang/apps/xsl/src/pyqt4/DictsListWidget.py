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
import DictsListWidgetItem


#####
def tr(str) :
	return Qt.QApplication.translate("@default", str)


#####
class DictsListWidget(Qt.QTableWidget) :
	def __init__(self, parent = None) :
		Qt.QTableWidget.__init__(self, parent)

		self.setColumnCount(1)
		self.setRowCount(0)

		self.horizontalHeader().hide()
		self.horizontalHeader().setStretchLastSection(True)

		self.verticalHeader().setResizeMode(Qt.QHeaderView.Fixed)

		self.setHorizontalScrollBarPolicy(Qt.Qt.ScrollBarAlwaysOff)

		self.setSelectionMode(Qt.QAbstractItemView.SingleSelection)

		self.setAlternatingRowColors(True)

		#####

		self.item_code_regexp = Qt.QRegExp("\\{(.+)\\}\\{(\\d)\\}")

		#####

		self.connect(self, Qt.SIGNAL("cellActivated(int, int)"), self.invertDictState)
		self.connect(self, Qt.SIGNAL("currentCellChanged(int, int, int, int)"), self.currentRowChanged)

		self.connect(self.verticalHeader(), Qt.SIGNAL("sectionClicked(int)"), self.setCurrentRow)


	### Public ###

	def setList(self, list) :
		self.setRowCount(0)

		count = 0
		while count < list.count() :
			Qt.QCoreApplication.processEvents(Qt.QEventLoop.ExcludeUserInputEvents)

			if not self.item_code_regexp.exactMatch(list[count]) :
				count += 1
				continue

			dict_name = self.item_code_regexp.cap(1)

			if self.item_code_regexp.cap(2).toInt()[0] > 0 :
				enable_dict_state = Qt.Qt.Checked
			else :
				enable_dict_state = Qt.Qt.Unchecked

			self.insertDictItem(DictsListWidgetItem.DictsListWidgetItem(dict_name, enable_dict_state))

			count += 1

		if count > 0 :
			self.setCurrentCell(0, 0)
			self.currentRowChangedSignal(0)

		self.dictsListChangedSignal()

	def list(self) :
		list = Qt.QStringList()

		count = 0
		while count < self.rowCount() :
			Qt.QCoreApplication.processEvents(Qt.QEventLoop.ExcludeUserInputEvents)

			item = self.cellWidget(count, 0)

			dict_name = item.dictName()

			if item.dictState() == Qt.Qt.Checked :
				enable_dict_flag = 1
			else :
				enable_dict_flag = 0

			list << Qt.QString("{%1}{%2}").arg(dict_name).arg(enable_dict_flag)

			count += 1

		return list

	###

	def dictsList(self) :
		list = Qt.QStringList()

		count = 0
		while count < self.rowCount() :
			Qt.QCoreApplication.processEvents(Qt.QEventLoop.ExcludeUserInputEvents)

			item = self.cellWidget(count, 0)

			if item.dictState() == Qt.Qt.Checked :
				list << item.dictName()

			count += 1

		return list

	###

	def up(self) :
		index = self.currentRow()
		if self.isUpAvailable(index) :
			item = self.takeDictItem(index)
			self.insertDictItem(item, index -1)
			self.setCurrentCell(index -1, 0)
			self.dictsListChangedSignal()

	def down(self) :
		index = self.currentRow()
		if self.isDownAvailable(index) :
			item = self.takeDictItem(index)
			self.insertDictItem(item, index +1)
			self.setCurrentCell(index +1, 0)
			self.dictsListChangedSignal()

	###

	def setFilter(self, str) :
		count = 0
		while count < self.rowCount() :
			item = self.cellWidget(count, 0)

			dict = Qt.QString("%1.%2").arg(item.dictCaption()).arg(item.dictDirection())
			if not dict.contains(str, Qt.Qt.CaseInsensitive) :
				self.hideRow(count)
			else :
				self.showRow(count)

			count += 1


	### Private ###

	def insertDictItem(self, item, index = -1) :
		if index < 0 or index > self.rowCount() :
			self.insertRow(self.rowCount())
			index = self.rowCount() -1
		else :
			self.insertRow(index)

		self.setRowHeight(index, item.height())
		self.setCellWidget(index, 0, item)

		self.connect(item, Qt.SIGNAL("stateChanged(int)"), self.dictsListChangedSignal)

	def takeDictItem(self, index) :
		if index < 0 or index >= self.rowCount() :
			return None

		internal_widget = self.cellWidget(index, 0)
		external_widget = DictsListWidgetItem.DictsListWidgetItem(internal_widget.dictName(), internal_widget.dictState())

		self.removeRow(index)

		return external_widget

	###

	def setCurrentRow(self, index) :
		self.setCurrentCell(index, 0)

	###

	def isUpAvailable(self, index) :
		if 0 < index < self.rowCount() :
			return True
		else :
			return False

	def isDownAvailable(self, index) :
		if 0 <= index < self.rowCount() -1 :
			return True
		else :
			return False

	###

	def currentRowChanged(self, index) :
		self.setCurrentCell(index, 0)
		self.currentRowChangedSignal(index)

		if self.isUpAvailable(index) :
			self.upAvailableSignal(True)
		else :
			self.upAvailableSignal(False)

		if self.isDownAvailable(index) :
			self.downAvailableSignal(True)
		else :
			self.downAvailableSignal(False)

	###

	def invertDictState(self, index) :
		self.cellWidget(index, 0).invertDictState()


	### Signals ###

	def currentRowChangedSignal(self, index) :
		self.emit(Qt.SIGNAL("currentRowChanged(int)"), index)

	def dictsListChangedSignal(self) :
		self.emit(Qt.SIGNAL("dictsListChanged(const QStringList &)"), self.dictsList())

	def upAvailableSignal(self, up_available_flag) :
		self.emit(Qt.SIGNAL("upAvailable(bool)"), up_available_flag)

	def downAvailableSignal(self, down_available_flag) :
		self.emit(Qt.SIGNAL("downAvailable(bool)"), down_available_flag)


	### Events ###

	def keyPressEvent(self, event) :
		if event.modifiers() == Qt.Qt.ControlModifier :
			if event.key() == Qt.Qt.Key_Up :
				self.up()
			elif event.key() == Qt.Qt.Key_Down :
				self.down()
		else :
			Qt.QTableWidget.keyPressEvent(self, event)

