from PyQt4 import Qt
import Const

class PopupWindow(Qt.QDialog):
	### Window wich show after press some buttons to show info about e.g. some option ##
	def __init__(self,doc_center,parent = None):
		Qt.QDialog.__init__(self,parent)
				
		self.setWindowFlags(Qt.Qt.Popup)
		self.resize(300,200)
		
		self.doc_center = doc_center
		
		self.cursor = Qt.QCursor()
		
		self.close_button = Qt.QToolButton()
		self.close_button.setIcon(Qt.QIcon(Const.Icons_path + "close_popup.png"))
		self.connect(self.close_button,Qt.SIGNAL("clicked()"),self.hide)
		
		self.title_label = Qt.QLabel()
		
		self.text_browser = Qt.QTextBrowser()
		
		self.top_layout = Qt.QHBoxLayout()
		self.top_layout.addWidget(self.title_label)
		self.top_layout.addStretch()
		self.top_layout.addWidget(self.close_button)
		
		self.main_layout = Qt.QVBoxLayout()
		self.main_layout.setMargin(2)
		self.main_layout.setSpacing(2)
		self.main_layout.addLayout(self.top_layout)
		self.main_layout.addWidget(self.text_browser)
		
		self.setLayout(self.main_layout)
	
	def setData(self,popup_title,popup_text,doc_mark = None,width = 300,height = 200):
		### Set text in text browser ###
		self.resize(width,height)
		
		# Search documentation 
		if doc_mark != None:
			if self.doc_center.getInfoAboutFs(doc_mark) != None:
				popup_text += "<br>" + self.doc_center.getInfoAboutFs(doc_mark)
			elif self.doc_center.getGeneralInfo(doc_mark) != None:
				popup_text += "<br>" + self.doc_center.getGeneralInfo(doc_mark)
			elif self.doc_center.getCommonOptionInfo(doc_mark) != None:
				popup_text += "<br>" + self.doc_center.getCommonOptionInfo(doc_mark)
			elif self.doc_center.getDependsOnFsOptionInfo(doc_mark) != None:
				popup_text += "<br>" + self.doc_center.getDependsOnFsOptionInfo(doc_mark)
						
		
		
		# move window under cursor
		self.move(self.cursor.pos())
		
		self.title_label.setText("<b>" + popup_title + "</b>")
		
		if Qt.QString(popup_text).trimmed().isEmpty():
			popup_text = self.tr("There isn't documentation. Update package \"mountmanager-doc\" or report to developers at the site") + " " + Const.Site 
		
		self.text_browser.setHtml(popup_text)
		
		self.show()
		
		