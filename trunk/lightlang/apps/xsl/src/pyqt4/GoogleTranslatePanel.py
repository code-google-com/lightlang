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
import User
import GoogleTranslate
import TextEdit


#####
IconsDir = Config.Prefix+"/lib/xsl/icons/"


#####
def tr(str) :
	return Qt.QApplication.translate("@default", str)


#####
class GoogleTranslatePanel(Qt.QDockWidget) :
	def __init__(self, parent = None) :
		Qt.QDockWidget.__init__(self, parent)

		self.setObjectName("google_translate_panel")

		self.setWindowTitle(tr("Google Translate"))

		self.setAllowedAreas(Qt.Qt.AllDockWidgetAreas)

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

		self.langs_list = [
			[ tr("Albanian"),		Qt.QVariant("sq") ],
			[ tr("Arabic"),			Qt.QVariant("ar") ],
			[ tr("Bulgarian"),		Qt.QVariant("bg") ],
			[ tr("Catalan"),		Qt.QVariant("ca") ],
			[ tr("Chinese (Simplified)"),	Qt.QVariant("zh-CN") ],
			[ tr("Chinese (Traditional)"),	Qt.QVariant("zh-TW") ],
			[ tr("Croatian"),		Qt.QVariant("hr") ],
			[ tr("Czech"),			Qt.QVariant("cs") ],
			[ tr("Danish"),			Qt.QVariant("da") ],
			[ tr("Dutch"),			Qt.QVariant("nl") ],
			[ tr("English"),		Qt.QVariant("en") ],
			[ tr("Estonian"),		Qt.QVariant("et") ],
			[ tr("Filipino"),		Qt.QVariant("tl") ],
			[ tr("Finnish"),		Qt.QVariant("fi") ],
			[ tr("French"),			Qt.QVariant("fr") ],
			[ tr("Galician"),		Qt.QVariant("gl") ],
			[ tr("German"),			Qt.QVariant("de") ],
			[ tr("Greek"),			Qt.QVariant("el") ],
			[ tr("Hebrew"),			Qt.QVariant("iw") ],
			[ tr("Hindi"),			Qt.QVariant("hi") ],
			[ tr("Hungarian"),		Qt.QVariant("hu") ],
			[ tr("Indonesian"),		Qt.QVariant("id") ],
			[ tr("Italian"),		Qt.QVariant("it") ],
			[ tr("Japanese"),		Qt.QVariant("ja") ],
			[ tr("Korean"),			Qt.QVariant("ko") ],
			[ tr("Latvian"),		Qt.QVariant("lv") ],
			[ tr("Lithuanian"),		Qt.QVariant("lt") ],
			[ tr("Maltese"),		Qt.QVariant("mt") ],
			[ tr("Norwegian"),		Qt.QVariant("no") ],
			[ tr("Polish"),			Qt.QVariant("pl") ],
			[ tr("Portuguese"),		Qt.QVariant("pt") ],
			[ tr("Romanian"),		Qt.QVariant("ro") ],
			[ tr("Russian"),		Qt.QVariant("ru") ],
			[ tr("Serbian"),		Qt.QVariant("sr") ],
			[ tr("Slovak"),			Qt.QVariant("sk") ],
			[ tr("Slovenian"),		Qt.QVariant("sl") ],
			[ tr("Spanish"),		Qt.QVariant("es") ],
			[ tr("Swedish"),		Qt.QVariant("sv") ],
			[ tr("Thai"),			Qt.QVariant("th") ],
			[ tr("Turkish"),		Qt.QVariant("tr") ],
			[ tr("Ukrainian"),		Qt.QVariant("uk") ],
			[ tr("Vietnamese"),		Qt.QVariant("vi") ],
			]
		self.internalSortLangs(0, len(self.langs_list) -1)

		self.lang = Locale.mainLang()

		#####

		self.sl_combobox = Qt.QComboBox()
		self.sl_combobox.setSizeAdjustPolicy(Qt.QComboBox.AdjustToMinimumContentsLength)
		self.sl_combobox.setMaxVisibleItems(15)
		for langs_list_item in self.langs_list :
			self.sl_combobox.addItem(Qt.QIcon(IconsDir+"flags/"+langs_list_item[1].toString()+".png"),
				langs_list_item[0], langs_list_item[1])
		self.sl_combobox.addItem(Qt.QIcon(IconsDir+"question_16.png"), tr("I don't know..."), Qt.QVariant("auto"))
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
		for langs_list_item in self.langs_list :
			self.tl_combobox.addItem(Qt.QIcon(IconsDir+"flags/"+langs_list_item[1].toString()+".png"),
				langs_list_item[0], langs_list_item[1])
		self.tl_combobox.addItem(Qt.QIcon(IconsDir+"flags/"+self.lang+".png"), tr("Your language"), Qt.QVariant(self.lang))
		self.langs_layout.addWidget(self.tl_combobox)

		self.text_edit = TextEdit.TextEdit()
		self.text_edit_layout.addWidget(self.text_edit)

		self.clear_text_edit_button = Qt.QToolButton()
		self.clear_text_edit_button.setIcon(Qt.QIcon(IconsDir+"clear_22.png"))
		self.clear_text_edit_button.setIconSize(Qt.QSize(16, 16))
		size_policy = self.clear_text_edit_button.sizePolicy()
		size_policy.setVerticalPolicy(Qt.QSizePolicy.Expanding)
		self.clear_text_edit_button.setSizePolicy(size_policy)
		self.clear_text_edit_button.setEnabled(False)
		self.text_edit_layout.addWidget(self.clear_text_edit_button)

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
		self.connect(self.text_edit, Qt.SIGNAL("translateRequest()"), self.translate_button.animateClick)

		self.connect(self.clear_text_edit_button, Qt.SIGNAL("clicked()"), self.clearTextEdit)

		self.connect(self.translate_button, Qt.SIGNAL("clicked()"), self.translate)
		self.connect(self.translate_button, Qt.SIGNAL("clicked()"), lambda : self.text_edit.setFocus(Qt.Qt.OtherFocusReason))
		self.connect(self.abort_button, Qt.SIGNAL("clicked()"), self.abort)


	### Public ###

	def saveSettings(self) :
		settings = User.settings()
		settings.setValue("google_translate_panel/sl_combobox_index",
			Qt.QVariant(self.sl_combobox.currentIndex()))
		settings.setValue("google_translate_panel/tl_combobox_index",
			Qt.QVariant(self.tl_combobox.currentIndex()))

	def loadSettings(self) :
		settings = User.settings()
		self.sl_combobox.setCurrentIndex(settings.value("google_translate_panel/sl_combobox_index",
			Qt.QVariant(0)).toInt()[0])
		self.tl_combobox.setCurrentIndex(settings.value("google_translate_panel/tl_combobox_index",
			Qt.QVariant(0)).toInt()[0])

	###

	def clear(self) :
		self.text_edit.clear()

	def setFocus(self, reason = Qt.Qt.OtherFocusReason) :
		self.text_edit.setFocus(reason)
		self.text_edit.selectAll()

	def hasInternalFocus(self) :
		return self.text_edit.hasFocus()


	### Private ###

	def internalSortLangs(self, left, right) :
		if left >= right :
			return

		i = j = left
		while j <= right :
			if self.langs_list[j][0] <= self.langs_list[right][0] :
				self.langs_list[i], self.langs_list[j] = self.langs_list[j], self.langs_list[i]
				i += 1
			j += 1

		self.internalSortLangs(left, i - 2)
		self.internalSortLangs(i, right)

	###

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

		self.clear_text_edit_button.setEnabled(False)
		self.translate_button.setEnabled(False)

		self.processStartedSignal()

	def processFinished(self) :
		self.abort_button.setEnabled(False)

		self.clear_text_edit_button.setEnabled(True)
		self.translate_button.setEnabled(True)

		self.processFinishedSignal()

	def setStatusFromTextEdit(self) :
		if self.text_edit.toPlainText().simplified().isEmpty() :
			self.clear_text_edit_button.setEnabled(False)
			self.translate_button.setEnabled(False)
		else :
			self.clear_text_edit_button.setEnabled(True)
			self.translate_button.setEnabled(True)

	def activateDockWidget(self, activate_flag) :
		if activate_flag :
			self.text_edit.setFocus(Qt.Qt.OtherFocusReason)
			self.text_edit.selectAll()

	###

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

