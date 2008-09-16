# -*- mode: python; coding: utf-8; -*-

import re
import gtk, gobject
import htmltextview

def get_style_colors(widget):
	""" Возвращает кортеж из двух строк
	"""
	style = widget.get_style()
	bg = color_to_hex(style.bg[gtk.STATE_ACTIVE])
	fg = color_to_hex(style.text[gtk.STATE_NORMAL])
	return (bg, fg)

def color_to_hex(color):
	""" Конвертирует объект color класса gtk.gdk.Color
		в строку содержащую, шестнадцеричное значение цвета
		формата RGB
	"""
	r = color.red / 256
	g = color.green / 256
	b = color.blue / 256

	rgb = r << 16 | g << 8 | b
	rgb_hex = str(hex(rgb))[2:]
	return "#%s" % (rgb_hex.zfill(6))

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

		self.add(self.htmlview)
		self.htmlview.show()

		self.clear()

	def replace_colors(self, html):
		(bg, fg) = get_style_colors(self.htmlview)
		bg_to = "background-color: %s;" % bg
		fg_to = " color: %s;" % fg

		bg_re = re.compile("background-color: #\w{6};")
		fg_re = re.compile("[^-]color: #\w{6};")

		retval = bg_re.sub(bg_to, html)
		retval = fg_re.sub(fg_to, retval)

		return retval

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

		#doc = translate
		doc = self.replace_colors(translate)

		self.htmlview.display_html(doc)

	def __show_welcome(self):
		h = """<body><br/>
			<p style='background-color: #000000; color: #ffffff; font-size: 200%; text-align: center'>
			Welcome to the SLog - the part of LightLang, the system of electronic dictionaries</p>
			</body>"""
		r = self.replace_colors(h)
		self.htmlview.display_html(r)

	def clear(self):
		self.label.set_text(_("Welcome"))
		self.__clear_htmlview()
		gobject.idle_add(self.__show_welcome)


