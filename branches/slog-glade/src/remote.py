# -*- mode: python; coding: utf-8; -*-

import dbus
import dbus.service, dbus.mainloop.glib

class Remote:
	def __init__(self):
		bus = dbus.SessionBus()
		slog_obj = bus.get_object("org.LightLang.SLog", "/SLog")
		self.iface = dbus.Interface(slog_obj, "org.LightLang.SLogInterface")
	
	def __spy_toggle(self):
		self.iface.spy_toggle()
	
	def __window_toggle(self):
		self.iface.toggle()

	def __show(self):
		self.iface.show()

	def execute(self, cmd):
		if cmd == "toggle":
			self.__window_toggle()
		elif cmd == "spy-toggle":
			self.__spy_toggle()
		elif cmd == "show":
			self.__show()

class SLogDBus(dbus.service.Object):
	def __init__(self, interface, obj_path = "/SLog"):
		self.interface = interface
		bus = dbus.SessionBus()
		bus_name = dbus.service.BusName("org.LightLang.SLog", bus)
		dbus.service.Object.__init__(self, bus_name, obj_path)

	@dbus.service.method("org.LightLang.SLogInterface")
	def spy_toggle(self):
		self.interface.spy_action.activate()

	@dbus.service.method("org.LightLang.SLogInterface")
	def toggle(self):
		self.interface.window_toggle()

	@dbus.service.method("org.LightLang.SLogInterface")
	def show(self):
		self.interface.hide()
		self.interface.app_show()

