# -*- mode: python; coding: utf-8; -*-

import os, subprocess
import gtk, gobject

from slog.config import SlogConf
import slog.gui_helper as ghlp

plugin_name = "LightLang SL"
plugin_version = "0.1.0"
plugin_author = "Nasyrov Renat <renatn@gmail.com>"
plugin_description = _("Client for LightLang SL dictionary")

def enable():
	return SLView()

FMT_HTML = "html"
FMT_TEXT = "text"
MODE_LIST = "l"
MODE_WORD = "f"

class SLEngine:

	def __do_find(self, format, mode, dicts, word):
		sl_exec = SlogConf().get_sl_exec()

		if word == "" or dicts == "":
			return []

		cmd = [sl_exec, "--output-format=%s" % (format), \
				"--use-list=%s" % (dicts), "-%s" % (mode), word]
		try:
			pipe = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout
			lines = pipe.readlines()
		except OSError, msg:
			print "Error: check field sl_prefix in ~/.config/slog/slogrc"
			return []

		return lines

	def get_list(self, word):
		dictionaries = SlogConf().get_used_dicts()
		return self.__do_find(FMT_TEXT, MODE_LIST, dictionaries, word)

	def get_translate(self, dictionary, word):
		return self.__do_find(FMT_HTML, MODE_WORD, dictionary, word)


class SLView(gtk.VBox):
	def __init__(self):
		gtk.VBox.__init__(self, False, 0)

		self.timer = 0
		self.callbacks = {}
		self.sl = SLEngine()

		tooltips = gtk.Tooltips()
		hbox = gtk.HBox(False, 0)
		hbox.set_border_width(4)
		self.pack_start(hbox, False, False, 0)

		self.word_entry = gtk.Entry()
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
		#if self.word_entry.get_text() == "":
		#	return
		model, iter = selection.get_selected()
		if iter is not None:
			item = model.get_value(iter, 0)
			if item.startswith("("):
				word = item[4:].strip()
				parent = self.treestore.iter_parent(iter)
				dictionary = model.get_value(parent, 0)
				self.find_word(dictionary, word)

	def find_list(self, word):
		if word == "":
			#self.statusbar.pop(self.context_id)
			#tv = self.tabs[self.notebook.get_current_page()]
			#tv.clear()
			return
		count = 0

		model = self.treestore
		model.clear()

		lines = self.sl.get_list(word)
		if lines is not None:
			for line in lines:
				if line.startswith("="):
					item = line.strip().strip("=").strip()
					dictionary = model.append(None, ["%s" % (item)])
				elif line.startswith(" ("):
					model.append(dictionary, [line.strip()])
					count += 1
		if count>0:
			self.treeview.expand_all()
			self.word_selection.select_path((0,0))
		else:
			model.append(None, [_("This word is not found")])

		self.__fire_status_changed(_("Total: %i") % (count))

	def find_word(self, dictionary, word):
		lines = self.sl.get_translate(dictionary, word)
		self.__fire_translate_changed(word, "".join(lines))

	def connect(self, event, callback):
		self.callbacks[event] = callback

	def get_engine(self):
		return self.sl

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

		label = gtk.Label("SL_PREFIX:")
		hbox.pack_start(label, False, False, 0)

		prefix_entry = gtk.Entry()
		prefix_entry.set_text(conf.sl_prefix)
		hbox.pack_start(prefix_entry, True, True, 0)
		
		btn_browse = gtk.Button("...")
		btn_browse.connect("clicked", self.on_browse_clicked, prefix_entry)
		hbox.pack_start(btn_browse, False, False, 0)

		label.set_mnemonic_widget(prefix_entry)
		dlg.show_all()

		response = dlg.run()
		if response == gtk.RESPONSE_OK:
			prefix = prefix_entry.get_text()
			if not os.path.exists(prefix):
				ghlp.show_error(window, _("Path not exists!"))
			conf.sl_prefix = prefix

		dlg.destroy()

	def on_browse_clicked(self, widget, data):
		chooser = gtk.FileChooserDialog("Open..", None, gtk.FILE_CHOOSER_ACTION_OPEN,
							(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OPEN, gtk.RESPONSE_OK))

		sl_filter = gtk.FileFilter()
		sl_filter.set_name("SL execute")
		sl_filter.add_pattern("sl")
		chooser.add_filter(sl_filter)

		sl_prefix = data.get_text()
		if os.path.exists(sl_prefix):
			chooser.set_current_folder(sl_prefix)

		response = chooser.run()
		if response == gtk.RESPONSE_OK:
			sl_path = chooser.get_filenames()[0]
			sl_prefix = sl_path.split("/bin/sl")[0]
			data.set_text(sl_prefix)

		chooser.destroy()

