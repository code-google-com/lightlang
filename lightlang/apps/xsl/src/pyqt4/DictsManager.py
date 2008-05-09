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

#####
MyIcon = Config.Prefix+"/lib/xsl/icons/xsl_16.png"
WaitPicture = Config.Prefix+"/lib/xsl/pictures/circular.gif"

AllDictsDir = Config.Prefix+"/share/sl/dicts/"
IconsDir = Config.Prefix+"/lib/xsl/icons/"

#####
class DictInformationWindow(Qt.QWidget) :
	def __init__(self, dict_name, parent = None) :
		Qt.QWidget.__init__(self, parent)

		self.setWindowTitle(self.tr("Dict Information"))
		self.setWindowIcon(Qt.QIcon(MyIcon))

		self.setMinimumSize(550, 400)
		self.resize(550, 400)

		#####

		self.main_layout = Qt.QVBoxLayout()
		self.setLayout(self.main_layout)

		self.dict_information_browser_layout = Qt.QVBoxLayout()
		self.main_layout.addLayout(self.dict_information_browser_layout)

		self.control_buttons_layout = Qt.QHBoxLayout()
		self.main_layout.addLayout(self.control_buttons_layout)

		#####

		self.dict_name = Qt.QString(dict_name)

		self.is_loaded_flag = False

		#####

		self.dict_information_browser = Qt.QTextBrowser()
		self.dict_information_browser_layout.addWidget(self.dict_information_browser)

		self.wait_picture_movie = Qt.QMovie(WaitPicture)
		icon_width = icon_height = self.style().pixelMetric(Qt.QStyle.PM_SmallIconSize)
		self.wait_picture_movie.setScaledSize(Qt.QSize(icon_width, icon_height))
		self.wait_picture_movie.jumpToFrame(0)
		self.wait_picture_movie_label = Qt.QLabel()
		self.wait_picture_movie_label.setMovie(self.wait_picture_movie)
		self.wait_picture_movie_label.setVisible(False)
		self.control_buttons_layout.addWidget(self.wait_picture_movie_label)

		self.wait_message_label = Qt.QLabel(self.tr("Please wait..."))
		self.wait_message_label.setVisible(False)
		self.control_buttons_layout.addWidget(self.wait_message_label)

		self.control_buttons_layout.addStretch()

		self.update_information_button = Qt.QPushButton(Qt.QIcon(IconsDir+"update_16.png"), self.tr("Update"))
		self.control_buttons_layout.addWidget(self.update_information_button)

		self.ok_button = Qt.QPushButton(Qt.QIcon(IconsDir+"ok_16.png"), self.tr("OK"))
		self.ok_button.setDefault(True)
		self.control_buttons_layout.addWidget(self.ok_button)

		#####

		self.connect(self.update_information_button, Qt.SIGNAL("clicked()"), self.updateInformation)
		self.connect(self.ok_button, Qt.SIGNAL("clicked()"), self.close)


	### Public ###

	def updateInformation(self) :
		if self.dict_name.isEmpty() :
			return

		self.update_information_button.blockSignals(True)

		self.wait_picture_movie_label.setVisible(True)
		self.wait_picture_movie.start()
		self.wait_message_label.setVisible(True)

		###

		dict_information = Qt.QString()

		dict_information.append(self.record(self.tr("Caption:"), self.dictCaption()))
		self.dict_information_browser.setHtml(dict_information)

		dict_information.append(self.record(self.tr("Direction:"), self.dictDirection()))
		self.dict_information_browser.setHtml(dict_information)

		dict_information.append(self.record(self.tr("File path:"), self.dictFilePath()))
		self.dict_information_browser.setHtml(dict_information)

		dict_information.append(self.record(self.tr("File size (KB):"), self.dictFileSize()))
		self.dict_information_browser.setHtml(dict_information)

		dict_description, word_count = self.dictDescriptionAndWordCount()
		dict_information.append(self.record(self.tr("Count of words:"), word_count))
		dict_information.append(self.record(self.tr("Description:"), dict_description))
		self.dict_information_browser.setHtml(dict_information)

		###

		self.wait_picture_movie_label.setVisible(False)
		self.wait_picture_movie.stop()
		self.wait_picture_movie.jumpToFrame(0)
		self.wait_message_label.setVisible(False)

		self.update_information_button.blockSignals(False)

	def show(self) :
		x_window_position = (Qt.QApplication.desktop().width() - self.width()) / 2
		if x_window_position < 0 :
			x_window_position = 0
		y_window_position = (Qt.QApplication.desktop().height() - self.height()) / 2
		if y_window_position < 0 :
			y_window_position = 0

		self.move(Qt.QPoint(x_window_position, y_window_position))

		Qt.QWidget.show(self)
		self.raise_()
		self.activateWindow()

		if not self.is_loaded_flag :
			self.is_loaded_flag = True
			self.updateInformation()


	### Private ###

	def dictCaption(self) :
		index = self.dict_name.lastIndexOf(".")
		if index >= 0 :
			dict_caption = self.dict_name.left(index)
		else :
			dict_caption = Qt.QString(self.dict_name)
		dict_caption.replace("_", " ")
		return dict_caption

	def dictDirection(self) :
		index = self.dict_name.lastIndexOf(".")
		if index >= 0 :
			return self.dict_name.mid(index +1)
		else :
			return self.tr("Unavailable")

	def dictFilePath(self) :
		dict_file_path = Qt.QString(AllDictsDir+self.dict_name)
		if Qt.QFile.exists(dict_file_path) :
			return dict_file_path
		else :
			return self.tr("Unavailable")

	def dictFileSize(self) :
		dict_file = Qt.QFile(AllDictsDir+self.dict_name)
		return Qt.QString().setNum(dict_file.size() / 1024) # KB

	def dictDescriptionAndWordCount(self) :
		dict_file = Qt.QFile(AllDictsDir+self.dict_name)
		dict_file_stream = Qt.QTextStream(dict_file)

		dict_description = Qt.QString()
		word_count = 0

		if dict_file.open(Qt.QIODevice.ReadOnly) :
			first_comment_flag = False
			while not dict_file.atEnd() :
				Qt.QCoreApplication.processEvents(Qt.QEventLoop.ExcludeUserInputEvents)
				str = dict_file_stream.readLine()
				if str.isEmpty() :
					continue
				if str[0] == "#" :
					str.remove(0, 1)
					str.remove("\n")
					str.append("<br>")
					dict_description.append(str)
					continue
				if str.contains("  ") :
					word_count += 1
			dict_file.close()
			dict_description.trimmed()
			dict_description.prepend("<br>")

		if dict_description.isEmpty() :
			dict_description = self.tr("Unavailable")

		return dict_description, Qt.QString().setNum(word_count)

	###

	def record(self, label, text) :
		return Qt.QString("<em><strong><font color=\"#494949\">%1"
			"</font></strong> %2</em><br>").arg(label).arg(text)


