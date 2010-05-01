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

		self.main_layout = Qt.QHBoxLayout()
		self.main_layout.setContentsMargins(2, 0, 0, 0)
		self.main_layout.setSpacing(0)
		self.setLayout(self.main_layout)

		self.horizontal_grab_widget = HorizontalGrabWidget.HorizontalGrabWidget()
		self.main_layout.addWidget(self.horizontal_grab_widget)

		self.enable_dict_checkbox_layout = Qt.QVBoxLayout()
		self.enable_dict_checkbox_layout.setContentsMargins(5, 5, 5, 5)
		self.enable_dict_checkbox_layout.setSpacing(3)
		self.main_layout.addLayout(self.enable_dict_checkbox_layout)

		self.vertical_frame1 = Qt.QFrame()
		self.vertical_frame1.setFrameStyle(Qt.QFrame.VLine|Qt.QFrame.Sunken)
		self.main_layout.addWidget(self.vertical_frame1)

		self.dict_info_layout = Qt.QVBoxLayout()
		self.dict_info_layout.setContentsMargins(10, 1, 10, 1)
		self.dict_info_layout.setSpacing(1)
		self.main_layout.addLayout(self.dict_info_layout)

		self.dict_name_layout = Qt.QHBoxLayout()
		self.dict_info_layout.addLayout(self.dict_name_layout)

		self.dict_details_layout = Qt.QHBoxLayout()
		self.dict_info_layout.addLayout(self.dict_details_layout)

		#####

		self.dict_name = Qt.QString(dict_name)

		self.dict_info_window = DictInfoWindow.DictInfoWindow(dict_name)

		#####

		self.enable_dict_checkbox = Qt.QCheckBox()
		self.enable_dict_checkbox.setCheckState(dict_state)
		self.enable_dict_checkbox.setToolTip(tr("Enter"))
		self.enable_dict_checkbox_layout.addWidget(self.enable_dict_checkbox)

		###

		self.dict_caption_label = Qt.QLabel()
		self.dict_caption_label.setTextFormat(Qt.Qt.RichText)
		self.dict_name_layout.addWidget(self.dict_caption_label)

		self.dict_name_layout.addStretch()

		self.dict_direction_label = Qt.QLabel()
		self.dict_direction_label.setTextFormat(Qt.Qt.RichText)
		self.dict_name_layout.addWidget(self.dict_direction_label)

		self.dict_details_layout.addItem(Qt.QSpacerItem(40, 0))

		self.dict_full_direction_label = Qt.QLabel()
		self.dict_full_direction_label.setTextFormat(Qt.Qt.RichText)
		self.dict_details_layout.addWidget(self.dict_full_direction_label)

		dict_name_regexp = Qt.QRegExp("([^\\.]+)\\.((..)-(..))")
		if dict_name_regexp.exactMatch(dict_name) :
			dict_caption = dict_name_regexp.cap(1)
			dict_caption.replace("_", " ")
			dict_caption.replace(".", " ")
			self.dict_caption_label.setText(Qt.QString("<html><head><style>%1</style></head><body><font class=\"text_label_font\">"
				"%2</font></body></html>").arg(UserStyleCss.userStyleCss()).arg(dict_caption))

			self.dict_direction_label.setText(Qt.QString("<html><head><style>%1</style></head><body><font class=\"text_label_font\">"
				"%2</font></body></html>").arg(UserStyleCss.userStyleCss()).arg(dict_name_regexp.cap(2)))

			self.dict_details_layout.insertSpacing(0, 10)

			self.dict_full_direction_label.setText(Qt.QString("%1 &#187; %2")
				.arg(LangsList.langName(dict_name_regexp.cap(3))).arg(LangsList.langName(dict_name_regexp.cap(4))))
		else :
			self.dict_caption_label.setText(Qt.QString("<html><head><style>%1</style></head><body><font class=\"red_alert_background\">"
				"%2</font></body></html>").arg(UserStyleCss.userStyleCss()).arg(dict_name))

		###

		self.dict_details_layout.addStretch()

		self.show_info_button = Qt.QToolButton()
		self.show_info_button.setIcon(IconsLoader.icon("help-about"))
		self.show_info_button.setIconSize(Qt.QSize(16, 16))
		self.show_info_button.setCursor(Qt.Qt.ArrowCursor)
		self.show_info_button.setAutoRaise(True)
		self.dict_details_layout.addWidget(self.show_info_button)

		#####

		self.connect(self.enable_dict_checkbox, Qt.SIGNAL("stateChanged(int)"), self.stateChangedSignal)

		self.connect(self.show_info_button, Qt.SIGNAL("clicked()"), self.dict_info_window.show)


	### Public ###

	def dictState(self) :
		return self.enable_dict_checkbox.checkState()

	def dictName(self) :
		return Qt.QString(self.dict_name)

	def dictInfo(self) :
		return self.dict_info_window.dictInfo()

	###

	def invertDictState(self) :
		if self.enable_dict_checkbox.checkState() == Qt.Qt.Checked :
			self.enable_dict_checkbox.setCheckState(Qt.Qt.Unchecked)
		else :
			self.enable_dict_checkbox.setCheckState(Qt.Qt.Checked)


	### Signals ###

	def stateChangedSignal(self, state) :
		self.emit(Qt.SIGNAL("stateChanged(int)"), state)

