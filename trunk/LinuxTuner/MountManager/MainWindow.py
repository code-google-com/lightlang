from PyQt4 import Qt
import CentralWidget
import Const
import sys

class MainWindow(Qt.QMainWindow):
	def __init__(self,parent = None):
		Qt.QMainWindow.__init__(self,parent)
		
		# Actions
		
		self.quit_action = Qt.QAction(self)
		self.quit_action.setText(self.tr("Quit"))
		self.quit_action.setShortcut(Qt.QKeySequence("Ctrl+Q"))
		
		self.expert_mode_action = Qt.QAction(self)
		self.expert_mode_action.setText(self.tr("Expert mode"))
		self.expert_mode_action.setCheckable(True)
		
		# Toolbar
		self.tool_bar = Qt.QToolBar(self.tr("Main tool bar"))
		self.tool_bar.setObjectName("MainToolBar")		
		
		self.tool_bar.addAction(self.quit_action)
		self.tool_bar.addAction(self.expert_mode_action)
		
		# Menus
		
		self.menu_bar = Qt.QMenuBar()
		
			# Partition menu
		self.partition_menu = Qt.QMenu("&" + self.tr("Partition"))
		self.partition_menu.addAction(self.quit_action)
		
			# Tools menu
		self.tools_menu = Qt.QMenu("&" + self.tr("Tools"))
		self.tools_menu.addAction(self.expert_mode_action)
		
			# Settings menu
		self.settings_menu = Qt.QMenu("&" + self.tr("Settings"))
		
			# Actions menu
		self.actions_menu = Qt.QMenu("&" + self.tr("Actions"))
		
			# Help menu
		self.help_menu = Qt.QMenu("&" + self.tr("Help"))
		
		self.menu_bar.addMenu(self.partition_menu)
		self.menu_bar.addMenu(self.tools_menu)
		self.menu_bar.addMenu(self.settings_menu)
		self.menu_bar.addMenu(self.actions_menu)
		self.menu_bar.addMenu(self.help_menu)
		
		self.setMenuBar(self.menu_bar)
		
		# Central widget
		self.central_widget = CentralWidget.CentralWidget()
		self.setCentralWidget(self.central_widget)
		
		# Connections:
		self.connect(self.quit_action,Qt.SIGNAL("triggered()"),self.quitFromProgram)
		self.connect(self.expert_mode_action,Qt.SIGNAL("toggled(bool)"),self.setExpertMode)
		
		# Add tool bars
		self.addToolBar(self.tool_bar)
		
		# Settings of main window
		self.setWindowTitle(Const.Program_name + " " + Const.Version)
		self.setWindowIcon(Qt.QIcon(Const.Icons_path + "mountmanager.png"))
		self.loadSettings()
	
	### Private ###
	
	def closeEvent(self,event):
		self.quitFromProgram()
	
	def quitFromProgram(self):
		### Quit function ###
		# Remove block file
		if not Qt.QFile.remove(str(Qt.QDir.tempPath()) + "/" + Const.Program_name + ".block"):
			print "Cannot remove block file"
			
		self.saveSettings()
		self.central_widget.saveLogFile()
		sys.exit()
		
	def saveSettings(self):
		### Save settings of application ###
		settings = Qt.QSettings(Const.Organization,Const.Program_name)
		settings.beginGroup("WindowOptions")
		settings.setValue("Size",Qt.QVariant(self.size()))
		settings.setValue("Position",Qt.QVariant(self.pos()))
		settings.setValue("WindowState",Qt.QVariant(self.saveState()))
		settings.setValue("ShowSystemPartitions",Qt.QVariant(self.central_widget.show_system_partitions.isChecked()))
		settings.setValue("ExpertMode",Qt.QVariant(self.expert_mode_action.isChecked()))
		settings.endGroup()
		
	def loadSettings(self):
		### Load previous settings of application ###
		settings = Qt.QSettings(Const.Organization,Const.Program_name)
		settings.beginGroup("WindowOptions")
		self.resize(settings.value("Size",Qt.QVariant(800,500)).toSize())
		self.move(settings.value("Position",Qt.QVariant(0,0)).toPoint())
		self.restoreState(settings.value("WindowState").toByteArray())
		self.central_widget.show_system_partitions.setChecked(settings.value("ShowSystemPartitions",Qt.QVariant(False)).toBool())
		self.expert_mode_action.setChecked(settings.value("ExpertMode",Qt.QVariant(False)).toBool())
		settings.endGroup()
		
	
	def setExpertMode(self,b):
		### Hide some settings and information ###
		self.central_widget.setExpertMode(b)
		