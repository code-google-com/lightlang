# -*- mode: python; coding: utf-8; -*-

import urllib, urllib2

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

#TODO: Remove from here
from slog.config import SlogConf

class GoogleEngine(object):

	def __init__(self):

		self.languages = {LANG_ARABIC:_("Arabic"), LANG_CHINESE:_("Chinese"), LANG_ENGLISH:_("English"),
						LANG_FRENCH:_("French"), LANG_GERMAN:_("German"), LANG_ITALIAN:_("Italian"),
						LANG_JAPANESE:_("Japanese"), LANG_KOREAN:_("Korean"), LANG_PORTUGESE:_("Portugese"),
						LANG_RUSSIAN:_("Russian"), LANG_SPANISH:_("Spanish")}

		# TODO: Remove
		self.targets = ((LANG_ENGLISH, LANG_ARABIC), (LANG_ENGLISH, LANG_ITALIAN), (LANG_ENGLISH, LANG_CHINESE),
					(LANG_ENGLISH, LANG_KOREAN), (LANG_ENGLISH, LANG_GERMAN), (LANG_ENGLISH, LANG_PORTUGESE),
					(LANG_ENGLISH, LANG_RUSSIAN), (LANG_ENGLISH, LANG_FRENCH), (LANG_ENGLISH, LANG_JAPANESE),
					(LANG_ENGLISH, LANG_SPANISH), (LANG_ARABIC, LANG_ENGLISH), (LANG_SPANISH, LANG_ENGLISH),
					(LANG_ITALIAN, LANG_ENGLISH), (LANG_CHINESE, LANG_ENGLISH), (LANG_KOREAN, LANG_ENGLISH),
					(LANG_GERMAN, LANG_ENGLISH), (LANG_GERMAN, LANG_FRENCH), (LANG_PORTUGESE, LANG_ENGLISH),
					(LANG_RUSSIAN, LANG_ENGLISH), (LANG_FRENCH, LANG_ENGLISH), (LANG_FRENCH, LANG_GERMAN),
					(LANG_JAPANESE, LANG_ENGLISH))

	def get_targets(self):
		""" Возвращает список строк, направлений перевода.		
		"""
		res = []
		for target in self.targets:
			target_str = self.languages[target[0]] + " - " + self.languages[target[1]]
			res.append(target_str)
		return res

	def get_langs(self):
		return self.languages

	def translate(self, src, dst, text):
		import socket
		socket.setdefaulttimeout(10)

		conf = SlogConf()
		if conf.proxy != 0 and conf.proxy_host != "" and conf.proxy_port != 0:
			proxy_url = "http://%s:%s" % (conf.proxy_host, conf.proxy_port)
			proxy_support = urllib2.ProxyHandler({"http" : proxy_url})
			opener = urllib2.build_opener(proxy_support, urllib2.HTTPHandler)
		else:
			opener = urllib2.build_opener(urllib2.HTTPHandler)

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

