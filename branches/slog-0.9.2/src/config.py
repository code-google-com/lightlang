# -*- mode: python; coding: utf-8; -*-

import os, sys
import ConfigParser
import gtk.gdk as gdk

# Implementation Singleton pattern
class SlogConf:

	class __impl:

		def __init__(self):
			self.width = 584;
			self.height = 412;
			self.left = 0;
			self.top = 0;
			self.paned = 240;
			self.used_dicts_list = ""
			self.spy_dicts_param = ""
			self.enabled_plugins = "LightLang SL:Google Translate"
			self.sl_dicts_dir = "/usr/share/sl/dicts"
			self.google_target = 6
			self.engine = 0
			self.tray_exit = 0
			self.tray_info = 1
			self.tray_start = 0
			self.spy_auto = 0
			self.mod_key = 0

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
			if conf.has_option("window", "paned"):
				self.paned = conf.getint("window", "paned")
			if conf.has_option("window", "tray_exit"):
				self.tray_exit = conf.getint("window", "tray_exit")
			if conf.has_option("window", "tray_info"):
				self.tray_info = conf.getint("window", "tray_info")
			if conf.has_option("window", "tray_start"):
				self.tray_start = conf.getint("window", "tray_start")
			if conf.has_option("spy", "auto"):
				self.spy_auto = conf.getint("spy", "auto")
			if conf.has_option("spy", "mod_key"):
				self.mod_key = conf.getint("spy", "mod_key")
			if conf.has_option("sl", "dicts_dir"):
				self.sl_dicts_dir = conf.get("sl", "dicts_dir")
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
			conf.set("window", "paned", self.paned)
			conf.set("window", "tray_exit", self.tray_exit)
			conf.set("window", "tray_info", self.tray_info)
			conf.set("window", "tray_start", self.tray_start)
			conf.add_section("spy")
			conf.set("spy", "mod_key", self.mod_key)
			conf.set("spy", "auto", self.spy_auto)
			conf.add_section("sl")
			conf.set("sl", "dicts_dir", self.sl_dicts_dir)
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
			return self.used_dicts_list.split("|")

		def set_used_dicts(self, used_dicts):
			self.used_dicts_list = used_dicts

		def get_spy_dicts(self):
			return self.spy_dicts_param.split("|")

		def set_spy_dicts(self, spy_dicts):
			self.spy_dicts_param = spy_dicts

		def get_engine(self):
			return self.engine

		def set_engine(self, index):
			self.engine = index

		def get_mod_key(self):
			modkeys = {0:gdk.CONTROL_MASK, 1:gdk.MOD1_MASK,
						2:gdk.SHIFT_MASK, 3:gdk.MOD4_MASK,
						4:8191}
			return modkeys[self.mod_key]

		def get_enabled_plugins(self):
			return self.enabled_plugins.split(":")

		def get_dic_path(self, dic):
			return os.path.join(self.sl_dicts_dir, dic)

	__instance = __impl( )

	def __getattr__(self, attr):
		return getattr(self.__instance, attr)

	def __setattr__(self, attr, value):
		return setattr(self.__instance, attr, value)

