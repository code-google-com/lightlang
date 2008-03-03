# -*- mode: python; coding: utf-8; -*-

import os, shutil, stat, subprocess
import gtk, gobject
import gtk.gdk as gdk
import urllib, urllib2
import xml.sax

from bz2 import BZ2File
import slog.gui_helper as ghlp
from slog.config import SlogConf
from slog.dhandler import DictHandler

(
    COLUMN_USED,
	COLUMN_SPY,
    COLUMN_NAME
) = range(3)

(
	COLUMN_FILE,
	COLUMN_DICT,
	COLUMN_TARGET,
	COLUMN_SIZE
) = range(4)

FTP_LL_URL = "ftp://etc.edu.ru/pub/soft/for_linux/lightlang"
FTP_DICTS_URL = FTP_LL_URL + "/dicts"
FTP_REPO_URL = FTP_DICTS_URL + "/repodata/primary.xml"

REPO_FILE = os.path.expanduser("~/.config/slog/primary.xml")

#FTP_LL_URL = "ftp://ftp.lightlang.org.ru/dicts"
SL_TMP_DIR = "/tmp/sl"

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

		self.list_avail = gtk.ListStore(gobject.TYPE_STRING, gobject.TYPE_STRING,
										gobject.TYPE_STRING, gobject.TYPE_STRING)
		sw1, tree_avail = self.__create_treeview(self.list_avail)
		avail_selection = tree_avail.get_selection()
		column = gtk.TreeViewColumn(_("Name"), gtk.CellRendererText(), text=COLUMN_DICT)
		column.set_sizing(gtk.TREE_VIEW_COLUMN_AUTOSIZE)
		column.set_resizable(True)
		tree_avail.append_column(column)
		column = gtk.TreeViewColumn(_("Target"), gtk.CellRendererText(), text=COLUMN_TARGET)
		tree_avail.append_column(column)
		column = gtk.TreeViewColumn(_("Size"), gtk.CellRendererText(), text=COLUMN_SIZE)
		tree_avail.append_column(column)

		self.list_inst = gtk.ListStore(gobject.TYPE_BOOLEAN, gobject.TYPE_BOOLEAN, gobject.TYPE_STRING)
		sw2, tree_inst = self.__create_treeview(self.list_inst)
		inst_selection = tree_inst.get_selection()

		renderer = gtk.CellRendererToggle()
		renderer.connect('toggled', self.on_item_toggled, self.list_inst)
		renderer.set_data("column", COLUMN_USED)
		column = gtk.TreeViewColumn(_("Used"), renderer, active=COLUMN_USED)
		column.set_sizing(gtk.TREE_VIEW_COLUMN_FIXED)
		column.set_fixed_width(64)
		tree_inst.append_column(column)

		renderer = gtk.CellRendererToggle()
		renderer.connect('toggled', self.on_item_toggled, self.list_inst)
		renderer.set_data("column", COLUMN_SPY)
		column = gtk.TreeViewColumn(_("Spy"), renderer, active=COLUMN_SPY)
		column.set_sizing(gtk.TREE_VIEW_COLUMN_FIXED)
		column.set_fixed_width(64)
		tree_inst.append_column(column)

		column = gtk.TreeViewColumn(_("Name"), gtk.CellRendererText(), text=COLUMN_NAME)
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
		self.load_installed_dicts()
		self.load_available_dicts()

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

	# Get list available dictionaries from FTP
	def on_btn_fresh_clicked(self, widget, data=None):
		self.list_avail.clear()
		self.window.set_cursor(gdk.Cursor(gdk.WATCH))

		try:
			doc = urllib2.urlopen(FTP_REPO_URL)
		except IOError, e:
			ghlp.show_error(self, str(e))
		else:
			fp = open(REPO_FILE, "w")
			fp.write(doc.read())
			fp.close()
			doc.close()
			self.load_available_dicts()

		self.window.set_cursor(None)

	# Install dictionary
	def on_btn_right_clicked(self, widget, selection):
		(model, l_iter) = selection.get_selected()
		if l_iter is None:
			return
		sl_dict = model.get_value(l_iter, COLUMN_FILE)

		#Check duplicate
		if self.is_dict_installed(sl_dict[:-4]):
			ghlp.show_error(self, _("Dictionary already installed!"))
			return

		#Check permissions
		dicts_dir = self.conf.get_sl_dicts_dir()
		if not self.is_path_writable(dicts_dir):
			ghlp.show_error(self, _("You do not have permissions!"))
			return

		installer = DictInstaller(sl_dict)
		try:
			installer.do_install()
		except IOError, msg:
			ghlp.show_error(self, str(msg))
		else:
			l_iter = self.list_inst.append()
			self.list_inst.set(l_iter, COLUMN_USED, True, COLUMN_SPY, False, COLUMN_NAME, sl_dict[:-4])
			self.sync_used_dicts()

	# Remove installed dictionary
	def on_btn_left_clicked(self, widget, selection):
		(model, l_iter) = selection.get_selected()
		if l_iter is None:
			return
		dname = model.get_value(l_iter, COLUMN_NAME)

		#Check permissions
		dicts_dir = self.conf.get_sl_dicts_dir()
		if not self.is_path_writable(dicts_dir):
			ghlp.show_error(self, _("You do not have permissions!"))
			return

		#Question user to delete dictionary
		dlg = gtk.MessageDialog(self,
					gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
					gtk.MESSAGE_QUESTION,
					gtk.BUTTONS_YES_NO,
					_("Are you sure you want uninstall this dictionary?"))
		dlg.set_title(_("Uninstall dictionary"))
		dlg.format_secondary_text(dname)
		response = dlg.run()
		if response == gtk.RESPONSE_YES:
			#Remove dictionary
			path = os.path.join(self.conf.get_sl_dicts_dir(), dname)
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

	def load_available_dicts(self):
		if os.path.isfile(REPO_FILE):
			parser = xml.sax.make_parser()
			chandler = DictHandler()
			parser.setContentHandler(chandler)
			parser.parse(REPO_FILE)
			d_list = chandler.get_result()
			for dfile in d_list.keys():
				l_iter = self.list_avail.append()
				dname, dtarget, dsize = d_list[dfile]
				self.list_avail.set(l_iter, COLUMN_FILE, dfile, COLUMN_DICT, dname,
								COLUMN_TARGET, dtarget, COLUMN_SIZE, dsize)

	def load_installed_dicts(self):
		sl_dicts_dir = self.conf.get_sl_dicts_dir()
		used_dict_list = self.conf.get_used_dicts().split("|")
		spy_dict_list = self.conf.get_spy_dicts().split("|")

		#Get installed dictionaries
		if os.path.exists(sl_dicts_dir):
			d_list = os.listdir(sl_dicts_dir)
			for dict in d_list:
				iter = self.list_inst.append()
				used = dict in used_dict_list
				spy = dict in spy_dict_list
				self.list_inst.set(iter, COLUMN_USED, used, COLUMN_SPY, spy, COLUMN_NAME, dict)

	def sync_used_dicts(self):
		used_dicts = []
		spy_dicts = []
		l_iter = self.list_inst.get_iter_first()
		while l_iter:
			name = self.list_inst.get_value(l_iter, COLUMN_NAME)
			used = self.list_inst.get_value(l_iter, COLUMN_USED)
			spy = self.list_inst.get_value(l_iter, COLUMN_SPY)
			if used:
				used_dicts.append(name)
			if spy:
				spy_dicts.append(name)
			l_iter = self.list_inst.iter_next(l_iter)

		ud = "|".join(used_dicts)
		sd = "|".join(spy_dicts)

		self.conf.set_used_dicts(ud)
		self.conf.set_spy_dicts(sd)

	def is_path_writable(self, path):
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

	def is_dict_installed(self, name):
		d_list = [row[COLUMN_NAME] for row in self.list_inst]
		return (name in d_list)

