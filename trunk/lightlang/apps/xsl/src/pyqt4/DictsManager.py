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
import User
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
class DictsManager(Qt.QWidget) :
	def __init__(self, parent = None) :
		Qt.QWidget.__init__(self, parent)

		self.setWindowTitle(tr("Dicts Manager"))
		self.setWindowIcon(Qt.QIcon(MyIcon))

		#####

		self.main_layout = Qt.QVBoxLayout()
		self.setLayout(self.main_layout)

		self.line_edit_layout = Qt.QHBoxLayout()
		self.main_layout.addLayout(self.line_edit_layout)

		self.stacked_widget = Qt.QStackedWidget()
		self.main_layout.addWidget(self.stacked_widget)

		self.stacked_widget_buttons_layout = Qt.QHBoxLayout()
		self.main_layout.addLayout(self.stacked_widget_buttons_layout)

		self.horizontal_frame = Qt.QFrame()
		self.horizontal_frame.setFrameStyle(Qt.QFrame.HLine|Qt.QFrame.Sunken)
		self.main_layout.addWidget(self.horizontal_frame)

		self.control_buttons_layout = Qt.QHBoxLayout()
		self.main_layout.addLayout(self.control_buttons_layout)

		#####

		self.filter_label = Qt.QLabel(tr("&Filter:"))
		self.line_edit_layout.addWidget(self.filter_label)

		self.line_edit = Qt.QLineEdit()
		self.filter_label.setBuddy(self.line_edit)
		self.line_edit_layout.addWidget(self.line_edit)

		self.clear_line_edit_button = Qt.QToolButton()
		self.clear_line_edit_button.setIcon(Qt.QIcon(IconsDir+"clear_22.png"))
		self.clear_line_edit_button.setIconSize(Qt.QSize(16, 16))
		self.clear_line_edit_button.setEnabled(False)
		self.line_edit_layout.addWidget(self.clear_line_edit_button)

		self.dicts_list = DictsListWidget.DictsListWidget()
		self.stacked_widget.addWidget(self.dicts_list)

		self.wait_picture_movie = Qt.QMovie(WaitPicture)
		self.wait_picture_movie.setScaledSize(Qt.QSize(32, 32))
		self.wait_picture_movie.jumpToFrame(0)
		self.wait_picture_movie_label = Qt.QLabel()
		self.wait_picture_movie_label.setAlignment(Qt.Qt.AlignHCenter|Qt.Qt.AlignVCenter)
		self.wait_picture_movie_label.setMovie(self.wait_picture_movie)
		self.stacked_widget.addWidget(self.wait_picture_movie_label)

		self.up_button = Qt.QToolButton()
		self.up_button.setIcon(Qt.QIcon(IconsDir+"up_22.png"))
		self.up_button.setIconSize(Qt.QSize(22, 22))
		self.up_button.setEnabled(False)
		self.stacked_widget_buttons_layout.addWidget(self.up_button)

		self.down_button = Qt.QToolButton()
		self.down_button.setIcon(Qt.QIcon(IconsDir+"down_22.png"))
		self.down_button.setIconSize(Qt.QSize(22, 22))
		self.down_button.setEnabled(False)
		self.stacked_widget_buttons_layout.addWidget(self.down_button)

		self.stacked_widget_buttons_layout.addStretch()

		self.update_dicts_button = Qt.QToolButton()
		self.update_dicts_button.setIcon(Qt.QIcon(IconsDir+"update_22.png"))
		self.update_dicts_button.setIconSize(Qt.QSize(22, 22))
		self.stacked_widget_buttons_layout.addWidget(self.update_dicts_button)

		self.wait_message_label = Qt.QLabel(tr("Please wait..."))
		self.wait_message_label.hide()
		self.control_buttons_layout.addWidget(self.wait_message_label)

		self.control_buttons_layout.addStretch()

		self.ok_button = Qt.QPushButton(Qt.QIcon(IconsDir+"ok_16.png"), tr("&OK"))
		self.ok_button.setAutoDefault(False)
		self.ok_button.setDefault(False)
		self.control_buttons_layout.addWidget(self.ok_button)

		#####

		self.connect(self.line_edit, Qt.SIGNAL("textChanged(const QString &)"), self.setStatusFromLineEdit)
		self.connect(self.line_edit, Qt.SIGNAL("textChanged(const QString &)"), self.dicts_list.setFilter)
		self.connect(self.clear_line_edit_button, Qt.SIGNAL("clicked()"), self.clearLineEdit)

		self.connect(self.dicts_list, Qt.SIGNAL("upAvailable(bool)"), self.up_button.setEnabled)
		self.connect(self.dicts_list, Qt.SIGNAL("downAvailable(bool)"), self.down_button.setEnabled)
		self.connect(self.dicts_list, Qt.SIGNAL("dictsListChanged(const QStringList &)"), self.dictsListChangedSignal)

		self.connect(self.up_button, Qt.SIGNAL("clicked()"), self.dicts_list.up)
		self.connect(self.down_button, Qt.SIGNAL("clicked()"), self.dicts_list.down)
		self.connect(self.update_dicts_button, Qt.SIGNAL("clicked()"), self.updateDicts)

		self.connect(self.ok_button, Qt.SIGNAL("clicked()"), self.close)

		#####

		self.dicts_list.setFocus(Qt.Qt.OtherFocusReason)


	### Public ###

	def updateDicts(self) :
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

		#####

		self.dicts_list.setFocus(Qt.Qt.OtherFocusReason)

	###

	def saveSettings(self) :
		settings = User.settings()
		settings.setValue("dicts_manager/size", Qt.QVariant(self.size()))
		settings.setValue("dicts_manager/dicts_list", Qt.QVariant(self.dicts_list.list()))

	def loadSettings(self) :
		self.update_dicts_button.blockSignals(True)
		self.update_dicts_button.setEnabled(False)

		###

		settings = User.settings()

		self.resize(settings.value("dicts_manager/size", Qt.QVariant(Qt.QSize(400, 550))).toSize())

		local_dicts_list = settings.value("dicts_manager/dicts_list", Qt.QVariant(Qt.QStringList())).toStringList()
		self.dicts_list.setList(self.allAndLocalDicts(local_dicts_list))

		###

		Qt.QCoreApplication.processEvents()

		self.update_dicts_button.setEnabled(True)
		self.update_dicts_button.blockSignals(False)

	###

	def show(self) :
		x_window_position = (Qt.QApplication.desktop().width() - self.width()) / 2
		if x_window_position < 0 :
			x_window_position = 0
		y_window_position = (Qt.QApplication.desktop().height() - self.height()) / 2
		if y_window_position < 0 :
			y_window_position = 0

		self.move(Qt.QPoint(x_window_position, y_window_position))

		self.dicts_list.setFocus(Qt.Qt.OtherFocusReason)

		Qt.QWidget.show(self)
		self.raise_()
		self.activateWindow()


	### Private ###

	def allAndLocalDicts(self, local_dicts_list) :
		all_dicts_dir = Qt.QDir(AllDictsDir)
		all_dicts_dir.setFilter(Qt.QDir.Files)
		all_dicts_dir.setSorting(Qt.QDir.Name)
		all_dicts_dir_entry_list = all_dicts_dir.entryList()

		local_dicts_list = Qt.QStringList(local_dicts_list)

		###

		item_code_regexp = Qt.QRegExp("\\{(\\d)\\}\\{(.+)\\}")

		###

		count = 0
		while count < local_dicts_list.count() :
			Qt.QCoreApplication.processEvents(Qt.QEventLoop.ExcludeUserInputEvents)

			if not item_code_regexp.exactMatch(local_dicts_list[count]) :
				local_dicts_list.removeAt(count)
				count += 1
				continue

			if not all_dicts_dir_entry_list.contains(item_code_regexp.cap(2)) :
				local_dicts_list.removeAt(count)
				count += 1
				continue

			count += 1

		###

		tmp_list = Qt.QStringList(local_dicts_list)
		tmp_list.replaceInStrings(item_code_regexp, "\\2")

		###

		count = 0
		while count < all_dicts_dir_entry_list.count() :
			Qt.QCoreApplication.processEvents(Qt.QEventLoop.ExcludeUserInputEvents)

			if not tmp_list.contains(all_dicts_dir_entry_list[count]) :
				local_dicts_list << Qt.QString("{0}{%1}").arg(all_dicts_dir_entry_list[count])

			count += 1

		return local_dicts_list

	###

	def setStatusFromLineEdit(self, word) :
		if word.isEmpty() : # Not simplified
			self.clear_line_edit_button.setEnabled(False)
		else :
			self.clear_line_edit_button.setEnabled(True)

	def clearLineEdit(self) :
		self.line_edit.clear()
		self.line_edit.setFocus(Qt.Qt.OtherFocusReason)


	### Signals ###

	def dictsListChangedSignal(self, list) :
		self.emit(Qt.SIGNAL("dictsListChanged(const QStringList &)"), list)

