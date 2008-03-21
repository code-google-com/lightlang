# -*- mode: python; coding: utf-8; -*-

import gtk
import gtkhtml2

class TransView(gtk.ScrolledWindow):

	def __init__(self, label=None):
		gtk.ScrolledWindow.__init__(self)
		self.set_border_width(4)

		if label == None:
			self.label = gtk.Label()
		else:
			self.label = label

		self.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
		self.set_shadow_type(gtk.SHADOW_IN)

		self.document = gtkhtml2.Document()
		self.clear()

		textview = gtkhtml2.View()
		textview.set_document(self.document)
		self.add(textview)
		textview.show()

	def get_label():
		return self.label

	def set_translate(self, word, translate):
		if word == "":
			self.clear()
			return

		self.label.set_text(word)

		self.document.clear()
		self.document.open_stream("text/html")
		self.document.write_stream(translate)
		self.document.close_stream()

	def clear(self):
		self.label.set_text(_("Welcome"))
		self.document.clear()
		self.document.open_stream("text/html")
		self.document.write_stream("<html><body><br><br><hr>" \
			"<table border=\"0\" width=\"100%\"><tr><td bgcolor=\"#DFEDFF\"><h2 align=\"center\"><em>" \
			"Welcome to the LightLang - the system of electronic dictionaries</em></h2></td></tr></table>" \
			"<hr>")

		self.document.close_stream()

