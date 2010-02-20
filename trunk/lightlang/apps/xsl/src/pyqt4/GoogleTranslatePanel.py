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
import GoogleTranslate
import LangsList
import TextEdit


#####
IconsDir = Config.DataRootDir+"/xsl/icons/"


#####
def tr(str) :
	return Qt.QApplication.translate("@default", str)


#####
class GoogleTranslatePanel(Qt.QDockWidget) :
	def __init__(self, parent = None) :
		Qt.QDockWidget.__init__(self, parent)

		self.setObjectName("google_translate_panel")

		self.setAllowedAreas(Qt.Qt.AllDockWidgetAreas)

		self.setWindowTitle(tr("Google Translate"))

		#####

		self.main_widget = Qt.QWidget()
		self.setWidget(self.main_widget)

		self.main_layout = Qt.QVBoxLayout()
		self.main_widget.setLayout(self.main_layout)

		self.langs_layout = Qt.QHBoxLayout()
		self.main_layout.addLayout(self.langs_layout)

		self.text_edit_layout = Qt.QHBoxLayout()
		self.main_layout.addLayout(self.text_edit_layout)

		self.control_buttons_layout = Qt.QHBoxLayout()
		self.main_layout.addLayout(self.control_buttons_layout)

		#####

		self.google_translate = GoogleTranslate.GoogleTranslate()

		#####

		self.sl_combobox = Qt.QComboBox()
		self.sl_combobox.setSizeAdjustPolicy(Qt.QComboBox.AdjustToMinimumContentsLength)
		self.sl_combobox.setMaxVisibleItems(15)
		self.sl_combobox.addItem(Qt.QIcon(IconsDir+"question_16.png"), tr("Guess"), Qt.QVariant(""))
		self.sl_combobox.insertSeparator(1)
		for langs_list_item in LangsList.langsList() :
			self.sl_combobox.addItem(Qt.QIcon(IconsDir+"flags/"+langs_list_item["code"]+".png"),
				langs_list_item["name"], Qt.QVariant(langs_list_item["code"]))
		self.langs_layout.addWidget(self.sl_combobox)

		self.invert_langs_button = Qt.QToolButton()
		self.invert_langs_button.setIcon(Qt.QIcon(IconsDir+"invert_16.png"))
		self.invert_langs_button.setIconSize(Qt.QSize(16, 16))
		self.invert_langs_button.setCursor(Qt.Qt.ArrowCursor)
		self.invert_langs_button.setAutoRaise(True)
		self.langs_layout.addWidget(self.invert_langs_button)

		self.tl_combobox = Qt.QComboBox()
		self.tl_combobox.setSizeAdjustPolicy(Qt.QComboBox.AdjustToMinimumContentsLength)
		self.tl_combobox.setMaxVisibleItems(15)
		self.tl_combobox.addItem(Qt.QIcon(IconsDir+"flags/"+Locale.mainLang()+".png"), LangsList.langName(Locale.mainLang()),
			Qt.QVariant(Locale.mainLang()))
		self.tl_combobox.insertSeparator(1)
		for langs_list_item in LangsList.langsList() :
			self.tl_combobox.addItem(Qt.QIcon(IconsDir+"flags/"+langs_list_item["code"]+".png"),
				langs_list_item["name"], Qt.QVariant(langs_list_item["code"]))
		self.langs_layout.addWidget(self.tl_combobox)

		self.text_edit = TextEdit.TextEdit()
		self.text_edit_layout.addWidget(self.text_edit)

		self.translate_button = Qt.QPushButton(tr("T&ranslate"))
		self.translate_button.setEnabled(False)
		self.translate_button.setToolTip(tr("Ctrl+Enter"))
		self.control_buttons_layout.addWidget(self.translate_button)

		self.abort_button = Qt.QToolButton()
		self.abort_button.setIcon(Qt.QIcon(IconsDir+"abort_16.png"))
		self.abort_button.setIconSize(Qt.QSize(16, 16))
		self.abort_button.setEnabled(False)
		self.control_buttons_layout.addWidget(self.abort_button)

		#####

		self.connect(self, Qt.SIGNAL("visibilityChanged(bool)"), self.activateDockWidget)

		self.connect(self.google_translate, Qt.SIGNAL("processStarted()"), self.processStarted)
		self.connect(self.google_translate, Qt.SIGNAL("processFinished()"), self.processFinished)
		self.connect(self.google_translate, Qt.SIGNAL("clearRequest()"), self.clearRequestSignal)
		self.connect(self.google_translate, Qt.SIGNAL("wordChanged(const QString &)"), self.wordChangedSignal)
		self.connect(self.google_translate, Qt.SIGNAL("textChanged(const QString &)"), self.textChangedSignal)
		self.connect(self.google_translate, Qt.SIGNAL("statusChanged(const QString &)"), self.statusChangedSignal)

		self.connect(self.invert_langs_button, Qt.SIGNAL("clicked()"), self.invertLangs)

		self.connect(self.text_edit, Qt.SIGNAL("textChanged()"), self.setStatusFromTextEdit)
		self.connect(self.text_edit, Qt.SIGNAL("textApplied()"), self.translate_button.animateClick)

		self.connect(self.translate_button, Qt.SIGNAL("clicked()"), self.translate)
		self.connect(self.translate_button, Qt.SIGNAL("clicked()"), self.setFocus)
		self.connect(self.abort_button, Qt.SIGNAL("clicked()"), self.abort)


	### Public ###

	def requisites(self) :
		return [ Qt.QIcon(IconsDir+"web_16.png"), self.windowTitle(), Qt.Qt.LeftDockWidgetArea, Qt.QKeySequence("Ctrl+G") ]

	def translateMethods(self) :
		return [ [tr("Google Translate"), self.objectName(), "googleTranslate", self.googleTranslateMethod] ]

	###

	def setText(self, text) :
		self.text_edit.setText(text)

	###

	def googleTranslateMethod(self, text) :
		self.setText(text)
		self.translate()

	###

	def saveSettings(self) :
		settings = Settings.settings()
		settings.setValue("google_translate_panel/sl_combobox_index", Qt.QVariant(self.sl_combobox.currentIndex()))
		settings.setValue("google_translate_panel/tl_combobox_index", Qt.QVariant(self.tl_combobox.currentIndex()))

	def loadSettings(self) :
		settings = Settings.settings()
		self.sl_combobox.setCurrentIndex(settings.value("google_translate_panel/sl_combobox_index", Qt.QVariant(0)).toInt()[0])
		self.tl_combobox.setCurrentIndex(settings.value("google_translate_panel/tl_combobox_index", Qt.QVariant(0)).toInt()[0])

	###

	def show(self) :
		Qt.QDockWidget.show(self)
		self.raise_()
		self.setFocus()

	def setFocus(self, reason = Qt.Qt.OtherFocusReason) :
		self.text_edit.setFocus(reason)
		self.text_edit.selectAll()

	def hasInternalFocus(self) :
		return self.text_edit.hasFocus()

	def clear(self) :
		self.text_edit.clear()


	### Private ###

	def invertLangs(self) :
		sl_index = self.sl_combobox.currentIndex()
		tl_index = self.tl_combobox.currentIndex()

		self.sl_combobox.setCurrentIndex(tl_index)
		self.tl_combobox.setCurrentIndex(sl_index)

	def translate(self) :
		text = self.text_edit.toPlainText()
		if text.simplified().isEmpty() :
			return

		sl_index = self.sl_combobox.currentIndex()
		sl = self.sl_combobox.itemData(sl_index).toString()

		tl_index = self.tl_combobox.currentIndex()
		tl = self.tl_combobox.itemData(tl_index).toString()

		self.google_translate.translate(sl, tl, text)

	def abort(self) :
		self.google_translate.abort()

	###

	def processStarted(self) :
		self.abort_button.setEnabled(True)
		self.translate_button.setEnabled(False)

		self.processStartedSignal()

	def processFinished(self) :
		self.abort_button.setEnabled(False)
		self.translate_button.setEnabled(not self.text_edit.toPlainText().simplified().isEmpty())

		self.processFinishedSignal()

	###

	def setStatusFromTextEdit(self) :
		self.translate_button.setEnabled(not self.text_edit.toPlainText().simplified().isEmpty())

	###

	def activateDockWidget(self, activate_flag) :
		if activate_flag :
			self.text_edit.setFocus(Qt.Qt.OtherFocusReason)
			self.text_edit.selectAll()


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

