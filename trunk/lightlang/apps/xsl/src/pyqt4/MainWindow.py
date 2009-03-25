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
import FindInSLPanel
import GoogleTranslatePanel
import HistoryPanel
import TabbedTranslateBrowser
import DictsManager
import TranslateWindow
import StatusBar
import SpyMenu
try : # FIXME: Rrrrr... :-(
	import IFAMenu
	import TranslateSitesMenu
except : pass
import InternetLinksMenu
import HelpBrowser
import About


#####
MyIcon = Config.Prefix+"/lib/xsl/icons/xsl_16.png"
IconsDir = Config.Prefix+"/lib/xsl/icons/"


#####
def tr(str) :
	return Qt.QApplication.translate("@default", str)


#####
class MainWindow(Qt.QMainWindow) :
	def __init__(self, parent = None) :
		Qt.QMainWindow.__init__(self, parent)

		self.setWindowTitle(Const.Organization+" "+Const.MyName+" "+Const.Version)
		self.setWindowIcon(Qt.QIcon(MyIcon))

		self.setDockOptions(self.dockOptions()|Qt.QMainWindow.VerticalTabs)

		#####

		self.main_widget = Qt.QWidget()
		self.setCentralWidget(self.main_widget)

		self.main_layout = Qt.QVBoxLayout()
		self.main_widget.setLayout(self.main_layout)

		##############################
		##### Creating Resources #####
		##############################

		self.source_objects_list = []

		self.panels_list = []
		self.panels_focus_flags_list = []

		#####

		self.printer = Qt.QPrinter()
		self.print_dialog = Qt.QPrintDialog(self.printer)
		self.print_dialog.setWindowTitle(tr("Print page"))

		self.find_in_sl_panel = FindInSLPanel.FindInSLPanel()
		self.addDockWidget(Qt.Qt.LeftDockWidgetArea, self.find_in_sl_panel)
		self.addSourceObject(self.find_in_sl_panel)
		self.addPanel(self.find_in_sl_panel)

		self.history_panel = HistoryPanel.HistoryPanel()
		self.addDockWidget(Qt.Qt.LeftDockWidgetArea, self.history_panel)
		self.tabifyDockWidget(self.find_in_sl_panel, self.history_panel)
		self.addPanel(self.history_panel)

		self.google_translate_panel = GoogleTranslatePanel.GoogleTranslatePanel()
		self.addDockWidget(Qt.Qt.RightDockWidgetArea, self.google_translate_panel)
		self.tabifyDockWidget(self.history_panel, self.google_translate_panel)
		self.addSourceObject(self.google_translate_panel)
		self.addPanel(self.google_translate_panel)

		self.tabbed_translate_browser = TabbedTranslateBrowser.TabbedTranslateBrowser()
		self.main_layout.addWidget(self.tabbed_translate_browser)

		self.status_bar = StatusBar.StatusBar()
		self.setStatusBar(self.status_bar)

		self.translate_window = TranslateWindow.TranslateWindow()

		self.dicts_manager = DictsManager.DictsManager()

		self.help_browser = HelpBrowser.HelpBrowser()

		self.about = About.About()

		### Exclusive connections

		self.connect(self.find_in_sl_panel, Qt.SIGNAL("clearRequest()"), self.translate_window.clear)
		self.connect(self.find_in_sl_panel, Qt.SIGNAL("wordChanged(const QString &)"), self.history_panel.addWord)
		self.connect(self.find_in_sl_panel, Qt.SIGNAL("wordChanged(const QString &)"), self.translate_window.setCaption)
		self.connect(self.find_in_sl_panel, Qt.SIGNAL("textChanged(const QString &)"), self.translate_window.setText)

		self.connect(self.history_panel, Qt.SIGNAL("wordChanged(const QString &)"), self.find_in_sl_panel.setWord)
		self.connect(self.history_panel, Qt.SIGNAL("wordChanged(const QString &)"), self.showFindInSLPanel)

		self.connect(self.tabbed_translate_browser, Qt.SIGNAL("uFindRequest(const QString &)"), self.find_in_sl_panel.setWord)
		self.connect(self.tabbed_translate_browser, Qt.SIGNAL("uFindRequest(const QString &)"), self.find_in_sl_panel.uFind)
		self.connect(self.tabbed_translate_browser, Qt.SIGNAL("cFindRequest(const QString &)"), self.find_in_sl_panel.setWord)
		self.connect(self.tabbed_translate_browser, Qt.SIGNAL("cFindRequest(const QString &)"), self.find_in_sl_panel.cFind)
		self.connect(self.tabbed_translate_browser, Qt.SIGNAL("statusChanged(const QString &)"), self.status_bar.showStatusMessage)

		self.connect(self.translate_window, Qt.SIGNAL("newTabRequest()"), self.addTabbedTranslateBrowserTab)
		self.connect(self.translate_window, Qt.SIGNAL("uFindRequest(const QString &)"), self.find_in_sl_panel.setWord)
		self.connect(self.translate_window, Qt.SIGNAL("uFindRequest(const QString &)"), self.find_in_sl_panel.uFind)
		self.connect(self.translate_window, Qt.SIGNAL("cFindRequest(const QString &)"), self.find_in_sl_panel.setWord)
		self.connect(self.translate_window, Qt.SIGNAL("cFindRequest(const QString &)"), self.find_in_sl_panel.cFind)
		self.connect(self.translate_window, Qt.SIGNAL("uFindRequest(const QString &)"), self.showUp)
		self.connect(self.translate_window, Qt.SIGNAL("cFindRequest(const QString &)"), self.showUp)

		self.connect(self.dicts_manager, Qt.SIGNAL("dictsListChanged(const QStringList &)"), self.find_in_sl_panel.setDictsList)
		self.connect(self.dicts_manager, Qt.SIGNAL("dictsListChanged(const QStringList &)"), self.find_in_sl_panel.lFind)
		
		#########################
		##### Creating Menu #####
		#########################

		self.main_menu_bar = Qt.QMenuBar()
		self.setMenuBar(self.main_menu_bar)

		### Pages Menu

		self.pages_menu = self.main_menu_bar.addMenu(tr("&Pages"))
		self.pages_menu.addAction(Qt.QIcon(IconsDir+"save_16.png"), tr("Save current page"),
			self.saveCurrentTabbedTranslateBrowserPage)
		self.pages_menu.addAction(Qt.QIcon(IconsDir+"print_16.png"), tr("Print current page"),
			self.printCurrentTabbedTranslateBrowserPage, Qt.QKeySequence("Ctrl+P"))
		self.pages_menu.addSeparator()
		self.pages_menu.addAction(Qt.QIcon(IconsDir+"clear_16.png"), tr("Clear current page"),
			self.clearTabbedTranslateBrowserPage, Qt.QKeySequence("Ctrl+E"))
		self.pages_menu.addAction(Qt.QIcon(IconsDir+"clear_16.png"), tr("Clear all"),
			self.clearAllTabbedTranslateBrowser, Qt.QKeySequence("Ctrl+K"))
		self.pages_menu.addSeparator()
		self.pages_menu.addAction(Qt.QIcon(IconsDir+"find_16.png"), tr("Search in translations"),
			self.tabbed_translate_browser.showFindInTextFrame, Qt.QKeySequence("Ctrl+F"))
		self.pages_menu.addSeparator()
		self.pages_menu.addAction(Qt.QIcon(IconsDir+"add_16.png"), tr("New tab"),
			self.addTabbedTranslateBrowserTab, Qt.QKeySequence("Ctrl+T"))
		self.pages_menu.addAction(Qt.QIcon(IconsDir+"remove_16.png"), tr("Close tab"),
			self.removeTabbedTranslateBrowserTab, Qt.QKeySequence("Ctrl+W"))
		self.pages_menu.addSeparator()
		self.pages_menu.addAction(Qt.QIcon(IconsDir+"exit_16.png"), tr("Quit"),
			self.exit, Qt.QKeySequence("Ctrl+Q"))

		### View Menu

		self.view_menu = self.main_menu_bar.addMenu(tr("&View"))
		self.view_menu.addAction(Qt.QIcon(IconsDir+"zoom_in_16.png"), tr("Zoom in"),
			self.tabbed_translate_browser.zoomIn, Qt.QKeySequence("Ctrl++"))
		self.view_menu.addAction(Qt.QIcon(IconsDir+"zoom_out_16.png"), tr("Zoom out"),
			self.tabbed_translate_browser.zoomOut, Qt.QKeySequence("Ctrl+-"))
		self.view_menu.addSeparator()
		self.view_menu.addAction(Qt.QIcon(IconsDir+"window_16.png"), tr("Toggle to fullscreen"),
			self.toggleFullScreen, Qt.QKeySequence("F11"))

		### Spy Menu

		self.spy_menu = SpyMenu.SpyMenu(tr("Sp&y"))
		self.main_menu_bar.addMenu(self.spy_menu)

		### Tools Menu

		self.tools_menu = self.main_menu_bar.addMenu(tr("&Tools"))
		self.tools_menu.addAction(Qt.QIcon(IconsDir+"xsl_16.png"), tr("SL search"),
			self.showFindInSLPanel, Qt.QKeySequence("Ctrl+S"))
		self.tools_menu.addAction(Qt.QIcon(IconsDir+"history_16.png"), tr("Search history"),
			self.showHistoryPanel, Qt.QKeySequence("Ctrl+H"))
		self.tools_menu.addAction(Qt.QIcon(IconsDir+"web_16.png"), tr("Google-Translate client"),
			 self.showGoogleTranslatePanel, Qt.QKeySequence("Ctrl+G"))
		self.tools_menu.addSeparator()
		self.tools_menu.addAction(Qt.QIcon(IconsDir+"dicts_manager_16.png"), tr("Dicts management"),
			self.showDictsManager, Qt.QKeySequence("Ctrl+D"))
		try : # FIXME: Rrrrr... :-(
			self.tools_menu.addSeparator()
			self.translate_sites_menu = TranslateSitesMenu.TranslateSitesMenu(tr("Web translate"))
			self.translate_sites_menu.setIcon(Qt.QIcon(IconsDir+"web_16.png"))
			self.tools_menu.addMenu(self.translate_sites_menu)
		except : pass
		try : # FIXME: Rrrrr... :-(
			self.tools_menu.addSeparator()
			self.ifa_menu = IFAMenu.IFAMenu(tr("Applications"))
			self.ifa_menu.setIcon(Qt.QIcon(IconsDir+"ifa_16.png"))
			self.tools_menu.addMenu(self.ifa_menu)
		except : pass

		### Help Menu

		self.help_menu = self.main_menu_bar.addMenu(tr("&Help"))
		self.help_menu.addAction(Qt.QIcon(IconsDir+"help_16.png"),
			tr("%1 manual").arg(Const.Organization), self.showHelpBrowser, Qt.QKeySequence("F1"))
		self.help_menu.addSeparator()
		self.internet_links_menu = InternetLinksMenu.InternetLinksMenu(tr("Internet links"))
		self.internet_links_menu.setIcon(Qt.QIcon(IconsDir+"web_16.png"))
		self.help_menu.addMenu(self.internet_links_menu)
		self.help_menu.addSeparator()
		self.help_menu.addAction(Qt.QIcon(IconsDir+"xsl_16.png"), tr("About %1").arg(Const.MyName), self.showAbout)
		self.help_menu.addAction(Qt.QIcon(IconsDir+"about_16.png"), tr("About Qt4"), self.showAboutQt)

		### Additional connections

		self.connect(self.spy_menu, Qt.SIGNAL("spyStarted()"), self.spyStartedSignal)
		self.connect(self.spy_menu, Qt.SIGNAL("spyStopped()"), self.spyStoppedSignal)
		self.connect(self.spy_menu, Qt.SIGNAL("statusChanged(const QString &)"), self.status_bar.showStatusMessage)
		self.connect(self.spy_menu, Qt.SIGNAL("uFindRequest(const QString &)"), self.find_in_sl_panel.setWord)
		self.connect(self.spy_menu, Qt.SIGNAL("uFindRequest(const QString &)"), self.find_in_sl_panel.uFind)
		self.connect(self.spy_menu, Qt.SIGNAL("showTranslateWindowRequest()"), self.translate_window.show)
		self.connect(self.spy_menu, Qt.SIGNAL("showTranslateWindowRequest()"), self.translate_window.setFocus)

		################
		##### Misc #####
		################

		self.tabbed_translate_browser.setCaption(0, tr("Welcome"))
		self.tabbed_translate_browser.setText(0, tr("<br><br><hr>"
			"<table border=\"0\" width=\"100%\"><tr><td bgcolor=\"#DFEDFF\"><h2 align=\"center\"><em>"
			"Welcome to the %1 - the system of electronic dictionaries</em></h2></td></tr></table>"
			"<hr>").arg(Const.Organization))

		self.find_in_sl_panel.setFocus()
		self.find_in_sl_panel.raise_()


	### Public ###

	def startSpy(self) :
		self.spy_menu.startSpy()

        def stopSpy(self) :
		self.spy_menu.stopSpy()

	###

	def save(self) :
		for panel in self.panels_list :
			panel.saveSettings()

		self.dicts_manager.saveSettings()
		self.spy_menu.saveSettings()
		self.translate_window.saveSettings()

		self.saveSettings()

	def load(self) :
		for panel in self.panels_list :
			panel.loadSettings()

		self.dicts_manager.loadSettings()
		self.spy_menu.loadSettings()
		self.translate_window.loadSettings()

		self.loadSettings()

		self.find_in_sl_panel.setFocus()
		self.find_in_sl_panel.raise_()

		self.status_bar.showStatusMessage(tr("Ready"))

	###

	def visibleChange(self) :
		if not self.isVisible() or self.isMinimized() or not self.isActiveWindow() :
			self.close() # FIXME: small crutch
			self.showNormal()
			self.activateFocus()
		else :
			self.close()

	###

	def focusChanged(self) :
		new_panels_focus_flags_list = []
		for panel in self.panels_list :
			new_panels_focus_flags_list.append(panel.hasInternalFocus())
		if True in new_panels_focus_flags_list :
			self.panels_focus_flags_list = new_panels_focus_flags_list

	def activateFocus(self) :
		count = 0
		while count < len(self.panels_list) :
			if self.panels_focus_flags_list[count] :
				self.panels_list[count].setFocus()
			count += 1

	###

	def showUp(self) :
		if self.isVisible() :
			self.visibleChange()
		self.visibleChange()

	###

	def exit(self) :
		self.save()
		sys.exit(0)


	### Private ###

	def addPanel(self, panel) :
		self.panels_list.append(panel)
		self.panels_focus_flags_list.append(False)

	###

	def addSourceObject(self, source_object) :
		self.source_objects_list.append([source_object, -1])

		index = len(self.source_objects_list) -1

		def registrate_stream(n = index) : self.registrateStream(n)
		def release_stream(n = index) : self.releaseStream(n)
		def clear_tabbed_translate_browser(n = index) : self.clearTabbedTranslateBrowser(n)
		def set_tabbed_translate_browser_caption(word, n = index) : self.setTabbedTranslateBrowserCaption(n, word)
		def set_tabbed_translate_browser_text(text, n = index) : self.setTabbedTranslateBrowserText(n, text)
		def add_tabbed_translate_browser_tab(n = index) : self.addTabbedTranslateBrowserTab()
		def status_bar_start_wait_movie(n = index) : self.status_bar.startWaitMovie()
		def status_bar_stop_wait_movie(n = index) : self.status_bar.stopWaitMovie()
		def status_bar_show_status_message(str, n = index) : self.status_bar.showStatusMessage(str)

		self.connect(self.source_objects_list[index][0], Qt.SIGNAL("processStarted()"), registrate_stream)
		self.connect(self.source_objects_list[index][0], Qt.SIGNAL("processStarted()"), status_bar_start_wait_movie)
		self.connect(self.source_objects_list[index][0], Qt.SIGNAL("processFinished()"), release_stream)
		self.connect(self.source_objects_list[index][0], Qt.SIGNAL("processFinished()"), status_bar_stop_wait_movie)
		self.connect(self.source_objects_list[index][0], Qt.SIGNAL("clearRequest()"), clear_tabbed_translate_browser)
		self.connect(self.source_objects_list[index][0], Qt.SIGNAL("wordChanged(const QString &)"), set_tabbed_translate_browser_caption)
		self.connect(self.source_objects_list[index][0], Qt.SIGNAL("textChanged(const QString &)"), set_tabbed_translate_browser_text)
		self.connect(self.source_objects_list[index][0], Qt.SIGNAL("newTabRequest()"), add_tabbed_translate_browser_tab)
		self.connect(self.source_objects_list[index][0], Qt.SIGNAL("statusChanged(const QString &)"), status_bar_show_status_message)
		

	###

	def registrateStream(self, source_object_index) :
		self.tabbed_translate_browser.setShredLock(True)
		tabbed_translate_browser_index = self.tabbed_translate_browser.currentIndex()
		for source_object in self.source_objects_list :
			if source_object[1] == tabbed_translate_browser_index :
				self.tabbed_translate_browser.addTab()
				tabbed_translate_browser_index = self.tabbed_translate_browser.currentIndex()
				break
		self.source_objects_list[source_object_index][1] = tabbed_translate_browser_index

	def releaseStream(self, source_object_index) :
		self.tabbed_translate_browser.setShredLock(False)
		self.source_objects_list[source_object_index][1] = -1

	def checkBusyStreams(self) :
		for source_object in self.source_objects_list :
			if source_object[1] != -1 :
				return True
		return False

	def clearTabbedTranslateBrowser(self, source_object_index) :
		self.tabbed_translate_browser.clear(self.source_objects_list[source_object_index][1])

	def setTabbedTranslateBrowserCaption(self, source_object_index, word) :
		self.tabbed_translate_browser.setCaption(self.source_objects_list[source_object_index][1], word)

	def setTabbedTranslateBrowserText(self, source_object_index, text) :
		self.tabbed_translate_browser.setText(self.source_objects_list[source_object_index][1], text)

	def addTabbedTranslateBrowserTab(self) :
		self.tabbed_translate_browser.addTab()

	def removeTabbedTranslateBrowserTab(self) :
		if self.checkBusyStreams() :
			return
		self.tabbed_translate_browser.removeTab()

	###

	def saveCurrentTabbedTranslateBrowserPage(self) :
		if self.checkBusyStreams() :
			return

		index = self.tabbed_translate_browser.currentIndex()
		file_name = Qt.QFileDialog.getSaveFileName(None,
			tr("Save page \"%1\"").arg(self.tabbed_translate_browser.caption(index)),
			Qt.QDir.homePath(), "*.html *.htm")
		if file_name.simplified().isEmpty() :
			return

		file = Qt.QFile(file_name)
		if not file.open(Qt.QIODevice.WriteOnly|Qt.QIODevice.Text) :
			Qt.QMessageBox.warning(None, Const.MyName,
				tr("This file cannot by open for saving"),
				Qt.QMessageBox.Yes)
			return

		file_stream = Qt.QTextStream(file)
		file_stream << self.tabbed_translate_browser.text(index)

		file.close()

		self.status_bar.showStatusMessage(tr("Saved"))

	def printCurrentTabbedTranslateBrowserPage(self) :
		if self.checkBusyStreams() :
			return

		if self.print_dialog.exec_() != Qt.QDialog.Accepted :
			return

		index = self.tabbed_translate_browser.currentIndex()
		text_document = self.tabbed_translate_browser.document(index)
		text_document.print_(self.printer)

		self.status_bar.showStatusMessage(tr("Printing..."))

	def clearAllTabbedTranslateBrowser(self) :
		if self.checkBusyStreams() :
			return

		for panel in self.panels_list :
			panel.clear()

		self.tabbed_translate_browser.clearAll()

		self.activateFocus()

	def clearTabbedTranslateBrowserPage(self) :
		if self.checkBusyStreams() :
			return
		self.tabbed_translate_browser.clearPage()

		self.activateFocus()

	###

	def saveSettings(self) :
		settings = Qt.QSettings(Const.Organization, Const.MyName)
		settings.setValue("main_window/size", Qt.QVariant(self.size()))
		settings.setValue("main_window/position", Qt.QVariant(self.pos()))
		settings.setValue("main_window/is_visible_flag", Qt.QVariant(self.isVisible()))
		settings.setValue("main_window/state", Qt.QVariant(self.saveState()))

	def loadSettings(self) :
		settings = Qt.QSettings(Const.Organization, Const.MyName)
		self.resize(settings.value("main_window/size", Qt.QVariant(Qt.QSize(800, 500))).toSize())
		self.move(settings.value("main_window/position", Qt.QVariant(Qt.QPoint(0, 0))).toPoint())
		self.setVisible(settings.value("main_window/is_visible_flag", Qt.QVariant(True)).toBool())
		self.restoreState(settings.value("main_window/state", Qt.QVariant(Qt.QByteArray())).toByteArray())

	def toggleFullScreen(self) :
		if self.isFullScreen() :
			self.showNormal()
		else :
			self.showFullScreen()

	###

	def showFindInSLPanel(self) :
		self.find_in_sl_panel.setFocus()
		self.find_in_sl_panel.raise_()

	def showHistoryPanel(self) :
		self.history_panel.show()
		self.history_panel.setFocus()
		self.history_panel.raise_()

	def showGoogleTranslatePanel(self) :
		self.google_translate_panel.show()
		self.google_translate_panel.setFocus()
		self.google_translate_panel.raise_()

	def showDictsManager(self) :
		self.dicts_manager.show()
		self.dicts_manager.raise_()
		self.dicts_manager.activateWindow()

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

