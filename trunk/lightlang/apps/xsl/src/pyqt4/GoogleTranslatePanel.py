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
import GoogleTranslate

#####
IconsDir = Config.Prefix+"/lib/xsl/icons/"

#####
class GoogleTranslatePanel(Qt.QDockWidget) :
	def __init__(self, parent = None) :
		Qt.QDockWidget.__init__(self, parent)

		self.setObjectName("google_translate_panel")

		self.setWindowTitle(self.tr("Google Translate"))
		self.setAllowedAreas(Qt.Qt.AllDockWidgetAreas)

		self.main_widget = Qt.QWidget()
		self.setWidget(self.main_widget)

		self.main_layout = Qt.QVBoxLayout()
		self.main_widget.setLayout(self.main_layout)

		#####

		self.langpair_combobox_layout = Qt.QHBoxLayout()
		self.main_layout.addLayout(self.langpair_combobox_layout)

		self.text_edit_layout = Qt.QHBoxLayout()
		self.main_layout.addLayout(self.text_edit_layout)

		self.control_buttons_layout = Qt.QHBoxLayout()
		self.main_layout.addLayout(self.control_buttons_layout)

		#####

		self.google_translate = GoogleTranslate.GoogleTranslate()

		#####

		self.langpair_combobox = Qt.QComboBox()
		self.langpair_combobox.addItem(self.tr("Arabic to English"), Qt.QVariant("ar|en"))
		self.langpair_combobox.addItem(self.tr("Chinese to English"), Qt.QVariant("zh|en"))
		self.langpair_combobox.addItem(self.tr("Chinese (S. to T.)"), Qt.QVariant("zh-CN|zh-TW"))
		self.langpair_combobox.addItem(self.tr("Chinese (T. to S.)"), Qt.QVariant("zh-TW|zh-CN"))
		self.langpair_combobox.addItem(self.tr("English to Arabic"), Qt.QVariant("en|ar"))
		self.langpair_combobox.addItem(self.tr("English to Chinese (S.)"), Qt.QVariant("en|zh-CN"))
		self.langpair_combobox.addItem(self.tr("English to Chinese (T.)"), Qt.QVariant("en|zh-TW"))
		self.langpair_combobox.addItem(self.tr("English to French"), Qt.QVariant("en|fr"))
		self.langpair_combobox.addItem(self.tr("English to German"), Qt.QVariant("en|de"))
		self.langpair_combobox.addItem(self.tr("English to Italian"), Qt.QVariant("en|it"))
		self.langpair_combobox.addItem(self.tr("English to Japanese"), Qt.QVariant("en|ja"))
		self.langpair_combobox.addItem(self.tr("English to Korean"), Qt.QVariant("en|ko"))
		self.langpair_combobox.addItem(self.tr("English to Portuguese"), Qt.QVariant("en|pt"))
		self.langpair_combobox.addItem(self.tr("English to Russian"), Qt.QVariant("en|ru"))
		self.langpair_combobox.addItem(self.tr("English to Spanish"), Qt.QVariant("en|es"))
		self.langpair_combobox.addItem(self.tr("French to English"), Qt.QVariant("fr|en"))
		self.langpair_combobox.addItem(self.tr("French to German"), Qt.QVariant("fr|de"))
		self.langpair_combobox.addItem(self.tr("German to English"), Qt.QVariant("de|en"))
		self.langpair_combobox.addItem(self.tr("German to French"), Qt.QVariant("de|fr"))
		self.langpair_combobox.addItem(self.tr("Italian to English"), Qt.QVariant("it|en"))
		self.langpair_combobox.addItem(self.tr("Japanese to English"), Qt.QVariant("ja|en"))
		self.langpair_combobox.addItem(self.tr("Korean to English"), Qt.QVariant("ko|en"))
		self.langpair_combobox.addItem(self.tr("Portuguese to English"), Qt.QVariant("pt|en"))
		self.langpair_combobox.addItem(self.tr("Russian to English"), Qt.QVariant("ru|en"))
		self.langpair_combobox.addItem(self.tr("Spanish to English"), Qt.QVariant("es|en"))
		self.langpair_combobox_layout.addWidget(self.langpair_combobox)

		self.text_edit = Qt.QTextEdit()
		self.text_edit_layout.addWidget(self.text_edit)

		self.clear_text_edit_button = Qt.QToolButton()
		self.clear_text_edit_button.setIcon(Qt.QIcon(IconsDir+"clear_22.png"))
		self.clear_text_edit_button.setIconSize(Qt.QSize(16, 16))
		size_policy = self.clear_text_edit_button.sizePolicy()
		size_policy.setVerticalPolicy(Qt.QSizePolicy.Expanding)
		self.clear_text_edit_button.setSizePolicy(size_policy)
		self.clear_text_edit_button.setEnabled(False)
		self.text_edit_layout.addWidget(self.clear_text_edit_button)

		self.translate_button = Qt.QPushButton(self.tr("&Translate"))
		self.translate_button.setEnabled(False)
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

		self.connect(self.text_edit, Qt.SIGNAL("textChanged()"), self.setStatusFromTextEdit)

		self.connect(self.clear_text_edit_button, Qt.SIGNAL("clicked()"), self.clearTextEdit)

		self.connect(self.translate_button, Qt.SIGNAL("clicked()"), self.translate)
		self.connect(self.abort_button, Qt.SIGNAL("clicked()"), self.abort)


	### Public ###

	def saveSettings(self) :
		settings = Qt.QSettings(Const.Organization, Const.MyName)
		settings.setValue("google_translate_panel/langpair_combobox_index",
			Qt.QVariant(self.langpair_combobox.currentIndex()))

	def loadSettings(self) :
		settings = Qt.QSettings(Const.Organization, Const.MyName)
		self.langpair_combobox.setCurrentIndex(settings.value("google_translate_panel/langpair_combobox_index",
			Qt.QVariant(0)).toInt()[0])

	###

	def clear(self) :
		self.text_edit.clear()

	def setFocus(self, reason = Qt.Qt.OtherFocusReason) :
		self.text_edit.setFocus(reason)
		self.text_edit.selectAll()


	### Private ###

	def abort(self) :
		self.google_translate.abort()

	def translate(self) :
		index = self.langpair_combobox.currentIndex()
		langpair = self.langpair_combobox.itemData(index).toString()
		text = self.text_edit.toPlainText()

		self.google_translate.translate(langpair, text)

		self.abort_button.setEnabled(True)

	###

	def processStarted(self) :
		self.abort_button.setEnabled(True)

		self.clear_text_edit_button.setEnabled(False)
		self.translate_button.setEnabled(False)

		self.processStartedSignal()

	def processFinished(self) :
		self.abort_button.setEnabled(False)

		self.clear_text_edit_button.setEnabled(True)
		self.translate_button.setEnabled(True)

		self.processFinishedSignal()

	def setStatusFromTextEdit(self) :
		if self.text_edit.toPlainText().isEmpty() :
			self.clear_text_edit_button.setEnabled(False)
			self.translate_button.setEnabled(False)
		else :
			self.clear_text_edit_button.setEnabled(True)
			self.translate_button.setEnabled(True)

	def activateDockWidget(self, activate_flag) :
		if activate_flag :
			self.text_edit.setFocus(Qt.Qt.OtherFocusReason)
			self.text_edit.selectAll()

	def clearTextEdit(self) :
		self.text_edit.clear()
		self.text_edit.setFocus(Qt.Qt.OtherFocusReason)


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

