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
import SLFind

#####
IconsDir = Config.Prefix+"/lib/xsl/icons/"

ResizeDirectionNone = 0
ResizeDirectionTop = 1
ResizeDirectionBottom = 2
ResizeDirectionLeft = 3
ResizeDirectionRight = 4
# TopLeft - move
ResizeDirectionTopRight = 5
ResizeDirectionBottomLeft = 6
ResizeDirectionBottomRight = 7

#####
class PopupWindow(Qt.QFrame) :
	def __init__(self, parent = None) :
		Qt.QFrame.__init__(self, parent)

		self.setWindowFlags(Qt.Qt.Popup)
		self.setMouseTracking(True)

		self.setFrameStyle(Qt.QFrame.Box)
		self.setFrameShadow(Qt.QFrame.Raised)
		self.setLineWidth(1)
		self.setMidLineWidth(2)

		####

		self.default_size = Qt.QSize(550, 400)

		self.resize_timer = Qt.QTimer()
		self.resize_timer.setInterval(10)

		self.resize_direction = ResizeDirectionNone

		self.move_timer = Qt.QTimer()
		self.move_timer.setInterval(10)

		#####

		self.connect(self.resize_timer, Qt.SIGNAL("timeout()"), self.doResize)
		self.connect(self.move_timer, Qt.SIGNAL("timeout()"), self.doMove)


	### Public ###

	def show(self) :
		if self.default_size != self.size() :
			self.resize(self.default_size)

		cursor_position = Qt.QCursor.pos() + Qt.QPoint(15, 15)
		if cursor_position.x() < 0 :
			cursor_position.setX(0)
		if cursor_position.y() < 0 :
			cursor_position.setY(0)

		if cursor_position.x() + self.width() > Qt.QApplication.desktop().width() :
			x_window_position = Qt.QApplication.desktop().width() - self.width() - 20
		else :
			x_window_position = cursor_position.x()
		if cursor_position.y() + self.height() > Qt.QApplication.desktop().height() :
			y_window_position = Qt.QApplication.desktop().height() - self.height() - 20
		else :
			y_window_position = cursor_position.y()

		self.move(Qt.QPoint(x_window_position, y_window_position))
		Qt.QWidget.show(self)


	### Private ###

	def startResize(self) :
		self.resize_timer.start()

	def stopResize(self) :
		self.resize_timer.stop()
		self.resize_direction = ResizeDirectionNone

	def doResize(self) :
		if Qt.QApplication.mouseButtons() == Qt.Qt.NoButton :
			self.stopResize()
			return

		if self.resize_direction == ResizeDirectionNone :
			return

		new_geometry = self.frameGeometry()

		if self.resize_direction == ResizeDirectionTop :
			new_geometry.setTop(Qt.QCursor.pos().y())
		elif self.resize_direction == ResizeDirectionBottom :
			new_geometry.setBottom(Qt.QCursor.pos().y())
		elif self.resize_direction == ResizeDirectionLeft :
			new_geometry.setLeft(Qt.QCursor.pos().x())
		elif self.resize_direction == ResizeDirectionRight :
			new_geometry.setRight(Qt.QCursor.pos().x())
		elif self.resize_direction == ResizeDirectionTopRight :
			new_geometry.setTopRight(Qt.QCursor.pos())
		elif self.resize_direction == ResizeDirectionBottomLeft :
			new_geometry.setBottomLeft(Qt.QCursor.pos())
		elif self.resize_direction == ResizeDirectionBottomRight :
			new_geometry.setBottomRight(Qt.QCursor.pos())

		if new_geometry.width() < self.default_size.width() / 2 :
			new_geometry.setWidth(self.default_size.width() / 2)
			new_geometry.moveLeft(self.frameGeometry().left())
		if new_geometry.height() < self.default_size.height() / 2 :
			new_geometry.setHeight(self.default_size.height() / 2)
			new_geometry.moveTop(self.frameGeometry().top())

		if new_geometry != self.frameGeometry() :
			self.setGeometry(new_geometry)

	###

	def startMove(self) :
		self.move_timer.start()

	def stopMove(self) :
		self.move_timer.stop()

	def doMove(self) :
		if Qt.QApplication.mouseButtons() == Qt.Qt.NoButton :
			self.stopMove()
			return
		self.move(Qt.QCursor.pos())


	### Handlers ###

	def mousePressEvent(self, event) :
		if not self.frameGeometry().contains(event.globalPos()) :
			self.stopResize()
			self.stopMove()
			self.close()
			return

		x = event.x()
		y = event.y()
		w = self.width()
		h = self.height()
		f = self.frameWidth()
		c = 10

		if x < c and y < c : # TopLeft
			self.stopResize()
			self.startMove()
			return

		if x >= w - c and y < c :
			self.resize_direction = ResizeDirectionTopRight
		elif x < c and y >= h - c :
			self.resize_direction = ResizeDirectionBottomLeft
		elif x >= w - c and y >= h - c :
			self.resize_direction = ResizeDirectionBottomRight
		elif x < f :
			self.resize_direction = ResizeDirectionLeft
		elif x >= w - f :
			self.resize_direction = ResizeDirectionRight
		elif y < f :
			self.resize_direction = ResizeDirectionTop
		elif y >= h - f :
			self.resize_direction = ResizeDirectionBottom
		else :
			self.resize_direction = ResizeDirectionNone

		if self.resize_direction != ResizeDirectionNone :
			self.stopMove()
			self.startResize()

	def mouseReleaseEvent(self, event) :
		self.stopResize()
		self.stopMove()

	def mouseMoveEvent(self, event) :
		x = event.x()
		y = event.y()
		w = self.width()
		h = self.height()
		f = self.frameWidth()
		c = 10

		if 0 <= x < c and 0 <= y < c :
			cursor_shape = Qt.Qt.SizeAllCursor
		elif w - c <= x < w and h - c <= y < h :
			cursor_shape = Qt.Qt.SizeFDiagCursor
		elif (w - c <= x < w and 0 <= y < c) or (0 <= x < c and h - c <= y < h) :
			cursor_shape = Qt.Qt.SizeBDiagCursor
		elif 0 <= x <= w and (0 <= y < f or h - f <= y < h) :
			cursor_shape = Qt.Qt.SizeVerCursor
		elif 0 <= y <= h and (0 <= x < f or w - f <= x < w) :
			cursor_shape = Qt.Qt.SizeHorCursor
		else :
			cursor_shape = Qt.Qt.ArrowCursor

		if self.cursor().shape() != cursor_shape :
			self.setCursor(cursor_shape)


