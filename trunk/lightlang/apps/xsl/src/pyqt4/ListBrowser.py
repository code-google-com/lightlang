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


#####
def tr(str) :
	return Qt.QApplication.translate("@default", str)


#####
class ListBrowser(Qt.QListWidget) :
	def __init__(self, parent = None) :
		Qt.QListWidget.__init__(self, parent)

		#####

		self.warning_item_regexp = Qt.QRegExp("\\{\\{(.*)\\}\\}")
		self.warning_item_regexp.setMinimal(True)

		self.caption_item_regexp = Qt.QRegExp("\\[\\[(.*)\\|\\|(.*)\\]\\]")
		self.caption_item_regexp.setMinimal(True)


	### Public ###

	def setList(self, list) :
		self.clear()

		count = 0
		while count < list.count() :
			if self.warning_item_regexp.exactMatch(list[count]) :
				warning_item = Qt.QListWidgetItem(self.warning_item_regexp.cap(1))
				warning_item.setFlags(Qt.Qt.NoItemFlags)

				self.addItem(warning_item)
			elif self.caption_item_regexp.exactMatch(list[count]) :
				caption_item = Qt.QListWidgetItem(self.caption_item_regexp.cap(1))

				caption_item_font = caption_item.font()
				caption_item_font.setBold(True)
				caption_item_font.setItalic(True)

				if caption_item_font.pixelSize() > 0 :
					caption_item_font.setPixelSize(caption_item_font.pixelSize() +1)
				elif caption_item_font.pointSize() > 0 :
					caption_item_font.setPointSize(caption_item_font.pointSize() +1)

				caption_item_foreground_brush = caption_item.foreground()
				caption_item_foreground_brush.setStyle(Qt.Qt.SolidPattern)

				caption_item_background_brush = caption_item.background()
				caption_item_background_brush.setStyle(Qt.Qt.SolidPattern)
				caption_item_background_brush.setColor(Qt.QColor(self.caption_item_regexp.cap(2)))

				caption_item.setFlags(Qt.Qt.NoItemFlags)
				caption_item.setTextAlignment(Qt.Qt.AlignHCenter|Qt.Qt.AlignVCenter)
				caption_item.setFont(caption_item_font)
				caption_item.setForeground(caption_item_foreground_brush)
				caption_item.setBackground(caption_item_background_brush)

				self.addItem(caption_item)
			else :
				self.addItem(list[count])

			count += 1

	def setText(self, text) :
		self.clear()

		item = Qt.QListWidgetItem(text)
		item.setFlags(Qt.Qt.NoItemFlags)
		self.addItem(item)

