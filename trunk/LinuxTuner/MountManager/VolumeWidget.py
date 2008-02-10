from PyQt4 import Qt
import GeneralSettingsWidget

class VolumeWidget(Qt.QWidget):
	def __init__(self,item,popup_widget,parent = None):
		Qt.QWidget.__init__(self,parent)
		
		self.item = item
		
		# Tool box
		self.tab_widget = Qt.QTabWidget()
		
		# Option line
		self.option_line = Qt.QLineEdit()
		if self.item.getOptionsAsLine() != None:
			self.option_line.setText(self.item.getOptionsAsLine())
		self.option_line.setReadOnly(True)
		
		# General settings widget
		self.general_settings_widget = GeneralSettingsWidget.GeneralSettingsWidget(item,popup_widget)
		
		# Not depends on file system options
		self.not_depends_widget = Qt.QWidget()
		
		# Depends on file system options
		self.depends_widget = Qt.QWidget()
		
		self.tab_widget.addTab(self.general_settings_widget,self.tr("General settings"))
		self.tab_widget.addTab(self.not_depends_widget,self.tr("Independent options"))
		self.tab_widget.addTab(self.depends_widget,self.tr("Depends on file system options"))
		# Main layout 
		self.main_layout = Qt.QVBoxLayout()
		self.main_layout.addWidget(self.option_line)
		self.main_layout.addWidget(self.tab_widget)
		
		self.setLayout(self.main_layout)
	
	def getMountOptions(self):
		
		if self.option_line.text().isEmpty():
			return None
		return self.option_line.text().split(",")
	
	def setExpertMode(self,b):
		self.option_line.setVisible(b)
		self.general_settings_widget.setExpertMode(b)