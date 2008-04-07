# -*- mode: python; coding: utf-8; -*-

import os, shutil, stat
import gtk, gobject
import gtk.gdk as gdk
import urllib, urllib2
import threading
import xml.sax

from bz2 import BZ2File
import libsl
import slog.gui_helper as ghlp
from slog.config import SlogConf
from slog.dhandler import DictHandler

(
    COL_A_NAME,
	COL_A_TARGET,
	COL_A_SIZE
) = range(3)

(
    COL_I_USED,
	COL_I_SPY,
    COL_I_NAME,
	COL_I_TARGET
) = range (4)

FTP_LL_URL = "ftp://etc.edu.ru/pub/soft/for_linux/lightlang"
FTP_DICTS_URL = FTP_LL_URL + "/dicts"
FTP_REPO_URL = FTP_DICTS_URL + "/repodata/primary.xml"
REPO_FILE = os.path.expanduser("~/.config/slog/primary.xml")
#FTP_LL_URL = "ftp://ftp.lightlang.org.ru/dicts"
SL_TMP_DIR = "/tmp/sl"

def is_path_writable(path):
	if os.path.exists(path):
		s = os.stat(path)
		mode = s[stat.ST_MODE] & 0777

	if mode & 02:
		return True
	elif s[stat.ST_GID] == os.getgid() and mode & 020:
		return True
	elif s[stat.ST_UID] == os.getuid() and mode & 0200:
		return True

	return False

# Dictionary filename format: | Dictionary Name |.| Target |.| bz2 |
def filename_parse(filename):
	i = filename.find(".")
	j = filename.find(".", i+1)
	dname = filename[:i]
	if j == -1:
		dtarget = filename[i+1:]
	else:
		dtarget = filename[i+1:j]
	return dname, dtarget

