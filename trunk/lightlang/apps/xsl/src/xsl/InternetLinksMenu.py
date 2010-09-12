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


#####
def tr(str) :
	return Qt.QApplication.translate("@default", str)


#####
class InternetLinksMenu(Qt.QMenu) :
	def __init__(self, title, parent = None) :
		Qt.QMenu.__init__(self, title, parent)

		#####

		self.addLink(IconsLoader.icon("mail-send"), tr("Developer e-mail"), "mailto:"+Const.DeveloperMail+"?subject="+Const.Organization)
		self.addLink(IconsLoader.icon("mail-send"), tr("Offers e-mail"), "mailto:"+Const.OffersMail+"?subject="+Const.Organization)
		self.addLink(IconsLoader.icon("mail-send"), tr("Bugtrack e-mail"), "mailto:"+Const.BugtrackMail+"?subject="+Const.Organization)

		self.addSeparator()

		self.addLink(IconsLoader.icon("applications-internet"), tr("Home page"), Const.HomePageAddress)

		self.addSeparator()

		self.addLink(IconsLoader.icon("mail-send"), tr("Register %1").arg(Const.Organization),
			Qt.QString("mailto:"+Const.UserCountMail+"?subject="+Const.Organization+"&body=")+
			tr("Count me, please :-)\nRegistration date/time: %1\nPackage version: %2")
			.arg(Qt.QDateTime().currentDateTime().toString()).arg(Const.PackageVersion))


	### Private ###

	def addLink(self, icon, title, link) :
		self.addAction(icon, title, lambda : Qt.QDesktopServices.openUrl(Qt.QUrl(link)))