class DictInstaller:
	def __init__(self, ftp_filename):
		self.filename = ftp_filename

	def do_install(self):
		if not os.path.exists(SL_TMP_DIR):
			os.mkdir(SL_TMP_DIR)

		self.__download()
		self.__decompress()
		self.__indexating()

	#def url_hook_report(*a):
	#	print a

	def __download(self):
		print "Start download...", self.filename
		file_dict = os.path.join(SL_TMP_DIR, self.filename)

		if os.path.isfile(file_dict):
			print "File already downloaded..."
			return

		url_dict = FTP_DICTS_URL +"/" + self.filename

		fp = open(file_dict, "wb")
		urllib.urlretrieve(url_dict, file_dict)
		#urllib.urlretrieve(url_dict, file_dict, self.url_hook_report)

	def __decompress(self):
		print "Start decompressing..."
		fp = open(os.path.join(SL_TMP_DIR, self.filename[:-4]), "wb")
		bz2f = BZ2File(os.path.join(SL_TMP_DIR, self.filename))
		try:
			fp.write(bz2f.read())
		except EOFError, msg:
			raise IOError(msg)
		else:
			self.filename = self.filename[:-4]
		finally:
			bz2f.close()
			fp.close()

	def __indexating(self):
		print "Start indexating..."
		conf = SlogConf()
		sl_exec = conf.get_sl_exec()
		sl_dicts = conf.get_sl_dicts_dir()

		file_orig = os.path.join(SL_TMP_DIR, self.filename)
		file_idx1 = os.path.join(SL_TMP_DIR, (self.filename + ".idx1"))
		file_idx2 = os.path.join(SL_TMP_DIR, (self.filename + ".idx2"))
		file_inst = os.path.join(sl_dicts, self.filename)

		print "* create index, step 1..."
		retcode = subprocess.call("%s --print-index %s 1>%s" % (sl_exec, file_orig, file_idx1), shell=True)
		if retcode != 0:
			raise IOError("failed indexating")
		retcode = subprocess.call("cat %s 1>>%s" % (file_orig, file_idx1), shell=True)
		if retcode != 0:
			raise IOError("failed indexating")

		print "* create index, step 2..."
		retcode = subprocess.call("%s --print-index %s 1>%s" % (sl_exec, file_idx1, file_idx2), shell=True)
		if retcode != 0:
			raise IOError("failed indexating")
		retcode = subprocess.call("cat %s 1>>%s" % (file_orig, file_idx2), shell=True)
		if retcode != 0:
			raise IOError("failed indexating")

		print "Install...", file_inst
		shutil.copyfile(file_idx2, file_inst)
		#print "Cleanup..."
		#shutil.rmtree(SL_TMP_DIR)
		print "done"