class DictsDialog(gtk.Dialog):
	def __init__(self, parent):
		gtk.Dialog.__init__(self, _("Manage dictionaries"), parent,
								gtk.DIALOG_MODAL, (gtk.STOCK_CLOSE, gtk.RESPONSE_OK))

		self.tooltips = gtk.Tooltips()
		hbox = gtk.HBox(False, 0)
		self.vbox.pack_start(hbox, True, True, 0)

		frame_left = gtk.Frame(_(" Available "))
		frame_left.set_border_width(4)
		frame_right = gtk.Frame(_(" Installed "))
		frame_right.set_border_width(4)

		hbox_left = gtk.HBox(False, 4)
		hbox_left.set_border_width(4)
		hbox_right = gtk.HBox(False, 4)
		hbox_right.set_border_width(4)

		self.list_avail = AvailDataModel()
		sw1, tree_avail = self.__create_treeview(self.list_avail)
		avail_selection = tree_avail.get_selection()
		column = gtk.TreeViewColumn(_("Name"), gtk.CellRendererText(), text=COL_A_NAME)
		column.set_sizing(gtk.TREE_VIEW_COLUMN_AUTOSIZE)
		column.set_resizable(True)
		tree_avail.append_column(column)
		column = gtk.TreeViewColumn(_("Target"), gtk.CellRendererText(), text=COL_A_TARGET)
		tree_avail.append_column(column)
		column = gtk.TreeViewColumn(_("Size"), gtk.CellRendererText(), text=COL_A_SIZE)
		tree_avail.append_column(column)

		self.list_inst = InstDataModel()
		sw2, tree_inst = self.__create_treeview(self.list_inst)
		inst_selection = tree_inst.get_selection()

		renderer = gtk.CellRendererToggle()
		renderer.connect('toggled', self.on_item_toggled, self.list_inst)
		renderer.set_data("column", COL_I_USED)
		column = gtk.TreeViewColumn(_("Used"), renderer, active=COL_I_USED)
		column.set_sizing(gtk.TREE_VIEW_COLUMN_FIXED)
		column.set_fixed_width(64)
		tree_inst.append_column(column)

		renderer = gtk.CellRendererToggle()
		renderer.connect('toggled', self.on_item_toggled, self.list_inst)
		renderer.set_data("column", COL_I_SPY)
		column = gtk.TreeViewColumn(_("Spy"), renderer, active=COL_I_SPY)
		column.set_sizing(gtk.TREE_VIEW_COLUMN_FIXED)
		column.set_fixed_width(64)
		tree_inst.append_column(column)

		column = gtk.TreeViewColumn(_("Name"), gtk.CellRendererText(), text=COL_I_NAME)
		tree_inst.append_column(column)
		column = gtk.TreeViewColumn(_("Target"), gtk.CellRendererText(), text=COL_I_TARGET)
		tree_inst.append_column(column)

		btn_fresh = self.__create_button(gtk.STOCK_REFRESH, _("Refresh"))
		btn_fresh.connect("clicked", self.on_btn_fresh_clicked)
		btn_right = self.__create_button(gtk.STOCK_GO_FORWARD, _("Add"))
		btn_right.connect("clicked", self.on_btn_right_clicked, avail_selection)
		btn_left  = self.__create_button(gtk.STOCK_GO_BACK, _("Remove"))
		btn_left.connect("clicked", self.on_btn_left_clicked, inst_selection)
		btn_up    = self.__create_button(gtk.STOCK_GO_UP, _("Up"))
		btn_up.connect("clicked", self.on_btn_up_clicked, inst_selection)
		btn_down  = self.__create_button(gtk.STOCK_GO_DOWN, _("Down"))
		btn_down.connect("clicked", self.on_btn_down_clicked, inst_selection)

		vbox_left, vbox_1 = self.__create_bbox()
		vbox_right, vbox_2 = self.__create_bbox()

		vbox_1.pack_start(btn_fresh, False, False, 0)
		vbox_1.pack_start(btn_right, False, False, 0)
		vbox_2.pack_start(btn_up, False, False, 0)
		vbox_2.pack_start(btn_left, False, False, 0)
		vbox_2.pack_start(btn_down, False, False, 0)

		hbox_left.pack_start(sw1, True, True, 0)
		hbox_left.pack_start(vbox_left, False, False, 0)

		hbox_right.pack_start(vbox_right, False, False, 0)
		hbox_right.pack_start(sw2, True, True, 0)

		frame_left.add(hbox_left)
		frame_right.add(hbox_right)

		hbox.pack_start(frame_left, True, True, 0)
		hbox.pack_start(frame_right, True, True, 0)
		hbox.show_all()

		self.conf = SlogConf()

	def __create_treeview(self, model):
		scrollwin = gtk.ScrolledWindow()
		scrollwin.set_shadow_type(gtk.SHADOW_IN)
		scrollwin.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)

		treeview = gtk.TreeView(model)
		treeview.set_rules_hint(True)
		treeview.set_size_request(360, 280)
		#treeview.set_fixed_height_mode(True)

		scrollwin.add(treeview)
		return scrollwin, treeview

	def	__create_button(self, stock, tooltip):
		btn = ghlp.create_speed_button(stock)
		self.tooltips.set_tip(btn, tooltip)
		return btn

	def __create_bbox(self):
		vbox_out = gtk.VBox(False, 4)
		vbox_in = gtk.VBox(False, 4)
		vbox_out.pack_start(vbox_in, True, False, 0)
		return vbox_out, vbox_in

	def __change_cursor(self, cursor):
		for w in gdk.window_get_toplevels():
			w.set_cursor(cursor)

	# Get list available dictionaries from FTP
	def on_btn_fresh_clicked(self, widget, data=None):
		self.list_avail.refresh()


	# Install dictionary
	def on_btn_right_clicked(self, widget, selection):
		(model, l_iter) = selection.get_selected()
		if l_iter is None:
			return

		dname, dtarget = model.get(l_iter, COL_A_NAME, COL_A_TARGET)
		fname = dname + "." + dtarget + ".bz2"

		#Check duplicate
		if self.list_inst.is_exists(dname, dtarget):
			ghlp.show_error(self, _("Dictionary already installed!"))
			return

		#Check permissions
		if not is_path_writable(self.conf.sl_dicts_dir):
			ghlp.show_error(self, _("You do not have permissions!"))
			return

		pg = ghlp.ProgressDialog(self, "Installation...", "Download..")
		installer = DictInstaller(fname, pg)
		try:
			installer.start()

			gdk.threads_enter()
			self.__change_cursor(gdk.Cursor(gdk.WATCH))
			pg.show_all()
			gdk.threads_leave()

			installer.join()

			gdk.threads_enter()
			pg.destroy()
			gdk.threads_leave()

		except IOError, msg:
			ghlp.show_error(self, str(msg))
		else:
			self.list_inst.append_row(True, False, dname, dtarget)
			self.sync_used_dicts()

		self.__change_cursor(None)

	# Remove installed dictionary
	def on_btn_left_clicked(self, widget, selection):
		(model, l_iter) = selection.get_selected()
		if l_iter is None:
			return
		dname, dtarget = model.get(l_iter, COL_I_NAME, COL_I_TARGET)
		fname = dname + "." + dtarget

		#Check permissions
		if not is_path_writable(self.conf.sl_dicts_dir):
			ghlp.show_error(self, _("You do not have permissions!"))
			return

		#Question user to delete dictionary
		dlg = gtk.MessageDialog(self,
					gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
					gtk.MESSAGE_QUESTION,
					gtk.BUTTONS_YES_NO,
					_("Are you sure you want uninstall this dictionary?"))
		dlg.set_title(_("Uninstall dictionary"))
		dlg.format_secondary_text(fname)
		response = dlg.run()
		if response == gtk.RESPONSE_YES:
			#Remove dictionary
			path = os.path.join(self.conf.sl_dicts_dir, fname)
			os.unlink(path)
			model.remove(l_iter)
			self.sync_used_dicts()
		dlg.destroy()

	def on_btn_up_clicked(self, widget, selection):
		(model, iter) = selection.get_selected()
		if iter is None:
			return
		model.move_after(iter, None)
		self.sync_used_dicts()

	def on_btn_down_clicked(self, widget, selection):
		(model, iter) = selection.get_selected()
		if iter is None:
			return
		model.move_before(iter, None)
		self.sync_used_dicts()

	def on_item_toggled(self, cell, path, model):
		column = cell.get_data("column")
		l_iter = model.get_iter((int(path),))
		used = model.get_value(l_iter, column)
		used = not used
		model.set(l_iter, column, used)
		self.sync_used_dicts()

	def sync_used_dicts(self):
		used_dicts = []
		spy_dicts = []
		l_iter = self.list_inst.get_iter_first()
		while l_iter:
			used, spy, name, target = self.list_inst.get(l_iter, COL_I_USED, COL_I_SPY,
															COL_I_NAME, COL_I_TARGET)
			fname = name + "." + target
			if used:
				used_dicts.append(fname)
			if spy:
				spy_dicts.append(fname)
			l_iter = self.list_inst.iter_next(l_iter)

		ud = "|".join(used_dicts)
		sd = "|".join(spy_dicts)

		self.conf.set_used_dicts(ud)
		self.conf.set_spy_dicts(sd)


