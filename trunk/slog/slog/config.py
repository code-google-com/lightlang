# -*- mode: python; coding: utf-8; -*-

import os, sys
import ConfigParser
import gtk.gdk as gdk

SL_PREFIX = sys.prefix

# Implementation Singleton pattern
class SlogConf:

	class __impl:

		def __init__(self):
			self.width = 584;
			self.height = 412;
			self.left = 0;
			self.top = 0;
			self.used_dicts_list = ""
			self.spy_dicts_param = ""
			self.enabled_plugins = "Google Translate:DICT Client"
			self.sl_prefix = SL_PREFIX
			self.google_target = 6
			self.engine = 0
			self.tray_exit = 0
			self.tray_info = 1
			self.tray_start = 0
			self.mod_key = 0
			self.prefix = sys.prefix

			self.__load()

		def __load(self):

			conf = ConfigParser.ConfigParser()
			if os.path.exists(os.path.expanduser("~/.config")) == False:
				os.mkdir(os.path.expanduser("~/.config"))
			if os.path.exists(os.path.expanduser("~/.config/slog")) == False:
				os.mkdir(os.path.expanduser("~/.config/slog"))
			if os.path.isfile(os.path.expanduser("~/.config/slog/slogrc")):
				conf.read(os.path.expanduser("~/.config/slog/slogrc"))

			if conf.has_option("window", "engine"):
				self.engine = conf.getint("window", "engine")
			if conf.has_option("window", "width"):
				self.width = conf.getint("window", "width")
			if conf.has_option("window", "height"):
				self.height = conf.getint("window", "height")
			if conf.has_option("window", "left"):
				self.left = conf.getint("window", "left")
			if conf.has_option("window", "top"):
				self.top = conf.getint("window", "top")
			if conf.has_option("window", "tray_exit"):
				self.tray_exit = conf.getint("window", "tray_exit")
			if conf.has_option("window", "tray_info"):
				self.tray_info = conf.getint("window", "tray_info")
			if conf.has_option("window", "mod_key"):
				self.mod_key = conf.getint("window", "mod_key")
			if conf.has_option("sl", "sl_prefix"):
				self.sl_prefix = conf.get("sl", "sl_prefix")
			if conf.has_option("sl", "used_dicts"):
				self.used_dicts_list = conf.get("sl", "used_dicts")
			if conf.has_option("sl", "spy_dicts"):
				self.spy_dicts_param = conf.get("sl", "spy_dicts")
			if conf.has_option("google", "target"):
				self.google_target = conf.getint("google", "target")
			if conf.has_option("plugins", "enabled"):
				self.enabled_plugins = conf.get("plugins", "enabled")

			# Try import used dict list from XSL configuration
			if self.used_dicts_list == "":
				xsl_conf_file = os.path.join(os.path.expanduser("~"), ".config/LightLang/XSL.conf")
				if os.path.isfile(xsl_conf_file):
					ini = ConfigParser.ConfigParser()
					ini.read(xsl_conf_file)
					raw_used_dicts_list = ini.get("dicts_manager", "used_dicts_list")
					self.used_dicts_list = raw_used_dicts_list.replace(", ", "|")

		def save(self):
			conf = ConfigParser.ConfigParser()
			conf.add_section("window")
			conf.set("window", "engine",  self.engine)
			conf.set("window", "width",  self.width)
			conf.set("window", "height", self.height)
			conf.set("window", "left",  self.left)
			conf.set("window", "top", self.top)
			conf.set("window", "tray_exit", self.tray_exit)
			conf.set("window", "tray_info", self.tray_info)
			conf.set("window", "mod_key", self.mod_key)
			conf.add_section("sl")
			conf.set("sl", "sl_prefix", self.sl_prefix)
			conf.set("sl", "used_dicts", self.used_dicts_list)
			conf.set("sl", "spy_dicts", self.spy_dicts_param)
			conf.add_section("google")
			conf.set("google", "target", self.google_target)
			conf.add_section("plugins")
			conf.set("plugins", "enabled", self.enabled_plugins)

			conf.write(file(os.path.expanduser("~/.config/slog/slogrc"), "w"))

		def get_size(self):
			return self.width, self.height

		def set_size(self, width, height):
			self.width = width
			self.height = height

		def get_pos(self):
			return self.left, self.top

		def set_pos(self, left, top):
			self.left = left
			self.top = top

		def get_used_dicts(self):
			return self.used_dicts_list

		def set_used_dicts(self, used_dicts):
			self.used_dicts_list = used_dicts

		def get_spy_dicts(self):
			return self.spy_dicts_param

		def set_spy_dicts(self, spy_dicts):
			self.spy_dicts_param = spy_dicts

		def get_sl_prefix(self):
			return self.sl_prefix

		def get_sl_exec(self):
			return os.path.join(self.sl_prefix, "bin/sl")

		def get_sl_dicts_dir(self):
			return os.path.join(self.sl_prefix, "share/sl/dicts")

		def get_engine(self):
			return self.engine

		def set_engine(self, index):
			self.engine = index

		def get_mod_key(self):
			modkeys = {0:gdk.CONTROL_MASK, 1:gdk.MOD1_MASK,
						2:gdk.SHIFT_MASK, 3:gdk.MOD4_MASK,
						4:0}
			return modkeys[self.mod_key]

		def get_pixmap_dir(self):
			return os.path.join(self.prefix, "share", "pixmaps")

		def get_data_dir(self):
			return os.path.join(self.prefix, "share", "slog")

		def get_enabled_plugins(self):
			return self.enabled_plugins.split(":")

	__instance = __impl( )

	def __getattr__(self, attr):
		return getattr(self.__instance, attr)

	def __setattr__(self, attr, value):
		return setattr(self.__instance, attr, value)

