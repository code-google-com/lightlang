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
HighlightLabelWidthDelta = 8
HighlightLabelHeight = 6


#####
def tr(str) :
	return Qt.QApplication.translate("@default", str)


#####
class ChromeScrollBar(Qt.QScrollBar) :
	def __init__(self, parent = None) :
		Qt.QScrollBar.__init__(self, parent)

		self.setOrientation(Qt.Qt.Vertical)

		#####

		self.highlight_labels_list = []

		self.highlight_color = Qt.QApplication.palette().color(Qt.QPalette.Highlight)
		self.highlight_color.setAlpha(100)

		self.highlight_pen = Qt.QPen()
		self.highlight_pen.setColor(self.highlight_color)
		self.highlight_pen.setStyle(Qt.Qt.SolidLine)


	### Public ###

	def addHighlight(self, block_number, block_count) :
		if not [block_number, block_count] in self.highlight_labels_list :
			self.highlight_labels_list.append([block_number, block_count])

	def drawHighlight(self) :
		self.update()

	def isHighlighted(self) :
		return bool(len(self.highlight_labels_list))

	def clearHighlight(self) :
		self.highlight_labels_list = []
		self.update()


	### Handlers ###

	def paintEvent(self, event) :
		Qt.QScrollBar.paintEvent(self, event)

		if len(self.highlight_labels_list) > 0 :
			painter = Qt.QPainter(self)
			painter.setPen(self.highlight_pen)
			painter.setBrush(self.highlight_color)
			for highlight_labels_list_item in self.highlight_labels_list :
				pos = (self.height() * highlight_labels_list_item[0]) / highlight_labels_list_item[1]
				if 0 <= pos < self.width() :
					pos += self.width()
				elif pos >= self.height() - self.width() * 2 - HighlightLabelHeight :
					pos -= self.width() * 2
				painter.drawRect(HighlightLabelWidthDelta / 2, pos, self.width() - HighlightLabelWidthDelta, HighlightLabelHeight)

