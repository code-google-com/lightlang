# -*- mode: python; coding: utf-8; -*-

import sys
import gtk
import string
import socket

from slog.config import SlogConf
import slog.gui_helper as ghlp

plugin_name = "DICT Client"
plugin_version = "0.1"
plugin_author = "Nasyrov Renat <renatn@gmail.com>"
plugin_description = _("Client for a dictionary server protocol (DICT)")
plugin_configurable = False

def enable():
	return DCView()

class DictClient:
	def __init__(self):
		self.verbose = 1
		self.is_connected = False

	def dial(self):
		host = "127.0.0.1"
		port = 2628

		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.connect((host, port))

		self.f = self.sock.makefile("r")

		welcome = self.f.readline()
		if welcome[0:4] != '220 ':
			raise Exception("server doesn't want you (%s)" % welcome[0:4])
		r, _ = self._cmd('CLIENT slog, 0.9.2')
		if r != '250':
			raise Exception('sending client string failed')

		self.is_connected = True

	def debug(self, s):
		if self.verbose:
			print >>sys.stderr, s

	def validword(self, s):
		bad = [chr(i) for i in range(20)]
		if s == '':
			return 0
		for c in s:
			if c in bad:
				return 0
		return 1

	def getdbs(self):
		r, line = self._cmd('SHOW DB')
		if r != '110':
			raise Exception('show db failed (%s)' % line)

		return [tuple(string.split(line, ' ', 1)) for line in self._readlist()]

	def getstrats(self):
		r, line = self._cmd('SHOW STRAT')
		if r != '111':
			raise Exception('show strat failed (%s)' % line)

		return [tuple(string.split(line, ' ', 1)) for line in self._readlist()]

	def getserverinfo(self):
		r, line = self._cmd('SHOW SERVER')
		if r != '114':
			raise Exception('show server failed (%s)' % line)
		return '\n'.join(self._readlist())

	def getdbinfo(self, db):
		if not self.validword(db):
			raise Exception('invalid database: "%s"' % db)
		r, line = self._cmd('SHOW INFO %s' % self.quote(db))
		if r != '112':
			raise Exception('show info failed (%s)' % line)
		return '\n'.join(self._readlist())

	def match(self, word, db='!', strat='.'):
		if not self.is_connected:
			self.dial()

		for key, value in [('word', word), ('database', db), ('strategy', strat)]:
			if not self.validword(value):
				raise Exception('invalid %s: "%s"' % (key, value))

		code, line = self._cmd('MATCH %s %s %s' % (self.quote(db), self.quote(strat), self.quote(word)))
		if code == "552":
			return []

		if code[0] in ['4', '5']:
			raise Exception('response to match: %s' % line)

		lines = [tuple(self.split(l, ' ', 1)) for l in self._readlist()]

		line = self._read()
		if line[0:4] != '250 ':
			raise Exception('expected code 250 after match (%s)' % line)

		return lines

	def definition(self, word, db='!'):
		for key, value in [('word', word), ('database', db)]:
			if not self.validword(value):
				raise Exception('invalid %s: "%s"' % (key, value))

		r, line = self._cmd('DEFINE %s %s' % (self.quote(db), self.quote(word)))
		if r == '552':
			return []
		if r[0] in ['4', '5']:
			raise Exception('response to define: %s' % line)

		defs = []
		while 1:
			line = self._read()
			if line[0:4] == "151 ":
				definition = self._readlist()
				defs.append((definition))
			else:
				break
		return defs

	def quote(self, word):
		if ' ' in word or "'" in word or '"' in word:
			return "'%s'" % string.replace(word, "'", "''")
		return word

	def split(self, line, delim, num):
		def unquote(l):
			if l[0] in ['"', "'"]:
				q = l[0]
				offset = 1
				while 1:
					offset = string.find(l[offset:], q)
					if offset == -1:
						raise Exception('Invalidly quoted line from server')

					if l[offset-1:offset+1] == (r'\%s' % q):
						offset += 1
					else:
						word = string.replace(l[1:offset+1], r'\%s' % q, q)
						l = string.lstrip(l[offset+2:])
						break
			else:
				word, l = string.split(l, delim, 1)
			return word, l

		r = []
		l = line
		while num != 0:
			word, l = unquote(l)
			r.append(word)
			num -= 1
		word, rest = unquote(l)
		r.append(word)

		return r

	def _readlist(self):
		lines = []
		while 1:
			line = self._read()
			if line == '.':
				break
			if line[0:2] == '..':
				line = line[1:]
			lines.append(line)
		return lines

	def _read(self):
		line = self.f.readline()
		if line[-1] == '\n':
			line = line[0:-1]
		if line[-1] == '\r':
			line = line[0:-1]
		self.debug('< %s' % line)
		return line

	def _cmd(self, cmd):
		self.sock.sendall(cmd + '\r\n')
		self.f.flush()
		self.debug('> %s' % cmd)

		line = self._read()

		code = line[0:3]
		return code, line