#####
class DictsListWidgetItem(Qt.QWidget) :
	def __init__(self, dict_name, enable_dict_state = Qt.Qt.Unchecked, parent = None) :
		Qt.QWidget.__init__(self, parent)

		self.main_layout = Qt.QHBoxLayout()
		self.main_layout.setMargin(5)
		self.main_layout.setSpacing(3)
		self.setLayout(self.main_layout)

		if self.font().pixelSize() > 0 :
			self.setFixedHeight((self.font().pixelSize() + 5) * 2)
		elif self.font().pointSize() > 0 :
			self.setFixedHeight((self.font().pointSize() + 5) * 2)
		else :
			self.setFixedHeight(30)

		#####

		self.dict_name = Qt.QString(dict_name)

		#####

		self.dict_information_window = DictInformationWindow(dict_name)

		#####

		self.enable_dict_checkbox = Qt.QCheckBox()
		self.enable_dict_checkbox.setCheckState(enable_dict_state)
		self.main_layout.addWidget(self.enable_dict_checkbox)

		self.vertical_frame1 = Qt.QFrame()
		self.vertical_frame1.setFrameStyle(Qt.QFrame.VLine|Qt.QFrame.Sunken)
		self.main_layout.addWidget(self.vertical_frame1)

		self.dict_caption_label = Qt.QLabel()
		index = dict_name.lastIndexOf(".")
		if index >= 0 :
			dict_caption = dict_name.left(index)
		else :
			dict_caption = Qt.QString(dict_name)
		dict_caption.replace("_", " ")
		self.dict_caption_label.setText(dict_caption)
		self.main_layout.addWidget(self.dict_caption_label)

		self.main_layout.addStretch()

		self.dict_direction_label = Qt.QLabel()
		index = dict_name.lastIndexOf(".")
		if index >= 0 :
			self.dict_direction_label.setText(dict_name.mid(index +1))
		self.main_layout.addWidget(self.dict_direction_label)

		self.vertical_frame2 = Qt.QFrame()
		self.vertical_frame2.setFrameStyle(Qt.QFrame.VLine|Qt.QFrame.Sunken)
		self.main_layout.addWidget(self.vertical_frame2)

		self.show_information_button = Qt.QToolButton()
		self.show_information_button.setIcon(Qt.QIcon(IconsDir+"info_16.png"))
		self.show_information_button.setIconSize(Qt.QSize(16, 16))
		self.show_information_button.setCursor(Qt.Qt.ArrowCursor)
		self.show_information_button.setAutoRaise(True)
		self.main_layout.addWidget(self.show_information_button)

		#####

		self.connect(self.enable_dict_checkbox, Qt.SIGNAL("stateChanged(int)"), self.stateChangedSignal)

		self.connect(self.show_information_button, Qt.SIGNAL("clicked()"),
			self.dict_information_window.show)


	### Public ###

	def dictName(self) :
		return Qt.QString(self.dict_name)

	def dictCaption(self) :
		return self.dict_caption_label.text()

	def dictDirection(self) :
		return self.dict_direction_label.text()

	def dictState(self) :
		return self.enable_dict_checkbox.checkState()


	### Signals ###

	def stateChangedSignal(self, state) :
		self.emit(Qt.SIGNAL("stateChanged(int)"), state)


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

		self.connect(self, Qt.SIGNAL("currentCellChanged(int, int, int, int)"),
			self.currentRowChanged)

		self.connect(self.verticalHeader(), Qt.SIGNAL("sectionClicked(int)"), self.setCurrentRow)


	### Public ###

	def setList(self, list) :
		item_code_regexp = Qt.QRegExp("\\{(.+)\\}\\{(\\d)\\}")

		self.setRowCount(0)
		count = 0
		while count < list.count() :
			Qt.QCoreApplication.processEvents(Qt.QEventLoop.ExcludeUserInputEvents)

			if not item_code_regexp.exactMatch(list[count]) :
				count += 1
				continue

			dict_name = item_code_regexp.cap(1)

			if item_code_regexp.cap(2).toInt()[0] > 0 :
				enable_dict_state = Qt.Qt.Checked
			else :
				enable_dict_state = Qt.Qt.Unchecked

			self.insertDictItem(DictsListWidgetItem(dict_name, enable_dict_state))

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
			if item == None :
				count += 1
				continue

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
			if item == None :
				count += 1
				continue

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
			if item == None :
				count += 1
				continue

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
		external_widget = DictsListWidgetItem(internal_widget.dictName(), internal_widget.dictState())

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


	### Signals ###

	def currentRowChangedSignal(self, index) :
		self.emit(Qt.SIGNAL("currentRowChanged(int)"), index)

	def dictsListChangedSignal(self) :
		self.emit(Qt.SIGNAL("dictsListChanged(const QStringList &)"), self.dictsList())

	def upAvailableSignal(self, up_available_flag) :
		self.emit(Qt.SIGNAL("upAvailable(bool)"), up_available_flag)

	def downAvailableSignal(self, down_available_flag) :
		self.emit(Qt.SIGNAL("downAvailable(bool)"), down_available_flag)


