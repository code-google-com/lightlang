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
IconsDir = Config.Prefix+"/lib/xsl/icons/"


#####
def tr(str) :
	return Qt.QApplication.translate("@default", str)


#####
class HistoryPanel(Qt.QDockWidget) :
	def __init__(self, parent = None) :
		Qt.QDockWidget.__init__(self, parent)

		self.setObjectName("history_panel")

		self.setWindowTitle(tr("Search history"))

		self.setAllowedAreas(Qt.Qt.LeftDockWidgetArea|Qt.Qt.RightDockWidgetArea)

		#####

		self.main_widget = Qt.QWidget()
		self.setWidget(self.main_widget)

		self.main_layout = Qt.QVBoxLayout()
		self.main_widget.setLayout(self.main_layout)

		self.line_edit_layout = Qt.QHBoxLayout()
		self.main_layout.addLayout(self.line_edit_layout)

		#####

		self.line_edit = Qt.QLineEdit()
		self.line_edit_layout.addWidget(self.line_edit)

		self.clear_line_edit_button = Qt.QToolButton()
		self.clear_line_edit_button.setIcon(Qt.QIcon(IconsDir+"clear_22.png"))
		self.clear_line_edit_button.setIconSize(Qt.QSize(16, 16))
		self.clear_line_edit_button.setEnabled(False)
		self.line_edit_layout.addWidget(self.clear_line_edit_button)

		self.history_browser = Qt.QListWidget()
		self.history_browser.setSortingEnabled(True)
		self.main_layout.addWidget(self.history_browser)

		self.clear_history_button = Qt.QPushButton(tr("Clear history"))
		self.clear_history_button.setEnabled(False)
		self.main_layout.addWidget(self.clear_history_button)

		#####

		self.connect(self, Qt.SIGNAL("visibilityChanged(bool)"), self.activateDockWidget)

		self.connect(self.line_edit, Qt.SIGNAL("textChanged(const QString &)"), self.setStatusFromLineEdit)
		self.connect(self.line_edit, Qt.SIGNAL("textChanged(const QString &)"), self.setFilter)
		self.connect(self.clear_line_edit_button, Qt.SIGNAL("clicked()"), self.clearLineEdit)

		self.connect(self.history_browser, Qt.SIGNAL("itemActivated(QListWidgetItem *)"),
			self.wordChangedSignal)
		self.connect(self.clear_history_button, Qt.SIGNAL("clicked()"), self.clearHistory)


	### Public ###

	def addWord(self, word) :
		if not self.list().contains(word) :
			count = self.history_browser.count()
			while count >= 100 : # 100 - default value
				self.history_browser.takeItem(count -1)
				count = self.history_browser.count()
			self.history_browser.addItem(word)

			self.clear_history_button.setEnabled(True)

	###

	def saveSettings(self) :
		settings = Qt.QSettings(Const.Organization, Const.MyName)
		settings.setValue("history_panel/list", Qt.QVariant(self.list()))

	def loadSettings(self) :
		settings = Qt.QSettings(Const.Organization, Const.MyName)
		self.setList(settings.value("history_panel/list", Qt.QVariant(Qt.QStringList())).toStringList())

	###

	def setFocus(self, reason = Qt.Qt.OtherFocusReason) :
		self.line_edit.setFocus(reason)
		self.line_edit.selectAll()

	def hasInternalFocus(self) :
		return self.line_edit.hasFocus()

	def clear(self) :
		self.line_edit.clear()


	### Private ###

	def list(self) :
		list = Qt.QStringList()
		count = 0
		while count < self.history_browser.count() :
			list << self.history_browser.item(count).text()
			count += 1
		return list

	def setList(self, list) :
		self.history_browser.addItems(list)

		if list.count() > 0 :
			self.clear_history_button.setEnabled(True)

	def setFilter(self, word) :
		word = word.simplified()
		count = 0
		while count < self.history_browser.count() :
			item = self.history_browser.item(count)
			item_word = item.text();
			item.setHidden(not item_word.startsWith(word, Qt.Qt.CaseInsensitive))
			count += 1

	def clearHistory(self) :
		self.history_browser.clear()
		self.clear_history_button.setEnabled(False)

	def setStatusFromLineEdit(self, word) :
		if word.simplified().isEmpty() :
			self.clear_line_edit_button.setEnabled(False)
		else :
			self.clear_line_edit_button.setEnabled(True)

	def activateDockWidget(self, activate_flag) :
		if activate_flag :
			self.line_edit.setFocus(Qt.Qt.OtherFocusReason)
			self.line_edit.selectAll()

	def clearLineEdit(self) :
		self.line_edit.clear()
		self.line_edit.setFocus(Qt.Qt.OtherFocusReason)


	### Signals ###

	def wordChangedSignal(self, item) :
		self.emit(Qt.SIGNAL("wordChanged(const QString &)"), item.text())

