# -*- mode: python; coding: utf-8; -*-

import dbus

class Remote:
	def __init__(self):
		bus = dbus.SessionBus()
		slog_obj = bus.get_object("org.LightLang.SLog", "/SLog")
		self.slog_iface = dbus.Interface(slog_obj, "org.LightLang.SLogInterface")
	
	def __spy_toggle(self):
		self.slog_iface.dbus_spy_toggle()
	
	def __window_toggle(self):
		self.slog_iface.toggle()

	def __show(self):
		self.slog_iface.show()

	def execute(self, cmd):
		if cmd == "toggle":
			self.__window_toggle()
		elif cmd == "spy-toggle":
			self.__spy_toggle()
		elif cmd == "show":
			self.__show()
