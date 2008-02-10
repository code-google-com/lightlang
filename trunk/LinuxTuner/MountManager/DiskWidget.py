from PyQt4 import Qt
import Menu
import Const

class DiskWidget(Qt.QTableWidget):
	def __init__(self,item,parent = None):
		Qt.QTableWidget.__init__(self,parent)
		
		self.tree_widget_item = item
		self.setColumnCount(7)
		self.setHorizontalHeaderLabels([self.tr("Device"),self.tr("Mount point"), \
				self.tr("File system"),self.tr("Dump"),self.tr("Fsck"),self.tr("Status"),self.tr("Options")])
		
		self.setSelectionBehavior(Qt.QAbstractItemView.SelectRows)
		self.setSelectionMode(Qt.QAbstractItemView.SingleSelection)
    	 	self.horizontalHeader().setStretchLastSection(True)
    	 	self.setEditTriggers(Qt.QAbstractItemView.NoEditTriggers)
		
		self.menu = Menu.Menu(Qt.QIcon(Const.Icons_path + "disk_widget_menu.png"))
		
		self.move_action = Qt.QAction(self.menu)
		self.move_action.setText(self.tr("Manage this partition"))
		self.connect(self.move_action,Qt.SIGNAL("triggered()"),self.changeCurrentPageSignal)
		
		self.menu.addAction(self.move_action)
		
		self.expert_items = []
		
		self.tree_widget_items = []
		
	def addVolume(self,tree_widget_item):
		### Add row to table ###
		
		self.tree_widget_items.append(tree_widget_item)
		row = self.rowCount()
		self.insertRow(row)
		
		item = Qt.QTableWidgetItem()
		item.setText(str(tree_widget_item.getDeviceName()))
		self.setItem(row,0,item)
		
		item = Qt.QTableWidgetItem()
		item.setText(str(tree_widget_item.getMountPoint()))
		self.setItem(row,1,item)
		
		item = Qt.QTableWidgetItem()
		item.setText(str(tree_widget_item.getFileSystem()))
		self.setItem(row,2,item)
		
		item = Qt.QTableWidgetItem()
		item.setText(str(tree_widget_item.getDumpFlag()))
		self.setItem(row,3,item)
		
		item = Qt.QTableWidgetItem()
		item.setText(str(tree_widget_item.getFsck()))
		self.setItem(row,4,item)
		
		item = Qt.QTableWidgetItem()
		if tree_widget_item.isMounted():
			item.setText(self.tr("Mounted"))
		else:
			item.setText(self.tr("Unmounted"))
		self.setItem(row,5,item)
		
		item = Qt.QTableWidgetItem()
		item.setText(str(tree_widget_item.getOptionsAsLine()))
		self.setItem(row,6,item)
		self.expert_items.append(item)
		
		self.resizeColumnsToContents()
				
	def contextMenuEvent(self,event):
		
		self.menu.move(event.globalX(),event.globalY())
		item = self.itemAt(event.pos())
		if item != None:
			self.menu.setCaption(self.item(item.row(),0).text())
			self.menu.show()
			
	def changeCurrentPageSignal(self):
		self.emit(Qt.SIGNAL("changeCurrentPage(QTreeWidgetItem*)"),self.tree_widget_items[self.currentRow()])
		
	def setExpertMode(self,b):
		self.setColumnHidden(6,not b)
		self.setColumnHidden(3,not b)
		self.setColumnHidden(4,not b)
		self.resizeColumnsToContents()