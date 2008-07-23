# -*- mode: python; coding: utf-8; -*-

import os
import gtk, gobject, gtk.glade
import pango
import threading

import libsl
from slog.common import *
from slog.config import SlogConf

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

		self.treemodel_lock = threading.Lock()

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
		self.find_all(word, mode = libsl.SL_FIND_FUZZY)

	def on_btn_clear_clicked(self, widget, data=None):
		self.word_entry.set_text("")
		self.word_entry.grab_focus()
		self.treestore.clear()
		self.treestore.append(None, [_("Enter the word, please...")])
		self.__fire_status_changed("")

	def on_timer_timeout(self):
		self.timer = 0;
		word = self.word_entry.get_text().lower()
		self.find_all(word)

	def on_word_changed(self, widget, data=None):
		if self.timer == 0:
			self.timer = gobject.timeout_add(500, self.on_timer_timeout)

	def on_word_entry_activate(self, widget, data=None):
		word = widget.get_text().lower()
		self.find_all(word)

	def on_wordlist_changed(self, selection):
		model, treeiter = selection.get_selected()
		self.find_word(treeiter, newTab = False)

	def __thread_find(self, node, word, mode, dict_name):

		filename = self.conf.get_dic_path(dict_name)
		items = libsl.find_word(word, mode, filename)

		self.treemodel_lock.acquire()
		if items == []:
			self.treestore.remove(node)
		else:
			for item in items:
				self.treestore.append(node, [item])
		self.treemodel_lock.release()
	
	def __get_n_rows(self):
		""" Функция возвращает количество выведенных
			вариантов слова
		"""
		count = 0

		it = self.treestore.get_iter_first()
		while it:
			if self.treestore.iter_has_child(it):
				ti = self.treestore.iter_children(it)
				while ti:
					count += 1
					ti = self.treestore.iter_next(ti)
			it = self.treestore.iter_next(it)

		return count

	def find_all(self, word, mode = libsl.SL_FIND_LIST):
		""" Выполняет поиск слова в отмеченных пользователем
			словарях, и добавляет найденные варианты на панель
			результатов поиска.
		"""
		if word == "":
			return

		self.treestore.clear()
		threads = []

		dictionaries = self.conf.get_sl_used_dicts()
		for dic in dictionaries:
			
			node = self.treestore.append(None, [dic])
			t = threading.Thread(target = self.__thread_find, args = (node, word, mode, dic))
			threads.append(t)
			t.start()

		for t in threads:
			t.join()

		count = self.__get_n_rows()

		if count>0:
			self.treeview.expand_all()
			self.word_selection.select_path((0,0))
		else:
			self.treestore.append(None, [_("This word is not found")])

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

