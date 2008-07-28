# -*- mode: python; coding: utf-8; -*-

import gtk
import htmltextview

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

		self.htmlview = htmltextview.HtmlTextView()
		self.htmlview.set_wrap_mode(gtk.WRAP_WORD)

		self.htmlview.set_border_width(1)
		self.htmlview.set_accepts_tab(True)
		self.htmlview.set_editable(False)
		self.htmlview.set_cursor_visible(False)
		self.htmlview.set_wrap_mode(gtk.WRAP_WORD_CHAR)
		self.htmlview.set_left_margin(2)
		self.htmlview.set_right_margin(2)

		self.clear()

		self.add(self.htmlview)
		self.htmlview.show()

	def __clear_htmlview(self):
		textbuffer = self.htmlview.get_buffer()
		start, end = textbuffer.get_bounds()
		textbuffer.delete(start, end)

	def get_label():
		return self.label

	def set_translate(self, word, translate):
		if word == "":
			self.clear()
			return

		self.label.set_text(word)
		self.__clear_htmlview()
		self.htmlview.display_html(translate)

	def clear(self):
		self.label.set_text(_("Welcome"))
		self.__clear_htmlview()

		bg = self.label.get_style().base[gtk.STATE_SELECTED]
		fg = self.label.get_style().base[gtk.STATE_NORMAL]
		bg_hex = self.color_to_hex(bg)
		fg_hex = self.color_to_hex(fg)
		p = "<p style='background-color: %s; font-size: 200%%; text-align: center'>" % (bg_hex)

		self.htmlview.display_html(
			"<body><br/>" + p +
			"Welcome to the SLog - the part of LightLang, the system of electronic dictionaries</p>" +
			"</body>"
		)

	def color_to_hex(self, color):

		r = color.red / 256
		g = color.green / 256
		b = color.blue / 256

		rgb = r << 16 | g << 8 | b
		rgb_hex = str(hex(rgb))[2:]

		return "#%s" % (rgb_hex.zfill(6))

