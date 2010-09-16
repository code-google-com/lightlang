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
import IconsLoader
import LineEdit
import SlWordSearch
import SlListBrowser


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

		self._main_widget = Qt.QWidget()
		self.setWidget(self._main_widget)

		self._main_layout = Qt.QVBoxLayout()
		self._main_widget.setLayout(self._main_layout)

		self._line_edit_layout = Qt.QHBoxLayout()
		self._main_layout.addLayout(self._line_edit_layout)

		self._list_browser_layout = Qt.QVBoxLayout()
		self._main_layout.addLayout(self._list_browser_layout)

		self._bottom_search_buttons_layout = Qt.QHBoxLayout()
		self._main_layout.addLayout(self._bottom_search_buttons_layout)

		#####

		self._delay_timer = Qt.QTimer()
		self._delay_timer.setInterval(300)

		self._internal_word_search = SlWordSearch.SlWordSearch()
		self._external_word_search = SlWordSearch.SlWordSearch()

		#####

		self._line_edit = LineEdit.LineEdit()
		self._line_edit_layout.addWidget(self._line_edit)

		self._u_find_button = Qt.QPushButton(tr("&Search"))
		self._u_find_button.setEnabled(False)
		self._line_edit_layout.addWidget(self._u_find_button)

		self._list_browser = SlListBrowser.SlListBrowser()
		self._list_browser.setText(tr("Enter the word, please"))
		self._list_browser_layout.addWidget(self._list_browser)

		self._c_find_button = Qt.QPushButton(tr("&Expanded search"))
		self._c_find_button.setEnabled(False)
		self._bottom_search_buttons_layout.addWidget(self._c_find_button)

		self._i_find_button = Qt.QPushButton(tr("S&imilar words"))
		self._i_find_button.setEnabled(False)
		self._bottom_search_buttons_layout.addWidget(self._i_find_button)

		#####

		self.connect(self, Qt.SIGNAL("visibilityChanged(bool)"), self.activateDockWidget)

		self.connect(self._delay_timer, Qt.SIGNAL("timeout()"), self.lFindAfterDelay)

		self.connect(self._internal_word_search, Qt.SIGNAL("clearRequest()"), self._list_browser.clear)
		self.connect(self._internal_word_search, Qt.SIGNAL("listChanged(const QStringList &)"), self._list_browser.setList)

		self.connect(self._external_word_search, Qt.SIGNAL("processStarted()"), self.processStarted)
		self.connect(self._external_word_search, Qt.SIGNAL("processFinished()"), self.processFinished)
		self.connect(self._external_word_search, Qt.SIGNAL("clearRequest()"), self.clearRequestSignal)
		self.connect(self._external_word_search, Qt.SIGNAL("textChanged(const QString &)"), self.textChangedSignal)

		self.connect(self._line_edit, Qt.SIGNAL("returnPressed()"), self._u_find_button.animateClick)
		self.connect(self._line_edit, Qt.SIGNAL("textChanged(const QString &)"), self.setStatusFromLineEdit)
		self.connect(self._line_edit, Qt.SIGNAL("textChanged(const QString &)"), self._delay_timer.start)

		self.connect(self._u_find_button, Qt.SIGNAL("clicked()"), self.uFind)
		self.connect(self._u_find_button, Qt.SIGNAL("clicked()"), self.setFocus)

		self.connect(self._list_browser, Qt.SIGNAL("uFindRequest(const QString &)"), self.uFind)
		self.connect(self._list_browser, Qt.SIGNAL("uFindInNewTabRequest(const QString &)"), self.uFindInNewTab)
		self.connect(self._list_browser, Qt.SIGNAL("cFindInNewTabRequest(const QString &)"), self.cFindInNewTab)

		self.connect(self._c_find_button, Qt.SIGNAL("clicked()"), self.cFind)
		self.connect(self._c_find_button, Qt.SIGNAL("clicked()"), self.setFocus)

		self.connect(self._i_find_button, Qt.SIGNAL("clicked()"), self.iFind)
		self.connect(self._i_find_button, Qt.SIGNAL("clicked()"), self.setFocus)


	### Public ###

	def requisites(self) :
		return {
			"icon" : IconsLoader.icon("xsl"),
			"title" : self.windowTitle(),
			"area" : Qt.Qt.LeftDockWidgetArea,
			"hotkey" : Qt.QKeySequence("Ctrl+S")
		}

	def translateMethods(self) :
		return [
			{
				"title" : tr("SL usually search"),
				"object_name" : self.objectName(),
				"method_name" : self.uFindTranslateMethod.__name__,
				"method" : self.uFindTranslateMethod
			},
			{
				"title" : tr("SL expanded search"),
				"object_name" : self.objectName(),
				"method_name" : self.cFindTranslateMethod.__name__,
				"method" : self.cFindTranslateMethod
			}
		]

	###

	def setWord(self, word) :
		self._line_edit.setText(word)
		self.setFocus()

	def setDictsList(self, dicts_list) :
		self._internal_word_search.setDictsList(dicts_list)
		self._external_word_search.setDictsList(dicts_list)

	###

	def uFind(self, word = None) :
		word = ( self._line_edit.text().simplified() if word == None else word.simplified() )
		if word.isEmpty() :
			return
		self._external_word_search.uFind(word)
		self.wordChangedSignal(word)

	def cFind(self, word = None) :
		word = ( self._line_edit.text().simplified() if word == None else word.simplified() )
		if word.isEmpty() :
			return
		self._external_word_search.cFind(word)
		self.wordChangedSignal(word)

	def lFind(self, word = None) :
		word = ( self._line_edit.text().simplified() if word == None else word.simplified() )
		if word.isEmpty() :
			self._list_browser.setText(tr("Enter the word, please"))
			return
		self._internal_word_search.lFind(word)

	def iFind(self, word = None) :
		word = ( self._line_edit.text().simplified() if word == None else word.simplified() )
		if word.isEmpty() :
			self._list_browser.setText(tr("Enter the word, please"))
			return
		self._internal_word_search.iFind(word)

	def uFindInNewTab(self, word = None) :
		word = ( self._line_edit.text().simplified() if word == None else word.simplified() )
		if word.isEmpty() :
			return
		self.newTabRequestSignal()
		self._external_word_search.uFind(word)
		self.wordChangedSignal(word)

	def cFindInNewTab(self, word = None) :
		word = ( self._line_edit.text().simplified() if word == None else word.simplified() )
		if word.isEmpty() :
			return
		self.newTabRequestSignal()
		self._external_word_search.cFind(word)
		self.wordChangedSignal(word)

	###

	def uFindTranslateMethod(self, word) :
		self.setWord(word)
		self.uFind(word)

	def cFindTranslateMethod(self, word) :
		self.setWord(word)
		self.cFind(word)

	###

	def saveSettings(self) :
		pass

	def loadSettings(self) :
		pass

	###

	def show(self) :
		Qt.QDockWidget.show(self)
		self.raise_()
		self.setFocus()

	def setFocus(self, reason = Qt.Qt.OtherFocusReason) :
		self._line_edit.setFocus(reason)
		self._line_edit.selectAll()

	def hasInternalFocus(self) :
		return self._line_edit.hasFocus()

	def clear(self) :
		self._line_edit.clear()


	### Private ###

	def lFindAfterDelay(self) :
		self._delay_timer.stop()
		self.lFind()

	###

	def processStarted(self) :
		self._u_find_button.setEnabled(False)
		self._c_find_button.setEnabled(False)
		self._i_find_button.setEnabled(False)

		self.processStartedSignal()

	def processFinished(self) :
		line_edit_empty_flag = self._line_edit.text().simplified().isEmpty()
		self._u_find_button.setEnabled(not line_edit_empty_flag)
		self._c_find_button.setEnabled(not line_edit_empty_flag)
		self._i_find_button.setEnabled(not line_edit_empty_flag)

		self.processFinishedSignal()
	###

	def setStatusFromLineEdit(self, word) :
		line_edit_empty_flag = word.simplified().isEmpty()
		self._u_find_button.setEnabled(not line_edit_empty_flag)
		self._c_find_button.setEnabled(not line_edit_empty_flag)
		self._i_find_button.setEnabled(not line_edit_empty_flag)

	###

	def activateDockWidget(self, activate_flag) :
		if activate_flag :
			self._line_edit.setFocus(Qt.Qt.OtherFocusReason)
			self._line_edit.selectAll()


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

