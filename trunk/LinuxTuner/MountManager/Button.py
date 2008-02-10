from PyQt4 import Qt
import Const

class Button(Qt.QPushButton):
	### Common class for all types of buttons in the program ###
	def __init__(self,type,popup_text,popup_widget,popup_title = None,doc_mark = None,parent = None):
		Qt.QPushButton.__init__(self,parent)
		
		self.popup_text = popup_text
		self.popup_widget = popup_widget
		self.popup_title = popup_title
		self.type = type
		self.doc_mark = doc_mark
		
		if type == "advanced":
			self.setIcon(Qt.QIcon(Const.Icons_path + "warning.png"))
			self.setFlat(True)
		elif type == "info":
			self.setIcon(Qt.QIcon(Const.Icons_path + "info.png"))
			
		self.connect(self,Qt.SIGNAL("clicked()"),self.showPopup)
		
	def showPopup(self):
 		### Show popup window ###
		
		self.popup_widget.setData(self.popup_title,self.popup_text,self.doc_mark)
			
			
		
		