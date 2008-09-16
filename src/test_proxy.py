import unittest
import os
import urllib

from proxy import Proxy

REPO_URL = "ftp://etc.edu.ru/pub/soft/for_linux/lightlang/dicts/repodata/primary.xml"
REPO_FILE = "/tmp/primary.xml"

class ConfMock(object):
	def get_proxy_url(self):
		return "http://192.168.0.1:3128"

class TestProxy(unittest.TestCase):

	""" Unit test for Proxy """

	def setUp(self):
		conf = ConfMock()
		self.proxy = Proxy(conf)

	def tearDown(self):
		urllib.urlcleanup()

	def testFTP(self):
		downloader = self.proxy.get_ftp_downloader()
		downloader.retrieve(REPO_URL, REPO_FILE)
		self.assertEqual(os.path.isfile(REPO_FILE), True)
		
if __name__ == "__main__":
	unittest.main()
