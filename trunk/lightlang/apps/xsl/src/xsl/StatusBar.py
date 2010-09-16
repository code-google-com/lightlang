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
import sys
import Config
import Const


#####
WaitPicture = Config.DataRootDir+"/xsl/pictures/circular.gif"


#####
class StatusBar(Qt.QStatusBar) :
	def __init__(self, parent = None) :
		Qt.QStatusBar.__init__(self, parent)

		#####

		self._activation_semaphore = 0

		self._timer = Qt.QTimer()

		#####

		icon_width = icon_height = label_height = self.style().pixelMetric(Qt.QStyle.PM_SmallIconSize)

		self._message_label = Qt.QLabel()
		self._message_label.setTextFormat(Qt.Qt.PlainText)
		self._message_label.setMaximumHeight(label_height)
		self.addWidget(self._message_label, 1)

		self._wait_picture_movie = Qt.QMovie(WaitPicture)
		self._wait_picture_movie.setScaledSize(Qt.QSize(icon_width, icon_height))
		self._wait_picture_movie.jumpToFrame(0)
		self._wait_picture_movie_label = Qt.QLabel()
		self._wait_picture_movie_label.setMovie(self._wait_picture_movie)
		self._wait_picture_movie_label.hide()
		self.addWidget(self._wait_picture_movie_label)

		#####

		self.connect(self._timer, Qt.SIGNAL("timeout()"), self.clearStatusMessage)


	### Public ###

	def startWaitMovie(self) :
		if self._activation_semaphore != 0 :
			self._activation_semaphore += 1
			return

		self._wait_picture_movie_label.show()
		self._wait_picture_movie.start()

	def stopWaitMovie(self) :
		if self._activation_semaphore > 1 :
			return
		if self._activation_semaphore > 0 :
			self._activation_semaphore -= 1

		self._wait_picture_movie_label.hide()
		self._wait_picture_movie.stop()
		self._wait_picture_movie.jumpToFrame(0)

	###

	def showStatusMessage(self, text, timeout = 2000) :
		self._message_label.setText(text)
		if timeout != 0 :
			self._timer.start(timeout)

	def clearStatusMessage(self) :
		self._message_label.clear()