#####
class DictsManager(Qt.QDialog) :
	def __init__(self, parent = None) :
		Qt.QDialog.__init__(self, parent)

		self.setWindowTitle(self.tr("Dicts Manager"))
		self.setWindowIcon(Qt.QIcon(MyIcon))

		self.resize(400, 550)

		self.main_layout = Qt.QVBoxLayout()
		self.setLayout(self.main_layout)

		self.line_edit_layout = Qt.QHBoxLayout()
		self.main_layout.addLayout(self.line_edit_layout)

		self.dicts_list_layout = Qt.QVBoxLayout()
		self.main_layout.addLayout(self.dicts_list_layout)

		self.dicts_list_buttons_layout = Qt.QHBoxLayout()
		self.main_layout.addLayout(self.dicts_list_buttons_layout)

		self.horizontal_frame = Qt.QFrame()
		self.horizontal_frame.setFrameStyle(Qt.QFrame.HLine|Qt.QFrame.Sunken)
		self.main_layout.addWidget(self.horizontal_frame)

		self.control_buttons_layout = Qt.QHBoxLayout()
		self.main_layout.addLayout(self.control_buttons_layout)

		#####

		self.filter_label = Qt.QLabel(self.tr("Filter:"))
		self.line_edit_layout.addWidget(self.filter_label)

		self.line_edit = Qt.QLineEdit()
		self.line_edit_layout.addWidget(self.line_edit)

		self.clear_line_edit_button = Qt.QToolButton()
		self.clear_line_edit_button.setIcon(Qt.QIcon(IconsDir+"clear_22.png"))
		self.clear_line_edit_button.setIconSize(Qt.QSize(16, 16))
		self.clear_line_edit_button.setEnabled(False)
		self.line_edit_layout.addWidget(self.clear_line_edit_button)

		self.dicts_list = DictsListWidget()
		self.dicts_list_layout.addWidget(self.dicts_list)

		self.up_button = Qt.QToolButton()
		self.up_button.setIcon(Qt.QIcon(IconsDir+"up_22.png"))
		self.up_button.setIconSize(Qt.QSize(22, 22))
		self.up_button.setEnabled(False)
		self.dicts_list_buttons_layout.addWidget(self.up_button)

		self.down_button = Qt.QToolButton()
		self.down_button.setIcon(Qt.QIcon(IconsDir+"down_22.png"))
		self.down_button.setIconSize(Qt.QSize(22, 22))
		self.down_button.setEnabled(False)
		self.dicts_list_buttons_layout.addWidget(self.down_button)

		self.dicts_list_buttons_layout.addStretch()

		self.update_dicts_button = Qt.QToolButton()
		self.update_dicts_button.setIcon(Qt.QIcon(IconsDir+"update_22.png"))
		self.update_dicts_button.setIconSize(Qt.QSize(22, 22))
		self.dicts_list_buttons_layout.addWidget(self.update_dicts_button)

		self.wait_picture_movie = Qt.QMovie(WaitPicture)
		icon_width = icon_height = self.style().pixelMetric(Qt.QStyle.PM_SmallIconSize)
		self.wait_picture_movie.setScaledSize(Qt.QSize(icon_width, icon_height))
		self.wait_picture_movie.jumpToFrame(0)
		self.wait_picture_movie_label = Qt.QLabel()
		self.wait_picture_movie_label.setMovie(self.wait_picture_movie)
		self.wait_picture_movie_label.setVisible(False)
		self.control_buttons_layout.addWidget(self.wait_picture_movie_label)

		self.wait_message_label = Qt.QLabel(self.tr("Please wait..."))
		self.wait_message_label.setVisible(False)
		self.control_buttons_layout.addWidget(self.wait_message_label)

		self.control_buttons_layout.addStretch()

		self.ok_button = Qt.QPushButton(Qt.QIcon(IconsDir+"ok_16.png"), self.tr("OK"))
		self.ok_button.setDefault(True)
		self.control_buttons_layout.addWidget(self.ok_button)

		#####

		self.connect(self.line_edit, Qt.SIGNAL("textChanged(const QString &)"), self.setStatusFromLineEdit)
		self.connect(self.line_edit, Qt.SIGNAL("textChanged(const QString &)"), self.dicts_list.setFilter)
		self.connect(self.clear_line_edit_button, Qt.SIGNAL("clicked()"), self.clearLineEdit)

		self.connect(self.dicts_list, Qt.SIGNAL("upAvailable(bool)"), self.up_button.setEnabled)
		self.connect(self.dicts_list, Qt.SIGNAL("downAvailable(bool)"), self.down_button.setEnabled)
		self.connect(self.dicts_list, Qt.SIGNAL("dictsListChanged(const QStringList &)"),
			self.dictsListChangedSignal)

		self.connect(self.up_button, Qt.SIGNAL("clicked()"), self.dicts_list.up)

		self.connect(self.down_button, Qt.SIGNAL("clicked()"), self.dicts_list.down)

		self.connect(self.update_dicts_button, Qt.SIGNAL("clicked()"), self.updateDicts)

		self.connect(self.ok_button, Qt.SIGNAL("clicked()"), self.accept)


	### Public ###

	def updateDicts(self) :
		self.update_dicts_button.blockSignals(True)

		self.wait_picture_movie_label.setVisible(True)
		self.wait_picture_movie.start()
		self.wait_message_label.setVisible(True)

		self.dicts_list.setList(self.syncLists(self.listOfAllDicts(), self.dicts_list.list()))

		self.wait_picture_movie_label.setVisible(False)
		self.wait_picture_movie.stop()
		self.wait_picture_movie.jumpToFrame(0)
		self.wait_message_label.setVisible(False)

		self.update_dicts_button.blockSignals(False)

	def saveSettings(self) :
		settings = Qt.QSettings(Const.Organization, Const.MyName)
		settings.setValue("dicts_manager/dicts_list", Qt.QVariant(self.dicts_list.list()))

	def loadSettings(self) :
		self.update_dicts_button.blockSignals(True)

		settings = Qt.QSettings(Const.Organization, Const.MyName)

		all_dicts_list = self.listOfAllDicts()
		local_dicts_list = settings.value("dicts_manager/dicts_list",
			Qt.QVariant(Qt.QStringList())).toStringList()

		self.dicts_list.setList(self.syncLists(all_dicts_list, local_dicts_list))

		self.update_dicts_button.blockSignals(False)


	### Private ###

	def listOfAllDicts(self) :
		all_dicts_dir = Qt.QDir(AllDictsDir)
		all_dicts_dir.setFilter(Qt.QDir.Files)
		all_dicts_dir.setSorting(Qt.QDir.Name)
		return all_dicts_dir.entryList()

	def syncLists(self, all_dicts_list, local_dicts_list) :
		local_dicts_list = Qt.QStringList(local_dicts_list)

		item_code_regexp = Qt.QRegExp("\\{(.+)\\}\\{(\\d)\\}")

		count = 0
		while count < local_dicts_list.count() :
			Qt.QCoreApplication.processEvents(Qt.QEventLoop.ExcludeUserInputEvents)

			if not item_code_regexp.exactMatch(local_dicts_list[count]) :
				local_dicts_list.removeAt(count)
				count += 1
				continue

			if not all_dicts_list.contains(item_code_regexp.cap(1)) :
				local_dicts_list.removeAt(count)
				count += 1
				continue

			count += 1

		tmp_list = Qt.QStringList()
		count = 0
		while count < local_dicts_list.count() :
			Qt.QCoreApplication.processEvents(Qt.QEventLoop.ExcludeUserInputEvents)

			if not item_code_regexp.exactMatch(local_dicts_list[count]) :
				count += 1
				continue

			tmp_list << item_code_regexp.cap(1)

			count += 1

		count = 0
		while count < all_dicts_list.count() :
			Qt.QCoreApplication.processEvents(Qt.QEventLoop.ExcludeUserInputEvents)

			if not tmp_list.contains(all_dicts_list[count]) :
				local_dicts_list << Qt.QString("{%1}{0}").arg(all_dicts_list[count])

			count += 1

		return local_dicts_list

	###

	def setStatusFromLineEdit(self, word) :
		if word.simplified().isEmpty() :
			self.clear_line_edit_button.setEnabled(False)
		else :
			self.clear_line_edit_button.setEnabled(True)

	def clearLineEdit(self) :
		self.line_edit.clear()
		self.line_edit.setFocus(Qt.Qt.OtherFocusReason)


	### Signals ###

	def dictsListChangedSignal(self, list) :
		self.emit(Qt.SIGNAL("dictsListChanged(const QStringList &)"), list)

