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
IconsDir = Config.Prefix+"/lib/xsl/icons/"

#####
class InternetLinksMenu(Qt.QMenu) :
	def __init__(self, title, parent=None) :
		Qt.QMenu.__init__(self, title, parent)

		self.addLink(Qt.QIcon(IconsDir+"mail_16.png"), self.tr("Developer e-mail"),
			"mailto:"+Const.DeveloperMail+"?subject="+Const.Organization)
		self.addLink(Qt.QIcon(IconsDir+"mail_16.png"), self.tr("Offers e-mail"),
			"mailto:"+Const.OffersMail+"?subject="+Const.Organization)
		self.addLink(Qt.QIcon(IconsDir+"mail_16.png"), self.tr("Bugtrack e-mail"),
			"mailto:"+Const.BugtrackMail+"?subject="+Const.Organization)

		self.addSeparator()

		self.addLink(Qt.QIcon(IconsDir+"web_16.png"), self.tr("Home page"), Const.HomePageAddress)

		self.addSeparator()

		self.addLink(Qt.QIcon(IconsDir+"mail_16.png"), self.tr("Register %1").arg(Const.Organization),
			Qt.QString("mailto:"+Const.UserCountMail+"?subject="+Const.Organization+"&body=")+
			self.tr("Count me, please :-)\nRegistration date/time: %1\nPackage version: %2")
			.arg(Qt.QDateTime().currentDateTime().toString()).arg(Const.PackageVersion))


	### Private ###

	def addLink(self, icon, title, link) :
		self.addAction(icon, title, lambda : Qt.QDesktopServices.openUrl(Qt.QUrl(link)))
