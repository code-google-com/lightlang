# -*- mode: python; coding: utf-8; -*-

import os
import gtk, gobject, gtk.glade
import urllib, urllib2
import threading
import pango

from Google.google_translate import GoogleEngine

from slog.config import SlogConf
import slog.gui_helper as ghlp

plugin_name = "Google Translate"
plugin_version = "0.1.2"
plugin_author = "Nasyrov Renat <renatn@gmail.com>"
plugin_description = _("Client for Google Translate")

def enable():
	return GoogleView()

def slog_init(plugin_path):
	global path
	path = plugin_path

def reload_targets(languages, model, targets):
	model.clear()
	for t in targets:
		src, dst = t
		title = languages[src] + " - " + languages[dst]
		model.append([title, src, dst])
			
class PrefDialog(object):

	def __init__(self, window, conf, google, model):
		gladefile = os.path.join(path, "google.glade")
		wtree = gtk.glade.XML(gladefile, domain="slog")
		wtree.signal_autoconnect({
				"on_btn_add_clicked" : self.on_target_added,
				"on_btn_del_clicked" : self.on_target_removed,
				"on_btn_def_clicked" : lambda w: self.__load_default_targets()
		})

		self.google = google
		self.conf = conf
		self.model = model

		self.dlg = wtree.get_widget("pref_dialog")
		self.dlg.set_transient_for(window)

		self.__init_tooltips(wtree)

		model = gtk.ListStore(str)
		for lang in self.google.languages.values():
			model.append([lang])

		self.cmb_from = wtree.get_widget("combo_from")
		self.cmb_to = wtree.get_widget("combo_to")
		self.__init_combobox(self.cmb_from, model)
		self.__init_combobox(self.cmb_to, model)
	
		self.tv_targets = wtree.get_widget("tree_targets")
		selection = self.tv_targets.get_selection()
		selection.set_mode(gtk.SELECTION_MULTIPLE)
		self.tv_targets.set_model(self.model)

		cell = gtk.CellRendererText()
		cell.set_property("ellipsize", pango.ELLIPSIZE_END)
		tvcolumn = gtk.TreeViewColumn("Target", cell, text=0)
		self.tv_targets.append_column(tvcolumn)

	def __init_tooltips(self, wtree):
		tooltips = gtk.Tooltips()
		w = wtree.get_widget("btn_add")
		tooltips.set_tip(w, _("Add"))
		w = wtree.get_widget("btn_del")
		tooltips.set_tip(w, _("Remove selected"))
		w = wtree.get_widget("btn_def")
		tooltips.set_tip(w, _("Load default"))

	def __load_default_targets(self):
		reload_targets(self.google.languages, self.model, self.conf.get_google_defaults())
		self.sync_with_config()

	def __init_combobox(self, combobox, model):
		cell = gtk.CellRendererText()
		combobox.pack_start(cell, True)
		combobox.add_attribute(cell, 'text', 0)
		combobox.set_model(model)
		combobox.set_active(0)

	def on_target_added(self, widget, data=None):
		langs = self.google.get_langs()
		i = self.cmb_from.get_active()
		j = self.cmb_to.get_active()
		if i == j:
			print "Warning: Selected languages is equal"
			return

		src = langs.keys()[i]
		dst = langs.keys()[j]

		title = langs[src] + " - " + langs[dst]

		#TODO: Check dublicate
		#TODO: Insert if exists selection
		#TODO: Save into configuration
	
		self.model.append([title, src, dst])
		self.conf.google_targets.append(src+":"+dst)

	def on_target_removed(self, widget, data=None):
		selection = self.tv_targets.get_selection()
		model, rows = selection.get_selected_rows()
		
		rowref_list = []
		for path in rows:
			rowref_list.append(gtk.TreeRowReference(model, path))
		for rowref in rowref_list:
			path = rowref.get_path()
			if path:
				it = model.get_iter(path)
				if it: model.remove(it)

		self.sync_with_config()

	def sync_with_config(self):

		for row in self.model:
			src, dst = row[1], row[2]
		self.conf.google_targets =

	#====================== Public =============================

	def run(self):
		return self.dlg.run()

	def destroy(self):
		self.dlg.destroy()

class GoogleView(object):
	def __init__(self):

		self.callbacks = {}
		self.google = GoogleEngine()
		self.conf = SlogConf()

		gladefile = os.path.join(path, "google.glade")
		self.wtree = gtk.glade.XML(gladefile, domain="slog")
		self.wtree.signal_autoconnect({
				"on_btn_clear_clicked" : self.on_btn_clear_clicked,
				"on_btn_translate_clicked" : self.on_translate_clicked
		})

		self.vbox = self.wtree.get_widget("vbox1")
		self.vbox.unparent()

		self.textview = self.wtree.get_widget("textview1")

		self.cmb_target = self.wtree.get_widget("combo_targets")
		cell = gtk.CellRendererText()
		self.cmb_target.pack_start(cell, True)
		self.cmb_target.add_attribute(cell, 'text', 0)
		self.model = gtk.ListStore(str, str, str)
		self.cmb_target.set_model(self.model)
		
		reload_targets(self.google.languages, self.model, self.conf.get_google_targets())
		self.cmb_target.set_active(self.conf.google_target)

	def __fire_translate_changed(self, translate):
		callback = self.callbacks["translate_it"]
		if callback is not None:
			callback("Google", translate)

	def __fire_status_changed(self, message, needClear=False):
		callback = self.callbacks["changed"]
		if callback is not None:
			gobject.idle_add(callback, message)
			if needClear:
				gobject.timeout_add(5000, self.__fire_status_changed, "")

	# Thread function
	def request_google(self, src, dst, text):
		try:
			translate = self.google.translate(src, dst, text)
		except urllib2.URLError, err:
			msg = "Google error: %s" % err
			print msg
			self.__fire_status_changed(msg, True)
		else:
			self.__fire_translate_changed(translate)
			self.__fire_status_changed("Done", True)
		finally:
			ghlp.change_cursor(None)

	def on_translate_clicked(self, widget, data=None):
		""" Обработчик собития нажатия на кнопку Translate
		"""
		curr = self.cmb_target.get_active()
		if curr == -1:
			print "Warning: Target not selected"
			return

		src = self.model[curr][1]
		dst = self.model[curr][2]
		
		textbuffer = self.textview.get_buffer()
		start, end = textbuffer.get_bounds()
		text = textbuffer.get_text(start, end)

		self.conf.google_target = curr

		if len(text) == 0:
			ghlp.show_error(None, _("Empty text"))
			return

		ghlp.change_cursor(gtk.gdk.Cursor(gtk.gdk.WATCH))
		self.__fire_status_changed("Send request...")

		thread = threading.Thread(target = self.request_google, args = (src, dst, text))
		thread.start()

	def on_btn_clear_clicked(self, widget, data=None):
		textbuffer = self.textview.get_buffer()
		start, end = textbuffer.get_bounds()
		textbuffer.delete(start, end)

	# ================================ SLog Plugins API ============================

	def connect(self, event, callback):
		self.callbacks[event] = callback

	def get_panel(self):
		return self.vbox

	def grab_focus(self):
		self.textview.grab_focus()

	def configure(self, window):
		dlg = PrefDialog(window, self.conf, self.google, self.model)
		dlg.run()
		dlg.destroy()

if __name__ == "__main__":
	slog_init("./")
	g = enable()
	g.configure(None)
