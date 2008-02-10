##########################################
###### File with constant values #########
##########################################
from PyQt4 import Qt
import Config

Version = "0.1.3"
Program_name = "MountManager"
Organization = "Vialinx"
Fstab_path = "/etc/fstab"
Program_path = "/lib/mountmanager"
Icons_path =  "icons/"
Doc_path = Qt.QDir.currentPath() + "/Doc"
Site = "http://lightlang.org.ru"

Root_dirs = \
[
	"/bin", \
	"/boot", \
	"/dev", \
	"/", \
	"/etc", \
	"/home", \
	"/tmp",  \
	"/media", \
	"/lib", \
	"/mnt", \
	"/initrd",\
	"/initrd.img",\
	"/lib", \
	"/lost+found",\
	"/opt",\
	"/proc",\
	"/root",\
	"/sbin",\
	"/srv",\
	"/sys",\
	"/usr",\
	"/var"
]

Supported_file_systems = \
[
	"ext3",\
	"ext2",\
	"ntfs",\
	"vfat",\
	"reiserfs",\
	"iso9660",\
	"swap"
]