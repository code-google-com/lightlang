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
import LineEdit
import SlWordSearch
import SlListBrowser


#####
IconsDir = Config.Prefix+"/lib/xsl/icons/"


#####
def tr(str) :
	return Qt.QApplication.translate("@default", str)


#####
class SlSearchPanel(Qt.QDockWidget) :
	def __init__(self, parent = None) :
		Qt.QDockWidget.__init__(self, parent)

		self.setObjectName("sl_search_panel")

		self.setAllowedAreas(Qt.Qt.AllDockWidgetAreas)
		self.setFeatures(Qt.QDockWidget.DockWidgetFloatable|Qt.QDockWidget.DockWidgetMovable)

		self.setWindowTitle(tr("SL Search"))

		#####

		self.main_widget = Qt.QWidget()
		self.setWidget(self.main_widget)

		self.main_layout = Qt.QVBoxLayout()
		self.main_widget.setLayout(self.main_layout)

		self.line_edit_layout = Qt.QHBoxLayout()
		self.main_layout.addLayout(self.line_edit_layout)

		self.top_search_buttons_layout = Qt.QHBoxLayout()
		self.main_layout.addLayout(self.top_search_buttons_layout)

		self.list_browser_layout = Qt.QVBoxLayout()
		self.main_layout.addLayout(self.list_browser_layout)

		self.bottom_search_buttons_layout = Qt.QHBoxLayout()
		self.main_layout.addLayout(self.bottom_search_buttons_layout)

		#####

		self.delay_timer = Qt.QTimer()
		self.delay_timer.setInterval(300)

		self.internal_word_search = SlWordSearch.SlWordSearch()
		self.external_word_search = SlWordSearch.SlWordSearch()

		#####

		self.line_edit = LineEdit.LineEdit()
		self.line_edit_layout.addWidget(self.line_edit)

		self.u_find_button = Qt.QPushButton(tr("&Search"))
		self.u_find_button.setEnabled(False)
		self.top_search_buttons_layout.addWidget(self.u_find_button)

		self.c_find_button = Qt.QPushButton(tr("&Expanded search"))
		self.c_find_button.setEnabled(False)
		self.top_search_buttons_layout.addWidget(self.c_find_button)

		self.list_browser = SlListBrowser.SlListBrowser()
		self.list_browser.setText(tr("Enter the word, please"))
		self.list_browser_layout.addWidget(self.list_browser)

		self.l_find_button = Qt.QPushButton(tr("Word &list"))
		self.l_find_button.setEnabled(False)
		self.bottom_search_buttons_layout.addWidget(self.l_find_button)

		self.i_find_button = Qt.QPushButton(tr("S&imilar words"))
		self.i_find_button.setEnabled(False)
		self.bottom_search_buttons_layout.addWidget(self.i_find_button)

		#####

		self.connect(self, Qt.SIGNAL("visibilityChanged(bool)"), self.activateDockWidget)

		self.connect(self.delay_timer, Qt.SIGNAL("timeout()"), self.lFindAfterDelay)

		self.connect(self.internal_word_search, Qt.SIGNAL("clearRequest()"), self.list_browser.clear)
		self.connect(self.internal_word_search, Qt.SIGNAL("listChanged(const QStringList &)"), self.list_browser.setList)

		self.connect(self.external_word_search, Qt.SIGNAL("processStarted()"), self.processStartedSignal)
		self.connect(self.external_word_search, Qt.SIGNAL("processFinished()"), self.processFinishedSignal)
		self.connect(self.external_word_search, Qt.SIGNAL("clearRequest()"), self.clearRequestSignal)
		self.connect(self.external_word_search, Qt.SIGNAL("textChanged(const QString &)"), self.textChangedSignal)

		self.connect(self.line_edit, Qt.SIGNAL("returnPressed()"), self.u_find_button.animateClick)
		self.connect(self.line_edit, Qt.SIGNAL("textChanged(const QString &)"), self.setStatusFromLineEdit)
		self.connect(self.line_edit, Qt.SIGNAL("textChanged(const QString &)"), self.delay_timer.start)

		self.connect(self.u_find_button, Qt.SIGNAL("clicked()"), self.uFind)
		self.connect(self.u_find_button, Qt.SIGNAL("clicked()"), self.setFocus)
		self.connect(self.c_find_button, Qt.SIGNAL("clicked()"), self.cFind)
		self.connect(self.c_find_button, Qt.SIGNAL("clicked()"), self.setFocus)

		self.connect(self.list_browser, Qt.SIGNAL("uFindRequest(const QString &)"), self.uFind)
		self.connect(self.list_browser, Qt.SIGNAL("uFindInNewTabRequest(const QString &)"), self.uFindInNewTab)
		self.connect(self.list_browser, Qt.SIGNAL("cFindInNewTabRequest(const QString &)"), self.cFindInNewTab)

		self.connect(self.l_find_button, Qt.SIGNAL("clicked()"), self.lFind)
		self.connect(self.l_find_button, Qt.SIGNAL("clicked()"), self.setFocus)
		self.connect(self.i_find_button, Qt.SIGNAL("clicked()"), self.iFind)
		self.connect(self.i_find_button, Qt.SIGNAL("clicked()"), self.setFocus)


	### Public ###

	def show(self) :
		Qt.QDockWidget.show(self)
		self.raise_()
		self.setFocus()

	def setFocus(self, reason = Qt.Qt.OtherFocusReason) :
		self.line_edit.setFocus(reason)
		self.line_edit.selectAll()

	def hasInternalFocus(self) :
		return self.line_edit.hasFocus()

	def setWord(self, word) :
		self.line_edit.setText(word)
		self.setFocus()

	def setDictsList(self, dicts_list) :
		self.internal_word_search.setDictsList(dicts_list)
		self.external_word_search.setDictsList(dicts_list)

	def clear(self) :
		self.line_edit.clear()

	###

	def uFind(self, word = None) :
		word = ( self.line_edit.text().simplified() if word == None else word.simplified() )
		if word.isEmpty() :
			return
		self.external_word_search.uFind(word)
		self.wordChangedSignal(word)

	def cFind(self, word = None) :
		word = ( self.line_edit.text().simplified() if word == None else word.simplified() )
		if word.isEmpty() :
			return
		self.external_word_search.cFind(word)
		self.wordChangedSignal(word)

	def lFind(self, word = None) :
		word = ( self.line_edit.text().simplified() if word == None else word.simplified() )
		if word.isEmpty() :
			self.list_browser.setText(tr("Enter the word, please"))
			return
		self.internal_word_search.lFind(word)

	def iFind(self, word = None) :
		word = ( self.line_edit.text().simplified() if word == None else word.simplified() )
		if word.isEmpty() :
			self.list_browser.setText(tr("Enter the word, please"))
			return
		self.internal_word_search.iFind(word)

	def uFindInNewTab(self, word = None) :
		word = ( self.line_edit.text().simplified() if word == None else word.simplified() )
		if word.isEmpty() :
			return
		self.newTabRequestSignal()
		self.external_word_search.uFind(word)
		self.wordChangedSignal(word)

	def cFindInNewTab(self, word = None) :
		word = ( self.line_edit.text().simplified() if word == None else word.simplified() )
		if word.isEmpty() :
			return
		self.newTabRequestSignal()
		self.external_word_search.cFind(word)
		self.wordChangedSignal(word)

	###

	def saveSettings(self) :
		pass

	def loadSettings(self) :
		pass


	### Private ###

	def lFindAfterDelay(self) :
		self.delay_timer.stop()
		self.lFind()

	###

	def setStatusFromLineEdit(self, word) :
		line_edit_empty_flag = word.simplified().isEmpty()
		self.u_find_button.setEnabled(not line_edit_empty_flag)
		self.c_find_button.setEnabled(not line_edit_empty_flag)
		self.l_find_button.setEnabled(not line_edit_empty_flag)
		self.i_find_button.setEnabled(not line_edit_empty_flag)

	###

	def activateDockWidget(self, activate_flag) :
		if activate_flag :
			self.line_edit.setFocus(Qt.Qt.OtherFocusReason)
			self.line_edit.selectAll()


	### Signals ###

	def processStartedSignal(self) :
		self.emit(Qt.SIGNAL("processStarted()"))

	def processFinishedSignal(self) :
		self.emit(Qt.SIGNAL("processFinished()"))

	def wordChangedSignal(self, word) :
		self.emit(Qt.SIGNAL("wordChanged(const QString &)"), word)

	def textChangedSignal(self, text) :
		self.emit(Qt.SIGNAL("textChanged(const QString &)"), text)

	def newTabRequestSignal(self) :
		self.emit(Qt.SIGNAL("newTabRequest()"))

	def clearRequestSignal(self) :
		self.emit(Qt.SIGNAL("clearRequest()"))

