from PyQt4 import Qt

class MountDialog(Qt.QDialog):
	def __init__(self,parent = None):
		Qt.QDialog.__init__(self,parent)
		
		self.info_label = Qt.QLabel()
		self.info_label.setWordWrap(True)
		self.info_label.setText(self.tr("After clicking of the button \"Mount with options\" the partition will be mounted with such options:"))
		
		self.options_label = Qt.QLabel()
		self.options_label.setWordWrap(True)
		
		self.use_without_options = Qt.QPushButton()
		self.use_without_options.setText(self.tr("Mount without options"))
				
		self.use_options = Qt.QPushButton()
		self.use_options.setText(self.tr("Mount with options"))
		
		self.button_layout = Qt.QHBoxLayout()
		self.button_layout.addStretch()
		self.button_layout.addWidget(self.use_without_options)
		self.button_layout.addWidget(self.use_options)
		
		self.main_layout = Qt.QVBoxLayout()
		self.main_layout.addWidget(self.info_label)
		self.main_layout.addWidget(self.options_label)
		self.main_layout.addLayout(self.button_layout)
		
		self.setLayout(self.main_layout)
		self.setMinimumWidth(500)
		self.setMinimumHeight(150)
		
	def showDialog(self,device_name,is_system,options):
		
		self.setWindowTitle(self.tr("Mount") + " " + device_name)
		
		if is_system:
			self.info_label.setText("<font color='#FF0000'>" + self.tr("Be attention - this partition is system") +  \
				".</font> " + self.tr("After clicking of the button \"Mount with options\" the partition will be mounted with such options:"))
		
		option_text = "<br>"
		for option in options:
			option_text += "* " + str(option) + "<br>"
			 
	 	self.options_label.setText(option_text)
		
		self.show()