class DictInstaller(threading.Thread):
	def __init__(self, filename, progress, name="DictInstaller"):
		threading.Thread.__init__(self, name=name)
		self.__filename = filename
		self.__progress = progress
		self.conf = SlogConf()

	def update_gui(self):
		gdk.threads_enter()
		self.__progress.pulse()
		gdk.threads_leave()

	def url_hook_report(self, blocks, bytes_in_block, file_size):
		self.update_gui()

	def run(self):
		if not os.path.exists(SL_TMP_DIR):
			os.mkdir(SL_TMP_DIR)

		self.update_gui()

		gdk.threads_enter()
		try:
			import socket
			socket.setdefaulttimeout(5)

			print "Start download...", self.__filename
			file_dict = os.path.join(SL_TMP_DIR, self.__filename)

			url_dict = FTP_DICTS_URL +"/" + self.__filename
			#urllib.urlretrieve(url_dict, file_dict)
			urllib.urlretrieve(url_dict, file_dict, self.url_hook_report)
		except IOError:
			print "Network error while trying to get url: %s" % url_dict
			return
		finally:
			gdk.threads_leave()

		self.update_gui()

		self.__decompress()

		print "Start indexating..."
		file_orig = os.path.join(SL_TMP_DIR, self.__filename)
		file_idx = file_orig + ".res"
		file_inst = os.path.join(self.conf.sl_dicts_dir, self.__filename)

		libsl.indexating(file_orig)

		print "Install...", file_inst
		shutil.copyfile(file_idx, file_inst)

		print "Cleanup..."
		shutil.rmtree(SL_TMP_DIR)

	def __decompress(self):
		print "Start decompressing..."
		fp = open(os.path.join(SL_TMP_DIR, self.__filename[:-4]), "wb")
		bz2f = BZ2File(os.path.join(SL_TMP_DIR, self.__filename))
		try:
			fp.write(bz2f.read())
		except EOFError, msg:
			ghlp.show_error(self, str(msg))
		else:
			self.__filename = self.__filename[:-4]
		finally:
			bz2f.close()
			fp.close()

