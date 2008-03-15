# -*- coding: utf8 -*-
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
import SLFind
import Spy
import FindInSLPanel
import FindInTextPanel
import GoogleTranslatePanel
import HistoryPanel
import TextBrowser
import TranslateWindow
import DictsManager
import IFAMenu
import TranslateSitesMenu
import InternetLinksMenu
import Help

#####
MyIcon = Config.Prefix+"/lib/xsl/icons/xsl_16.png"
IconsDir = Config.Prefix+"/lib/xsl/icons/"

#####
class MainWindow(Qt.QMainWindow) :
	def __init__(self, parent = None) :
		Qt.QMainWindow.__init__(self, parent)

		self.setWindowTitle(Const.Organization+" "+Const.MyName+" "+Const.Version)
		self.setWindowIcon(Qt.QIcon(MyIcon))

		self.main_widget = Qt.QWidget()
		self.setCentralWidget(self.main_widget)

		self.main_layout = Qt.QVBoxLayout()
		self.main_widget.setLayout(self.main_layout)

		self.status_bar = Qt.QStatusBar()
		self.setStatusBar(self.status_bar)

		##############################
		##### Creating Resources #####
		##############################

		self.index = 0

		self.printer = Qt.QPrinter()
		self.print_dialog = Qt.QPrintDialog(self.printer)

		self.find_in_sl_panel = FindInSLPanel.FindInSLPanel()
		self.addDockWidget(Qt.Qt.LeftDockWidgetArea, self.find_in_sl_panel)

		self.find_in_text_panel = FindInTextPanel.FindInTextPanel()
		self.find_in_text_panel.setVisible(False)
		self.addDockWidget(Qt.Qt.LeftDockWidgetArea, self.find_in_text_panel)

		self.history_panel = HistoryPanel.HistoryPanel()
		self.history_panel.setVisible(False)
		self.addDockWidget(Qt.Qt.RightDockWidgetArea, self.history_panel)

		self.google_translate_panel = GoogleTranslatePanel.GoogleTranslatePanel()
		self.google_translate_panel.setVisible(False)
		self.addDockWidget(Qt.Qt.RightDockWidgetArea, self.google_translate_panel)

		self.text_browser = TextBrowser.TextBrowser()
		self.main_layout.addWidget(self.text_browser)

		self.spy = Spy.Spy()

		self.translate_window = TranslateWindow.TranslateWindow()

		self.dicts_manager = DictsManager.DictsManager()

		self.help_browser = Help.HelpBrowser()

		self.about = Help.About()

		### Connections

		self.connect(self.find_in_sl_panel, Qt.SIGNAL("newTabRequest()"), self.text_browser.addTab)
		self.connect(self.find_in_sl_panel, Qt.SIGNAL("clearRequest()"), self.registrateTextBrowser)
		self.connect(self.find_in_sl_panel, Qt.SIGNAL("wordChanged(const QString &)"), self.setTextBrowserCaption)
		self.connect(self.find_in_sl_panel, Qt.SIGNAL("wordChanged(const QString &)"), self.history_panel.addWord)
		self.connect(self.find_in_sl_panel, Qt.SIGNAL("textChanged(const QString &)"), self.setTextBrowserText)

		self.connect(self.find_in_text_panel, Qt.SIGNAL("findNextRequest(const QString &)"), self.findInTextNext)
		self.connect(self.find_in_text_panel, Qt.SIGNAL("findPreviousRequest(const QString &)"),
			self.findInTextPrevious)

		self.connect(self.history_panel, Qt.SIGNAL("wordChanged(const QString &)"), self.find_in_sl_panel.setWord)

		self.connect(self.google_translate_panel, Qt.SIGNAL("clearRequest()"),
			self.registrateTextBrowser)
		self.connect(self.google_translate_panel, Qt.SIGNAL("wordChanged(const QString &)"),
			self.setTextBrowserCaption)
		self.connect(self.google_translate_panel, Qt.SIGNAL("textChanged(const QString &)"),
			self.setTextBrowserText)

		self.connect(self.spy, Qt.SIGNAL("processStarted()"), self.showTranslateWindow)
		self.connect(self.spy, Qt.SIGNAL("clearRequest()"), self.registrateTextBrowser)
		self.connect(self.spy, Qt.SIGNAL("clearRequest()"), self.translate_window.clear)
		self.connect(self.spy, Qt.SIGNAL("wordChanged(const QString &)"), self.find_in_sl_panel.setWord)
		self.connect(self.spy, Qt.SIGNAL("wordChanged(const QString &)"), self.setTextBrowserCaption)
		self.connect(self.spy, Qt.SIGNAL("wordChanged(const QString &)"), self.translate_window.setCaption)
		self.connect(self.spy, Qt.SIGNAL("wordChanged(const QString &)"), self.history_panel.addWord)
		self.connect(self.spy, Qt.SIGNAL("textChanged(const QString &)"), self.setTextBrowserText)
		self.connect(self.spy, Qt.SIGNAL("textChanged(const QString &)"), self.translate_window.setText)

		self.connect(self.dicts_manager, Qt.SIGNAL("dictsChanged()"), self.find_in_sl_panel.lFind)

		#########################
		##### Creating Menu #####
		#########################

		self.main_menu_bar = Qt.QMenuBar()
		self.setMenuBar(self.main_menu_bar)

		### File Menu

		self.pages_menu = self.main_menu_bar.addMenu(self.tr("Pages"))
		self.pages_menu.addAction(Qt.QIcon(IconsDir+"save_16.png"), self.tr("Save current page"),
			self.saveCurrentPage)
		self.pages_menu.addAction(Qt.QIcon(IconsDir+"print_16.png"), self.tr("Print current page"),
			self.printCurrentPage, Qt.QKeySequence("Ctrl+P"))
		self.pages_menu.addSeparator()
		self.pages_menu.addAction(Qt.QIcon(IconsDir+"clear_16.png"), self.tr("Clear current page"),
			self.text_browser.clearPage, Qt.QKeySequence("Ctrl+E"))
		self.pages_menu.addAction(Qt.QIcon(IconsDir+"clear_16.png"), self.tr("Clear all"),
			self.clearAll, Qt.QKeySequence("Ctrl+K"))
		self.pages_menu.addSeparator()
		self.pages_menu.addAction(Qt.QIcon(IconsDir+"find_16.png"), self.tr("Search in translations"),
			self.showFindInTextPanel, Qt.QKeySequence("Ctrl+F"))
		self.pages_menu.addSeparator()
		self.pages_menu.addAction(Qt.QIcon(IconsDir+"add_16.png"), self.tr("New tab"),
			self.text_browser.addTab, Qt.QKeySequence("Ctrl+T"))
		self.pages_menu.addAction(Qt.QIcon(IconsDir+"remove_16.png"), self.tr("Close tab"),
			self.text_browser.removeTab, Qt.QKeySequence("Ctrl+W"))
		self.pages_menu.addSeparator()
		self.pages_menu.addAction(Qt.QIcon(IconsDir+"exit_16.png"), self.tr("Quit"),
			self.exit, Qt.QKeySequence("Ctrl+Q"))

		### View Menu

		self.view_menu = self.main_menu_bar.addMenu(self.tr("View"))
		self.view_menu.addAction(Qt.QIcon(IconsDir+"zoom_in_16.png"), self.tr("Zoom in"),
			self.text_browser.zoomIn, Qt.QKeySequence("Ctrl++"))
		self.view_menu.addAction(Qt.QIcon(IconsDir+"zoom_out_16.png"), self.tr("Zoom out"),
			self.text_browser.zoomOut, Qt.QKeySequence("Ctrl+-"))
		self.view_menu.addSeparator()
		self.view_menu.addAction(Qt.QIcon(IconsDir+"window_16.png"), self.tr("Switch to fullscreen"),
			self.fullScreen, Qt.QKeySequence("F11"))

		### Spy Menu

		self.spy_menu = self.main_menu_bar.addMenu(self.tr("Spy"))
		self.start_spy_menu_action = self.spy_menu.addAction(Qt.QIcon(IconsDir+"start_spy_16.png"),
			self.tr("Start Spy"), self.startSpy)
		self.stop_spy_menu_action = self.spy_menu.addAction(Qt.QIcon(IconsDir+"stop_spy_16.png"),
			self.tr("Stop Spy"), self.stopSpy)
		self.stop_spy_menu_action.setEnabled(False)
		self.spy_menu.addSeparator()
		self.show_translate_window_menu_action = self.spy_menu.addAction(self.tr("Show popup window"))
		self.show_translate_window_menu_action.setCheckable(True)
		self.auto_detect_window_menu_action = self.spy_menu.addAction(self.tr("Auto-detect window"))
		self.auto_detect_window_menu_action.setCheckable(True)

		### Tools Menu

		self.tools_menu = self.main_menu_bar.addMenu(self.tr("Tools"))
		self.tools_menu.addAction(Qt.QIcon(IconsDir+"dicts_manager_16.png"), self.tr("Dicts management"),
			self.showDictsManager, Qt.QKeySequence("Ctrl+D"))
		self.tools_menu.addAction(Qt.QIcon(IconsDir+"history_16.png"), self.tr("Search history"),
			self.showHistoryPanel, Qt.QKeySequence("Ctrl+H"))
		self.tools_menu.addSeparator()
		self.translate_sites_menu = TranslateSitesMenu.TranslateSitesMenu(self.tr("Web translate"))
		self.translate_sites_menu.setIcon(Qt.QIcon(IconsDir+"web_16.png"))
		self.tools_menu.addMenu(self.translate_sites_menu)
		self.tools_menu.addAction(Qt.QIcon(IconsDir+"web_16.png"), self.tr("Google-Translate client"),
			self.showGoogleTranslatePanel, Qt.QKeySequence("Ctrl+G"))
		self.ifa_menu = IFAMenu.IFAMenu(self.tr("Applications"))
		self.ifa_menu.setIcon(Qt.QIcon(IconsDir+"ifa_16.png"))
		self.tools_menu.addMenu(self.ifa_menu)

		### Help Menu

		self.help_menu = self.main_menu_bar.addMenu(self.tr("Help"))
		self.help_menu.addAction(Qt.QIcon(IconsDir+"handbook_16.png"),
			self.tr("%1 manual").arg(Const.Organization), self.showHelpBrowser, Qt.QKeySequence("F1"))
		self.help_menu.addSeparator()
		self.internet_links_menu = InternetLinksMenu.InternetLinksMenu(self.tr("Internet links"))
		self.internet_links_menu.setIcon(Qt.QIcon(IconsDir+"web_16.png"))
		self.help_menu.addMenu(self.internet_links_menu)
		self.help_menu.addSeparator()
		self.help_menu.addAction(Qt.QIcon(IconsDir+"xsl_16.png"), self.tr("About %1").arg(Const.MyName),
			self.showAbout)
		self.help_menu.addAction(Qt.QIcon(IconsDir+"about_16.png"), self.tr("About Qt4"), self.showAboutQt)

		################
		##### Misc #####
		################

		self.text_browser.setCaption(0, self.tr("Welcome"))
		self.text_browser.setText(0, self.tr("<br><br><hr>"
			"<table border=\"0\" width=\"100%\"><tr><td bgcolor=\"#DFEDFF\"><h2 align=\"center\"><em>"
			"Welcome to the %1 - the system of electronic dictionaries</em></h2></td></tr></table>"
			"<hr>").arg(Const.Organization))


	### Public ###

	def startSpy(self) :
		self.spy.start()

		self.start_spy_menu_action.setEnabled(False)
		self.stop_spy_menu_action.setEnabled(True)

		self.status_bar.showMessage(self.tr("Spy is running"), 2000)

		self.spyStartedSignal()

        def stopSpy(self) :
		self.spy.stop()

		self.start_spy_menu_action.setEnabled(True)
		self.stop_spy_menu_action.setEnabled(False)

		self.status_bar.showMessage(self.tr("Spy is stopped"), 2000)

		self.spyStoppedSignal()

	def save(self) :
		self.saveSettings()
		self.history_panel.saveSettings()
		self.dicts_manager.saveSettings()
		self.google_translate_panel.saveSettings()

	def load(self) :
		self.loadSettings()
		self.history_panel.loadSettings()
		self.dicts_manager.loadSettings()
		self.google_translate_panel.loadSettings()
		self.status_bar.showMessage(self.tr("Ready"), 2000)
		

	def exit(self) :
		self.save()
		sys.exit(0)


	### Private ###

	def registrateTextBrowser(self) :
		self.index = self.text_browser.currentIndex()
		self.text_browser.clear(self.index)

	def setTextBrowserCaption(self, word) :
		self.text_browser.setCaption(self.index, word)

	def setTextBrowserText(self, text) :
		self.text_browser.setText(self.index, text)

	###

	def findInTextNext(self, word) :
		index = self.text_browser.currentIndex()
		if not self.text_browser.findNext(index, word) :
			self.status_bar.showMessage(self.tr("Not found"), 2000)

	def findInTextPrevious(self, word) :
		index = self.text_browser.currentIndex()
		if not self.text_browser.findPrevious(index, word) :
			self.status_bar.showMessage(self.tr("Not found"), 2000)

	def saveCurrentPage(self) :
		index = self.text_browser.currentIndex()
		file_name = Qt.QFileDialog.getSaveFileName(None,
			self.tr("Save page \"%1\"").arg(self.text_browser.caption(index)),
			Qt.QDir.homePath(), "*.html *.htm")
		if file_name.simplified().isEmpty() :
			return

		file = Qt.QFile(file_name)
		if not file.open(Qt.QIODevice.WriteOnly|Qt.QIODevice.Text) :
			Qt.QMessageBox.warning(None, Const.MyName,
				self.tr("This file cannot by open for saving"),
				Qt.QMessageBox.Yes)
			return

		file_stream = Qt.QTextStream(file)
		file_stream << self.text_browser.text(index)

		file.close()

		self.status_bar.showMessage(self.tr("Saved"), 2000)

	def printCurrentPage(self) :
		if self.print_dialog.exec_() != Qt.QDialog.Accepted :
			return

		index = self.text_browser.currentIndex()
		text_document = self.text_browser.document(index)
		text_document.print_(self.printer)

		self.status_bar.showMessage(self.tr("Printing..."), 2000)

	def clearAll(self) :
		self.find_in_sl_panel.clear()
		self.text_browser.clearAll()
		self.find_in_sl_panel.setFocus(Qt.Qt.OtherFocusReason)

	###

	def saveSettings(self) :
		settings = Qt.QSettings(Const.Organization, Const.MyName)
		settings.setValue("main_window/size", Qt.QVariant(self.size()))
		settings.setValue("main_window/position", Qt.QVariant(self.pos()))
		settings.setValue("main_window/is_visible_flag", Qt.QVariant(self.isVisible()))
		settings.setValue("main_window/state", Qt.QVariant(self.saveState()))
		settings.setValue("main_window/show_translate_window_flag",
			Qt.QVariant(self.show_translate_window_menu_action.isChecked()))
		settings.setValue("main_window/auto_detect_window_flag",
			Qt.QVariant(self.auto_detect_window_menu_action.isChecked()))

	def loadSettings(self) :
		settings = Qt.QSettings(Const.Organization, Const.MyName)
		self.resize(settings.value("main_window/size", Qt.QVariant(Qt.QSize(845, 650))).toSize())
		self.move(settings.value("main_window/position", Qt.QVariant(Qt.QPoint(0, 0))).toPoint())
		self.setVisible(settings.value("main_window/is_visible_flag", Qt.QVariant(True)).toBool())
		self.restoreState(settings.value("main_window/state", Qt.QVariant(Qt.QByteArray())).toByteArray())
		self.show_translate_window_menu_action.setChecked(settings.value("main_window/show_translate_window_flag",
			Qt.QVariant(True)).toBool())
		self.auto_detect_window_menu_action.setChecked(settings.value("main_window/auto_detect_window_flag",
			Qt.QVariant(True)).toBool())

	def fullScreen(self) :
		if self.isFullScreen() :
			self.showNormal()
		else :
			self.showFullScreen()

	def setFocus(self, reason) :
		self.find_in_sl_panel.setFocus(reason)

	###

	def showFindInTextPanel(self) :
		self.find_in_text_panel.setVisible(True)
		self.find_in_text_panel.setFocus(Qt.Qt.OtherFocusReason)

	def showTranslateWindow(self) :
		if self.show_translate_window_menu_action.isChecked() :
			if self.auto_detect_window_menu_action.isChecked() :
				if Qt.QApplication.activeWindow() == None :
					self.translate_window.showUnderCursor()
			else :
				self.translate_window.showUnderCursor()

	def showHistoryPanel(self) :
		self.history_panel.setVisible(True)

	def showDictsManager(self) :
		self.dicts_manager.show()
		self.dicts_manager.raise_()
		self.dicts_manager.activateWindow()

	def showGoogleTranslatePanel(self) :
		self.google_translate_panel.setVisible(True)
		self.google_translate_panel.setFocus(Qt.Qt.OtherFocusReason)

	def showHelpBrowser(self) :
		self.help_browser.show()
		self.help_browser.raise_()
		self.help_browser.activateWindow()

	def showAbout(self) :
		self.about.show()
		self.about.raise_()
		self.about.activateWindow()

	def showAboutQt(self) :
		Qt.QMessageBox.aboutQt(None)


	### Signals ###

	def spyStartedSignal(self) :
		self.emit(Qt.SIGNAL("spyStarted()"))

	def spyStoppedSignal(self) :
		self.emit(Qt.SIGNAL("spyStopped()"))
