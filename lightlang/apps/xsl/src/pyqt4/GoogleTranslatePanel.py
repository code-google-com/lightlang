# -*- coding: utf8 -*-
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

		self.options_layout = Qt.QHBoxLayout()
		self.main_layout.addLayout(self.options_layout)

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
		self.options_layout.addWidget(self.langpair_combobox)

		self.translate_button = Qt.QPushButton(self.tr("Translate"))
		self.translate_button.setEnabled(False)
		self.translate_button.adjustSize()
		self.translate_button.setFixedSize(self.translate_button.size())
		self.options_layout.addWidget(self.translate_button)

		self.abort_button = Qt.QToolButton()
		self.abort_button.setIcon(Qt.QIcon(IconsDir+"abort_16.png"))
		self.abort_button.setIconSize(Qt.QSize(16, 16))
		self.abort_button.setEnabled(False)
		self.options_layout.addWidget(self.abort_button)

		self.text_edit = Qt.QTextEdit()
		self.main_layout.addWidget(self.text_edit)

		#####

		self.connect(self.google_translate, Qt.SIGNAL("processStarted()"), self.setEnabledAbortButton)
		self.connect(self.google_translate, Qt.SIGNAL("processFinished()"), self.setDisabledAbortButton)
		self.connect(self.google_translate, Qt.SIGNAL("clearRequest()"), self.clearRequestSignal)
		self.connect(self.google_translate, Qt.SIGNAL("wordChanged(const QString &)"), self.wordChangedSignal)
		self.connect(self.google_translate, Qt.SIGNAL("textChanged(const QString &)"), self.textChangedSignal)
		self.connect(self.google_translate, Qt.SIGNAL("statusChanged(const QString &)"), self.statusChangedSignal)

		self.connect(self.translate_button, Qt.SIGNAL("clicked()"), self.translate)
		self.connect(self.abort_button, Qt.SIGNAL("clicked()"), self.abort)
		self.connect(self.text_edit, Qt.SIGNAL("textChanged()"), self.setStatusFromTextEdit)


	### Public ###

	def saveSettings(self) :
		settings = Qt.QSettings(Const.Organization, Const.MyName)
		settings.setValue("google_translate_panel/langpair_combobox_index",
			Qt.QVariant(self.langpair_combobox.currentIndex()))

	def loadSettings(self) :
		settings = Qt.QSettings(Const.Organization, Const.MyName)
		self.langpair_combobox.setCurrentIndex(settings.value("google_translate_panel/langpair_combobox_index",
			Qt.QVariant(0)).toInt()[0])

	def setFocus(self, reason) :
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

	def setEnabledAbortButton(self) :
		self.abort_button.setEnabled(True)

	def setDisabledAbortButton(self) :
		self.abort_button.setEnabled(False)

	def setStatusFromTextEdit(self) :
		if self.text_edit.toPlainText().isEmpty() :
			self.translate_button.setEnabled(False)
		else :
			self.translate_button.setEnabled(True)


	### Signals ###

	def wordChangedSignal(self, word) :
		self.emit(Qt.SIGNAL("wordChanged(const QString &)"), word)

	def textChangedSignal(self, text) :
		self.emit(Qt.SIGNAL("textChanged(const QString &)"), text)

	def clearRequestSignal(self) :
		self.emit(Qt.SIGNAL("clearRequest()"))

	def statusChangedSignal(self, str) :
		self.emit(Qt.SIGNAL("statusChanged(const QString &)"), str)
