from PyQt4 import Qt
import TreeWidget
import DeviceItem
import dbus
import FstabFile
import Documentation

class InfoCenter:
	def __init__(self):
		
		self.documentation_center = Documentation.DocumentationCenter()
		
		self.physical_disks = []
		self.logical_disks = []
		self.tree_widget = TreeWidget.TreeWidget()
		
	def refreshInformation(self):
		
		self.fstab_parser = FstabFile.FstabParser()
		self.fstab_records = self.fstab_parser.getFstabRecords()
		
		self.physical_disks = []
		self.logical_disks = []
		self.tree_widget_items = []
		
		# Tune d-bus
		self.bus = dbus.SystemBus()
		self.log = "Dbus was activated\n"
		self.hal_object = self.bus.get_object("org.freedesktop.Hal", "/org/freedesktop/Hal/Manager")
		self.hal_interface = dbus.Interface(self.hal_object,"org.freedesktop.Hal.Manager")
		
		# Check all devices of user and choose only storage devices	
		for device in self.hal_interface.GetAllDevices():
			obj = self.bus.get_object("org.freedesktop.Hal",device)
			# Get properties of a device
			properties = obj.GetAllProperties(dbus_interface="org.freedesktop.Hal.Device")
			# If it isn't a storage device or there are no info about it, skip this device
			if not properties.has_key("info.category") or not properties.has_key("block.device"):
				continue
			if properties["info.category"] != "storage" and properties["info.category"] != "volume":
				continue
			
			self.log += "Was found storage device: " + properties["block.device"] + "-" + properties["info.category"] + "\n"
			
			if properties["info.category"] == "storage":
				self.physical_disks.append(properties)
			elif properties["info.category"] == "volume":
				# If there is no info about parent report about it
				if not properties.has_key("info.parent"):
					self.log += "Warning: " + "There is logical disk without parent - " + properties["block.device"] + "\n"
					print "There is logical disk without parent: ",properties["block.device"]
					continue
				# If there is no info about file system report about it
				if not properties.has_key("volume.fstype") or properties["volume.fstype"] == '':
					self.log += "Warning: " + "There is logical disk with unknown file system - " + properties["block.device"] + "\n"
					print "There is logical disk with unknown file system: ",properties["block.device"]
					continue
				self.logical_disks.append(properties)
		
		self.physical_disks.reverse()
		self.logical_disks.reverse()
		
		self.log += "="*15 + "Define partitions of disks" + "="*15 + "\n"
		# Run all devices and add them	
		for physical_disk in self.physical_disks:
			fstab = None
			for fstab_record in self.fstab_records:
				if physical_disk["block.device"] == fstab_record.device_name:
					fstab = fstab_record
					break
				elif physical_disk.has_key("volume.uuid"):
					if "UUID=" + physical_disk["volume.uuid"] == fstab_record.device_name:
						fstab = fstab_record
						break
				elif physical_disk.has_key("volume.label"):
					if "LABEL=" + physical_disk["volume.label"] == fstab_record.device_name:
						fstab = fstab_record
						break
			physical_disk_item = DeviceItem.DeviceItem(physical_disk,fstab,len(self.tree_widget_items),self.tree_widget)
			physical_disk_item.setText(0,Qt.QString(physical_disk["block.device"]).replace("/dev/",""))
			physical_disk_item.setText(1,physical_disk_item.getSize())
			self.tree_widget_items.append(physical_disk_item)
			
			# Search partitions of physical disk
			for logical_disk in self.logical_disks:
				self.log += "Physical disk: " + physical_disk["info.parent"] + " | Logical disk: " + logical_disk["info.udi"] + "\n"
				if logical_disk["info.parent"] == physical_disk["info.udi"]:
					fstab = None
					for fstab_record in self.fstab_records:
						if logical_disk["block.device"] == fstab_record.device_name:
							fstab = fstab_record
							break
						elif logical_disk.has_key("volume.uuid"):
							if "UUID=" + logical_disk["volume.uuid"] == fstab_record.device_name:
								fstab = fstab_record
								break
						elif logical_disk.has_key("volume.label"):
							if "LABEL=" + logical_disk["volume.label"] == fstab_record.device_name:
								fstab = fstab_record
								break
					logical_disk_item = DeviceItem.DeviceItem(logical_disk,fstab,len(self.tree_widget_items),physical_disk_item)
					logical_disk_item.setText(0,Qt.QString(logical_disk["block.device"]).replace("/dev/",""))
					logical_disk_item.setText(1,logical_disk_item.getSize())
					self.tree_widget_items.append(logical_disk_item)
					
	def getAllLogicalDisks(self):
		
		return self.logical_disks
	
	def getAllPhysicalDisks(self):
		
		return self.physical_disks
	
	def treeWidget(self):
		return self.tree_widget
		
	def treeWidgetItems(self):
		return self.tree_widget_items
	
	def getDocCenter(self):
		return self.documentation_center
		
		
		