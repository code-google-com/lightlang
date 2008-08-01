# -*- mode: python; coding: utf-8; -*-

import urllib

LANG_ARABIC = "ar"
LANG_CHINESE = "zh"
LANG_ENGLISH = "en"
LANG_FRENCH = "fr"
LANG_GERMAN = "de"
LANG_ITALIAN = "it"
LANG_JAPANESE = "ja"
LANG_KOREAN = "ko"
LANG_PORTUGESE = "pt"
LANG_RUSSIAN = "ru"
LANG_SPANISH = "es"

class GoogleEngine(object):

	def __init__(self, proxy):

		self.languages = {LANG_ARABIC:_("Arabic"), LANG_CHINESE:_("Chinese"), LANG_ENGLISH:_("English"),
						LANG_FRENCH:_("French"), LANG_GERMAN:_("German"), LANG_ITALIAN:_("Italian"),
						LANG_JAPANESE:_("Japanese"), LANG_KOREAN:_("Korean"), LANG_PORTUGESE:_("Portugese"),
						LANG_RUSSIAN:_("Russian"), LANG_SPANISH:_("Spanish")}

		self.proxy = proxy

	def translate(self, src, dst, text):
		import socket
		socket.setdefaulttimeout(10)

		opener = self.proxy.get_http_opener()

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

