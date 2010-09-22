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
import Settings
import IconsLoader
import SlSearchPanel
import GoogleTranslatePanel
import HistoryPanel
import TabbedTranslateBrowser
import StatusBar
import DictsManagerWindow
import TranslateWindow
import SpyMenu
import IfaMenu
import TranslateSitesMenu
import InternetLinksMenu
import HelpBrowserWindow
import AboutWindow


##### Public classes #####
class MainWindow(Qt.QMainWindow) :
	def __init__(self, parent = None) :
		Qt.QMainWindow.__init__(self, parent)

		self.setObjectName("main_window")

		self.setDockOptions(self.dockOptions()|Qt.QMainWindow.VerticalTabs)

		self.setWindowTitle(Const.Organization+" "+Const.MyName)
		self.setWindowIcon(IconsLoader.icon("xsl"))

		#####

		self._main_widget = Qt.QWidget()
		self.setCentralWidget(self._main_widget)

		self._main_layout = Qt.QVBoxLayout()
		self._main_layout.setContentsMargins(0, 0, 0, 0)
		self._main_widget.setLayout(self._main_layout)


		##### Creating resources #####

		self._source_objects_list = []

		self._panels_list = []
		self._panels_focus_flags_list = []

		#####

		self._tabbed_translate_browser = TabbedTranslateBrowser.TabbedTranslateBrowser()
		self._main_layout.addWidget(self._tabbed_translate_browser)

		self._status_bar = StatusBar.StatusBar()
		self.setStatusBar(self._status_bar)

		self._translate_window = TranslateWindow.TranslateWindow()

		self._dicts_manager_window = DictsManagerWindow.DictsManagerWindow()

		self._help_browser_window = HelpBrowserWindow.HelpBrowserWindow()

		self._about_window = AboutWindow.AboutWindow()


		##### Creating menues #####

		self._main_menu_bar = Qt.QMenuBar()
		self.setMenuBar(self._main_menu_bar)

		### Pages menu

		self._pages_menu = self._main_menu_bar.addMenu(tr("&Pages"))
		self._pages_menu.addAction(IconsLoader.icon("document-save-as"), tr("Save current page"),
			self.saveCurrentTabbedTranslateBrowserPage)
		self._pages_menu.addAction(IconsLoader.icon("document-print"), tr("Print current page"),
			self.printCurrentTabbedTranslateBrowserPage)
		self._pages_menu.addSeparator()
		self._pages_menu.addAction(IconsLoader.icon("edit-clear"), tr("Clear current page"),
			self.clearTabbedTranslateBrowserPage, Qt.QKeySequence("Ctrl+E"))
		self._pages_menu.addAction(IconsLoader.icon("edit-clear"), tr("Clear all"),
			self.clearAllTabbedTranslateBrowser, Qt.QKeySequence("Ctrl+K"))
		self._pages_menu.addSeparator()
		self._pages_menu.addAction(IconsLoader.icon("edit-find"), tr("Search in translations"),
			self._tabbed_translate_browser.showTextSearchFrame, Qt.QKeySequence("Ctrl+F"))
		self._pages_menu.addSeparator()
		self._pages_menu.addAction(IconsLoader.icon("tab-new"), tr("New tab"),
			self.addTabbedTranslateBrowserTab, Qt.QKeySequence("Ctrl+T"))
		self._pages_menu.addAction(IconsLoader.icon("tab-close"), tr("Close tab"),
			self.removeTabbedTranslateBrowserTab, Qt.QKeySequence("Ctrl+W"))
		self._pages_menu.addSeparator()
		self._pages_menu.addAction(IconsLoader.icon("application-exit"), tr("Quit"),
			self.exit, Qt.QKeySequence("Ctrl+Q"))

		### Panels menu

		self._panels_menu = self._main_menu_bar.addMenu(tr("&Panels"))

		### View menu

		self._view_menu = self._main_menu_bar.addMenu(tr("&View"))
		self._view_menu.addAction(IconsLoader.icon("zoom-in"), tr("Zoom in"),
			self._tabbed_translate_browser.zoomIn, Qt.QKeySequence("Ctrl++"))
		self._view_menu.addAction(IconsLoader.icon("zoom-out"), tr("Zoom out"),
			self._tabbed_translate_browser.zoomOut, Qt.QKeySequence("Ctrl+-"))
		self._view_menu.addAction(IconsLoader.icon("zoom-original"), tr("Zoom normal"),
			self._tabbed_translate_browser.zoomNormal, Qt.QKeySequence("Ctrl+0"))

		### Spy menu

		self._spy_menu = SpyMenu.SpyMenu(tr("Sp&y"))
		self._main_menu_bar.addMenu(self._spy_menu)

		### Tools menu

		self._tools_menu = self._main_menu_bar.addMenu(tr("&Tools"))
		self._tools_menu.addAction(IconsLoader.icon("configure"), tr("Dicts management"),
			self._dicts_manager_window.show, Qt.QKeySequence("Ctrl+D"))
		self._tools_menu.addSeparator()
		self._translate_sites_menu = TranslateSitesMenu.TranslateSitesMenu(tr("Web translate"))
		self._translate_sites_menu.setIcon(IconsLoader.icon("applications-internet"))
		self._tools_menu.addMenu(self._translate_sites_menu)
		self._ifa_menu = IfaMenu.IfaMenu(tr("Applications"))
		self._ifa_menu.setIcon(IconsLoader.icon("fork"))
		self._tools_menu.addMenu(self._ifa_menu)

		### Help menu

		self._help_menu = self._main_menu_bar.addMenu(tr("&Help"))
		self._help_menu.addAction(IconsLoader.icon("help-contents"), tr("%1 manual").arg(Const.Organization),
			self._help_browser_window.show, Qt.QKeySequence("F1"))
		self._help_menu.addSeparator()
		self._internet_links_menu = InternetLinksMenu.InternetLinksMenu(tr("Internet links"))
		self._internet_links_menu.setIcon(IconsLoader.icon("applications-internet"))
		self._help_menu.addMenu(self._internet_links_menu)
		self._help_menu.addSeparator()
		self._help_menu.addAction(IconsLoader.icon("xsl"), tr("About %1").arg(Const.MyName), self._about_window.show)
		self._help_menu.addAction(IconsLoader.icon("help-about"), tr("About Qt4"), lambda : Qt.QMessageBox.aboutQt(None))


		##### Creating panels #####

		self._sl_search_panel = SlSearchPanel.SlSearchPanel()
		self.addPanel(self._sl_search_panel)

		self._history_panel = HistoryPanel.HistoryPanel()
		self.addPanel(self._history_panel)

		self._google_translate_panel = GoogleTranslatePanel.GoogleTranslatePanel()
		self.addPanel(self._google_translate_panel)


		##### Source objects #####

		self.addSourceObject(self._sl_search_panel)
		self.addSourceObject(self._google_translate_panel)


		##### Exclusive connections #####

		self.connect(self._spy_menu, Qt.SIGNAL("spyStarted()"), self.spyStartedSignal)
		self.connect(self._spy_menu, Qt.SIGNAL("spyStopped()"), self.spyStoppedSignal)
		self.connect(self._spy_menu, Qt.SIGNAL("statusChanged(const QString &)"), self._status_bar.showStatusMessage)
		self.connect(self._spy_menu, Qt.SIGNAL("showTranslateWindowRequest()"), self._translate_window.show)
		self.connect(self._spy_menu, Qt.SIGNAL("showTranslateWindowRequest()"), self._translate_window.setFocus)

		self.connect(self._sl_search_panel, Qt.SIGNAL("wordChanged(const QString &)"), self._history_panel.addWord)

		self.connect(self._history_panel, Qt.SIGNAL("wordChanged(const QString &)"), self._sl_search_panel.setWord)
		self.connect(self._history_panel, Qt.SIGNAL("wordChanged(const QString &)"), self._sl_search_panel.show)

		self.connect(self._tabbed_translate_browser, Qt.SIGNAL("uFindRequest(const QString &)"), self._sl_search_panel.setWord)
		self.connect(self._tabbed_translate_browser, Qt.SIGNAL("uFindRequest(const QString &)"), self._sl_search_panel.uFind)
		self.connect(self._tabbed_translate_browser, Qt.SIGNAL("uFindRequest(const QString &)"), self._sl_search_panel.show)
		self.connect(self._tabbed_translate_browser, Qt.SIGNAL("cFindRequest(const QString &)"), self._sl_search_panel.setWord)
		self.connect(self._tabbed_translate_browser, Qt.SIGNAL("cFindRequest(const QString &)"), self._sl_search_panel.cFind)
		self.connect(self._tabbed_translate_browser, Qt.SIGNAL("cFindRequest(const QString &)"), self._sl_search_panel.show)
		self.connect(self._tabbed_translate_browser, Qt.SIGNAL("statusChanged(const QString &)"), self._status_bar.showStatusMessage)

		self.connect(self._translate_window, Qt.SIGNAL("newTabRequest()"), self.addTabbedTranslateBrowserTab)
		self.connect(self._translate_window, Qt.SIGNAL("uFindRequest(const QString &)"), self._sl_search_panel.setWord)
		self.connect(self._translate_window, Qt.SIGNAL("uFindRequest(const QString &)"), self._sl_search_panel.uFind)
		self.connect(self._translate_window, Qt.SIGNAL("uFindRequest(const QString &)"), self._sl_search_panel.show)
		self.connect(self._translate_window, Qt.SIGNAL("uFindRequest(const QString &)"), self.showUp)
		self.connect(self._translate_window, Qt.SIGNAL("cFindRequest(const QString &)"), self._sl_search_panel.setWord)
		self.connect(self._translate_window, Qt.SIGNAL("cFindRequest(const QString &)"), self._sl_search_panel.cFind)
		self.connect(self._translate_window, Qt.SIGNAL("cFindRequest(const QString &)"), self._sl_search_panel.show)
		self.connect(self._translate_window, Qt.SIGNAL("cFindRequest(const QString &)"), self.showUp)

		self.connect(self._dicts_manager_window, Qt.SIGNAL("dictsListChanged(const QStringList &)"), self._sl_search_panel.setDictsList)
		self.connect(self._dicts_manager_window, Qt.SIGNAL("dictsListChanged(const QStringList &)"), lambda : self._sl_search_panel.lFind())


	### Public ###

	def startSpy(self) :
		self._spy_menu.startSpy()

        def stopSpy(self) :
		self._spy_menu.stopSpy()

	###

	def save(self) :
		for panels_list_item in self._panels_list :
			panels_list_item.saveSettings()

		self._dicts_manager_window.saveSettings()
		self._translate_window.saveSettings()
		self._help_browser_window.saveSettings()
		self._spy_menu.saveSettings()
		self._translate_sites_menu.saveSettings()
		self._ifa_menu.saveSettings()

		self.saveSettings()

	def load(self) :
		for panels_list_item in self._panels_list :
			panels_list_item.loadSettings()

		self._dicts_manager_window.loadSettings()
		self._translate_window.loadSettings()
		self._help_browser_window.loadSettings()
		self._spy_menu.loadSettings()
		self._translate_sites_menu.loadSettings()
		self._ifa_menu.loadSettings()

		self.loadSettings()

		self._sl_search_panel.setFocus()
		self._sl_search_panel.raise_()

		self._tabbed_translate_browser.setCaption(0, tr("Welcome"))
		self._tabbed_translate_browser.setText(0, tr("<br><br><hr><table border=\"0\" width=\"100%\"><tr>"
			"<td class=\"dict_header_background\" align=\"center\"><font class=\"dict_header_font\">"
			"Welcome to the %1 - the system of electronic dictionaries</font></td></tr></table><hr>").arg(Const.Organization))

		self._status_bar.showStatusMessage(tr("Ready"))

	###

	def visibleChange(self) :
		if not self.isVisible() or self.isMinimized() or not self.isActiveWindow() :
			self.close() # FIXME (Issue 58): Normal window move to top
			self.showNormal()
			self.activateFocus()
		else :
			self.close()

	def showUp(self) :
		if self.isVisible() :
			self.visibleChange()
		self.visibleChange()

	###

	def focusChanged(self) :
		new_panels_focus_flags_list = [ panels_list_item.hasInternalFocus() for panels_list_item in self._panels_list ]
		if True in new_panels_focus_flags_list :
			self._panels_focus_flags_list = new_panels_focus_flags_list

	def activateFocus(self) :
		for count in xrange(len(self._panels_list)) :
			if self._panels_focus_flags_list[count] :
				self._panels_list[count].setFocus()

	###

	def exit(self) :
		self.save()
		Qt.QApplication.exit(0)


	### Private ###

	def addPanel(self, panel) :
		self._panels_list.append(panel)
		self._panels_focus_flags_list.append(False)

		requisites = panel.requisites()
		self.addDockWidget(requisites["area"], panel)
		if len(self._panels_list) > 1 :
			self.tabifyDockWidget(self._panels_list[-2], self._panels_list[-1])
		self._panels_menu.addAction(requisites["icon"], requisites["title"], panel.show, requisites["hotkey"])

	def addSourceObject(self, source_object) :
		self._source_objects_list.append({ "object" : source_object, "index" : -1 })

		index = len(self._source_objects_list) - 1

		registrate_stream = ( lambda n = index : self.registrateStream(n) )
		release_stream = ( lambda n = index : self.releaseStream(n) )
		clear_tabbed_translate_browser = ( lambda n = index : self.clearTabbedTranslateBrowser(n) )
		set_tabbed_translate_browser_caption = ( lambda word, n = index : self.setTabbedTranslateBrowserCaption(n, word) )
		set_tabbed_translate_browser_text = ( lambda text, n = index : self.setTabbedTranslateBrowserText(n, text) )
		add_tabbed_translate_browser_tab = ( lambda : self.addTabbedTranslateBrowserTab() )
		status_bar_start_wait_movie = ( lambda : self._status_bar.startWaitMovie() )
		status_bar_stop_wait_movie = ( lambda : self._status_bar.stopWaitMovie() )
		status_bar_show_status_message = ( lambda str : self._status_bar.showStatusMessage(str) )
		set_translate_window_caption = ( lambda word : self.setTranslateWindowCaption(word) )
		set_translate_window_text = ( lambda text : self.setTranslateWindowText(text) )
		clear_translate_window = ( lambda : self.clearTranslateWindow() )

		self.connect(self._source_objects_list[index]["object"], Qt.SIGNAL("processStarted()"), registrate_stream)
		self.connect(self._source_objects_list[index]["object"], Qt.SIGNAL("processStarted()"), status_bar_start_wait_movie)
		self.connect(self._source_objects_list[index]["object"], Qt.SIGNAL("processFinished()"), release_stream)
		self.connect(self._source_objects_list[index]["object"], Qt.SIGNAL("processFinished()"), status_bar_stop_wait_movie)
		self.connect(self._source_objects_list[index]["object"], Qt.SIGNAL("clearRequest()"), clear_tabbed_translate_browser)
		self.connect(self._source_objects_list[index]["object"], Qt.SIGNAL("clearRequest()"), clear_translate_window)
		self.connect(self._source_objects_list[index]["object"], Qt.SIGNAL("wordChanged(const QString &)"), set_tabbed_translate_browser_caption)
		self.connect(self._source_objects_list[index]["object"], Qt.SIGNAL("wordChanged(const QString &)"), set_translate_window_caption)
		self.connect(self._source_objects_list[index]["object"], Qt.SIGNAL("textChanged(const QString &)"), set_tabbed_translate_browser_text)
		self.connect(self._source_objects_list[index]["object"], Qt.SIGNAL("textChanged(const QString &)"), set_translate_window_text)
		self.connect(self._source_objects_list[index]["object"], Qt.SIGNAL("newTabRequest()"), add_tabbed_translate_browser_tab)
		self.connect(self._source_objects_list[index]["object"], Qt.SIGNAL("statusChanged(const QString &)"), status_bar_show_status_message)

		for translate_methods_list_item in self._source_objects_list[index]["object"].translateMethods() :
			signal_string = self._spy_menu.addTranslateMethod(translate_methods_list_item["title"],
				translate_methods_list_item["object_name"], translate_methods_list_item["method_name"])
			self.connect(self._spy_menu, Qt.SIGNAL(signal_string), translate_methods_list_item["method"])
			self.connect(self._spy_menu, Qt.SIGNAL(signal_string), self._source_objects_list[index]["object"].show)

	###

	def registrateStream(self, source_object_index) :
		self._tabbed_translate_browser.setShredLock(True)
		tabbed_translate_browser_index = self._tabbed_translate_browser.currentIndex()
		for source_objects_list_item in self._source_objects_list :
			if source_objects_list_item["index"] == tabbed_translate_browser_index :
				self._tabbed_translate_browser.addTab()
				tabbed_translate_browser_index = self._tabbed_translate_browser.currentIndex()
				break
		self._source_objects_list[source_object_index]["index"] = tabbed_translate_browser_index

	def releaseStream(self, source_object_index) :
		self._tabbed_translate_browser.setShredLock(False)
		self._source_objects_list[source_object_index]["index"] = -1

	def checkBusyStreams(self) :
		for source_objects_list_item in self._source_objects_list :
			if source_objects_list_item["index"] != -1 :
				return True
		return False

	def clearTabbedTranslateBrowser(self, source_object_index) :
		self._tabbed_translate_browser.clear(self._source_objects_list[source_object_index]["index"])

	def setTabbedTranslateBrowserCaption(self, source_object_index, word) :
		self._tabbed_translate_browser.setCaption(self._source_objects_list[source_object_index]["index"], word)

	def setTabbedTranslateBrowserText(self, source_object_index, text) :
		self._tabbed_translate_browser.setText(self._source_objects_list[source_object_index]["index"], text)

	def addTabbedTranslateBrowserTab(self) :
		self._tabbed_translate_browser.addTab()

	def removeTabbedTranslateBrowserTab(self) :
		if self.checkBusyStreams() :
			return
		self._tabbed_translate_browser.removeTab()

	###

	def setTranslateWindowCaption(self, word) :
		self._translate_window.setCaption(word)

	def setTranslateWindowText(self, text) :
		self._translate_window.setText(text)

	def clearTranslateWindow(self) :
		self._translate_window.clear()

	###

	def saveCurrentTabbedTranslateBrowserPage(self) :
		if self.checkBusyStreams() :
			return

		index = self._tabbed_translate_browser.currentIndex()
		file_path = Qt.QFileDialog.getSaveFileName(None,
			tr("Save page \"%1\"").arg(self._tabbed_translate_browser.caption(index)),
			Qt.QDir.homePath(), "*.html *.htm")
		if file_path.simplified().isEmpty() :
			return

		file = Qt.QFile(file_path)
		if not file.open(Qt.QIODevice.WriteOnly|Qt.QIODevice.Text) :
			Qt.QMessageBox.warning(None, Const.MyName,
				tr("This file cannot by open for saving"),
				Qt.QMessageBox.Yes)
			return

		file_stream = Qt.QTextStream(file)
		file_stream << self._tabbed_translate_browser.document(index).toHtml("utf-8")

		file.close()

		self._status_bar.showStatusMessage(tr("Saved"))

	def printCurrentTabbedTranslateBrowserPage(self) :
		if self.checkBusyStreams() :
			return

		printer = Qt.QPrinter()
		print_dialog = Qt.QPrintDialog(printer)
		print_dialog.setWindowTitle(tr("Print page"))

		if print_dialog.exec_() != Qt.QDialog.Accepted :
			return

		index = self._tabbed_translate_browser.currentIndex()
		text_document = self._tabbed_translate_browser.document(index)
		text_document.print_(printer)

		self._status_bar.showStatusMessage(tr("Printing..."))

	def clearAllTabbedTranslateBrowser(self) :
		if self.checkBusyStreams() :
			return

		for panels_list_item in self._panels_list :
			panels_list_item.clear()

		self._tabbed_translate_browser.clearAll()

		self.activateFocus()

	def clearTabbedTranslateBrowserPage(self) :
		if self.checkBusyStreams() :
			return
		self._tabbed_translate_browser.clearPage()

		self.activateFocus()

	###

	def saveSettings(self) :
		settings = Settings.settings()
		settings.setValue("main_window/size", Qt.QVariant(self.size()))
		settings.setValue("main_window/position", Qt.QVariant(self.pos()))
		settings.setValue("main_window/is_visible_flag", Qt.QVariant(self.isVisible()))
		settings.setValue("main_window/state", Qt.QVariant(self.saveState()))

	def loadSettings(self) :
		settings = Settings.settings()
		self.resize(settings.value("main_window/size", Qt.QVariant(Qt.QSize(800, 500))).toSize())
		self.move(settings.value("main_window/position", Qt.QVariant(Qt.QPoint(0, 0))).toPoint())
		self.setVisible(settings.value("main_window/is_visible_flag", Qt.QVariant(True)).toBool())
		self.restoreState(settings.value("main_window/state", Qt.QVariant(Qt.QByteArray())).toByteArray())


	### Signals ###

	def spyStartedSignal(self) :
		self.emit(Qt.SIGNAL("spyStarted()"))

	def spyStoppedSignal(self) :
		self.emit(Qt.SIGNAL("spyStopped()"))

