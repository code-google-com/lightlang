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
			self.enabled_plugins = "LightLang SL:Google Translate"
			self.engine = 0
			self.tray_exit = 0
			self.tray_info = 1
			self.tray_start = 0
			self.spy_auto = 0
			self.mod_key = 0
			self.proxy = 0
			self.proxy_host = ""
			self.proxy_port = 0

			self.sl_dicts = []
			self.sl_dicts_dir = "/usr/share/sl/dicts"

			self.google_target = 6
			self.google_targets = []

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
			if conf.has_option("plugins", "enabled"):
				self.enabled_plugins = conf.get("plugins", "enabled")
			if conf.has_option("network", "proxy"):
				self.proxy = conf.getint("network", "proxy")
			if conf.has_option("network", "proxy_host"):
				self.proxy_host = conf.get("network", "proxy_host")
			if conf.has_option("network", "proxy_port"):
				self.proxy_port = conf.getint("network", "proxy_port")

			if conf.has_option("google", "current"):
				self.google_target = conf.getint("google", "current")

			if conf.has_option("google", "targets"):
				v = conf.get("google", "targets")
				try:
					self.google_targets = eval(v)
				except:
					print "Warning: Wron Google targets format"
					pass

			if conf.has_option("sl", "dicts_dir"):
				self.sl_dicts_dir = conf.get("sl", "dicts_dir")

			if conf.has_section("sl_dicts"):
				for opt in conf.options("sl_dicts"):
					v = conf.get("sl_dicts", opt)
					try:
						t = eval(v)
					except:
						pass
					else:
						self.sl_dicts.append(t)

			# Try import used dict list from XSL configuration
			#if self.used_dicts_list == "":
			#	xsl_conf_file = os.path.join(os.path.expanduser("~"), ".config/LightLang/XSL.conf")
			#	if os.path.isfile(xsl_conf_file):
			#		ini = ConfigParser.ConfigParser()
			#		ini.read(xsl_conf_file)
			#		raw_used_dicts_list = ini.get("dicts_manager", "used_dicts_list")
			#		self.used_dicts_list = raw_used_dicts_list.replace(", ", "|")

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
			conf.add_section("plugins")
			conf.set("plugins", "enabled", self.enabled_plugins)
			conf.add_section("network")
			conf.set("network", "proxy", self.proxy)
			conf.set("network", "proxy_host", self.proxy_host)
			conf.set("network", "proxy_port", self.proxy_port)

			conf.add_section("google")
			conf.set("google", "current", self.google_target)
			conf.set("google", "targets", self.google_targets)

			conf.add_section("sl")
			conf.set("sl", "dicts_dir", self.sl_dicts_dir)

			conf.add_section("sl_dicts")
			i = 1
			for rec in self.sl_dicts:
				o = "d%0.3d" % i
				conf.set("sl_dicts", o, rec)
				i += 1

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

		def get_sl_used_dicts(self):
			isused = lambda x: x[1] == True or False
			d_list = filter(isused, self.sl_dicts)
			c_list = [r[0] for r in d_list]
			return c_list

		def get_sl_spy_dicts(self):
			isspy = lambda x: x[2] == True or False
			d_list = filter(isspy, self.sl_dicts)
			c_list = [r[0] for r in d_list]
			return c_list

		def get_sl_dict_state(self, fname):
			used = False
			spy = False
			c_list = [r[0] for r in self.sl_dicts]
			if fname in c_list:
				idx = c_list.index(fname)
				rec = self.sl_dicts[idx]
				used, spy = rec[1], rec[2]
			return used, spy

		def set_sl_dict_state(self, fname, used, spy):
			c_list = [r[0] for r in self.sl_dicts]
			if fname in c_list:
				idx = c_list.index(fname)
				rec = self.sl_dicts[idx]
				if used == False and spy == False:
					self.sl_dicts.remove(rec)
				else:
					rec[1], rec[2] = used, spy
			else:
				if used == False and spy == False:
					pass
				else:
					rec = [fname, used, spy]
					self.sl_dicts.append(rec)

		def get_google_targets(self):
			targets = []
			for s in self.google_targets:
				fr, to = s.split(":")
				targets.append((fr, to))
			return targets

		def set_google_defaults(self):
			self.google_targets = ["en:ru", "ru:en"]

		def del_google_target(self, src, dst):
			self.google_targets.remove(src+":"+dst)

	__instance = __impl( )

	def __getattr__(self, attr):
		return getattr(self.__instance, attr)

	def __setattr__(self, attr, value):
		return setattr(self.__instance, attr, value)

