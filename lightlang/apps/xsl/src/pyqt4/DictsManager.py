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
DictsList = Qt.QString()

#####
class DictsManager(Qt.QDialog) :
	def __init__(self, parent = None) :
		Qt.QDialog.__init__(self, parent)

		self.setWindowTitle(self.tr("Dicts Manager"))
		self.setWindowIcon(Qt.QIcon(MyIcon))

		self.main_layout = Qt.QVBoxLayout()
		self.main_layout.setSizeConstraint(Qt.QLayout.SetFixedSize)
		self.setLayout(self.main_layout)

		self.browsers_layout = Qt.QHBoxLayout()
		self.main_layout.addLayout(self.browsers_layout)

		self.unused_dicts_group = Qt.QGroupBox(self.tr("Unused dicts"))
		self.browsers_layout.addWidget(self.unused_dicts_group)
		self.unused_dicts_group_layout = Qt.QHBoxLayout()
		self.unused_dicts_group.setLayout(self.unused_dicts_group_layout)
		self.unused_dicts_group_browser_layout = Qt.QVBoxLayout()
		self.unused_dicts_group_layout.addLayout(self.unused_dicts_group_browser_layout)
		self.unused_dicts_group_control_buttons_layout = Qt.QVBoxLayout()
		self.unused_dicts_group_layout.addLayout(self.unused_dicts_group_control_buttons_layout)

		self.used_dicts_group = Qt.QGroupBox(self.tr("Used dicts"))
		self.browsers_layout.addWidget(self.used_dicts_group)
		self.used_dicts_group_layout = Qt.QHBoxLayout()
		self.used_dicts_group.setLayout(self.used_dicts_group_layout)
		self.used_dicts_group_control_buttons_layout = Qt.QVBoxLayout()
		self.used_dicts_group_layout.addLayout(self.used_dicts_group_control_buttons_layout)
		self.used_dicts_group_browser_layout = Qt.QVBoxLayout()
		self.used_dicts_group_layout.addLayout(self.used_dicts_group_browser_layout)

		self.dict_information_group = Qt.QGroupBox(self.tr("Dict Information Center"))
		self.dict_information_group.setVisible(False)
		self.main_layout.addWidget(self.dict_information_group)
		self.dict_information_group_layout = Qt.QVBoxLayout()
		self.dict_information_group.setLayout(self.dict_information_group_layout)
		self.dict_information_group_lines_layout = Qt.QGridLayout()
		self.dict_information_group_layout.addLayout(self.dict_information_group_lines_layout)
		self.dict_information_group_browser_layout = Qt.QVBoxLayout()
		self.dict_information_group_layout.addLayout(self.dict_information_group_browser_layout)

		self.control_buttons_layout = Qt.QHBoxLayout()
		self.main_layout.addLayout(self.control_buttons_layout)

		#####

		self.unused_dicts_browser = Qt.QListWidget()
		self.unused_dicts_browser.setSortingEnabled(True)
		self.unused_dicts_group_browser_layout.addWidget(self.unused_dicts_browser)

		self.right_button = Qt.QToolButton()
		self.right_button.setIcon(Qt.QIcon(IconsDir+"right_22.png"))
		self.right_button.setIconSize(Qt.QSize(22, 22))
		self.unused_dicts_group_control_buttons_layout.addWidget(self.right_button)

		###

		self.used_dicts_browser = Qt.QListWidget()
		self.used_dicts_group_browser_layout.addWidget(self.used_dicts_browser)

		self.up_button = Qt.QToolButton()
		self.up_button.setIcon(Qt.QIcon(IconsDir+"up_22.png"))
		self.up_button.setIconSize(Qt.QSize(22, 22))
		self.used_dicts_group_control_buttons_layout.addWidget(self.up_button)

		self.left_button = Qt.QToolButton()
		self.left_button.setIcon(Qt.QIcon(IconsDir+"left_22.png"))
		self.left_button.setIconSize(Qt.QSize(22, 22))
		self.used_dicts_group_control_buttons_layout.addWidget(self.left_button)

		self.down_button = Qt.QToolButton()
		self.down_button.setIcon(Qt.QIcon(IconsDir+"down_22.png"))
		self.down_button.setIconSize(Qt.QSize(22, 22))
		self.used_dicts_group_control_buttons_layout.addWidget(self.down_button)

		###

		self.wait_picture_movie = Qt.QMovie(WaitPicture)
		self.wait_picture_movie.setScaledSize(Qt.QSize(16, 16))
		self.wait_picture_movie.jumpToFrame(0)
		self.wait_picture_movie_label = Qt.QLabel()
		self.wait_picture_movie_label.setMovie(self.wait_picture_movie)
		self.wait_picture_movie_label.setVisible(False)
		self.dict_information_group_lines_layout.addWidget(self.wait_picture_movie_label, 0, 0)

		self.dict_name_combobox = Qt.QComboBox()
		self.dict_information_group_lines_layout.addWidget(self.dict_name_combobox, 0, 1)

		self.dict_direction_label = Qt.QLabel(self.tr("Direction:"))
		self.dict_information_group_lines_layout.addWidget(self.dict_direction_label, 1, 0)

		self.dict_direction_line_browser = Qt.QLineEdit()
		self.dict_direction_line_browser.setReadOnly(True)
		self.dict_information_group_lines_layout.addWidget(self.dict_direction_line_browser, 1, 1)

		self.dict_file_size_label = Qt.QLabel(self.tr("File size (KB):"))
		self.dict_information_group_lines_layout.addWidget(self.dict_file_size_label, 2, 0)

		self.dict_file_size_line_browser = Qt.QLineEdit()
		self.dict_file_size_line_browser.setReadOnly(True)
		self.dict_information_group_lines_layout.addWidget(self.dict_file_size_line_browser, 2, 1)

		self.dict_words_count_label = Qt.QLabel(self.tr("Count of words:"))
		self.dict_information_group_lines_layout.addWidget(self.dict_words_count_label, 3, 0)

		self.dict_words_count_line_browser = Qt.QLineEdit()
		self.dict_words_count_line_browser.setReadOnly(True)
		self.dict_information_group_lines_layout.addWidget(self.dict_words_count_line_browser, 3, 1)

		self.dict_file_path_label = Qt.QLabel(self.tr("File path:"))
		self.dict_information_group_lines_layout.addWidget(self.dict_file_path_label, 4, 0)

		self.dict_file_path_line_browser = Qt.QLineEdit()
		self.dict_file_path_line_browser.setReadOnly(True)
		self.dict_information_group_lines_layout.addWidget(self.dict_file_path_line_browser, 4, 1)

		self.dict_information_browser = Qt.QTextBrowser()
		self.dict_information_group_browser_layout.addWidget(self.dict_information_browser)

		###

		self.more_button = Qt.QPushButton(self.tr("More"))
		self.more_button.setCheckable(True)
		self.more_button.setDefault(False)
		self.control_buttons_layout.addWidget(self.more_button)

		self.control_buttons_layout.addStretch()

		self.update_button = Qt.QPushButton(Qt.QIcon(IconsDir+"update_16.png"), self.tr("Update"))
		self.control_buttons_layout.addWidget(self.update_button)

		self.ok_button = Qt.QPushButton(Qt.QIcon(IconsDir+"ok_16.png"), self.tr("OK"))
		self.control_buttons_layout.addWidget(self.ok_button)

		#####

		self.connect(self.unused_dicts_browser, Qt.SIGNAL("itemDoubleClicked(QListWidgetItem *)"), self.moveRight)
		self.connect(self.used_dicts_browser, Qt.SIGNAL("itemDoubleClicked(QListWidgetItem *)"), self.moveLeft)

		self.connect(self.up_button, Qt.SIGNAL("clicked()"), self.moveUp)
		self.connect(self.down_button, Qt.SIGNAL("clicked()"), self.moveDown)
		self.connect(self.left_button, Qt.SIGNAL("clicked()"), self.moveLeft)
		self.connect(self.right_button, Qt.SIGNAL("clicked()"), self.moveRight)

		self.connect(self.dict_name_combobox, Qt.SIGNAL("currentIndexChanged(const QString &)"),
			self.setInformation)

		self.connect(self.more_button, Qt.SIGNAL("toggled(bool)"), self.dict_information_group.setVisible)
		self.connect(self.update_button, Qt.SIGNAL("clicked()"), self.update)
		self.connect(self.ok_button, Qt.SIGNAL("clicked()"), self.accept)


	### Public ###

	def update(self) :
		all_dicts_list = self.listOfAllDicts()
		used_dicts_list = self.listOfUsedDicts()

		unused_dicts_list, used_dicts_list = self.syncLists(all_dicts_list, used_dicts_list)

		self.update_button.blockSignals(True) # Block signals

		self.unused_dicts_browser.clear()
		self.used_dicts_browser.clear()
		self.dict_name_combobox.clear()

		self.unused_dicts_browser.addItems(unused_dicts_list)
		self.used_dicts_browser.addItems(used_dicts_list)
		self.dict_name_combobox.addItems(Qt.QStringList() << "" << all_dicts_list)

		self.update_button.blockSignals(False) # Unblock signals

		self.updateDictsList()

	def saveSettings(self) :
		settings = Qt.QSettings(Const.Organization, Const.MyName)
		settings.setValue("dicts_manager/used_dicts_list", Qt.QVariant(self.listOfUsedDicts()))

	def loadSettings(self) :
		settings = Qt.QSettings(Const.Organization, Const.MyName)

		all_dicts_list = self.listOfAllDicts()
		used_dicts_list = settings.value("dicts_manager/used_dicts_list",
			Qt.QVariant(Qt.QStringList())).toStringList()

		unused_dicts_list, used_dicts_list = self.syncLists(all_dicts_list, used_dicts_list)

		self.unused_dicts_browser.addItems(unused_dicts_list)
		self.used_dicts_browser.addItems(used_dicts_list)
		self.dict_name_combobox.addItems(Qt.QStringList() << "" << all_dicts_list)

		self.updateDictsList()


	### Private ###

	def moveUp(self) :
		index = self.used_dicts_browser.currentRow()
		if index == 0 :
			return
		item = self.used_dicts_browser.takeItem(index)
		self.used_dicts_browser.insertItem(index -1, item)
		self.used_dicts_browser.setCurrentRow(index -1)
		self.updateDictsList()

	def moveDown(self) :
		index = self.used_dicts_browser.currentRow()
		if index == self.used_dicts_browser.count() -1 :
			return
		item = self.used_dicts_browser.takeItem(index)
		self.used_dicts_browser.insertItem(index +1, item)
		self.used_dicts_browser.setCurrentRow(index +1)
		self.updateDictsList()

	def moveLeft(self) :
		index = self.used_dicts_browser.currentRow()
		item = self.used_dicts_browser.takeItem(index)
		self.unused_dicts_browser.addItem(item)
		self.updateDictsList()

	def moveRight(self) :
		index = self.unused_dicts_browser.currentRow()
		item = self.unused_dicts_browser.takeItem(index)
		self.used_dicts_browser.addItem(item)
		self.updateDictsList()

	def setInformation(self, dict_name) :
		if dict_name.simplified().isEmpty() :
			self.dict_direction_line_browser.clear()
			self.dict_file_size_line_browser.clear()
			self.dict_words_count_line_browser.clear()
			self.dict_file_path_line_browser.clear()
			self.dict_information_browser.clear()
		else :
			self.dict_name_combobox.setEnabled(False)
			self.update_button.blockSignals(True)

			self.wait_picture_movie_label.setVisible(True)
			self.wait_picture_movie.start()

			#####

			dict_direction = Qt.QString(self.tr("Unavailable"))
			dict_file_size = Qt.QString(self.tr("Unavailable"))
			dict_words_count = Qt.QString(self.tr("Unavailable"))
			dict_file_path = Qt.QString(self.tr("Unavailable"))
			dict_information = Qt.QString(self.tr("Unavailable"))
			dict_information_need_clear_flag = True

			self.dict_direction_line_browser.setText("Loading...")
			self.dict_file_size_line_browser.setText("Loading...")
			self.dict_words_count_line_browser.setText("Loading...")
			self.dict_file_path_line_browser.setText("Loading...")
			self.dict_information_browser.setHtml("<em>Loading...</em>")

			###

			dict_direction = dict_name.section(".", -1)

			dict_file = Qt.QFile(AllDictsDir+dict_name)

			dict_file_size.setNum(dict_file.size() / 1024) # KB

			dict_file_stream = Qt.QTextStream(dict_file)
			if dict_file.open(Qt.QIODevice.ReadOnly) :
				count = 0
				first_comment_flag = False
				while not dict_file.atEnd() :
					Qt.QCoreApplication.processEvents()
					str = dict_file_stream.readLine()
					if str.isEmpty() :
						continue
					if str[0] == "#" :
						if dict_information_need_clear_flag :
							dict_information.clear()
							dict_information_need_clear_flag = False
						str.remove("\n")
						str.append("\n")
						dict_information.append(str)
						continue
					if str.contains("  ") :
						count += 1
				dict_file.close()
				dict_words_count.setNum(count)
				dict_information.trimmed()

			dict_file_path = AllDictsDir+dict_name

			###

			self.dict_direction_line_browser.setText(dict_direction)
			self.dict_file_size_line_browser.setText(dict_file_size)
			self.dict_words_count_line_browser.setText(dict_words_count)
			self.dict_file_path_line_browser.setText(dict_file_path)
			self.dict_information_browser.setText(dict_information)

			#####

			self.wait_picture_movie.stop()
			self.wait_picture_movie_label.setVisible(False)
			self.wait_picture_movie.jumpToFrame(0)

			self.dict_name_combobox.setEnabled(True)
			self.update_button.blockSignals(False)

	###

	def listOfAllDicts(self) :
		all_dicts_list = Qt.QStringList()

		all_dicts_dir = Qt.QDir(AllDictsDir)
		all_dicts_dir.setFilter(Qt.QDir.Files)
		all_dicts_dir.setSorting(Qt.QDir.Name)

		count = 0
		while count < all_dicts_dir.count() :
			Qt.QCoreApplication.processEvents()
			all_dicts_list << all_dicts_dir[count]
			count += 1

		return all_dicts_list

	def listOfUsedDicts(self) :
		used_dicts_list = Qt.QStringList()
		count = 0
		while count < self.used_dicts_browser.count() :
			Qt.QCoreApplication.processEvents()
			used_dicts_list << self.used_dicts_browser.item(count).text()
			count += 1
		return used_dicts_list

	def syncLists(self, all_dicts_list, used_dicts_list) :
		all_dicts_list_sync = Qt.QStringList(all_dicts_list)
		used_dicts_list_sync = Qt.QStringList(used_dicts_list)

		count = 0
		while count < used_dicts_list_sync.count() :
			Qt.QCoreApplication.processEvents()
			if not all_dicts_list_sync.contains(used_dicts_list_sync[count]) :
				used_dicts_list_sync.removeAll(used_dicts_list_sync[count])
			count += 1
		
		count = 0
		while count < used_dicts_list_sync.count() :
			Qt.QCoreApplication.processEvents()
			if all_dicts_list_sync.contains(used_dicts_list_sync[count]) :
				all_dicts_list_sync.removeAll(used_dicts_list_sync[count])
			count += 1
		
		return all_dicts_list_sync, used_dicts_list_sync

	###

	def updateDictsList(self) :
		global DictsList
		DictsList = self.listOfUsedDicts().join("|")
		self.dictsChangedSignal()


	### Signals ###

	def dictsChangedSignal(self) :
		self.emit(Qt.SIGNAL("dictsChanged()"))
