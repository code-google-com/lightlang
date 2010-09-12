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
WaitPicture = Config.DataRootDir+"/xsl/pictures/circular.gif"


#####
def tr(str) :
	return Qt.QApplication.translate("@default", str)


#####
class DictInfoWindow(Qt.QDialog) :
	def __init__(self, dict_name, parent = None) :
		Qt.QDialog.__init__(self, parent)

		self.setWindowTitle(tr("Dict Information"))
		self.setWindowIcon(IconsLoader.icon("xsl"))

		self.setMinimumSize(550, 400)
		self.resize(550, 400)

		#####

		self.main_layout = Qt.QVBoxLayout()
		self.main_layout.setContentsMargins(0, 0, 0, 0)
		self.main_layout.setSpacing(0)
		self.setLayout(self.main_layout)

		self.dict_info_browser_layout = Qt.QVBoxLayout()
		self.dict_info_browser_layout.setContentsMargins(0, 0, 0, 0)
		self.dict_info_browser_layout.setSpacing(0)
		self.main_layout.addLayout(self.dict_info_browser_layout)

		self.control_buttons_layout = Qt.QHBoxLayout()
		self.control_buttons_layout.setContentsMargins(6, 6, 6, 6)
		self.control_buttons_layout.setSpacing(6)
		self.main_layout.addLayout(self.control_buttons_layout)

		#####

		self.dict_name = Qt.QString(dict_name)

		self.is_loaded_flag = False

		#####

		self.dict_info_browser = TextBrowser.TextBrowser()
		self.dict_info_browser_layout.addWidget(self.dict_info_browser)

		self.wait_picture_movie = Qt.QMovie(WaitPicture)
		icon_width = icon_height = self.style().pixelMetric(Qt.QStyle.PM_SmallIconSize)
		self.wait_picture_movie.setScaledSize(Qt.QSize(icon_width, icon_height))
		self.wait_picture_movie.jumpToFrame(0)
		self.wait_picture_movie_label = Qt.QLabel()
		self.wait_picture_movie_label.setMovie(self.wait_picture_movie)
		self.wait_picture_movie_label.hide()
		self.control_buttons_layout.addWidget(self.wait_picture_movie_label)

		self.wait_message_label = Qt.QLabel(tr("Please wait..."))
		self.wait_message_label.hide()
		self.control_buttons_layout.addWidget(self.wait_message_label)

		self.control_buttons_layout.addStretch()

		self.update_info_button = Qt.QPushButton(IconsLoader.icon("view-refresh"), tr("&Update"))
		self.control_buttons_layout.addWidget(self.update_info_button)

		self.ok_button = Qt.QPushButton(IconsLoader.icon("dialog-ok-apply"), tr("&OK"))
		self.ok_button.setDefault(True)
		self.control_buttons_layout.addWidget(self.ok_button)

		#####

		self.connect(self.update_info_button, Qt.SIGNAL("clicked()"), self.updateInfo)
		self.connect(self.ok_button, Qt.SIGNAL("clicked()"), self.accept)


	### Public ###

	def updateInfo(self) :
		self.clearInfo()
		self.loadInfo()

	###

	def dictInfo(self) :
		return self.dict_info_browser.text()

	###

	def show(self) :
		Qt.QDialog.show(self)
		self.raise_()
		self.activateWindow()

		if not self.is_loaded_flag :
			self.loadInfo()


	### Private ###

	def clearInfo(self) :
		SlDictsInfoLoader.clearInfo(self.dict_name)

	def loadInfo(self) :
		if self.dict_name.isEmpty() :
			return

		self.update_info_button.blockSignals(True)
		self.update_info_button.setEnabled(False)

		self.wait_picture_movie_label.show()
		self.wait_picture_movie.start()
		self.wait_message_label.show()

		###

		dict_info = Qt.QString()
		dict_info.append(tr("<font class=\"text_label_font\">Caption</font>: %2<hr>").arg(SlDictsInfoLoader.caption(self.dict_name)))
		dict_info.append(tr("<font class=\"text_label_font\">Translate direction</font>: %2<hr>").arg(SlDictsInfoLoader.direction(self.dict_name)))
		dict_info.append(tr("<font class=\"text_label_font\">Dictionary group</font>: %2<hr>").arg(SlDictsInfoLoader.group(self.dict_name)))
		dict_info.append(tr("<font class=\"text_label_font\">Dictionary version</font>: %2<hr>").arg(SlDictsInfoLoader.version(self.dict_name)))
		dict_info.append(tr("<font class=\"text_label_font\">Count of words</font>: %2<hr>").arg(SlDictsInfoLoader.wordCount(self.dict_name)))
		dict_info.append(tr("<font class=\"text_label_font\">File size (KB)</font>: %2<hr>").arg(SlDictsInfoLoader.fileSize(self.dict_name)))
		dict_info.append(tr("<font class=\"text_label_font\">Author</font>: %2<hr>").arg(SlDictsInfoLoader.author(self.dict_name)))
		dict_info.append(tr("<font class=\"text_label_font\">Homepage</font>: %2<hr>").arg(SlDictsInfoLoader.url(self.dict_name)))
		dict_info.append(tr("<font class=\"text_label_font\">License</font>: %2<hr>").arg(SlDictsInfoLoader.license(self.dict_name)))
		dict_info.append(tr("<font class=\"text_label_font\">Copyright</font>: %2<hr>").arg(SlDictsInfoLoader.copyright(self.dict_name)))
		dict_info.append(tr("<font class=\"text_label_font\">Description</font>: %2").arg(SlDictsInfoLoader.miscInfo(self.dict_name)))
		self.dict_info_browser.setText(dict_info)

		###

		Qt.QCoreApplication.processEvents()

		self.wait_picture_movie_label.hide()
		self.wait_picture_movie.stop()
		self.wait_picture_movie.jumpToFrame(0)
		self.wait_message_label.hide()

		self.update_info_button.setEnabled(True)
		self.update_info_button.blockSignals(False)

		###

		self.is_loaded_flag = True

