from PyQt4 import Qt
import OptionsGroup

class GeneralSettingsWidget(Qt.QWidget):
	def __init__(self,item,popup_widget,parent = None):
		Qt.QWidget.__init__(self,parent)
	
		self.options_group = OptionsGroup.OptionsGroup(popup_widget)
		self.options_group.setColumnStretch(3)
		
		self.options_group.addLabelOption(self.tr("File system")+":",item.getFileSystem(),False,item.getFileSystem())
		
		self.options_group.addLineOption("mount_point",item.getMountPoint(),True,self.tr("Mount point") + ":",item.isSystem(),"mountpoint")
		
		self.options_group.addComboBoxOption(item.getDumpFlag(),["On","Off"],["1","0"],"Dump " + self.tr("flag") + ":",True,"dumpflag")
		
		if item.getFsck() != None:
			self.options_group.addSpinBoxOption("fsck",item.getFsck(),"Fsck " +  self.tr("value") + ":",0,5,True,"fsckvalue")
		elif item.isSystem():
			self.options_group.addSpinBoxOption("fsck",2,"Fsck " +  self.tr("value") + ":",0,5,True,"fsckvalue")
		elif not item.isRemovable():
			self.options_group.addSpinBoxOption("fsck",1,"Fsck " +  self.tr("value") + ":",0,5,True,"fsckvalue")
		else:
			self.options_group.addSpinBoxOption("fsck",0,"Fsck " +  self.tr("value") + ":",0,5,True,"fsckvalue")
		
		
		self.main_layout = Qt.QVBoxLayout()
		self.main_layout.addWidget(self.options_group)
		self.main_layout.addWidget(Qt.QLabel("<hr>"))
		self.main_layout.addStretch()
		
		self.setLayout(self.main_layout)
		
	def setExpertMode(self,b):
		
		self.options_group.setExpertMode(b)