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
try : # FIXME: fucking debian packagers :-(
	import TranslateSitesMenu
except : pass
import Config
import Const

#####
MyIcon = Config.Prefix+"/lib/xsl/icons/xsl_16.png"
IconsDir = Config.Prefix+"/lib/xsl/icons/"

#####
class TrayMenu(Qt.QMenu) :
	def __init__(self, icon = None, text = None, parent = None) :
		Qt.QMenu.__init__(self, parent)

		if icon != None and text != None :
			self.addCaption(icon, text)


	### Public ###

	def addCaption(self, icon, text, before_action = None) :
		fictive_action = Qt.QWidgetAction(self)
		fictive_action.setEnabled(False)

		fictive_action_frame = Qt.QFrame()
		fictive_action_frame.setFrameShape(Qt.QFrame.Box) # Qt.QFrame.StyledPanel
		fictive_action.setDefaultWidget(fictive_action_frame)

		fictive_action_frame_layout = Qt.QHBoxLayout()
		fictive_action_frame_layout.setMargin(1)
		#fictive_action_frame_layout.setSpacing(5)
		fictive_action_frame.setLayout(fictive_action_frame_layout)

		fictive_action_icon_label = Qt.QLabel()
		icon_width = icon_height = self.style().pixelMetric(Qt.QStyle.PM_SmallIconSize)
		fictive_action_icon_label.setPixmap(icon.pixmap(Qt.QSize(icon_width, icon_height)))
		fictive_action_frame_layout.insertWidget(-1, fictive_action_icon_label, 0)

		fictive_action_caption_label = Qt.QLabel(text)
		fictive_action_frame_layout.insertWidget(-1, fictive_action_caption_label, 20)

		font = fictive_action_caption_label.font()
		font.setBold(True)
		fictive_action_caption_label.setFont(font)

		self.insertAction(before_action, fictive_action)

		return fictive_action


#####
class TrayIcon(Qt.QSystemTrayIcon) :
	def __init__(self, parent = None) :
		Qt.QSystemTrayIcon.__init__(self, parent)

		self.setIcon(Qt.QIcon(IconsDir+"xsl_22.png"))
		self.setToolTip(self.tr("XSL - graphical interface for SL\nSpy is stopped"))

		#####

		self.tray_menu = TrayMenu(Qt.QIcon(MyIcon), Const.Organization+" "+Const.MyName)

		self.start_spy_menu_action = self.tray_menu.addAction(Qt.QIcon(IconsDir+"start_spy_16.png"),
			self.tr("Start Spy"), self.startSpy)
		self.stop_spy_menu_action = self.tray_menu.addAction(Qt.QIcon(IconsDir+"stop_spy_16.png"),
			self.tr("Stop Spy"), self.stopSpy)
		self.stop_spy_menu_action.setEnabled(False)
		try : # FIXME: fucking debian packagers :-(
			self.tray_menu.addSeparator()
			self.translate_sites_menu = TranslateSitesMenu.TranslateSitesMenu(self.tr("Web translate"))
			self.translate_sites_menu.setIcon(Qt.QIcon(IconsDir+"web_16.png"))
			self.tray_menu.addMenu(self.translate_sites_menu)
		except : pass
		self.tray_menu.addSeparator()
		self.tray_menu.addAction(Qt.QIcon(IconsDir+"exit_16.png"), self.tr("Quit"), self.exit)
		self.setContextMenu(self.tray_menu)

		#####

		self.connect(self, Qt.SIGNAL("activated(QSystemTrayIcon::ActivationReason)"), self.act)


	### Public ###

	def spyStarted(self) :
		self.start_spy_menu_action.setEnabled(False)
		self.stop_spy_menu_action.setEnabled(True)

		self.setIcon(Qt.QIcon(IconsDir+"xsl+spy_22.png"))

		self.setToolTip(self.tr("XSL - graphical interface for SL\nSpy is running"))

	def spyStopped(self) :
		self.start_spy_menu_action.setEnabled(True)
		self.stop_spy_menu_action.setEnabled(False)

		self.setIcon(Qt.QIcon(IconsDir+"xsl_22.png"))

		self.setToolTip(self.tr("XSL - graphical interface for SL\nSpy is stopped"))


	### Private ###

	def startSpy(self) :
		self.spyStarted()
		self.startSpyRequestSignal()

	def stopSpy(self) :
		self.spyStopped()
		self.stopSpyRequestSignal()

	def act(self, reason) :
		if reason == Qt.QSystemTrayIcon.Trigger :
			self.visibleChangeRequestSignal()

	def exit(self) :
		self.exitRequestSignal()


	### Signals ###

	def startSpyRequestSignal(self) :
		self.emit(Qt.SIGNAL("startSpyRequest()"))

	def stopSpyRequestSignal(self) :
		self.emit(Qt.SIGNAL("stopSpyRequest()"))

	def visibleChangeRequestSignal(self) :
		self.emit(Qt.SIGNAL("visibleChangeRequest()"))

	def exitRequestSignal(self) :
		self.emit(Qt.SIGNAL("exitRequest()"))
