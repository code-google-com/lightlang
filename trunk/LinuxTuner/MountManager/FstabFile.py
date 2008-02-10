from PyQt4 import Qt
import Const 

def getFstabContent():
	### Return content if fstab file (/etc/fstab) ###
	
	fstab_file = Qt.QFile(Const.Fstab_path)
	fstab_file.open(Qt.QIODevice.ReadOnly)
	fstab_stream = Qt.QTextStream(fstab_file)
	return str(fstab_stream.readAll())


class FstabRecord:
	def __init__(self,device_name,mount_point,file_system,options,dump,fsck):
		
		self.device_name = device_name
		self.mount_point = mount_point
		self.file_system = file_system
		self.options = options
		self.dump = dump
		self.fsck = fsck
		
		
class FstabParser:
	def __init__(self):
		
		fstab_file = Qt.QFile(Const.Fstab_path)
		fstab_file.open(Qt.QIODevice.ReadOnly)
		fstab_stream = Qt.QTextStream(fstab_file)
		
		self.fstab_records = []
		
		while not fstab_stream.atEnd():
			line = fstab_stream.readLine()
			line = line.trimmed()
			if line.isEmpty():
				continue
			if line[0] == "#":
				continue
			
			line = line.replace("\t"," ")
			list = line.split(" ")
			index = list.count()-1
			while index > 0:
				if list[index].trimmed().isEmpty():
					list.removeAt(index)
				index-=1	
				
			if list.count() != 6:
				continue
			
			self.fstab_records.append(FstabRecord(list[0],list[1],list[2],list[3],list[4],list[5]))
			
	def getFstabRecords(self):
		return self.fstab_records
			
	