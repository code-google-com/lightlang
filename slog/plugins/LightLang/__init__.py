# -*- mode: python; coding: utf-8; -*-

import os
import gtk, gobject
import pango

import libsl
from slog.common import *
from slog.config import SlogConf
import slog.gui_helper as ghlp

plugin_name = "LightLang SL"
plugin_version = "0.1.0"
plugin_author = "Nasyrov Renat <renatn@gmail.com>"
plugin_description = _("Client for LightLang SL dictionary")

def enable():
	return SLView()

def slog_init(plugin_path):
	global path
	path = plugin_path

class SLView(object):
	def __init__(self):

		self.conf = SlogConf()
		self.timer = 0
		self.callbacks = {}

		gladefile = os.path.join(path, "xsl.glade")
		self.wtree = gtk.glade.XML(gladefile, domain="slog")
		self.wtree.signal_autoconnect(self)
		self.vbox = self.wtree.get_widget("sl_vbox")
		self.vbox.unparent()

		self.word_entry = self.wtree.get_widget("word_entry")

		self.treestore = gtk.TreeStore(str)
		self.treeview = self.wtree.get_widget("sl_tree")
		self.treeview.set_model(self.treestore)

		cell = gtk.CellRendererText()
		cell.set_property("ellipsize", pango.ELLIPSIZE_END)
		tvcolumn = gtk.TreeViewColumn("Result", cell, text=0)
		self.treeview.append_column(tvcolumn)
		self.treestore.append(None, [_("Enter the word, please...")])

		self.word_selection = self.treeview.get_selection()
		self.word_selection.connect("changed", self.on_wordlist_changed)

	def __fire_status_changed(self, message):
		callback = self.callbacks["changed"]
		if callback is not None:
			callback(message)

	def __fire_translate_changed(self, word, translate, newtab):
		callback = self.callbacks["translate_it"]
		if callback is not None:
			callback(word, translate, newtab)

	def on_btn_fuzzy_clicked(self, widget, data=None):
		word = self.word_entry.get_text()
		self.find_list(word, mode = libsl.SL_FIND_FUZZY)

	def on_btn_clear_clicked(self, widget, data=None):
		self.word_entry.set_text("")
		self.word_entry.grab_focus()
		self.treestore.clear()
		self.treestore.append(None, [_("Enter the word, please...")])
		self.__fire_status_changed("")

	def on_timer_timeout(self):
		self.timer = 0;
		word = self.word_entry.get_text().lower()
		self.find_list(word)

	def on_word_changed(self, widget, data=None):
		if self.timer == 0:
			self.timer = gobject.timeout_add(500, self.on_timer_timeout)

	def on_word_entry_activate(self, widget, data=None):
		word = widget.get_text().lower()
		self.find_list(word)

	def on_wordlist_changed(self, selection):
		model, treeiter = selection.get_selected()
		self.find_word(treeiter, newTab = False)

	def find_list(self, word, mode = libsl.SL_FIND_LIST):
		if word == "":
			return

		count = 0
		model = self.treestore
		model.clear()

		dictionaries = self.conf.get_sl_used_dicts()
		for dic in dictionaries:

			filename = self.conf.get_dic_path(dic)
			items = libsl.find_word(word, mode, filename)
			count += len(items)
			if items == []:
				continue

			root_node = model.append(None, [dic])
			for item in items:
				model.append(root_node, [item])

		if count>0:
			self.treeview.expand_all()
			self.word_selection.select_path((0,0))
		else:
			model.append(None, [_("This word is not found")])

		self.__fire_status_changed(_("Total: %i") % (count))

	def find_word(self, treeiter, mode = libsl.SL_FIND_MATCH, newTab=False):
		if treeiter is None:
			return

		parentiter = self.treestore.iter_parent(treeiter)
		if parentiter is None:
			return

		word = self.treestore.get_value(treeiter, 0)
		dic = self.treestore.get_value(parentiter, 0)

		filename = self.conf.get_dic_path(dic)
		lines = libsl.find_word(word, mode, filename)
		translate = "<body>%s</body>" % ("".join(lines))
		self.__fire_translate_changed(word, translate, newTab)

	# ================================ SLog Plugins API ============================

	def connect(self, event, callback):
		self.callbacks[event] = callback

	def get_panel(self):
		return self.vbox

	def grab_focus(self):
		self.word_entry.grab_focus()

	def configure(self, window):
		dlg = self.wtree.get_widget("pref_dialog")
		dlg.set_transient_for(window)
		dir_entry = self.wtree.get_widget("entry_folder")
		dir_entry.set_current_folder(self.conf.sl_dicts_dir)

		response = dlg.run()
		if response == gtk.RESPONSE_OK:
			self.conf.sl_dicts_dir = dir_entry.get_filename()

		dlg.hide()

