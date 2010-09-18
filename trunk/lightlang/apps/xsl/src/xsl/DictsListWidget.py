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
import DictsListWidgetItem


##### Public classes #####
class DictsListWidget(Qt.QTableWidget) :
	def __init__(self, parent = None) :
		Qt.QTableWidget.__init__(self, parent)

		self.setColumnCount(1)
		self.setRowCount(0)

		self.horizontalHeader().hide()
		self.horizontalHeader().setStretchLastSection(True)
		self.verticalHeader().setResizeMode(Qt.QHeaderView.Fixed)
		self.setHorizontalScrollBarPolicy(Qt.Qt.ScrollBarAlwaysOff)

		self.setMouseTracking(True)
		self.setSelectionBehavior(Qt.QAbstractItemView.SelectRows)
		self.setSelectionMode(Qt.QAbstractItemView.SingleSelection)
		self.setDragEnabled(True)
		self.setDragDropMode(Qt.QAbstractItemView.InternalMove)
		self.setAcceptDrops(True)
		self.setDropIndicatorShown(True)

		self.setAlternatingRowColors(True)

		#####

		self._item_code_regexp = Qt.QRegExp("\\{(\\d)\\}\\{(.+)\\}")

		self._start_drag_point = Qt.QPoint()
		self._pressed_drag_index = -1
		self._last_drag_move_y = -1

		self._scroll_timer = Qt.QTimer()
		self._scroll_timer.setInterval(200)

		#####

		self.connect(self, Qt.SIGNAL("cellActivated(int, int)"), self.invertDictState)
		self.connect(self, Qt.SIGNAL("currentCellChanged(int, int, int, int)"), self.currentRowChanged)

		self.connect(self._scroll_timer, Qt.SIGNAL("timeout()"), self.dragMoveScroll)

		self.connect(self.verticalHeader(), Qt.SIGNAL("sectionClicked(int)"), self.setCurrentRow)


	### Public ###

	def setList(self, list) :
		self.setRowCount(0)

		count = 0
		while count < list.count() :
			Qt.QCoreApplication.processEvents(Qt.QEventLoop.ExcludeUserInputEvents)
			if not self._item_code_regexp.exactMatch(list[count]) :
				count += 1
				continue
			dict_state = ( Qt.Qt.Checked if self._item_code_regexp.cap(1).toInt()[0] == 1 else Qt.Qt.Unchecked )
			dict_name = self._item_code_regexp.cap(2)
			self.insertDictItem(DictsListWidgetItem.DictsListWidgetItem(dict_state, dict_name))
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
			enable_dict_flag = ( 1 if self.cellWidget(count, 0).dictState() == Qt.Qt.Checked else 0 )
			dict_name = self.cellWidget(count, 0).dictName()
			list << Qt.QString("{%1}{%2}").arg(enable_dict_flag).arg(dict_name)
			count += 1

		return list

	###

	def dictsList(self) :
		list = Qt.QStringList()

		count = 0
		while count < self.rowCount() :
			Qt.QCoreApplication.processEvents(Qt.QEventLoop.ExcludeUserInputEvents)
			if self.cellWidget(count, 0).dictState() == Qt.Qt.Checked :
				list << self.cellWidget(count, 0).dictName()
			count += 1

		return list

	###

	def up(self) :
		index = self.currentRow()
		if self.isUpAvailable(index) :
			self.insertDictItem(self.takeDictItem(index), index - 1)
			self.setCurrentCell(index - 1, 0)
			self.dictsListChangedSignal()

	def down(self) :
		index = self.currentRow()
		if self.isDownAvailable(index) :
			self.insertDictItem(self.takeDictItem(index), index + 1)
			self.setCurrentCell(index + 1, 0)
			self.dictsListChangedSignal()

	###

	def setFilter(self, str) :
		count = 0
		while count < self.rowCount() :
			item = self.cellWidget(count, 0)

			dict_name = item.dictName()
			dict_name.replace("_", " ")
			dict_name.replace(".", " ")

			if not dict_name.contains(str, Qt.Qt.CaseInsensitive) :
				self.hideRow(count)
			else :
				self.showRow(count)

			count += 1


	### Private ###

	def insertDictItem(self, item, index = -1) :
		if index < 0 or index > self.rowCount() :
			self.insertRow(self.rowCount())
			index = self.rowCount() - 1
		else :
			self.insertRow(index)

		self.setRowHeight(index, item.height())
		self.setCellWidget(index, 0, item)

		self.connect(item, Qt.SIGNAL("stateChanged(int)"), self.dictsListChangedSignal)

	def takeDictItem(self, index) :
		if index < 0 or index >= self.rowCount() :
			return None

		dict_state = self.cellWidget(index, 0).dictState()
		dict_name = self.cellWidget(index, 0).dictName()

		item = DictsListWidgetItem.DictsListWidgetItem(dict_state, dict_name)

		self.removeRow(index)

		return item

	###

	def setCurrentRow(self, index) :
		self.setCurrentCell(index, 0)

	###

	def isUpAvailable(self, index) :
		return ( 0 < index < self.rowCount() )

	def isDownAvailable(self, index) :
		return ( 0 <= index < self.rowCount() - 1 )

	###

	def currentRowChanged(self, index) :
		self.setCurrentCell(index, 0)
		self.currentRowChangedSignal(index)

		self.upAvailableSignal(self.isUpAvailable(index))
		self.downAvailableSignal(self.isDownAvailable(index))

	###

	def invertDictState(self, index) :
		self.cellWidget(index, 0).invertDictState()

	###

	def dragMoveScroll(self) :
		if self._last_drag_move_y < self.height() / 10 :
			self.verticalScrollBar().setValue(self.verticalScrollBar().value() - 1)
		elif self.height() - self._last_drag_move_y < self.height() / 10 :
			self.verticalScrollBar().setValue(self.verticalScrollBar().value() + 1)


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

	###

	def mousePressEvent(self, event) :
		if event.button() == Qt.Qt.LeftButton and self.indexAt(event.pos()).row() > -1 :
			self._start_drag_point = event.pos()
		Qt.QTableWidget.mousePressEvent(self, event)

	def mouseMoveEvent(self, event) :
		if not ((event.buttons() & Qt.Qt.LeftButton) and self.indexAt(event.pos()).row() > -1) :
			return
		if (event.pos() - self._start_drag_point).manhattanLength() < Qt.QApplication.startDragDistance() :
			return

		self._pressed_drag_index = self.indexAt(event.pos()).row()

		mime_data = Qt.QMimeData()
		mime_data.setData("application/x-dictslistwidgetitem", Qt.QByteArray())

		drag = Qt.QDrag(self)
		drag.setMimeData(mime_data)
		drag.setPixmap(Qt.QPixmap.grabWidget(self.cellWidget(self._pressed_drag_index, 0), 0, 0))
		drag.exec_(Qt.Qt.MoveAction)

	def dragEnterEvent(self, event) :
		if event.mimeData().hasFormat("application/x-dictslistwidgetitem") :
			if event.source() == self :
				event.setDropAction(Qt.Qt.MoveAction)
				event.accept()
			else :
				event.acceptProposedAction()
		else :
			event.ignore()

	def dragMoveEvent(self, event) :
		if event.mimeData().hasFormat("application/x-dictslistwidgetitem") :
			if event.source() == self :
				event.setDropAction(Qt.Qt.MoveAction)
				event.accept()
			else :
				event.acceptProposedAction()
		else :
			event.ignore()

		if event.pos().y() < self.height() / 10 or self.height() - event.pos().y() < self.height() / 10 :
			self._last_drag_move_y = event.pos().y()
			if not self._scroll_timer.isActive() :
				self._scroll_timer.start()
		else :
			if self._scroll_timer.isActive() :
				self._scroll_timer.stop()

	def dropEvent(self, event) :
		if event.mimeData().hasFormat("application/x-dictslistwidgetitem") :
			current_drop_index = self.indexAt(event.pos()).row()

			if self._pressed_drag_index != current_drop_index :
				self.insertDictItem(self.takeDictItem(self._pressed_drag_index), current_drop_index)
				self.setCurrentCell(current_drop_index, 0)

			if event.source() == self :
				event.setDropAction(Qt.Qt.MoveAction)
				event.accept()
			else :
				event.acceptProposedAction()
		else :
			event.ignore()

		if self._scroll_timer.isActive() :
			self._scroll_timer.stop()

