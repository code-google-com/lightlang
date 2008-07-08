# -*- mode: python; coding: utf-8; -*-

import gtk, gobject
import urllib, urllib2
import threading

from slog.config import SlogConf
import slog.gui_helper as ghlp

plugin_name = "Google Translate"
plugin_version = "0.1.1"
plugin_author = "Nasyrov Renat <renatn@gmail.com>"
plugin_description = _("Client for Google Translate")

def enable():
	return GoogleView()

def slog_init(plugin_path):
	global path
	path = plugin_path

LANG_ARABIC = "ar";
LANG_CHINESE = "zh";
LANG_ENGLISH = "en";
LANG_FRENCH = "fr";
LANG_GERMAN = "de";
LANG_ITALIAN = "it";
LANG_JAPANESE = "ja";
LANG_KOREAN = "ko";
LANG_PORTUGESE = "pt";
LANG_RUSSIAN = "ru";
LANG_SPANISH = "es";

class GoogleEngine:

	def __init__(self):

		self.languages = {LANG_ARABIC:_("Arabic"), LANG_CHINESE:_("Chinese"), LANG_ENGLISH:_("English"),
						LANG_FRENCH:_("French"), LANG_GERMAN:_("German"), LANG_ITALIAN:_("Italian"),
						LANG_JAPANESE:_("Japanese"), LANG_KOREAN:_("Korean"), LANG_PORTUGESE:_("Portugese"),
						LANG_RUSSIAN:_("Russian"), LANG_SPANISH:_("Spanish")}

		self.targets = ((LANG_ENGLISH, LANG_ARABIC), (LANG_ENGLISH, LANG_ITALIAN), (LANG_ENGLISH, LANG_CHINESE),
					(LANG_ENGLISH, LANG_KOREAN), (LANG_ENGLISH, LANG_GERMAN), (LANG_ENGLISH, LANG_PORTUGESE),
					(LANG_ENGLISH, LANG_RUSSIAN), (LANG_ENGLISH, LANG_FRENCH), (LANG_ENGLISH, LANG_JAPANESE),
					(LANG_ENGLISH, LANG_SPANISH), (LANG_ARABIC, LANG_ENGLISH), (LANG_SPANISH, LANG_ENGLISH),
					(LANG_ITALIAN, LANG_ENGLISH), (LANG_CHINESE, LANG_ENGLISH), (LANG_KOREAN, LANG_ENGLISH),
					(LANG_GERMAN, LANG_ENGLISH), (LANG_GERMAN, LANG_FRENCH), (LANG_PORTUGESE, LANG_ENGLISH),
					(LANG_RUSSIAN, LANG_ENGLISH), (LANG_FRENCH, LANG_ENGLISH), (LANG_FRENCH, LANG_GERMAN),
					(LANG_JAPANESE, LANG_ENGLISH))

	def get_targets(self):
		res = []
		for target in self.targets:
			target_str = self.languages[target[0]] + " - " + self.languages[target[1]]
			res.append(target_str)
		return res

	def translate(self, target, text):
		import socket
		socket.setdefaulttimeout(5)

		conf = SlogConf()
		if conf.proxy != 0 and conf.proxy_host != "" and conf.proxy_port != 0:
			proxy_url = "http://%s:%s" % (conf.proxy_host, conf.proxy_port)
			proxy_support = urllib2.ProxyHandler({"http" : proxy_url})
			opener = urllib2.build_opener(proxy_support, urllib2.HTTPHandler)
		else:
			opener = urllib2.build_opener(urllib2.HTTPHandler)

		src, dst = self.targets[target]
		pair = src + "|" + dst

		params = urllib.urlencode({'langpair': pair, 'text': text.encode("utf8")})
		opener.addheaders = [('User-agent', 'Mozilla/5.0')]
		f = opener.open("http://translate.google.com/translate_t?%s" % params)

		response = str(f.read())
		result_box = response.find("<div id=result_box dir=")
		if result_box == -1:
			return "Bad answer from Google"

		target = response[result_box:]
		end = target.find("</div>")

		translate = "<body><p>" + target[29:end] + "</p></body>"

		return translate

class GoogleView(gtk.VBox):
	def __init__(self):
		gtk.VBox.__init__(self, False, 0)

		self.callbacks = {}
		self.google = GoogleEngine()
		self.conf = SlogConf()

		tooltips = gtk.Tooltips()
		hbox = gtk.HBox(False, 4)
		hbox.set_border_width(4)
		self.pack_start(hbox, False, False, 0)

		self.cmb_target = gtk.combo_box_new_text()

		for target in self.google.get_targets():
			self.cmb_target.append_text(target)
		self.cmb_target.set_active(self.conf.google_target)

		hbox.pack_start(self.cmb_target, True, True, 0)

		btn_clear = ghlp.create_speed_button(gtk.STOCK_CLEAR)
		btn_clear.connect("clicked", self.on_btn_clear_clicked)
		hbox.pack_start(btn_clear, False, False, 0)

		sw = gtk.ScrolledWindow()
		sw.set_border_width(4)
		sw.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
		sw.set_shadow_type(gtk.SHADOW_IN)
		self.pack_start(sw, True, True, 0)

		self.textview = gtk.TextView()
		self.textview.set_wrap_mode(gtk.WRAP_WORD)
		sw.add(self.textview)

		btn_translate = gtk.Button(_("Translate"))
		btn_translate.set_border_width(4)
		btn_translate.connect("clicked", self.on_translate_clicked)
		self.pack_start(btn_translate, False, True, 0)

	def __fire_translate_changed(self, translate):
		callback = self.callbacks["translate_it"]
		if callback is not None:
			callback("Google", translate)

	def __fire_status_changed(self, message, needClear=False):
		callback = self.callbacks["changed"]
		if callback is not None:
			gobject.idle_add(callback, message)
			if needClear:
				gobject.timeout_add(5000, self.__fire_status_changed, "")

	# Thread function
	def request_google(self, target, text):
		try:
			translate = self.google.translate(target, text)
		except urllib2.URLError, err:
			msg = "Google error: %s" % err
			print msg
			self.__fire_status_changed(msg, True)
		else:
			self.__fire_translate_changed(translate)
			self.__fire_status_changed("Done", True)
		finally:
			ghlp.change_cursor(None)

	def on_translate_clicked(self, widget, data=None):

		target = self.cmb_target.get_active()

		textbuffer = self.textview.get_buffer()
		start, end = textbuffer.get_bounds()
		text = textbuffer.get_text(start, end)

		if  len(text) == 0:
			ghlp.show_error(None, _("Empty text"))
			return

		#TODO: Move to on_combobox_changed()
		self.conf.google_target = self.cmb_target.get_active()

		ghlp.change_cursor(gtk.gdk.Cursor(gtk.gdk.WATCH))
		self.__fire_status_changed("Send request...")

		thread = threading.Thread(target = self.request_google, args = (target, text))
		thread.start()

	def on_btn_clear_clicked(self, widget, data=None):
		textbuffer = self.textview.get_buffer()
		start, end = textbuffer.get_bounds()
		textbuffer.delete(start, end)
		self.__fire_status_changed("")

	def connect(self, event, callback):
		self.callbacks[event] = callback

	def configure(self, window):
		ghlp.show_error(window, "Under construction!")