#####
class TranslateWindow(PopupWindow) :
	def __init__(self, parent = None) :
		PopupWindow.__init__(self, parent)

		self.main_layout = Qt.QVBoxLayout()
		self.main_layout.setMargin(0)
		self.main_layout.setSpacing(0)
		self.setLayout(self.main_layout)

		self.caption_frame = Qt.QFrame()
		self.caption_frame.setMouseTracking(True)
		self.caption_frame.setFrameShape(Qt.QFrame.Box)
		self.caption_frame.setFrameShadow(Qt.QFrame.Raised)
		try :
			self.caption_frame.setStyleSheet("QFrame {"
					"border: 2px solid gray;"
					"border-radius: 8px;"
				"}")
		except : pass
		self.main_layout.addWidget(self.caption_frame)

		self.caption_frame_layout = Qt.QHBoxLayout()
		self.caption_frame_layout.setMargin(1)
		self.caption_frame_layout.setSpacing(1)
		self.caption_frame.setLayout(self.caption_frame_layout)

		#####

		self.find_sound = SLFind.FindSound()

		#####

		self.caption_label = Qt.QLabel()
		self.caption_label.setWordWrap(True)
		self.caption_frame_layout.addWidget(self.caption_label)

		self.caption_frame_layout.addStretch()

		self.close_button = Qt.QToolButton()
		self.close_button.setIcon(Qt.QIcon(IconsDir+"close_22.png"))
		self.close_button.setIconSize(Qt.QSize(16, 16))
		self.close_button.setFixedSize(Qt.QSize(16, 16))
		self.close_button.setCursor(Qt.Qt.ArrowCursor)
		self.close_button.setAutoRaise(True)
		self.caption_frame_layout.addWidget(self.close_button)

		self.fictive_widget = Qt.QWidget()
		self.fictive_widget.setFixedSize(22, 22)
		self.caption_frame_layout.addWidget(self.fictive_widget)

		self.text_browser = Qt.QTextBrowser()
		self.text_browser.setOpenLinks(False)
		self.main_layout.addWidget(self.text_browser)

		#####

		self.connect(self.close_button, Qt.SIGNAL("clicked()"), self.close)
		self.connect(self.text_browser, Qt.SIGNAL("anchorClicked(const QUrl &)"), self.findFromAnchor)


	### Public ###

	def setCaption(self, str) :
		self.caption_label.setText("<em><strong><font color=\"#494949\">"
			"&nbsp;&nbsp;&nbsp;"+str+"&nbsp;&nbsp;&nbsp;</font></strong></em>")

	def setText(self, text) :
		self.text_browser.setHtml(text)

	def clear(self) :
		self.text_browser.clear()


	### Private ###

	def findFromAnchor(self, url) :
		word = url.toString()
		if word.startsWith("#s") :
			word.remove(0, word.indexOf("_")+1)
			word = word.simplified()
			if word.isEmpty() :
				return
			self.find_sound.find(word)
		elif word.startsWith("http://", Qt.Qt.CaseInsensitive) :
			Qt.QDesktopServices.openUrl(url)

