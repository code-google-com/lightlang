#!/usr/bin/python
from PyQt4 import Qt
import MainWindow
import Const
import sys

class MountManager:
	def __init__(self):
		self.app = Qt.QApplication(sys.argv)
		
		# For translation:
		self.lang = Qt.QLocale().name()
		self.lang.remove(self.lang.indexOf("_"), self.lang.length())

		self.translator = Qt.QTranslator()
		#self.translator.load(TrDir+self.lang)
		self.app.installTranslator(self.translator)
		
		# Check block file:
		if Qt.QFile.exists(Qt.QDir.tempPath() + "/" + Const.Program_name + ".block"):
			message_box = Qt.QMessageBox()
			message_box.setIconPixmap(Qt.QPixmap(Const.Icons_path + "mountmanager.png"))
			message_box.setWindowIcon(Qt.QIcon(Const.Icons_path + "mountmanager.png"))
			message_box.setWindowTitle(Const.Program_name + " " + Const.Version)
			message_box.setText(self.tr("The program is already running"))
			
			ok_button = message_box.addButton(self.tr("Ok"),Qt.QMessageBox.ActionRole)
			ignore_button = message_box.addButton(self.tr("Ignore"),Qt.QMessageBox.ActionRole)
	
			message_box.exec_()
	
			if message_box.clickedButton() == ok_button:
				sys.exit(0)
		else:
		# Create block file, if it doesn't exist
			block_file = Qt.QFile(Qt.QDir.tempPath() + "/" + Const.Program_name + ".block")
			block_file.open(Qt.QIODevice.WriteOnly)
					
		self.main_window = MainWindow.MainWindow()
		self.main_window.show()
		
		self.app.exec_()
		
	def tr(self, text):
		### Function of translating ###
		str = self.translator.translate("Main", text)
		if not str.simplified().isEmpty() :
			return str
		else :
			return text
		

mountmanager = MountManager()