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
import Locale
import Settings
import IconsLoader
import GoogleTranslate
import LangsList
import TextEdit


##### Public classes #####
class GoogleTranslatePanel(Qt.QDockWidget) :
	def __init__(self, parent = None) :
		Qt.QDockWidget.__init__(self, parent)

		self.setObjectName("google_translate_panel")

		self.setAllowedAreas(Qt.Qt.AllDockWidgetAreas)

		self.setWindowTitle(tr("Google Translate"))

		#####

		self._main_widget = Qt.QWidget()
		self.setWidget(self._main_widget)

		self._main_layout = Qt.QVBoxLayout()
		self._main_widget.setLayout(self._main_layout)

		self._langs_layout = Qt.QHBoxLayout()
		self._main_layout.addLayout(self._langs_layout)

		self._text_edit_layout = Qt.QHBoxLayout()
		self._main_layout.addLayout(self._text_edit_layout)

		self._control_buttons_layout = Qt.QHBoxLayout()
		self._main_layout.addLayout(self._control_buttons_layout)

		#####

		self._google_translate = GoogleTranslate.GoogleTranslate()

		#####

		self._sl_combobox = Qt.QComboBox()
		self._sl_combobox.setSizeAdjustPolicy(Qt.QComboBox.AdjustToMinimumContentsLength)
		self._sl_combobox.setMaxVisibleItems(15)
		self._sl_combobox.addItem(IconsLoader.icon("help-hint"), tr("Guess"), Qt.QVariant(""))
		self._sl_combobox.insertSeparator(1)
		for langs_list_item in LangsList.langsList() :
			self._sl_combobox.addItem(IconsLoader.icon("flags/"+langs_list_item["code"]),
				langs_list_item["name"], Qt.QVariant(langs_list_item["code"]))
		self._langs_layout.addWidget(self._sl_combobox)

		self._invert_langs_button = Qt.QToolButton()
		self._invert_langs_button.setIcon(IconsLoader.icon("go-jump"))
		self._invert_langs_button.setIconSize(Qt.QSize(16, 16))
		self._invert_langs_button.setCursor(Qt.Qt.ArrowCursor)
		self._invert_langs_button.setAutoRaise(True)
		self._langs_layout.addWidget(self._invert_langs_button)

		self._tl_combobox = Qt.QComboBox()
		self._tl_combobox.setSizeAdjustPolicy(Qt.QComboBox.AdjustToMinimumContentsLength)
		self._tl_combobox.setMaxVisibleItems(15)
		self._tl_combobox.addItem(IconsLoader.icon("flags/"+Locale.mainLang()),
			LangsList.langName(Locale.mainLang()), Qt.QVariant(Locale.mainLang()))
		self._tl_combobox.insertSeparator(1)
		for langs_list_item in LangsList.langsList() :
			self._tl_combobox.addItem(IconsLoader.icon("flags/"+langs_list_item["code"]),
				langs_list_item["name"], Qt.QVariant(langs_list_item["code"]))
		self._langs_layout.addWidget(self._tl_combobox)

		self._text_edit = TextEdit.TextEdit()
		self._text_edit_layout.addWidget(self._text_edit)

		self._translate_button = Qt.QPushButton(tr("T&ranslate"))
		self._translate_button.setEnabled(False)
		self._translate_button.setToolTip(tr("Ctrl+Enter"))
		self._control_buttons_layout.addWidget(self._translate_button)

		self._abort_button = Qt.QToolButton()
		self._abort_button.setIcon(IconsLoader.icon("dialog-cancel"))
		self._abort_button.setIconSize(Qt.QSize(16, 16))
		self._abort_button.setEnabled(False)
		self._control_buttons_layout.addWidget(self._abort_button)

		#####

		self.connect(self, Qt.SIGNAL("visibilityChanged(bool)"), self.activateDockWidget)

		self.connect(self._google_translate, Qt.SIGNAL("processStarted()"), self.processStarted)
		self.connect(self._google_translate, Qt.SIGNAL("processFinished()"), self.processFinished)
		self.connect(self._google_translate, Qt.SIGNAL("clearRequest()"), self.clearRequestSignal)
		self.connect(self._google_translate, Qt.SIGNAL("wordChanged(const QString &)"), self.wordChangedSignal)
		self.connect(self._google_translate, Qt.SIGNAL("textChanged(const QString &)"), self.textChangedSignal)
		self.connect(self._google_translate, Qt.SIGNAL("statusChanged(const QString &)"), self.statusChangedSignal)

		self.connect(self._invert_langs_button, Qt.SIGNAL("clicked()"), self.invertLangs)

		self.connect(self._text_edit, Qt.SIGNAL("textChanged()"), self.setStatusFromTextEdit)
		self.connect(self._text_edit, Qt.SIGNAL("textApplied()"), self._translate_button.animateClick)

		self.connect(self._translate_button, Qt.SIGNAL("clicked()"), self.translate)
		self.connect(self._translate_button, Qt.SIGNAL("clicked()"), self.setFocus)
		self.connect(self._abort_button, Qt.SIGNAL("clicked()"), self.abort)


	### Public ###

	def requisites(self) :
		return {
			"icon" : IconsLoader.icon("applications-internet"),
			"title" : self.windowTitle(),
			"area" : Qt.Qt.LeftDockWidgetArea,
			"hotkey" : Qt.QKeySequence("Ctrl+G")
		}

	def translateMethods(self) :
		return [
			{
				"title" : tr("Google Translate"),
				"object_name" : self.objectName(),
				"method_name" : self.googleTranslateMethod.__name__,
				"method" : self.googleTranslateMethod
			}
		]

	###

	def setText(self, text) :
		self._text_edit.setText(text)

	###

	def googleTranslateMethod(self, text) :
		self.setText(text)
		self.translate()

	###

	def saveSettings(self) :
		settings = Settings.settings()
		settings.setValue("google_translate_panel/sl_combobox_index", Qt.QVariant(self._sl_combobox.currentIndex()))
		settings.setValue("google_translate_panel/tl_combobox_index", Qt.QVariant(self._tl_combobox.currentIndex()))

	def loadSettings(self) :
		settings = Settings.settings()
		self._sl_combobox.setCurrentIndex(settings.value("google_translate_panel/sl_combobox_index", Qt.QVariant(0)).toInt()[0])
		self._tl_combobox.setCurrentIndex(settings.value("google_translate_panel/tl_combobox_index", Qt.QVariant(0)).toInt()[0])

	###

	def show(self) :
		Qt.QDockWidget.show(self)
		self.raise_()
		self.setFocus()

	def setFocus(self, reason = Qt.Qt.OtherFocusReason) :
		self._text_edit.setFocus(reason)
		self._text_edit.selectAll()

	def hasInternalFocus(self) :
		return self._text_edit.hasFocus()

	def clear(self) :
		self._text_edit.clear()


	### Private ###

	def invertLangs(self) :
		sl_index = self._sl_combobox.currentIndex()
		tl_index = self._tl_combobox.currentIndex()

		self._sl_combobox.setCurrentIndex(tl_index)
		self._tl_combobox.setCurrentIndex(sl_index)

	def translate(self) :
		text = self._text_edit.toPlainText()
		if text.simplified().isEmpty() :
			return

		sl_index = self._sl_combobox.currentIndex()
		sl = self._sl_combobox.itemData(sl_index).toString()

		tl_index = self._tl_combobox.currentIndex()
		tl = self._tl_combobox.itemData(tl_index).toString()

		self._google_translate.translate(sl, tl, text)

	def abort(self) :
		self._google_translate.abort()

	###

	def processStarted(self) :
		self._abort_button.setEnabled(True)
		self._translate_button.setEnabled(False)

		self.processStartedSignal()

	def processFinished(self) :
		self._abort_button.setEnabled(False)
		self._translate_button.setEnabled(not self._text_edit.toPlainText().simplified().isEmpty())

		self.processFinishedSignal()

	###

	def setStatusFromTextEdit(self) :
		self._translate_button.setEnabled(not self._text_edit.toPlainText().simplified().isEmpty())

	###

	def activateDockWidget(self, activate_flag) :
		if activate_flag :
			self._text_edit.setFocus(Qt.Qt.OtherFocusReason)
			self._text_edit.selectAll()


	### Signals ###

	def processStartedSignal(self) :
		self.emit(Qt.SIGNAL("processStarted()"))

	def processFinishedSignal(self) :
		self.emit(Qt.SIGNAL("processFinished()"))

	def wordChangedSignal(self, word) :
		self.emit(Qt.SIGNAL("wordChanged(const QString &)"), word)

	def textChangedSignal(self, text) :
		self.emit(Qt.SIGNAL("textChanged(const QString &)"), text)

	def clearRequestSignal(self) :
		self.emit(Qt.SIGNAL("clearRequest()"))

	def statusChangedSignal(self, str) :
		self.emit(Qt.SIGNAL("statusChanged(const QString &)"), str)

