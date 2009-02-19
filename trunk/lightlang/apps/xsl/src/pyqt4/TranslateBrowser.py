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
import TextBrowser
import FindSoundInSL

#####
class TranslateBrowser(TextBrowser.TextBrowser) :
	def __init__(self, parent = None) :
		TextBrowser.TextBrowser.__init__(self, parent)

		self.setOpenExternalLinks(False)
		self.setOpenLinks(False)

		#####

		self.find_sound = FindSoundInSL.FindSoundInSL()

		#####

		self.connect(self, Qt.SIGNAL("anchorClicked(const QUrl &)"), self.findFromAnchor)
		self.connect(self, Qt.SIGNAL("highlighted(const QString &)"), self.checkLink)


	### Private ###

	def findFromAnchor(self, url) :
		word = url.toString()
		if word.startsWith("#s") :
			word.remove(0, word.indexOf("_")+1)
			word = word.simplified()
			if word.isEmpty() :
				return
			self.find_sound.find(word)
		elif (word.startsWith("http:", Qt.Qt.CaseInsensitive) or 
			word.startsWith("mailto:", Qt.Qt.CaseInsensitive)) :
			Qt.QDesktopServices.openUrl(url)

	###

	def checkLink(self, word) :
		if word.startsWith("#s") :
                        word.remove(0, word.indexOf("_")+1)
                        word = word.simplified()
                        if word.isEmpty() :
                                return

			words_list = word.split(Qt.QRegExp("\\W+"), Qt.QString.SkipEmptyParts)
			if words_list.count() <= 1 :
				return

			count = 1
			while count < words_list.count() :
				if not self.find_sound.checkWord(words_list[0], words_list[count]) :
					self.statusChangedSignal(self.tr("Sound is not full"))
					return
				count += 1
		elif (word.startsWith("http:", Qt.Qt.CaseInsensitive) or
			word.startsWith("mailto:", Qt.Qt.CaseInsensitive)) :
			self.statusChangedSignal(word)

