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


#####
def tr(str) :
	return Qt.QApplication.translate("@default", str)


#####
class TrayMenu(Qt.QMenu) :
	def __init__(self, icon = None, text = None, parent = None) :
		Qt.QMenu.__init__(self, parent)

		if icon != None and text != None :
			self.addCaption(icon, text)


	### Public ###

	def addCaption(self, icon, text, before_action = None) :
		fictive_action = Qt.QWidgetAction(self)

		fictive_action_frame = Qt.QFrame()
		fictive_action_frame.setFrameShape(Qt.QFrame.Box) # Qt.QFrame.StyledPanel
		fictive_action.setDefaultWidget(fictive_action_frame)

		fictive_action_frame_layout = Qt.QHBoxLayout()
		fictive_action_frame_layout.setContentsMargins(1, 1, 50, 1)
		fictive_action_frame.setLayout(fictive_action_frame_layout)

		fictive_action_icon_label = Qt.QLabel()
		icon_width = icon_height = self.style().pixelMetric(Qt.QStyle.PM_SmallIconSize)
		fictive_action_icon_label.setPixmap(icon.pixmap(Qt.QSize(icon_width, icon_height)))
		fictive_action_frame_layout.insertWidget(-1, fictive_action_icon_label, 0)

		fictive_action_caption_label = Qt.QLabel(text)
		fictive_action_frame_layout.insertWidget(-1, fictive_action_caption_label, 20)

		font = fictive_action_caption_label.font()
		font.setBold(True)
		fictive_action_caption_label.setFont(font)

		self.insertAction(before_action, fictive_action)

		return fictive_action