class ListLoader(threading.Thread):
	def __init__(self, name="ListLoader"):
		threading.Thread.__init__(self, name=name)

	def run(self):
		try:
			doc = urllib2.urlopen(FTP_REPO_URL)
		except IOError, e:
			ghlp.show_error(self, str(e))
		else:
			fp = open(REPO_FILE, "w")
			fp.write(doc.read())
			fp.close()
			doc.close()

class AvailDataModel(gtk.ListStore):
	def __init__(self):
		gtk.ListStore.__init__(self, str, str, str)
		self.__load()

	def __load(self):
		if os.path.isfile(REPO_FILE):
			parser = xml.sax.make_parser()
			chandler = DictHandler()
			parser.setContentHandler(chandler)
			parser.parse(REPO_FILE)
			d_list = chandler.get_result()
			for dfile in d_list.keys():
				l_iter = self.append()
				dname, dtarget, dsize = d_list[dfile]
				self.set(l_iter, COL_A_NAME, dname,
								COL_A_TARGET, dtarget, COL_A_SIZE, dsize)
	def refresh():
		self.clear()

		loader = ListLoader()
		loader.start()
		loader.join()

		self.__load()

class InstDataModel(gtk.ListStore):
	def __init__(self):
		gtk.ListStore.__init__(self, bool, bool, str, str)
		self.__load()

	def __load(self):
		conf = SlogConf()
		used_dict_list = conf.get_used_dicts()
		spy_file_list = conf.get_spy_dicts()

		try:
			dict_list = os.listdir(conf.sl_dicts_dir)
		except OSError, msg:
			print str(msg)
			dicts_list = []

		for fname in dict_list:
			used = fname in used_dict_list
			spy = fname in spy_file_list
			dname, dtarget = filename_parse(fname)
			self.append_row(used, spy, dname, dtarget)

	def append_row(self, used, spy, name, target):
		l_iter = self.append()
		self.set(l_iter, COL_I_USED, used, COL_I_SPY, spy,
						COL_I_NAME, name, COL_I_TARGET, target)
	
	def is_exists(self, dname, dtarget):
		for row in self:
			if dname == row[COL_I_NAME] and dtarget == row[COL_I_TARGET]:
				return True
		return False
