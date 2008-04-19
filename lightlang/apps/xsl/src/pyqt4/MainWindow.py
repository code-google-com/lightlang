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
import Spy
import FindInSLPanel
import FindInTextPanel
import GoogleTranslatePanel
import HistoryPanel
import TextBrowser
import TranslateWindow
import DictsManager
try : # FIXME: fucking debian packagers :-(
	import IFAMenu
	import TranslateSitesMenu
except : pass
import InternetLinksMenu
import Help

#####
MyIcon = Config.Prefix+"/lib/xsl/icons/xsl_16.png"
IconsDir = Config.Prefix+"/lib/xsl/icons/"
WaitPicture = Config.Prefix+"/lib/xsl/pictures/circular.gif"

#####
class StatusBar(Qt.QStatusBar) :
	def __init__(self, parent = None) :
		Qt.QStatusBar.__init__(self, parent)

		icon_width = icon_height = label_height = self.style().pixelMetric(Qt.QStyle.PM_SmallIconSize)

		###

		self.activation_semaphore = 0

		self.timer = Qt.QTimer()

		###

		self.message_label = Qt.QLabel()
		self.message_label.setMaximumHeight(label_height)
		self.addWidget(self.message_label, 1)

		self.wait_picture_movie = Qt.QMovie(WaitPicture)
		self.wait_picture_movie.setScaledSize(Qt.QSize(icon_width, icon_height))
		self.wait_picture_movie.jumpToFrame(0)
		self.wait_picture_movie_label = Qt.QLabel()
		self.wait_picture_movie_label.setMovie(self.wait_picture_movie)
		self.wait_picture_movie_label.setVisible(False)
		self.addWidget(self.wait_picture_movie_label)

		###

		self.connect(self.timer, Qt.SIGNAL("timeout()"), self.clearStatusMessage)


	### Public ###

	def startWaitMovie(self) :
		if self.activation_semaphore != 0 :
			self.activation_semaphore += 1
			return

		self.wait_picture_movie_label.setVisible(True)
		self.wait_picture_movie.start()

	def stopWaitMovie(self) :
		if self.activation_semaphore > 1 :
			return
		if self.activation_semaphore > 0 :
			self.activation_semaphore -= 1

		self.wait_picture_movie_label.setVisible(False)
		self.wait_picture_movie.stop()
		self.wait_picture_movie.jumpToFrame(0)

	###

	def showStatusMessage(self, text, timeout = 2000) :
		self.message_label.setText(text)
		if timeout != 0 :
			self.timer.start(timeout)

	def clearStatusMessage(self) :
		self.message_label.clear()


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

		self.status_bar = StatusBar()
		self.setStatusBar(self.status_bar)

		##############################
		##### Creating Resources #####
		##############################

		self.source_objects_list = []

		self.printer = Qt.QPrinter()
		self.print_dialog = Qt.QPrintDialog(self.printer)

		self.find_in_sl_panel = FindInSLPanel.FindInSLPanel()
		self.addDockWidget(Qt.Qt.LeftDockWidgetArea, self.find_in_sl_panel)
		self.source_objects_list.append([self.find_in_sl_panel, -1])

		self.find_in_text_panel = FindInTextPanel.FindInTextPanel()
		self.find_in_text_panel.setVisible(False)
		self.addDockWidget(Qt.Qt.LeftDockWidgetArea, self.find_in_text_panel)

		self.history_panel = HistoryPanel.HistoryPanel()
		self.history_panel.setVisible(False)
		self.addDockWidget(Qt.Qt.RightDockWidgetArea, self.history_panel)

		self.google_translate_panel = GoogleTranslatePanel.GoogleTranslatePanel()
		self.google_translate_panel.setVisible(False)
		self.addDockWidget(Qt.Qt.RightDockWidgetArea, self.google_translate_panel)
		self.source_objects_list.append([self.google_translate_panel, -1])

		self.text_browser = TextBrowser.TextBrowser()
		self.main_layout.addWidget(self.text_browser)

		self.translate_window = TranslateWindow.TranslateWindow()

		self.dicts_manager = DictsManager.DictsManager()

		self.help_browser = Help.HelpBrowser()

		self.about = Help.About()

		### Connections

		self.connect(self.source_objects_list[0][0], Qt.SIGNAL("processStarted()"),
			lambda : self.registrateStream(0))
		self.connect(self.source_objects_list[0][0], Qt.SIGNAL("processFinished()"),
			lambda : self.releaseStream(0))
		self.connect(self.source_objects_list[0][0], Qt.SIGNAL("clearRequest()"),
			lambda : self.clearTextBrowser(0))
		self.connect(self.source_objects_list[0][0], Qt.SIGNAL("wordChanged(const QString &)"),
			lambda word : self.setTextBrowserCaption(0, word))
		self.connect(self.source_objects_list[0][0], Qt.SIGNAL("textChanged(const QString &)"),
			lambda text : self.setTextBrowserText(0, text))
		self.connect(self.source_objects_list[0][0], Qt.SIGNAL("newTabRequest()"),
			self.addTextBrowserTab)

		self.connect(self.source_objects_list[1][0], Qt.SIGNAL("processStarted()"),
			lambda : self.registrateStream(1))
		self.connect(self.source_objects_list[1][0], Qt.SIGNAL("processFinished()"),
			lambda : self.releaseStream(1))
		self.connect(self.source_objects_list[1][0], Qt.SIGNAL("clearRequest()"),
			lambda : self.clearTextBrowser(1))
		self.connect(self.source_objects_list[1][0], Qt.SIGNAL("wordChanged(const QString &)"),
			lambda word : self.setTextBrowserCaption(1, word))
		self.connect(self.source_objects_list[1][0], Qt.SIGNAL("textChanged(const QString &)"),
			lambda text : self.setTextBrowserText(1, text))
		self.connect(self.source_objects_list[1][0], Qt.SIGNAL("newTabRequest()"),
			self.addTextBrowserTab)

		self.connect(self.find_in_sl_panel, Qt.SIGNAL("processStarted()"), self.status_bar.startWaitMovie)
		self.connect(self.find_in_sl_panel, Qt.SIGNAL("processFinished()"), self.status_bar.stopWaitMovie)
		self.connect(self.find_in_sl_panel, Qt.SIGNAL("clearRequest()"), self.translate_window.clear)
		self.connect(self.find_in_sl_panel, Qt.SIGNAL("wordChanged(const QString &)"), self.history_panel.addWord)
		self.connect(self.find_in_sl_panel, Qt.SIGNAL("wordChanged(const QString &)"),
			self.translate_window.setCaption)
		self.connect(self.find_in_sl_panel, Qt.SIGNAL("textChanged(const QString &)"),
			self.translate_window.setText)

		self.connect(self.find_in_text_panel, Qt.SIGNAL("findNextRequest(const QString &)"),
			self.findInTextBrowserNext)
		self.connect(self.find_in_text_panel, Qt.SIGNAL("findPreviousRequest(const QString &)"),
			self.findInTextBrowserPrevious)

		self.connect(self.history_panel, Qt.SIGNAL("wordChanged(const QString &)"), self.find_in_sl_panel.setWord)

		self.connect(self.google_translate_panel, Qt.SIGNAL("processStarted()"),
			self.status_bar.startWaitMovie)
		self.connect(self.google_translate_panel, Qt.SIGNAL("processFinished()"),
			self.status_bar.stopWaitMovie)
		self.connect(self.google_translate_panel, Qt.SIGNAL("statusChanged(const QString &)"),
			self.status_bar.showStatusMessage)

		self.connect(self.text_browser, Qt.SIGNAL("uFindRequest(const QString &)"),
			self.find_in_sl_panel.setWord)
		self.connect(self.text_browser, Qt.SIGNAL("uFindRequest(const QString &)"),
			self.find_in_sl_panel.uFind)
		self.connect(self.text_browser, Qt.SIGNAL("cFindRequest(const QString &)"),
			self.find_in_sl_panel.setWord)
		self.connect(self.text_browser, Qt.SIGNAL("cFindRequest(const QString &)"),
			self.find_in_sl_panel.cFind)

		self.connect(self.dicts_manager, Qt.SIGNAL("dictsListChanged(const QStringList &)"),
			self.find_in_sl_panel.setDictsList)
		self.connect(self.dicts_manager, Qt.SIGNAL("dictsListChanged(const QStringList &)"),
			self.find_in_sl_panel.lFind)

		#########################
		##### Creating Menu #####
		#########################

		self.main_menu_bar = Qt.QMenuBar()
		self.setMenuBar(self.main_menu_bar)

		### File Menu

		self.pages_menu = self.main_menu_bar.addMenu(self.tr("Pages"))
		self.pages_menu.addAction(Qt.QIcon(IconsDir+"save_16.png"), self.tr("Save current page"),
			self.saveCurrentTextBrowserPage)
		self.pages_menu.addAction(Qt.QIcon(IconsDir+"print_16.png"), self.tr("Print current page"),
			self.printCurrentTextBrowserPage, Qt.QKeySequence("Ctrl+P"))
		self.pages_menu.addSeparator()
		self.pages_menu.addAction(Qt.QIcon(IconsDir+"clear_16.png"), self.tr("Clear current page"),
			self.clearTextBrowserPage, Qt.QKeySequence("Ctrl+E"))
		self.pages_menu.addAction(Qt.QIcon(IconsDir+"clear_16.png"), self.tr("Clear all"),
			self.clearAllTextBrowser, Qt.QKeySequence("Ctrl+K"))
		self.pages_menu.addSeparator()
		self.pages_menu.addAction(Qt.QIcon(IconsDir+"find_16.png"), self.tr("Search in translations"),
			self.showFindInTextPanel, Qt.QKeySequence("Ctrl+F"))
		self.pages_menu.addSeparator()
		self.pages_menu.addAction(Qt.QIcon(IconsDir+"add_16.png"), self.tr("New tab"),
			self.addTextBrowserTab, Qt.QKeySequence("Ctrl+T"))
		self.pages_menu.addAction(Qt.QIcon(IconsDir+"remove_16.png"), self.tr("Close tab"),
			self.removeTextBrowserTab, Qt.QKeySequence("Ctrl+W"))
		self.pages_menu.addSeparator()
		self.pages_menu.addAction(Qt.QIcon(IconsDir+"exit_16.png"), self.tr("Quit"),
			self.exit, Qt.QKeySequence("Ctrl+Q"))

		### View Menu

		self.view_menu = self.main_menu_bar.addMenu(self.tr("View"))
		self.view_menu.addAction(Qt.QIcon(IconsDir+"zoom_in_16.png"), self.tr("Zoom in"),
			self.zoomInTextBrowser, Qt.QKeySequence("Ctrl++"))
		self.view_menu.addAction(Qt.QIcon(IconsDir+"zoom_out_16.png"), self.tr("Zoom out"),
			self.zoomOutTextBrowser, Qt.QKeySequence("Ctrl+-"))
		self.view_menu.addSeparator()
		self.view_menu.addAction(Qt.QIcon(IconsDir+"window_16.png"), self.tr("Toggle to fullscreen"),
			self.toggleFullScreen, Qt.QKeySequence("F11"))

		### Spy Menu

		self.spy_menu = Spy.SpyMenu(self.tr("Spy"))
		self.main_menu_bar.addMenu(self.spy_menu)

		### Tools Menu

		self.tools_menu = self.main_menu_bar.addMenu(self.tr("Tools"))
		self.tools_menu.addAction(Qt.QIcon(IconsDir+"dicts_manager_16.png"), self.tr("Dicts management"),
			self.showDictsManager, Qt.QKeySequence("Ctrl+D"))
		self.tools_menu.addAction(Qt.QIcon(IconsDir+"history_16.png"), self.tr("Search history"),
			self.showHistoryPanel, Qt.QKeySequence("Ctrl+H"))
		self.tools_menu.addSeparator()
		try : # FIXME: fucking debian packagers :-(
			self.translate_sites_menu = TranslateSitesMenu.TranslateSitesMenu(self.tr("Web translate"))
			self.translate_sites_menu.setIcon(Qt.QIcon(IconsDir+"web_16.png"))
			self.tools_menu.addMenu(self.translate_sites_menu)
		except : pass
		self.tools_menu.addAction(Qt.QIcon(IconsDir+"web_16.png"), self.tr("Google-Translate client"),
			self.showGoogleTranslatePanel, Qt.QKeySequence("Ctrl+G"))
		try : # FIXME: fucking debian packagers :-(
			self.tools_menu.addSeparator()
			self.ifa_menu = IFAMenu.IFAMenu(self.tr("Applications"))
			self.ifa_menu.setIcon(Qt.QIcon(IconsDir+"ifa_16.png"))
			self.tools_menu.addMenu(self.ifa_menu)
		except : pass

		### Help Menu

		self.help_menu = self.main_menu_bar.addMenu(self.tr("Help"))
		self.help_menu.addAction(Qt.QIcon(IconsDir+"help_16.png"),
			self.tr("%1 manual").arg(Const.Organization), self.showHelpBrowser, Qt.QKeySequence("F1"))
		self.help_menu.addSeparator()
		self.internet_links_menu = InternetLinksMenu.InternetLinksMenu(self.tr("Internet links"))
		self.internet_links_menu.setIcon(Qt.QIcon(IconsDir+"web_16.png"))
		self.help_menu.addMenu(self.internet_links_menu)
		self.help_menu.addSeparator()
		self.help_menu.addAction(Qt.QIcon(IconsDir+"xsl_16.png"), self.tr("About %1").arg(Const.MyName),
			self.showAbout)
		self.help_menu.addAction(Qt.QIcon(IconsDir+"about_16.png"), self.tr("About Qt4"), self.showAboutQt)

		### Connections

		self.connect(self.spy_menu, Qt.SIGNAL("spyStarted()"), self.spyStartedSignal)
		self.connect(self.spy_menu, Qt.SIGNAL("spyStopped()"), self.spyStoppedSignal)
		self.connect(self.spy_menu, Qt.SIGNAL("statusChanged(const QString &)"),
			self.status_bar.showStatusMessage)
		self.connect(self.spy_menu, Qt.SIGNAL("uFindRequest(const QString &)"),
			self.find_in_sl_panel.setWord)
		self.connect(self.spy_menu, Qt.SIGNAL("uFindRequest(const QString &)"),
			self.find_in_sl_panel.uFind)
		self.connect(self.spy_menu, Qt.SIGNAL("showTranslateWindowRequest()"),
			self.translate_window.showUnderCursor)

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
		self.spy_menu.startSpy()

        def stopSpy(self) :
		self.spy_menu.stopSpy()

	###

	def save(self) :
		self.saveSettings()
		self.history_panel.saveSettings()
		self.dicts_manager.saveSettings()
		self.google_translate_panel.saveSettings()
		self.spy_menu.saveSettings()

	def load(self) :
		self.loadSettings()
		self.history_panel.loadSettings()
		self.dicts_manager.loadSettings()
		self.google_translate_panel.loadSettings()
		self.spy_menu.loadSettings()
		self.status_bar.showStatusMessage(self.tr("Ready"))

	###

	def visibleChange(self) :
		if self.isVisible() :
			self.hide()
		else :
			self.showNormal()
			self.setFocus()

	###

	def exit(self) :
		self.save()
		sys.exit(0)


	### Private ###

	def registrateStream(self, source_object_index) :
		text_browser_index = self.text_browser.currentIndex()
		for source_object in self.source_objects_list :
			Qt.QApplication.processEvents()
			if source_object[1] == text_browser_index :
				self.text_browser.addTab()
				text_browser_index = self.text_browser.currentIndex()
				break
		self.source_objects_list[source_object_index][1] = text_browser_index

	def releaseStream(self, source_object_index) :
		self.source_objects_list[source_object_index][1] = -1

	def clearTextBrowser(self, source_object_index) :
		self.text_browser.clear(self.source_objects_list[source_object_index][1])

	def setTextBrowserCaption(self, source_object_index, word) :
		self.text_browser.setCaption(self.source_objects_list[source_object_index][1], word)

	def setTextBrowserText(self, source_object_index, text) :
		self.text_browser.setText(self.source_objects_list[source_object_index][1], text)

	def addTextBrowserTab(self) :
		self.text_browser.addTab()

	def removeTextBrowserTab(self) :
		for source_object in self.source_objects_list :
			Qt.QApplication.processEvents()
			if source_object[1] != -1 :
				return
		self.text_browser.removeTab()

	###

	def findInTextBrowserNext(self, word) :
		for source_object in self.source_objects_list :
			Qt.QApplication.processEvents()
			if source_object[1] != -1 :
				return

		index = self.text_browser.currentIndex()
		if not self.text_browser.findNext(index, word) :
			self.status_bar.showStatusMessage(self.tr("Not found"))

	def findInTextBrowserPrevious(self, word) :
		for source_object in self.source_objects_list :
			Qt.QApplication.processEvents()
			if source_object[1] != -1 :
				return

		index = self.text_browser.currentIndex()
		if not self.text_browser.findPrevious(index, word) :
			self.status_bar.showStatusMessage(self.tr("Not found"))

	def saveCurrentTextBrowserPage(self) :
		for source_object in self.source_objects_list :
			Qt.QApplication.processEvents()
			if source_object[1] != -1 :
				return

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

		self.status_bar.showStatusMessage(self.tr("Saved"))

	def printCurrentTextBrowserPage(self) :
		for source_object in self.source_objects_list :
			Qt.QApplication.processEvents()
			if source_object[1] != -1 :
				return

		if self.print_dialog.exec_() != Qt.QDialog.Accepted :
			return

		index = self.text_browser.currentIndex()
		text_document = self.text_browser.document(index)
		text_document.print_(self.printer)

		self.status_bar.showStatusMessage(self.tr("Printing..."))

	def zoomInTextBrowser(self) :
		for source_object in self.source_objects_list :
			Qt.QApplication.processEvents()
			if source_object[1] != -1 :
				return
		self.text_browser.zoomIn()

	def zoomOutTextBrowser(self) :
		for source_object in self.source_objects_list :
			Qt.QApplication.processEvents()
			if source_object[1] != -1 :
				return
		self.text_browser.zoomOut()

	def clearAllTextBrowser(self) :
		for source_object in self.source_objects_list :
			Qt.QApplication.processEvents()
			if source_object[1] != -1 :
				return

		self.find_in_sl_panel.clear()
		self.text_browser.clearAll()
		self.find_in_sl_panel.setFocus()

	def clearTextBrowserPage(self) :
		for source_object in self.source_objects_list :
			Qt.QApplication.processEvents()
			if source_object[1] != -1 :
				return
		self.text_browser.clearPage()

	###

	def saveSettings(self) :
		settings = Qt.QSettings(Const.Organization, Const.MyName)
		settings.setValue("main_window/size", Qt.QVariant(self.size()))
		settings.setValue("main_window/position", Qt.QVariant(self.pos()))
		settings.setValue("main_window/is_visible_flag", Qt.QVariant(self.isVisible()))
		settings.setValue("main_window/state", Qt.QVariant(self.saveState()))

	def loadSettings(self) :
		settings = Qt.QSettings(Const.Organization, Const.MyName)
		self.resize(settings.value("main_window/size", Qt.QVariant(Qt.QSize(845, 650))).toSize())
		self.move(settings.value("main_window/position", Qt.QVariant(Qt.QPoint(0, 0))).toPoint())
		self.setVisible(settings.value("main_window/is_visible_flag", Qt.QVariant(True)).toBool())
		self.restoreState(settings.value("main_window/state", Qt.QVariant(Qt.QByteArray())).toByteArray())

	def toggleFullScreen(self) :
		if self.isFullScreen() :
			self.showNormal()
		else :
			self.showFullScreen()

	def setFocus(self, reason = Qt.Qt.OtherFocusReason) :
		self.find_in_sl_panel.setFocus(reason)

	###

	def showFindInTextPanel(self) :
		self.find_in_text_panel.setVisible(True)
		self.find_in_text_panel.setFocus()

	def showHistoryPanel(self) :
		self.history_panel.setVisible(True)

	def showDictsManager(self) :
		self.dicts_manager.show()
		self.dicts_manager.raise_()
		self.dicts_manager.activateWindow()

	def showGoogleTranslatePanel(self) :
		self.google_translate_panel.setVisible(True)
		self.google_translate_panel.setFocus()

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
