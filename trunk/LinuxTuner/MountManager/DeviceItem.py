from PyQt4 import Qt
import Const
import FstabFile

class DeviceItem(Qt.QTreeWidgetItem):
	def __init__(self,properties,fstab_record,index,parent = None):
		Qt.QTreeWidgetItem.__init__(self,parent)
		
		self.properties = properties
		self.fstab_record = fstab_record
		self.index = index
		
		if self.isSystem():
			self.setIcon(0,Qt.QIcon(Const.Icons_path + "warning.png"))
			
	def getIndex(self):
		return self.index
		
	def getSize(self):
		
		if self.properties.has_key("storage.size") or self.properties.has_key("volume.size"):
			# bits -> mb
			if self.properties.has_key("storage.size"):
				size = self.properties["storage.size"]/1048576
			else:
				size = self.properties["volume.size"]/1048576
			# If length of a number bigger then 4 characters
			if size/1000 != 0:
				# mb -> gb
				return str(size/1024) + "," + str(size%1024)[0] + " Gb"
			else:
				return str(size) + " Mb"
		else:
			return None
		
	def getType(self):
		
		if self.properties.has_key("storage.drive_type") and self.properties["storage.drive_type"] != '':
			return self.properties["storage.drive_type"]
		else:
			return None
		
	def getFileSystem(self):
		
		if self.properties.has_key("volume.fstype") and self.properties["volume.fstype"] != '':
			return self.properties["volume.fstype"]
		elif self.fstab_record != None:
			return self.fstab_record.file_system
		else:
			return None
	
	def getMountPoint(self):
		
		if self.fstab_record != None:
			return self.fstab_record.mount_point
		
		mount_point = None
		if self.properties.has_key("volume.mount_point") and self.properties["volume.mount_point"] != '':
			mount_point = self.properties["volume.mount_point"]
		elif self.properties.has_key("linux.fstab.mountpoint") and self.properties["linux.fstab.mountpoint"] != '':
			mount_point = self.properties["linux.fstab.mountpoint"]
		return mount_point
		
	def isSystem(self):
		
		for root_dir in Const.Root_dirs:
			if root_dir == self.getMountPoint() or self.getFileSystem() == "swap":
				return True
		return False
		
	def isMounted(self):
		
		if self.properties.has_key("volume.is_mounted") and self.properties["volume.is_mounted"] != '':
			if self.properties["volume.is_mounted"]:
				return True
			else:
				return False
		return None
		
	def getDeviceName(self):
		return self.properties["block.device"]
	
	def getDumpFlag(self):
		
		if self.fstab_record != None:
			if self.fstab_record.dump == "0":
				return "Off"
			return "On"
		return None
	
	def getFsck(self):
		
		if self.fstab_record != None:
			return self.fstab_record.fsck
		return None
		
	def getOptionsAsLine(self):
		
		if self.fstab_record != None:
			return self.fstab_record.options
		if self.properties.has_key("linux.fstab.options"):
			return self.properties["linux.fstab.options"]
		return None
	
	def getOptionsAsList(self):
		
		if self.getOptionsAsLine() == None:
			return []
		list = self.getOptionsAsLine().split(",")
		
		return list
	
	def isRemovable(self):
		if self.getType() == "cdrom" or self.getType() == "floppy":
			return True
		else:
			return False
		
	def isLogical(self):
		if self.parent() == None:
			return False
		return True