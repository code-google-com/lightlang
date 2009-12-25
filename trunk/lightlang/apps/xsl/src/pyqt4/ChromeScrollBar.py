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
DefaultHighlightHeight = 5
HighlightTransparentAlpha = 100
MinCharacterDistance = 50


#####
def tr(str) :
	return Qt.QApplication.translate("@default", str)


#####
class ChromeScrollBar(Qt.QScrollBar) :
	def __init__(self, parent = None) :
		Qt.QScrollBar.__init__(self, parent)

		self.setOrientation(Qt.Qt.Vertical)

		#####

		self.highlight_positions_list = []

		self.highlight_color = Qt.QApplication.palette().color(Qt.QPalette.Highlight)
		self.highlight_color.setAlpha(HighlightTransparentAlpha)

		self.highlight_pen = Qt.QPen()
		self.highlight_pen.setColor(self.highlight_color)
		self.highlight_pen.setStyle(Qt.Qt.SolidLine)


	### Public ###

	def addHighlight(self, pos, count) :
		if len(self.highlight_positions_list) == 0 or abs(self.highlight_positions_list[-1][0] - pos) > MinCharacterDistance :
			self.highlight_positions_list.append([pos, count])

	def drawHighlight(self) :
		self.update()

	def isHighlighted(self) :
		return bool(len(self.highlight_positions_list))

	def clearHighlight(self) :
		self.highlight_positions_list = []
		self.update()


	### Handlers ###

	def paintEvent(self, event) :
		Qt.QScrollBar.paintEvent(self, event)

		if len(self.highlight_positions_list) > 0 :
			highlight_rects_list = []

			highlight_pass = self.style().pixelMetric(Qt.QStyle.PM_ScrollBarSliderMin) -1
			highlight_area_height = self.height() - highlight_pass * 3

			for highlight_positions_list_item in self.highlight_positions_list :
				pos = highlight_area_height * highlight_positions_list_item[0] / highlight_positions_list_item[1] + highlight_pass

				if len(highlight_rects_list) == 0 or pos > highlight_rects_list[-1].bottom() :
					highlight_rects_list.append(Qt.QRect(0, pos, self.width(), DefaultHighlightHeight))
				else :
					highlight_rects_list[-1].setHeight(highlight_rects_list[-1].height() + (DefaultHighlightHeight -
						highlight_rects_list[-1].bottom() + pos))

				if highlight_rects_list[-1].bottom() > highlight_area_height + highlight_pass :
					highlight_rects_list[-1].setHeight(highlight_rects_list[-1].height() - (highlight_rects_list[-1].bottom() -
						(highlight_area_height + highlight_pass)))

			painter = Qt.QPainter(self)
			painter.setPen(self.highlight_pen)
			painter.setBrush(self.highlight_color)
			for highlight_rects_list_item in highlight_rects_list :
				painter.drawRect(highlight_rects_list_item)

