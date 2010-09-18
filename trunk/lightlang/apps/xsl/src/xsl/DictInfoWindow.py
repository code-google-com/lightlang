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
import IconsLoader
import TextBrowser
import SlDictsInfoLoader


#####
class DictInfoWindow(Qt.QDialog) :
	def __init__(self, dict_name, parent = None) :
		Qt.QDialog.__init__(self, parent)

		self.setWindowTitle(tr("Dict Information"))
		self.setWindowIcon(IconsLoader.icon("xsl"))

		self.setMinimumSize(550, 400)
		self.resize(550, 400)

		#####

		self._main_layout = Qt.QVBoxLayout()
		self._main_layout.setContentsMargins(0, 0, 0, 0)
		self._main_layout.setSpacing(0)
		self.setLayout(self._main_layout)

		self._dict_info_browser_layout = Qt.QVBoxLayout()
		self._dict_info_browser_layout.setContentsMargins(0, 0, 0, 0)
		self._dict_info_browser_layout.setSpacing(0)
		self._main_layout.addLayout(self._dict_info_browser_layout)

		self._control_buttons_layout = Qt.QHBoxLayout()
		self._control_buttons_layout.setContentsMargins(6, 6, 6, 6)
		self._control_buttons_layout.setSpacing(6)
		self._main_layout.addLayout(self._control_buttons_layout)

		#####

		self._dict_name = Qt.QString(dict_name)

		self._is_loaded_flag = False

		#####

		self._dict_info_browser = TextBrowser.TextBrowser()
		self._dict_info_browser_layout.addWidget(self._dict_info_browser)

		self._wait_picture_movie = IconsLoader.gifMovie("circular")
		icon_width = icon_height = self.style().pixelMetric(Qt.QStyle.PM_SmallIconSize)
		self._wait_picture_movie.setScaledSize(Qt.QSize(icon_width, icon_height))
		self._wait_picture_movie.jumpToFrame(0)
		self._wait_picture_movie_label = Qt.QLabel()
		self._wait_picture_movie_label.setMovie(self._wait_picture_movie)
		self._wait_picture_movie_label.hide()
		self._control_buttons_layout.addWidget(self._wait_picture_movie_label)

		self._wait_message_label = Qt.QLabel(tr("Please wait..."))
		self._wait_message_label.hide()
		self._control_buttons_layout.addWidget(self._wait_message_label)

		self._control_buttons_layout.addStretch()

		self._update_info_button = Qt.QPushButton(IconsLoader.icon("view-refresh"), tr("&Update"))
		self._control_buttons_layout.addWidget(self._update_info_button)

		self._ok_button = Qt.QPushButton(IconsLoader.icon("dialog-ok-apply"), tr("&OK"))
		self._ok_button.setDefault(True)
		self._control_buttons_layout.addWidget(self._ok_button)

		#####

		self.connect(self._update_info_button, Qt.SIGNAL("clicked()"), self.updateInfo)
		self.connect(self._ok_button, Qt.SIGNAL("clicked()"), self.accept)


	### Public ###

	def updateInfo(self) :
		self.clearInfo()
		self.loadInfo()

	###

	def dictInfo(self) :
		return self._dict_info_browser.text()

	###

	def show(self) :
		Qt.QDialog.show(self)
		self.raise_()
		self.activateWindow()

		if not self._is_loaded_flag :
			self.loadInfo()


	### Private ###

	def clearInfo(self) :
		SlDictsInfoLoader.clearInfo(self._dict_name)

	def loadInfo(self) :
		if self._dict_name.isEmpty() :
			return

		self._update_info_button.blockSignals(True)
		self._update_info_button.setEnabled(False)

		self._wait_picture_movie_label.show()
		self._wait_picture_movie.start()
		self._wait_message_label.show()

		###

		dict_info = Qt.QString()
		dict_info.append(tr("<font class=\"text_label_font\">Caption</font>: %2<hr>").arg(SlDictsInfoLoader.caption(self._dict_name)))
		dict_info.append(tr("<font class=\"text_label_font\">Translate direction</font>: %2<hr>").arg(SlDictsInfoLoader.direction(self._dict_name)))
		dict_info.append(tr("<font class=\"text_label_font\">Dictionary group</font>: %2<hr>").arg(SlDictsInfoLoader.group(self._dict_name)))
		dict_info.append(tr("<font class=\"text_label_font\">Dictionary version</font>: %2<hr>").arg(SlDictsInfoLoader.version(self._dict_name)))
		dict_info.append(tr("<font class=\"text_label_font\">Count of words</font>: %2<hr>").arg(SlDictsInfoLoader.wordCount(self._dict_name)))
		dict_info.append(tr("<font class=\"text_label_font\">File size (KB)</font>: %2<hr>").arg(SlDictsInfoLoader.fileSize(self._dict_name)))
		dict_info.append(tr("<font class=\"text_label_font\">Author</font>: %2<hr>").arg(SlDictsInfoLoader.author(self._dict_name)))
		dict_info.append(tr("<font class=\"text_label_font\">Homepage</font>: %2<hr>").arg(SlDictsInfoLoader.url(self._dict_name)))
		dict_info.append(tr("<font class=\"text_label_font\">License</font>: %2<hr>").arg(SlDictsInfoLoader.license(self._dict_name)))
		dict_info.append(tr("<font class=\"text_label_font\">Copyright</font>: %2<hr>").arg(SlDictsInfoLoader.copyright(self._dict_name)))
		dict_info.append(tr("<font class=\"text_label_font\">Description</font>: %2").arg(SlDictsInfoLoader.miscInfo(self._dict_name)))
		self._dict_info_browser.setText(dict_info)

		###

		self._wait_picture_movie_label.hide()
		self._wait_picture_movie.stop()
		self._wait_picture_movie.jumpToFrame(0)
		self._wait_message_label.hide()

		self._update_info_button.setEnabled(True)
		self._update_info_button.blockSignals(False)

		###

		self._is_loaded_flag = True

