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
import DictInformationWindow


#####
IconsDir = Config.Prefix+"/lib/xsl/icons/"


#####
def tr(str) :
	return Qt.QApplication.translate("@default", str)


#####
class DictsListWidgetItem(Qt.QWidget) :
	def __init__(self, dict_name, enable_dict_state, parent = None) :
		Qt.QWidget.__init__(self, parent)

		if self.font().pixelSize() > 0 :
			self.setFixedHeight((self.font().pixelSize() + 5) * 2)
		elif self.font().pointSize() > 0 :
			self.setFixedHeight((self.font().pointSize() + 5) * 2)
		else :
			self.setFixedHeight(30)

		#####

		self.main_layout = Qt.QHBoxLayout()
		self.main_layout.setContentsMargins(5, 5, 5, 5)
		self.main_layout.setSpacing(3)
		self.setLayout(self.main_layout)

		#####

		self.dict_name = Qt.QString(dict_name)

		self.dict_information_window = DictInformationWindow.DictInformationWindow(dict_name)

		#####

		self.enable_dict_checkbox = Qt.QCheckBox()
		self.enable_dict_checkbox.setCheckState(enable_dict_state)
		self.main_layout.addWidget(self.enable_dict_checkbox)

		self.vertical_frame1 = Qt.QFrame()
		self.vertical_frame1.setFrameStyle(Qt.QFrame.VLine|Qt.QFrame.Sunken)
		self.main_layout.addWidget(self.vertical_frame1)

		self.dict_caption_label = Qt.QLabel()
		index = dict_name.lastIndexOf(".")
		if index >= 0 :
			dict_caption = dict_name.left(index)
		else :
			dict_caption = Qt.QString(dict_name)
		dict_caption.replace("_", " ")
		self.dict_caption_label.setText(dict_caption)
		self.main_layout.addWidget(self.dict_caption_label)

		self.main_layout.addStretch()

		self.dict_direction_label = Qt.QLabel()
		index = dict_name.lastIndexOf(".")
		if index >= 0 :
			self.dict_direction_label.setText(dict_name.mid(index +1))
		self.main_layout.addWidget(self.dict_direction_label)

		self.vertical_frame2 = Qt.QFrame()
		self.vertical_frame2.setFrameStyle(Qt.QFrame.VLine|Qt.QFrame.Sunken)
		self.main_layout.addWidget(self.vertical_frame2)

		self.show_information_button = Qt.QToolButton()
		self.show_information_button.setIcon(Qt.QIcon(IconsDir+"info_16.png"))
		self.show_information_button.setIconSize(Qt.QSize(16, 16))
		self.show_information_button.setCursor(Qt.Qt.ArrowCursor)
		self.show_information_button.setAutoRaise(True)
		self.main_layout.addWidget(self.show_information_button)

		#####

		self.connect(self.enable_dict_checkbox, Qt.SIGNAL("stateChanged(int)"), self.stateChangedSignal)

		self.connect(self.show_information_button, Qt.SIGNAL("clicked()"), self.dict_information_window.show)


	### Public ###

	def dictName(self) :
		return Qt.QString(self.dict_name)

	def dictCaption(self) :
		return self.dict_caption_label.text()

	def dictDirection(self) :
		return self.dict_direction_label.text()

	def dictState(self) :
		return self.enable_dict_checkbox.checkState()

	###

	def invertDictState(self) :
		if self.enable_dict_checkbox.checkState() == Qt.Qt.Checked :
			self.enable_dict_checkbox.setCheckState(Qt.Qt.Unchecked)
		else :
			self.enable_dict_checkbox.setCheckState(Qt.Qt.Checked)


	### Signals ###

	def stateChangedSignal(self, state) :
		self.emit(Qt.SIGNAL("stateChanged(int)"), state)

