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
MyIcon = Config.Prefix+"/lib/xsl/icons/xsl_16.png"
WaitPicture = Config.Prefix+"/lib/xsl/pictures/circular.gif"

AllDictsDir = Config.Prefix+"/share/sl/dicts/"
IconsDir = Config.Prefix+"/lib/xsl/icons/"

#####
class DictInformationWindow(Qt.QWidget) :
	def __init__(self, dict_name, parent = None) :
		Qt.QWidget.__init__(self, parent)

		self.setWindowTitle(self.tr("Dict Information"))
		self.setWindowIcon(Qt.QIcon(MyIcon))

		self.setMinimumSize(550, 400)
		self.resize(550, 400)

		#####

		self.main_layout = Qt.QVBoxLayout()
		self.setLayout(self.main_layout)

		self.dict_information_browser_layout = Qt.QVBoxLayout()
		self.main_layout.addLayout(self.dict_information_browser_layout)

		self.control_buttons_layout = Qt.QHBoxLayout()
		self.main_layout.addLayout(self.control_buttons_layout)

		#####

		self.dict_name = Qt.QString(dict_name)

		self.is_loaded_flag = False

		#####

		self.dict_information_browser = Qt.QTextBrowser()
		self.dict_information_browser_layout.addWidget(self.dict_information_browser)

		self.wait_picture_movie = Qt.QMovie(WaitPicture)
		icon_width = icon_height = self.style().pixelMetric(Qt.QStyle.PM_SmallIconSize)
		self.wait_picture_movie.setScaledSize(Qt.QSize(icon_width, icon_height))
		self.wait_picture_movie.jumpToFrame(0)
		self.wait_picture_movie_label = Qt.QLabel()
		self.wait_picture_movie_label.setMovie(self.wait_picture_movie)
		self.wait_picture_movie_label.hide()
		self.control_buttons_layout.addWidget(self.wait_picture_movie_label)

		self.wait_message_label = Qt.QLabel(self.tr("Please wait..."))
		self.wait_message_label.hide()
		self.control_buttons_layout.addWidget(self.wait_message_label)

		self.control_buttons_layout.addStretch()

		self.update_information_button = Qt.QPushButton(Qt.QIcon(IconsDir+"update_16.png"), self.tr("&Update"))
		self.control_buttons_layout.addWidget(self.update_information_button)

		self.ok_button = Qt.QPushButton(Qt.QIcon(IconsDir+"ok_16.png"), self.tr("&OK"))
		self.ok_button.setDefault(True)
		self.control_buttons_layout.addWidget(self.ok_button)

		#####

		self.connect(self.update_information_button, Qt.SIGNAL("clicked()"), self.updateInformation)
		self.connect(self.ok_button, Qt.SIGNAL("clicked()"), self.close)


	### Public ###

	def updateInformation(self) :
		if self.dict_name.isEmpty() :
			return

		self.update_information_button.blockSignals(True)
		self.update_information_button.setEnabled(False)

		self.wait_picture_movie_label.show()
		self.wait_picture_movie.start()
		self.wait_message_label.show()

		###

		dict_information = Qt.QString()

		dict_information.append(self.record(self.tr("Caption:"), self.dictCaption()))
		self.dict_information_browser.setHtml(dict_information)

		dict_information.append(self.record(self.tr("Direction:"), self.dictDirection()))
		self.dict_information_browser.setHtml(dict_information)

		dict_information.append(self.record(self.tr("File path:"), self.dictFilePath()))
		self.dict_information_browser.setHtml(dict_information)

		dict_information.append(self.record(self.tr("File size (KB):"), self.dictFileSize()))
		self.dict_information_browser.setHtml(dict_information)

		dict_description, word_count = self.dictDescriptionAndWordCount()
		dict_information.append(self.record(self.tr("Count of words:"), word_count))
		dict_information.append(self.record(self.tr("Description:"), dict_description))
		self.dict_information_browser.setHtml(dict_information)

		###

		self.wait_picture_movie_label.hide()
		self.wait_picture_movie.stop()
		self.wait_picture_movie.jumpToFrame(0)
		self.wait_message_label.hide()

		Qt.QCoreApplication.processEvents()

		self.update_information_button.setEnabled(True)
		self.update_information_button.blockSignals(False)

	def show(self) :
		Qt.QWidget.show(self)
		self.raise_()
		self.activateWindow()

		if not self.is_loaded_flag :
			self.is_loaded_flag = True
			self.updateInformation()


	### Private ###

	def dictCaption(self) :
		index = self.dict_name.lastIndexOf(".")
		if index >= 0 :
			dict_caption = self.dict_name.left(index)
		else :
			dict_caption = Qt.QString(self.dict_name)
		dict_caption.replace("_", " ")
		return dict_caption

	def dictDirection(self) :
		index = self.dict_name.lastIndexOf(".")
		if index >= 0 :
			return self.dict_name.mid(index +1)
		else :
			return self.tr("Unavailable")

	def dictFilePath(self) :
		dict_file_path = Qt.QString(AllDictsDir+self.dict_name)
		if Qt.QFile.exists(dict_file_path) :
			return dict_file_path
		else :
			return self.tr("Unavailable")

	def dictFileSize(self) :
		dict_file = Qt.QFile(AllDictsDir+self.dict_name)
		return Qt.QString().setNum(dict_file.size() / 1024) # KB

	def dictDescriptionAndWordCount(self) :
		dict_file = Qt.QFile(AllDictsDir+self.dict_name)
		dict_file_stream = Qt.QTextStream(dict_file)

		dict_description = Qt.QString()
		word_count = 0

		if dict_file.open(Qt.QIODevice.ReadOnly) :
			first_comment_flag = False
			while not dict_file_stream.atEnd() :
				Qt.QCoreApplication.processEvents(Qt.QEventLoop.ExcludeUserInputEvents)
				str = dict_file_stream.readLine()
				if str.isEmpty() :
					continue
				if str[0] == "#" :
					str.remove(0, 1)
					str.remove("\n")
					str.append("<br>")
					dict_description.append(str)
					continue
				if str.contains("  ") :
					word_count += 1
			dict_file.close()
			dict_description.trimmed()
			dict_description.prepend("<br>")

		if dict_description.isEmpty() :
			dict_description = self.tr("Unavailable")

		return dict_description, Qt.QString().setNum(word_count)

	###

	def record(self, label, text) :
		return Qt.QString("<em><strong><font color=\"#494949\">%1"
			"</font></strong> %2</em><br>").arg(label).arg(text)

