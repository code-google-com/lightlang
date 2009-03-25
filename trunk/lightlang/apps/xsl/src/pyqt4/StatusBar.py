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
import sys
import Config
import Const


#####
WaitPicture = Config.Prefix+"/lib/xsl/pictures/circular.gif"


#####
def tr(str) :
	return Qt.QApplication.translate("@default", str)


#####
class StatusBar(Qt.QStatusBar) :
	def __init__(self, parent = None) :
		Qt.QStatusBar.__init__(self, parent)

		#####

		self.activation_semaphore = 0

		self.timer = Qt.QTimer()

		#####

		icon_width = icon_height = label_height = self.style().pixelMetric(Qt.QStyle.PM_SmallIconSize)

		self.message_label = Qt.QLabel()
		self.message_label.setMaximumHeight(label_height)
		self.addWidget(self.message_label, 1)

		self.wait_picture_movie = Qt.QMovie(WaitPicture)
		self.wait_picture_movie.setScaledSize(Qt.QSize(icon_width, icon_height))
		self.wait_picture_movie.jumpToFrame(0)
		self.wait_picture_movie_label = Qt.QLabel()
		self.wait_picture_movie_label.setMovie(self.wait_picture_movie)
		self.wait_picture_movie_label.hide()
		self.addWidget(self.wait_picture_movie_label)

		#####

		self.connect(self.timer, Qt.SIGNAL("timeout()"), self.clearStatusMessage)


	### Public ###

	def startWaitMovie(self) :
		if self.activation_semaphore != 0 :
			self.activation_semaphore += 1
			return

		self.wait_picture_movie_label.show()
		self.wait_picture_movie.start()

	def stopWaitMovie(self) :
		if self.activation_semaphore > 1 :
			return
		if self.activation_semaphore > 0 :
			self.activation_semaphore -= 1

		self.wait_picture_movie_label.hide()
		self.wait_picture_movie.stop()
		self.wait_picture_movie.jumpToFrame(0)

	###

	def showStatusMessage(self, text, timeout = 2000) :
		self.message_label.setText(text)
		if timeout != 0 :
			self.timer.start(timeout)

	def clearStatusMessage(self) :
		self.message_label.clear()

