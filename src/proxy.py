# -*- mode: python; coding: utf-8; -*-

import urllib, urllib2

class Proxy(object):
	
	def __init__(self, conf):
		self.conf = conf

	def get_ftp_downloader(self):
		proxies = None
		proxy_url = self.conf.get_proxy_url()
		if proxy_url is not None:
			proxies = {"ftp" : proxy_url}
		downloader = urllib.FancyURLopener(proxies)
		return downloader

	def get_http_opener(self):
		proxy_url = self.conf.get_proxy_url()
		if proxy_url is not None:
			proxy_support = urllib2.ProxyHandler({"http" : proxy_url})
			opener = urllib2.build_opener(proxy_support, urllib2.HTTPHandler)
		else:
			opener = urllib2.build_opener(urllib2.HTTPHandler)

		return opener
