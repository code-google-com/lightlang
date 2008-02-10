from PyQt4 import Qt
import Const

lang = Qt.QLocale().name()
lang.remove(lang.indexOf("_"), lang.length())

class DocumentationParser:
	def __init__(self):
		
		self.file_systems_doc = []
		self.general_doc = []
		self.common_options_doc = []
		self.depends_on_fs_options_doc = []
		
		self.file_systems_dir = Qt.QDir(Const.Doc_path + "/" + lang + "/FileSystems")
		self.general_dir = Qt.QDir(Const.Doc_path + "/" + lang + "/General")
		self.common_options_dir = Qt.QDir(Const.Doc_path + "/" + lang + "/Options/Common")
		self.depends_on_fs_options_dir = Qt.QDir(Const.Doc_path + "/" + lang + "/Options/DependsOnFS")
		
		self.file = Qt.QFile()
		self.stream = Qt.QTextStream(self.file)
		
		index = 2
		while index < self.file_systems_dir.count():
			self.file.setFileName(self.file_systems_dir.filePath(self.file_systems_dir[index]))
			self.file.open(Qt.QIODevice.ReadOnly)
			self.file_systems_doc.append([self.file_systems_dir[index].remove(".html"),self.stream.readAll()])
			index+=1
		
		index = 2
		while index < self.general_dir.count():
			self.file.setFileName(self.general_dir.filePath(self.general_dir[index]))
			self.file.open(Qt.QIODevice.ReadOnly)
			self.general_doc.append([self.general_dir[index].remove(".html"),self.stream.readAll()])
			index+=1
		
		index = 2
		while index < self.common_options_dir.count():
			self.file.setFileName(self.common_options_dir.filePath(self.common_options_dir[index]))
			self.file.open(Qt.QIODevice.ReadOnly)
			self.common_options_doc.append([self.common_options_dir[index].remove(".html"),self.stream.readAll()])
			index+=1
			
		index = 2
		while index < self.depends_on_fs_options_dir.count():
			self.file.setFileName(self.depends_on_fs_options_dir.filePath(self.depends_on_fs_options_dir[index]))
			self.file.open(Qt.QIODevice.ReadOnly)
			self.depends_on_fs_options_doc.append([self.depends_on_fs_options_dir[index].remove(".html"),self.stream.readAll()])
			index+=1
			
	def getDocAboutFileSystems(self):
		return self.file_systems_doc
	
	def getGeneralDoc(self):
		return self.general_doc
	
	def getCommonOptionsDoc(self):
		return self.common_options_doc
	
	def getDependsOnFsOptionsDoc(self):
		return self.depends_on_fs_options_doc
			
class DocumentationCenter:
	def __init__(self):
		
		self.doc_parser = DocumentationParser()
		
		self.fs_doc = self.doc_parser.getDocAboutFileSystems()
		self.general_doc = self.doc_parser.getGeneralDoc()
		self.common_options_doc = self.doc_parser.getCommonOptionsDoc()
		self.depends_on_fs_doc = self.doc_parser.getDependsOnFsOptionsDoc()
		
	def getInfoAboutFs(self,fs_name):
		
		for fs in self.fs_doc:
			if fs[0] == fs_name:
				return fs[1]
			
		return None
		
	def getGeneralInfo(self,mark):
		
		for general in self.general_doc:
			if general[0] == mark:
				return general[1]
		return None
		
	def getCommonOptionInfo(self,option_name):
		
		for common_option in self.common_options_doc:
			if common_option[0] == option_name:
				return option_name[1]
		return None
		
	def getDependsOnFsOptionInfo(self,option_name):
		
		for depends_on_fs_option in self.depends_on_fs_doc:
			if depends_on_fs_option[0] == option_name:
				return depends_on_fs_option[1]
		return None
		
		