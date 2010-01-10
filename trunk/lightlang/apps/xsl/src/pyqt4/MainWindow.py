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

		self.setObjectName("main_window")

		self.setDockOptions(self.dockOptions()|Qt.QMainWindow.VerticalTabs)

		self.setWindowTitle(Const.Organization+" "+Const.MyName)
		self.setWindowIcon(Qt.QIcon(MyIcon))

		#####

		self.main_widget = Qt.QWidget()
		self.setCentralWidget(self.main_widget)

		self.main_layout = Qt.QVBoxLayout()
		self.main_layout.setContentsMargins(-1, 0, 0, -1)
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

		self.sl_search_panel = SlSearchPanel.SlSearchPanel()
		self.addDockWidget(Qt.Qt.LeftDockWidgetArea, self.sl_search_panel)
		self.addSourceObject(self.sl_search_panel)
		self.addPanel(self.sl_search_panel)

		self.history_panel = HistoryPanel.HistoryPanel()
		self.addDockWidget(Qt.Qt.LeftDockWidgetArea, self.history_panel)
		self.tabifyDockWidget(self.sl_search_panel, self.history_panel)
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

		self.dicts_manager_window = DictsManagerWindow.DictsManagerWindow()

		self.help_browser_window = HelpBrowserWindow.HelpBrowserWindow()

		self.about_window = AboutWindow.AboutWindow()

		### Exclusive connections

		self.connect(self.sl_search_panel, Qt.SIGNAL("clearRequest()"), self.translate_window.clear)
		self.connect(self.sl_search_panel, Qt.SIGNAL("wordChanged(const QString &)"), self.history_panel.addWord)
		self.connect(self.sl_search_panel, Qt.SIGNAL("wordChanged(const QString &)"), self.translate_window.setCaption)
		self.connect(self.sl_search_panel, Qt.SIGNAL("textChanged(const QString &)"), self.translate_window.setText)

		self.connect(self.history_panel, Qt.SIGNAL("wordChanged(const QString &)"), self.sl_search_panel.setWord)
		self.connect(self.history_panel, Qt.SIGNAL("wordChanged(const QString &)"), self.sl_search_panel.show)

		self.connect(self.tabbed_translate_browser, Qt.SIGNAL("uFindRequest(const QString &)"), self.sl_search_panel.setWord)
		self.connect(self.tabbed_translate_browser, Qt.SIGNAL("uFindRequest(const QString &)"), self.sl_search_panel.uFind)
		self.connect(self.tabbed_translate_browser, Qt.SIGNAL("cFindRequest(const QString &)"), self.sl_search_panel.setWord)
		self.connect(self.tabbed_translate_browser, Qt.SIGNAL("cFindRequest(const QString &)"), self.sl_search_panel.cFind)
		self.connect(self.tabbed_translate_browser, Qt.SIGNAL("statusChanged(const QString &)"), self.status_bar.showStatusMessage)

		self.connect(self.translate_window, Qt.SIGNAL("newTabRequest()"), self.addTabbedTranslateBrowserTab)
		self.connect(self.translate_window, Qt.SIGNAL("uFindRequest(const QString &)"), self.sl_search_panel.setWord)
		self.connect(self.translate_window, Qt.SIGNAL("uFindRequest(const QString &)"), self.sl_search_panel.uFind)
		self.connect(self.translate_window, Qt.SIGNAL("cFindRequest(const QString &)"), self.sl_search_panel.setWord)
		self.connect(self.translate_window, Qt.SIGNAL("cFindRequest(const QString &)"), self.sl_search_panel.cFind)
		self.connect(self.translate_window, Qt.SIGNAL("uFindRequest(const QString &)"), self.sl_search_panel.show)
		self.connect(self.translate_window, Qt.SIGNAL("cFindRequest(const QString &)"), self.sl_search_panel.show)
		self.connect(self.translate_window, Qt.SIGNAL("uFindRequest(const QString &)"), self.showUp)
		self.connect(self.translate_window, Qt.SIGNAL("cFindRequest(const QString &)"), self.showUp)

		self.connect(self.dicts_manager_window, Qt.SIGNAL("dictsListChanged(const QStringList &)"), self.sl_search_panel.setDictsList)
		self.connect(self.dicts_manager_window, Qt.SIGNAL("dictsListChanged(const QStringList &)"), lambda : self.sl_search_panel.lFind())

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
			self.printCurrentTabbedTranslateBrowserPage)
		self.pages_menu.addSeparator()
		self.pages_menu.addAction(Qt.QIcon(IconsDir+"clear_16.png"), tr("Clear current page"),
			self.clearTabbedTranslateBrowserPage, Qt.QKeySequence("Ctrl+E"))
		self.pages_menu.addAction(Qt.QIcon(IconsDir+"clear_16.png"), tr("Clear all"),
			self.clearAllTabbedTranslateBrowser, Qt.QKeySequence("Ctrl+K"))
		self.pages_menu.addSeparator()
		self.pages_menu.addAction(Qt.QIcon(IconsDir+"search_16.png"), tr("Search in translations"),
			self.tabbed_translate_browser.showTextSearchFrame, Qt.QKeySequence("Ctrl+F"))
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
		self.view_menu.addAction(Qt.QIcon(IconsDir+"zoom_normal_16.png"), tr("Zoom normal"),
			self.tabbed_translate_browser.zoomNormal, Qt.QKeySequence("Ctrl+0"))

		### Spy Menu

		self.spy_menu = SpyMenu.SpyMenu(tr("Sp&y"))
		self.main_menu_bar.addMenu(self.spy_menu)

		### Tools Menu

		self.tools_menu = self.main_menu_bar.addMenu(tr("&Tools"))
		self.tools_menu.addAction(Qt.QIcon(IconsDir+"xsl_16.png"), tr("SL search"),
			self.sl_search_panel.show, Qt.QKeySequence("Ctrl+S"))
		self.tools_menu.addAction(Qt.QIcon(IconsDir+"history_16.png"), tr("Search history"),
			self.history_panel.show, Qt.QKeySequence("Ctrl+H"))
		self.tools_menu.addAction(Qt.QIcon(IconsDir+"web_16.png"), tr("Google-Translate client"),
			self.google_translate_panel.show, Qt.QKeySequence("Ctrl+G"))
		self.tools_menu.addSeparator()
		self.tools_menu.addAction(Qt.QIcon(IconsDir+"dicts_manager_16.png"), tr("Dicts management"),
			self.dicts_manager_window.show, Qt.QKeySequence("Ctrl+D"))
		self.tools_menu.addSeparator()
		self.translate_sites_menu = TranslateSitesMenu.TranslateSitesMenu(tr("Web translate"))
		self.translate_sites_menu.setIcon(Qt.QIcon(IconsDir+"web_16.png"))
		self.tools_menu.addMenu(self.translate_sites_menu)
		self.tools_menu.addSeparator()
		self.ifa_menu = IfaMenu.IfaMenu(tr("Applications"))
		self.ifa_menu.setIcon(Qt.QIcon(IconsDir+"ifa_16.png"))
		self.tools_menu.addMenu(self.ifa_menu)

		### Help Menu

		self.help_menu = self.main_menu_bar.addMenu(tr("&Help"))
		self.help_menu.addAction(Qt.QIcon(IconsDir+"help_16.png"), tr("%1 manual").arg(Const.Organization),
			self.help_browser_window.show, Qt.QKeySequence("F1"))
		self.help_menu.addSeparator()
		self.internet_links_menu = InternetLinksMenu.InternetLinksMenu(tr("Internet links"))
		self.internet_links_menu.setIcon(Qt.QIcon(IconsDir+"web_16.png"))
		self.help_menu.addMenu(self.internet_links_menu)
		self.help_menu.addSeparator()
		self.help_menu.addAction(Qt.QIcon(IconsDir+"xsl_16.png"), tr("About %1").arg(Const.MyName), self.about_window.show)
		self.help_menu.addAction(Qt.QIcon(IconsDir+"about_16.png"), tr("About Qt4"), lambda : Qt.QMessageBox.aboutQt(None))

		### Exclusive connections

		self.connect(self.spy_menu, Qt.SIGNAL("spyStarted()"), self.spyStartedSignal)
		self.connect(self.spy_menu, Qt.SIGNAL("spyStopped()"), self.spyStoppedSignal)
		self.connect(self.spy_menu, Qt.SIGNAL("statusChanged(const QString &)"), self.status_bar.showStatusMessage)
		self.connect(self.spy_menu, Qt.SIGNAL("uFindRequest(const QString &)"), self.sl_search_panel.setWord)
		self.connect(self.spy_menu, Qt.SIGNAL("uFindRequest(const QString &)"), self.sl_search_panel.uFind)
		self.connect(self.spy_menu, Qt.SIGNAL("showTranslateWindowRequest()"), self.translate_window.show)
		self.connect(self.spy_menu, Qt.SIGNAL("showTranslateWindowRequest()"), self.translate_window.setFocus)


	### Public ###

	def startSpy(self) :
		self.spy_menu.startSpy()

        def stopSpy(self) :
		self.spy_menu.stopSpy()

	###

	def save(self) :
		for panels_list_item in self.panels_list :
			panels_list_item.saveSettings()

		self.dicts_manager_window.saveSettings()
		self.translate_window.saveSettings()
		self.help_browser_window.saveSettings()
		self.spy_menu.saveSettings()
		self.translate_sites_menu.saveSettings()
		self.ifa_menu.saveSettings()

		self.saveSettings()

	def load(self) :
		for panels_list_item in self.panels_list :
			panels_list_item.loadSettings()

		self.dicts_manager_window.loadSettings()
		self.translate_window.loadSettings()
		self.help_browser_window.loadSettings()
		self.spy_menu.loadSettings()
		self.translate_sites_menu.loadSettings()
		self.ifa_menu.loadSettings()

		self.loadSettings()

		self.sl_search_panel.setFocus()
		self.sl_search_panel.raise_()

		self.tabbed_translate_browser.setCaption(0, tr("Welcome"))
		self.tabbed_translate_browser.setText(0, tr("<br><br><hr><table border=\"0\" width=\"100%\"><tr>"
			"<td class=\"dict_header_background\" align=\"center\"><font class=\"dict_header_font\">"
			"Welcome to the %1 - the system of electronic dictionaries</font></td></tr></table><hr>").arg(Const.Organization))

		self.status_bar.showStatusMessage(tr("Ready"))

	###

	def visibleChange(self) :
		if not self.isVisible() or self.isMinimized() or not self.isActiveWindow() :
			self.close() # FIXME: Normal window move to top
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
		new_panels_focus_flags_list = [ panels_list_item.hasInternalFocus() for panels_list_item in self.panels_list ]
		if True in new_panels_focus_flags_list :
			self.panels_focus_flags_list = new_panels_focus_flags_list

	def activateFocus(self) :
		count = 0
		while count < len(self.panels_list) :
			if self.panels_focus_flags_list[count] :
				self.panels_list[count].setFocus()
			count += 1

	###

	def exit(self) :
		self.save()
		Qt.QApplication.instance().exit(0)


	### Private ###

	def addPanel(self, panel) :
		self.panels_list.append(panel)
		self.panels_focus_flags_list.append(False)

	def addSourceObject(self, source_object) :
		self.source_objects_list.append([source_object, - 1])

		index = len(self.source_objects_list) - 1

		registrate_stream = ( lambda n = index : self.registrateStream(n) )
		release_stream = ( lambda n = index : self.releaseStream(n) )
		clear_tabbed_translate_browser = ( lambda n = index : self.clearTabbedTranslateBrowser(n) )
		set_tabbed_translate_browser_caption = ( lambda word, n = index : self.setTabbedTranslateBrowserCaption(n, word) )
		set_tabbed_translate_browser_text = ( lambda text, n = index : self.setTabbedTranslateBrowserText(n, text) )
		add_tabbed_translate_browser_tab = ( lambda : self.addTabbedTranslateBrowserTab() )
		status_bar_start_wait_movie = ( lambda : self.status_bar.startWaitMovie() )
		status_bar_stop_wait_movie = ( lambda : self.status_bar.stopWaitMovie() )
		status_bar_show_status_message = ( lambda str : self.status_bar.showStatusMessage(str) )

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
		for source_objects_list_item in self.source_objects_list :
			if source_objects_list_item[1] == tabbed_translate_browser_index :
				self.tabbed_translate_browser.addTab()
				tabbed_translate_browser_index = self.tabbed_translate_browser.currentIndex()
				break
		self.source_objects_list[source_object_index][1] = tabbed_translate_browser_index

	def releaseStream(self, source_object_index) :
		self.tabbed_translate_browser.setShredLock(False)
		self.source_objects_list[source_object_index][1] = -1

	def checkBusyStreams(self) :
		for source_objects_list_item in self.source_objects_list :
			if source_objects_list_item[1] != -1 :
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
		file_path = Qt.QFileDialog.getSaveFileName(None,
			tr("Save page \"%1\"").arg(self.tabbed_translate_browser.caption(index)),
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
		file_stream << self.tabbed_translate_browser.document(index).toHtml("utf-8")

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

		for panels_list_item in self.panels_list :
			panels_list_item.clear()

		self.tabbed_translate_browser.clearAll()

		self.activateFocus()

	def clearTabbedTranslateBrowserPage(self) :
		if self.checkBusyStreams() :
			return
		self.tabbed_translate_browser.clearPage()

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

