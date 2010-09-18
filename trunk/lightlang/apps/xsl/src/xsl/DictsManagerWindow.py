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
import Settings
import IconsLoader
import LineEdit
import DictsListWidget


#####
AllDictsDir = Config.DataRootDir+"/sl/dicts/"


#####
class DictsManagerWindow(Qt.QDialog) :
	def __init__(self, parent = None) :
		Qt.QDialog.__init__(self, parent)

		self.setObjectName("dicts_manager_window")

		self.setWindowTitle(tr("Dicts Manager"))
		self.setWindowIcon(IconsLoader.icon("xsl"))

		#####

		self._main_layout = Qt.QVBoxLayout()
		self._main_layout.setContentsMargins(0, 0, 0, 0)
		self.setLayout(self._main_layout)

		left_margin = self.style().pixelMetric(Qt.QStyle.PM_LayoutLeftMargin)
		top_margin = self.style().pixelMetric(Qt.QStyle.PM_LayoutTopMargin)
		right_margin = self.style().pixelMetric(Qt.QStyle.PM_LayoutRightMargin)
		bottom_margin = self.style().pixelMetric(Qt.QStyle.PM_LayoutBottomMargin)
		vertical_spacing = self.style().pixelMetric(Qt.QStyle.PM_LayoutVerticalSpacing)

		self._line_edit_layout = Qt.QHBoxLayout()
		self._line_edit_layout.setContentsMargins(left_margin, top_margin, right_margin, vertical_spacing)
		self._main_layout.addLayout(self._line_edit_layout)

		self._stacked_widget = Qt.QStackedWidget()
		self._main_layout.addWidget(self._stacked_widget)

		self._control_buttons_layout = Qt.QHBoxLayout()
		self._control_buttons_layout.setContentsMargins(left_margin, vertical_spacing, right_margin, bottom_margin)
		self._main_layout.addLayout(self._control_buttons_layout)

		#####

		self._item_code_regexp = Qt.QRegExp("\\{(\\d)\\}\\{(.+)\\}")

		self._all_dicts_dir_watcher = Qt.QFileSystemWatcher(Qt.QStringList() << AllDictsDir)
		self._all_dicts_dir_watcher_timer = Qt.QTimer()
		self._all_dicts_dir_watcher_timer.setInterval(5000)
		self._all_dicts_dir_watcher_timer.setSingleShot(True)

		#####

		self._filter_label = Qt.QLabel(tr("&Filter:"))
		self._line_edit_layout.addWidget(self._filter_label)

		self._line_edit = LineEdit.LineEdit()
		self._filter_label.setBuddy(self._line_edit)
		self._line_edit_layout.addWidget(self._line_edit)

		self._dicts_list = DictsListWidget.DictsListWidget()
		self._stacked_widget.addWidget(self._dicts_list)

		self._wait_picture_movie = IconsLoader.gifMovie("circular")
		self._wait_picture_movie.setScaledSize(Qt.QSize(32, 32))
		self._wait_picture_movie.jumpToFrame(0)
		self._wait_picture_movie_label = Qt.QLabel()
		self._wait_picture_movie_label.setAlignment(Qt.Qt.AlignHCenter|Qt.Qt.AlignVCenter)
		self._wait_picture_movie_label.setMovie(self._wait_picture_movie)
		self._stacked_widget.addWidget(self._wait_picture_movie_label)

		self._wait_message_label = Qt.QLabel(tr("Please wait..."))
		self._wait_message_label.hide()
		self._control_buttons_layout.addWidget(self._wait_message_label)

		self._control_buttons_layout.addStretch()

		self._update_dicts_button = Qt.QPushButton(IconsLoader.icon("view-refresh"), tr("&Update"))
		self._update_dicts_button.setAutoDefault(False)
		self._update_dicts_button.setDefault(False)
		self._control_buttons_layout.addWidget(self._update_dicts_button)

		self._ok_button = Qt.QPushButton(IconsLoader.icon("dialog-ok-apply"), tr("&OK"))
		self._ok_button.setAutoDefault(False)
		self._ok_button.setDefault(False)
		self._control_buttons_layout.addWidget(self._ok_button)

		#####

		self.connect(self._all_dicts_dir_watcher, Qt.SIGNAL("directoryChanged(const QString &)"), self.planToUpdateDicts)
		self.connect(self._all_dicts_dir_watcher_timer, Qt.SIGNAL("timeout()"), self.updateDicts)

		self.connect(self._line_edit, Qt.SIGNAL("textChanged(const QString &)"), self._dicts_list.setFilter)

		self.connect(self._dicts_list, Qt.SIGNAL("dictsListChanged(const QStringList &)"), self.dictsListChangedSignal)

		self.connect(self._update_dicts_button, Qt.SIGNAL("clicked()"), self.updateDicts)
		self.connect(self._ok_button, Qt.SIGNAL("clicked()"), self.accept)


	### Public ###

	def updateDicts(self) :
		self._all_dicts_dir_watcher.blockSignals(True)
		self._all_dicts_dir_watcher_timer.stop()
		self._update_dicts_button.blockSignals(True)
		self._update_dicts_button.setEnabled(False)

		self._line_edit.clear()
		self._line_edit.setEnabled(False)

		self._wait_message_label.show()
		self._stacked_widget.setCurrentIndex(1)
		self._wait_picture_movie.start()

		###

		self._dicts_list.setList(self.allAndLocalDicts(self._dicts_list.list()))

		###

		self._wait_message_label.hide()
		self._stacked_widget.setCurrentIndex(0)
		self._wait_picture_movie.stop()
		self._wait_picture_movie.jumpToFrame(0)

		self._line_edit.setEnabled(True)

		self._update_dicts_button.setEnabled(True)
		self._update_dicts_button.blockSignals(False)
		self._all_dicts_dir_watcher.blockSignals(False)

		#####

		self._dicts_list.setFocus(Qt.Qt.OtherFocusReason)

	###

	def saveSettings(self) :
		settings = Settings.settings()
		settings.setValue("dicts_manager_window/size", Qt.QVariant(self.size()))
		settings.setValue("dicts_manager_window/dicts_list", Qt.QVariant(self._dicts_list.list()))

	def loadSettings(self) :
		self._all_dicts_dir_watcher.blockSignals(True)
		self._all_dicts_dir_watcher_timer.stop()
		self._update_dicts_button.blockSignals(True)
		self._update_dicts_button.setEnabled(False)

		###

		settings = Settings.settings()

		self.resize(settings.value("dicts_manager_window/size", Qt.QVariant(Qt.QSize(400, 550))).toSize())

		local_dicts_list = settings.value("dicts_manager_window/dicts_list", Qt.QVariant(Qt.QStringList())).toStringList()
		self._dicts_list.setList(self.allAndLocalDicts(local_dicts_list))

		###

		self._update_dicts_button.setEnabled(True)
		self._update_dicts_button.blockSignals(False)
		self._all_dicts_dir_watcher.blockSignals(False)

	###

	def show(self) :
		Qt.QDialog.show(self)
		self.raise_()
		self.activateWindow()
		self._dicts_list.setFocus(Qt.Qt.OtherFocusReason)


	### Private ###

	def planToUpdateDicts(self) :
		if self._all_dicts_dir_watcher_timer.isActive() :
			self._all_dicts_dir_watcher_timer.stop()
		self._all_dicts_dir_watcher_timer.start()

	###

	def allAndLocalDicts(self, local_dicts_list) :
		all_dicts_file_name_filters = Qt.QStringList()
		all_dicts_file_name_filters << "*.??-??"

		all_dicts_dir = Qt.QDir(AllDictsDir)
		all_dicts_dir.setNameFilters(all_dicts_file_name_filters)
		all_dicts_dir.setFilter(Qt.QDir.Files)
		all_dicts_dir.setSorting(Qt.QDir.Name)
		all_dicts_dir_entry_list = all_dicts_dir.entryList()

		local_dicts_list = Qt.QStringList(local_dicts_list)

		###

		count = 0
		while count < local_dicts_list.count() :
			Qt.QCoreApplication.processEvents(Qt.QEventLoop.ExcludeUserInputEvents)

			if not self._item_code_regexp.exactMatch(local_dicts_list[count]) :
				local_dicts_list.removeAt(count)
				count += 1
				continue

			if not all_dicts_dir_entry_list.contains(self._item_code_regexp.cap(2)) :
				local_dicts_list.removeAt(count)
				count += 1
				continue

			count += 1

		###

		tmp_list = Qt.QStringList(local_dicts_list)
		tmp_list.replaceInStrings(self._item_code_regexp, "\\2")

		###

		count = 0
		while count < all_dicts_dir_entry_list.count() :
			Qt.QCoreApplication.processEvents(Qt.QEventLoop.ExcludeUserInputEvents)

			if not tmp_list.contains(all_dicts_dir_entry_list[count]) :
				local_dicts_list << Qt.QString("{0}{%1}").arg(all_dicts_dir_entry_list[count])

			count += 1

		return local_dicts_list


	### Signals ###

	def dictsListChangedSignal(self, list) :
		self.emit(Qt.SIGNAL("dictsListChanged(const QStringList &)"), list)

