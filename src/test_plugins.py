import unittest

from plugins import PluginManager

class TestPluginManager(unittest.TestCase):

	""" Unit test for PluginManager """

	def setUp(self):
		self.manager = PluginManager()
		self.manager.add_plugin_dir("/tmp/slog/share/slog/plugins")

	def testSearchPlugins(self):
		self.manager.scan_for_plugins()
		self.assertEqual(3, len(self.manager.get_available()))
		
if __name__ == "__main__":
	unittest.main()
