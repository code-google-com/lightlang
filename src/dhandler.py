# -*- mode: python; coding: utf-8; -*-

from xml.sax.handler import ContentHandler

class DictHandler(ContentHandler):
	def __init__(self):
		self.accumulator = ""
		self.d_list = {}

	def startElement(self, name, attrs):
		if name == "dictionary":
			self.filename = attrs.get("file", "")

	def endElement(self, name):
		self.accumulator = self.accumulator.strip("\n\t")
		if name == "dictionary":
			self.d_list[self.filename] = (self.name, self.target, self.size)
		elif name == "name":
			self.name = self.accumulator
		elif name == "target":
			self.target = self.accumulator
		elif name == "size":
			self.size = self.accumulator
		self.accumulator = ""

	def characters(self, ch):
		self.accumulator += ch

	def get_result(self):
		return self.d_list
