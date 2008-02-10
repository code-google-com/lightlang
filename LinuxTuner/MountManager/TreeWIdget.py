from PyQt4 import Qt
import Menu

class TreeWidget(Qt.QTreeWidget):
	def __init__(self,parent = None):
		Qt.QTreeWidget.__init__(self,parent)
		
		self.setColumnCount(2)
		self.setHorizontalScrollBarPolicy(Qt.Qt.ScrollBarAlwaysOff)
		self.setHeaderLabels([self.tr("Device"),self.tr("Size")])
		
		# Context menu
		self.context_menu = Menu.Menu(Qt.QIcon("mountmanager.png"))
		
			# Actions
		self.mount_action = Qt.QAction(self.context_menu)
		self.mount_action.setText(self.tr("Mount"))
		
		self.umount_action = Qt.QAction(self.context_menu)
		self.umount_action.setText(self.tr("Unmount"))
			
		self.show_info_about_file_system_action = Qt.QAction(self.context_menu)
		self.show_info_about_file_system_action.setText(self.tr("Show file system information"))
		
		self.context_menu.addAction(self.mount_action)
		self.context_menu.addAction(self.umount_action)
		self.context_menu.addAction(self.show_info_about_file_system_action)
		
	def contextMenuEvent(self,event):
		### If user clicked right button of the mouse, show menu ###
		item = self.itemAt(event.x(),event.y())
		if item != None:
			self.context_menu.setCaption(item.text(0))
			if item.text(3).isEmpty():
				self.mount_action.setEnabled(False)
				self.umount_action.setEnabled(False)
			elif item.text(3).toLower() == "unmounted":
				self.mount_action.setEnabled(True)
				self.umount_action.setEnabled(False)
			else:
				self.mount_action.setEnabled(False)
				if item.data(4,4).toString().isEmpty() or item.data(4,4).toString() == "/":
					self.umount_action.setEnabled(False)
				else:
					self.umount_action.setEnabled(True)
				
			self.context_menu.move(event.globalX(),event.globalY())
			self.context_menu.show()
			
			
		