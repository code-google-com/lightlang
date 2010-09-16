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
import UserStyleCss
import IconsLoader
import LangsList
import HorizontalGrabWidget
import DictInfoWindow


#####
def tr(str) :
	return Qt.QApplication.translate("@default", str)


#####
class DictsListWidgetItem(Qt.QWidget) :
	def __init__(self, dict_state, dict_name, parent = None) :
		Qt.QWidget.__init__(self, parent)

		if self.font().pixelSize() > 0 :
			self.setFixedHeight((self.font().pixelSize()) * 4)
		elif self.font().pointSize() > 0 :
			self.setFixedHeight((self.font().pointSize()) * 4)
		else :
			self.setFixedHeight(40)

		#####

		self._main_layout = Qt.QHBoxLayout()
		self._main_layout.setContentsMargins(2, 0, 0, 0)
		self._main_layout.setSpacing(0)
		self.setLayout(self._main_layout)

		self._horizontal_grab_widget = HorizontalGrabWidget.HorizontalGrabWidget()
		self._main_layout.addWidget(self._horizontal_grab_widget)

		self._enable_dict_checkbox_layout = Qt.QVBoxLayout()
		self._enable_dict_checkbox_layout.setContentsMargins(5, 5, 5, 5)
		self._enable_dict_checkbox_layout.setSpacing(3)
		self._main_layout.addLayout(self._enable_dict_checkbox_layout)

		self._vertical_frame1 = Qt.QFrame()
		self._vertical_frame1.setFrameStyle(Qt.QFrame.VLine|Qt.QFrame.Sunken)
		self._main_layout.addWidget(self._vertical_frame1)

		self._dict_info_layout = Qt.QVBoxLayout()
		self._dict_info_layout.setContentsMargins(10, 1, 10, 1)
		self._dict_info_layout.setSpacing(1)
		self._main_layout.addLayout(self._dict_info_layout)

		self._dict_name_layout = Qt.QHBoxLayout()
		self._dict_info_layout.addLayout(self._dict_name_layout)

		self._dict_details_layout = Qt.QHBoxLayout()
		self._dict_info_layout.addLayout(self._dict_details_layout)

		#####

		self._dict_name = Qt.QString(dict_name)

		self._dict_info_window = DictInfoWindow.DictInfoWindow(dict_name)

		#####

		self._enable_dict_checkbox = Qt.QCheckBox()
		self._enable_dict_checkbox.setCheckState(dict_state)
		self._enable_dict_checkbox.setToolTip(tr("Enter"))
		self._enable_dict_checkbox_layout.addWidget(self._enable_dict_checkbox)

		###

		self._dict_caption_label = Qt.QLabel()
		self._dict_caption_label.setTextFormat(Qt.Qt.RichText)
		self._dict_name_layout.addWidget(self._dict_caption_label)

		self._dict_name_layout.addStretch()

		self._dict_direction_label = Qt.QLabel()
		self._dict_direction_label.setTextFormat(Qt.Qt.RichText)
		self._dict_name_layout.addWidget(self._dict_direction_label)

		self._dict_details_layout.addItem(Qt.QSpacerItem(40, 0))

		self._dict_full_direction_label = Qt.QLabel()
		self._dict_full_direction_label.setTextFormat(Qt.Qt.RichText)
		self._dict_details_layout.addWidget(self._dict_full_direction_label)

		dict_name_regexp = Qt.QRegExp("([^\\.]+)\\.((..)-(..))")
		if dict_name_regexp.exactMatch(dict_name) :
			dict_caption = dict_name_regexp.cap(1)
			dict_caption.replace("_", " ")
			dict_caption.replace(".", " ")
			self._dict_caption_label.setText(Qt.QString("<html><head><style>%1</style></head><body><font class=\"text_label_font\">"
				"%2</font></body></html>").arg(UserStyleCss.userStyleCss()).arg(dict_caption))

			self._dict_direction_label.setText(Qt.QString("<html><head><style>%1</style></head><body><font class=\"text_label_font\">"
				"%2</font></body></html>").arg(UserStyleCss.userStyleCss()).arg(dict_name_regexp.cap(2)))

			self._dict_details_layout.insertSpacing(0, 10)

			self._dict_full_direction_label.setText(Qt.QString("%1 &#187; %2")
				.arg(LangsList.langName(dict_name_regexp.cap(3))).arg(LangsList.langName(dict_name_regexp.cap(4))))
		else :
			self._dict_caption_label.setText(Qt.QString("<html><head><style>%1</style></head><body><font class=\"red_alert_background\">"
				"%2</font></body></html>").arg(UserStyleCss.userStyleCss()).arg(dict_name))

		###

		self._dict_details_layout.addStretch()

		self._show_info_button = Qt.QToolButton()
		self._show_info_button.setIcon(IconsLoader.icon("help-about"))
		self._show_info_button.setIconSize(Qt.QSize(16, 16))
		self._show_info_button.setCursor(Qt.Qt.ArrowCursor)
		self._show_info_button.setAutoRaise(True)
		self._dict_details_layout.addWidget(self._show_info_button)

		#####

		self.connect(self._enable_dict_checkbox, Qt.SIGNAL("stateChanged(int)"), self.stateChangedSignal)

		self.connect(self._show_info_button, Qt.SIGNAL("clicked()"), self._dict_info_window.show)


	### Public ###

	def dictState(self) :
		return self._enable_dict_checkbox.checkState()

	def dictName(self) :
		return Qt.QString(self._dict_name)

	def dictInfo(self) :
		return self._dict_info_window.dictInfo()

	###

	def invertDictState(self) :
		if self._enable_dict_checkbox.checkState() == Qt.Qt.Checked :
			self._enable_dict_checkbox.setCheckState(Qt.Qt.Unchecked)
		else :
			self._enable_dict_checkbox.setCheckState(Qt.Qt.Checked)


	### Signals ###

	def stateChangedSignal(self, state) :
		self.emit(Qt.SIGNAL("stateChanged(int)"), state)

