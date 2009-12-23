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
import LineEdit
import DictsListWidget


#####
MyIcon = Config.Prefix+"/lib/xsl/icons/xsl_16.png"
WaitPicture = Config.Prefix+"/lib/xsl/pictures/circular.gif"

AllDictsDir = Config.Prefix+"/share/sl/dicts/"
IconsDir = Config.Prefix+"/lib/xsl/icons/"


#####
def tr(str) :
	return Qt.QApplication.translate("@default", str)


#####
class DictsManagerWindow(Qt.QDialog) :
	def __init__(self, parent = None) :
		Qt.QDialog.__init__(self, parent)

		self.setObjectName("dicts_manager_window")

		self.setWindowTitle(tr("Dicts Manager"))
		self.setWindowIcon(Qt.QIcon(MyIcon))

		#####

		self.main_layout = Qt.QVBoxLayout()
		self.main_layout.setContentsMargins(0, 0, 0, 0)
		self.setLayout(self.main_layout)

		left_margin = self.style().pixelMetric(Qt.QStyle.PM_LayoutLeftMargin)
		top_margin = self.style().pixelMetric(Qt.QStyle.PM_LayoutTopMargin)
		right_margin = self.style().pixelMetric(Qt.QStyle.PM_LayoutRightMargin)
		bottom_margin = self.style().pixelMetric(Qt.QStyle.PM_LayoutBottomMargin)
		vertical_spacing = self.style().pixelMetric(Qt.QStyle.PM_LayoutVerticalSpacing)

		self.line_edit_layout = Qt.QHBoxLayout()
		self.line_edit_layout.setContentsMargins(left_margin, top_margin, right_margin, vertical_spacing)
		self.main_layout.addLayout(self.line_edit_layout)

		self.stacked_widget = Qt.QStackedWidget()
		self.main_layout.addWidget(self.stacked_widget)

		self.control_buttons_layout = Qt.QHBoxLayout()
		self.control_buttons_layout.setContentsMargins(left_margin, vertical_spacing, right_margin, bottom_margin)
		self.main_layout.addLayout(self.control_buttons_layout)

		#####

		self.item_code_regexp = Qt.QRegExp("\\{(\\d)\\}\\{(.+)\\}")

		self.all_dicts_dir_watcher = Qt.QFileSystemWatcher(Qt.QStringList() << AllDictsDir)
		self.all_dicts_dir_watcher_timer = Qt.QTimer()
		self.all_dicts_dir_watcher_timer.setInterval(5000)
		self.all_dicts_dir_watcher_timer.setSingleShot(True)

		#####

		self.filter_label = Qt.QLabel(tr("&Filter:"))
		self.line_edit_layout.addWidget(self.filter_label)

		self.line_edit = LineEdit.LineEdit()
		self.filter_label.setBuddy(self.line_edit)
		self.line_edit_layout.addWidget(self.line_edit)

		self.dicts_list = DictsListWidget.DictsListWidget()
		self.stacked_widget.addWidget(self.dicts_list)

		self.wait_picture_movie = Qt.QMovie(WaitPicture)
		self.wait_picture_movie.setScaledSize(Qt.QSize(32, 32))
		self.wait_picture_movie.jumpToFrame(0)
		self.wait_picture_movie_label = Qt.QLabel()
		self.wait_picture_movie_label.setAlignment(Qt.Qt.AlignHCenter|Qt.Qt.AlignVCenter)
		self.wait_picture_movie_label.setMovie(self.wait_picture_movie)
		self.stacked_widget.addWidget(self.wait_picture_movie_label)

		self.wait_message_label = Qt.QLabel(tr("Please wait..."))
		self.wait_message_label.hide()
		self.control_buttons_layout.addWidget(self.wait_message_label)

		self.control_buttons_layout.addStretch()

		self.update_dicts_button = Qt.QPushButton(Qt.QIcon(IconsDir+"update_16.png"), tr("&Update"))
		self.update_dicts_button.setAutoDefault(False)
		self.update_dicts_button.setDefault(False)
		self.control_buttons_layout.addWidget(self.update_dicts_button)

		self.ok_button = Qt.QPushButton(Qt.QIcon(IconsDir+"ok_16.png"), tr("&OK"))
		self.ok_button.setAutoDefault(False)
		self.ok_button.setDefault(False)
		self.control_buttons_layout.addWidget(self.ok_button)

		#####

		self.connect(self.all_dicts_dir_watcher, Qt.SIGNAL("directoryChanged(const QString &)"), self.planToUpdateDicts)
		self.connect(self.all_dicts_dir_watcher_timer, Qt.SIGNAL("timeout()"), self.updateDicts)

		self.connect(self.line_edit, Qt.SIGNAL("textChanged(const QString &)"), self.dicts_list.setFilter)

		self.connect(self.dicts_list, Qt.SIGNAL("dictsListChanged(const QStringList &)"), self.dictsListChangedSignal)

		self.connect(self.update_dicts_button, Qt.SIGNAL("clicked()"), self.updateDicts)
		self.connect(self.ok_button, Qt.SIGNAL("clicked()"), self.accept)


	### Public ###

	def updateDicts(self) :
		self.all_dicts_dir_watcher.blockSignals(True)
		self.all_dicts_dir_watcher_timer.stop()
		self.update_dicts_button.blockSignals(True)
		self.update_dicts_button.setEnabled(False)

		self.line_edit.clear()
		self.line_edit.setEnabled(False)

		self.wait_message_label.show()
		self.stacked_widget.setCurrentIndex(1)
		self.wait_picture_movie.start()

		###

		self.dicts_list.setList(self.allAndLocalDicts(self.dicts_list.list()))

		###

		Qt.QCoreApplication.processEvents()

		self.wait_message_label.hide()
		self.stacked_widget.setCurrentIndex(0)
		self.wait_picture_movie.stop()
		self.wait_picture_movie.jumpToFrame(0)

		self.line_edit.setEnabled(True)

		self.update_dicts_button.setEnabled(True)
		self.update_dicts_button.blockSignals(False)
		self.all_dicts_dir_watcher.blockSignals(False)

		#####

		self.dicts_list.setFocus(Qt.Qt.OtherFocusReason)

	###

	def saveSettings(self) :
		settings = Settings.settings()
		settings.setValue("dicts_manager_window/size", Qt.QVariant(self.size()))
		settings.setValue("dicts_manager_window/dicts_list", Qt.QVariant(self.dicts_list.list()))

	def loadSettings(self) :
		self.all_dicts_dir_watcher.blockSignals(True)
		self.all_dicts_dir_watcher_timer.stop()
		self.update_dicts_button.blockSignals(True)
		self.update_dicts_button.setEnabled(False)

		###

		settings = Settings.settings()

		self.resize(settings.value("dicts_manager_window/size", Qt.QVariant(Qt.QSize(400, 550))).toSize())

		local_dicts_list = settings.value("dicts_manager_window/dicts_list", Qt.QVariant(Qt.QStringList())).toStringList()
		self.dicts_list.setList(self.allAndLocalDicts(local_dicts_list))

		###

		Qt.QCoreApplication.processEvents()

		self.update_dicts_button.setEnabled(True)
		self.update_dicts_button.blockSignals(False)
		self.all_dicts_dir_watcher.blockSignals(False)

	###

	def show(self) :
		Qt.QDialog.show(self)
		self.raise_()
		self.activateWindow()
		self.dicts_list.setFocus(Qt.Qt.OtherFocusReason)


	### Private ###

	def planToUpdateDicts(self) :
		if self.all_dicts_dir_watcher_timer.isActive() :
			self.all_dicts_dir_watcher_timer.stop()
		self.all_dicts_dir_watcher_timer.start()

	###

	def allAndLocalDicts(self, local_dicts_list) :
		all_dicts_dir = Qt.QDir(AllDictsDir)
		all_dicts_dir.setFilter(Qt.QDir.Files)
		all_dicts_dir.setSorting(Qt.QDir.Name)
		all_dicts_dir_entry_list = all_dicts_dir.entryList()

		local_dicts_list = Qt.QStringList(local_dicts_list)

		###

		count = 0
		while count < local_dicts_list.count() :
			Qt.QCoreApplication.processEvents(Qt.QEventLoop.ExcludeUserInputEvents)

			if not self.item_code_regexp.exactMatch(local_dicts_list[count]) :
				local_dicts_list.removeAt(count)
				count += 1
				continue

			if not all_dicts_dir_entry_list.contains(self.item_code_regexp.cap(2)) :
				local_dicts_list.removeAt(count)
				count += 1
				continue

			count += 1

		###

		tmp_list = Qt.QStringList(local_dicts_list)
		tmp_list.replaceInStrings(self.item_code_regexp, "\\2")

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

