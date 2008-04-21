# -*- mode: python; coding: utf-8; -*-

import os
import gtk, gobject
import pango

import libsl
from slog.config import SlogConf
import slog.gui_helper as ghlp

plugin_name = "LightLang SL"
plugin_version = "0.1.0"
plugin_author = "Nasyrov Renat <renatn@gmail.com>"
plugin_description = _("Client for LightLang SL dictionary")

def enable():
	return SLView()

class SLView(gtk.VBox):
	def __init__(self):
		gtk.VBox.__init__(self, False, 0)

		self.conf = SlogConf()
		self.timer = 0
		self.callbacks = {}

		tooltips = gtk.Tooltips()
		hbox = gtk.HBox(False, 0)
		hbox.set_border_width(4)
		self.pack_start(hbox, False, False, 0)

		self.word_entry = gtk.Entry()
		self.word_entry.set_size_request(60, -1)
		self.word_entry.connect("activate", self.on_word_entry_activate)
		self.word_entry.connect("changed", self.on_word_entry_changed)
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
		self.treeview.connect("row-activated", self.on_row_activated)
		sw.add(self.treeview)

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

	def on_row_activated(self, widget, path, column, data=None):
		treeiter = self.treestore.get_iter(path)
		self.find_word(treeiter, True)

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

	def on_word_entry_changed(self, widget, data=None):
		if self.timer == 0:
			self.timer = gobject.timeout_add(500, self.on_timer_timeout)

	def on_word_entry_activate(self, widget, data=None):
		word = widget.get_text().lower()
		self.find_list(word)

	def on_wordlist_changed(self, selection):
		model, treeiter = selection.get_selected()
		self.find_word(treeiter, False)

	def find_list(self, word):
		if word == "":
			return

		count = 0
		model = self.treestore
		model.clear()

		dictionaries = self.conf.get_used_dicts()
		for dic in dictionaries:

			filename = self.conf.get_dic_path(dic)
			items = libsl.find_word(word, 0, filename)
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

	def find_word(self, treeiter, newtab=False):
		if treeiter is None:
			return
		
		parentiter = self.treestore.iter_parent(treeiter)
		if parentiter is None:
			return

		word = self.treestore.get_value(treeiter, 0)
		dic = self.treestore.get_value(parentiter, 0)

		filename = self.conf.get_dic_path(dic)
		lines = libsl.find_word(word, 1, filename)
		translate = "<body>%s</body>" % ("".join(lines))
		self.__fire_translate_changed(word, translate, newtab)

	def connect(self, event, callback):
		self.callbacks[event] = callback

	def grab_focus(self):
		self.word_entry.grab_focus()

	# ================================ Plugin support ============================

	def configure(self, window):
		conf = SlogConf()

		dlg = gtk.Dialog(plugin_name, window, 0, (gtk.STOCK_OK, gtk.RESPONSE_OK))

		hbox = gtk.HBox(False, 8)
		hbox.set_border_width(8)
		dlg.vbox.pack_start(hbox, False, False, 0)

		stock = gtk.image_new_from_stock(
				gtk.STOCK_DIALOG_QUESTION,
				gtk.ICON_SIZE_DIALOG)
		hbox.pack_start(stock, False, False, 0)

		label = gtk.Label(_("Dictionaries dir:"))
		hbox.pack_start(label, False, False, 0)

		dir_entry = gtk.Entry()
		dir_entry.set_text(conf.sl_dicts_dir)
		hbox.pack_start(dir_entry, True, True, 0)
		
		btn_browse = gtk.Button("...")
		btn_browse.connect("clicked", self.on_browse_clicked, window, dir_entry)
		hbox.pack_start(btn_browse, False, False, 0)

		label.set_mnemonic_widget(dir_entry)
		dlg.show_all()

		response = dlg.run()
		if response == gtk.RESPONSE_OK:
			ddir = dir_entry.get_text()
			if not os.path.exists(ddir):
				ghlp.show_error(window, _("Path not exists!"))
			conf.sl_dicts_dir = ddir

		dlg.destroy()

	def on_browse_clicked(self, widget, window, entry):
		chooser = gtk.FileChooserDialog("Open..", window, gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER,
							(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OK, gtk.RESPONSE_OK))

		dicts_dir = entry.get_text()
		if os.path.exists(dicts_dir):
			chooser.set_current_folder(dicts_dir)

		response = chooser.run()
		if response == gtk.RESPONSE_OK:
			path = chooser.get_filename()
			entry.set_text(path)

		chooser.destroy()