class DCView(gtk.VBox):
	def __init__(self):
		gtk.VBox.__init__(self, False, 0)

		self.callbacks = {}
		self.dclient = DictClient()

		tooltips = gtk.Tooltips()
		hbox = gtk.HBox(False, 0)
		hbox.set_border_width(4)
		self.pack_start(hbox, False, False, 0)

		self.word_entry = gtk.Entry()
		self.word_entry.connect("activate", self.on_word_entry_activate)
		hbox.pack_start(self.word_entry, True, True, 4)

		btn_clear = ghlp.create_speed_button(gtk.STOCK_CLEAR)
		tooltips.set_tip(btn_clear, _("Clear field"))
		btn_clear.connect("clicked", self.on_btn_clear_clicked)
		hbox.pack_start(btn_clear, False, False, 0)

		sw = gtk.ScrolledWindow()
		sw.set_border_width(4)

		sw.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
		sw.set_shadow_type(gtk.SHADOW_IN)
		self.pack_start(sw, True, True, 0)

		self.treestore = gtk.TreeStore(str)
		self.treeview = gtk.TreeView(self.treestore)
		self.treeview.set_headers_visible(False)
		self.treeview.set_rules_hint(True)
		sw.add(self.treeview)

		cell = gtk.CellRendererText()
		tvcolumn = gtk.TreeViewColumn("Result", cell, text=0)
		self.treeview.append_column(tvcolumn)

		self.treestore.append(None, [_("Enter the word, please...")])
		self.word_selection = self.treeview.get_selection()
		self.word_selection.connect("changed", self.on_wordlist_changed)

	def __fire_status_changed(self, message):
		callback = self.callbacks["changed"]
		if callback is not None:
			callback(message)

	def __fire_translate_changed(self, word, translate):
		callback = self.callbacks["translate_it"]
		if callback is not None:
			callback(word, translate)

	def on_btn_clear_clicked(self, widget, data=None):
		self.word_entry.set_text("")
		self.word_entry.grab_focus()
		self.treestore.clear()
		self.treestore.append(None, [_("Enter the word, please...")])
		self.__fire_status_changed("")

	def on_word_entry_activate(self, widget, data=None):
		word = widget.get_text().lower()
		lines = self.dclient.match(word)
		count = 0
		model = self.treestore
		model.clear()
		d_old = None
		for d, word in lines:
			if d != d_old:
				dir_entry = model.append(None, ["%s" % (d)])
				d_old = d
			model.append(dir_entry, [word])
			count += 1

		if count>0:
			self.treeview.expand_all()
			self.word_selection.select_path((0,0))
		else:
			model.append(None, [_("This word is not found")])

		self.__fire_status_changed(_("Total: %i") % (count))

	def on_wordlist_changed(self, selection):
		model, iter = selection.get_selected()
		if iter is None:
			return

		word = model.get_value(iter, 0)
		parent = self.treestore.iter_parent(iter)
		dictionary = model.get_value(parent, 0)

		defs = self.dclient.definition(word, db=dictionary)

		lines = defs[0]
		print "Lines:"
		print lines

		buf = ["<html><head><meta content=\"text/html; charset=UTF-8\" http-equiv=Content-Type></head><body><p>"]
		for line in lines:
			buf.append(line)
		buf.append("</body></html>")

		translate = "\n".join(buf)

		self.__fire_translate_changed(word, translate)

	def connect(self, event, callback):
		self.callbacks[event] = callback
