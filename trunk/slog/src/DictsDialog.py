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

#FTP_LL_URL = "ftp://ftp.lightlang.org.ru/dicts"
FTP_LL_URL = "ftp://etc.edu.ru/pub/soft/for_linux/lightlang"
FTP_DICTS_URL = FTP_LL_URL + "/dicts"
FTP_REPO_URL = FTP_DICTS_URL + "/repodata/primary.xml"
REPO_FILE = os.path.expanduser("~/.config/slog/primary.xml")
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

class DictsDialog(gtk.Dialog):
	def __init__(self, parent):
		gtk.Dialog.__init__(self, _("Manage dictionaries"), parent,
								gtk.DIALOG_DESTROY_WITH_PARENT, (gtk.STOCK_CLOSE, gtk.RESPONSE_OK))

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

	# Thread function, showing progressbar while connecting
	def __wait_connection(self, event, progressbar):
		while not event.isSet():
			progressbar.pulse()
			event.wait(0.1)
			while gtk.events_pending():
				gtk.main_iteration(False)

	def on_installer_change(self, event):
		if event.state == 0: # Notify
			if event.msg is not None:
				self.pg.set_task(event.msg)
			if event.data != -1:
				self.pg.set_progress(event.data)
			else:
				self.pg.pulse()
		elif event.state == 1: # Error
			gobject.idle_add(ghlp.show_error, self, event.msg)
		elif event.state == 2: # Done
			dname, dtarget = libsl.filename_parse(event.data)
			self.list_inst.append_row(True, False, dname, dtarget)
			self.sync_used_dicts()
		#3 - Cancel

		if event.state in (1, 2, 3):
			self.pg.destroy()
			ghlp.change_cursor(None)

		while gtk.events_pending():
			gtk.main_iteration(False)

	# Get list available dictionaries from FTP
	def on_btn_fresh_clicked(self, widget, data=None):
		self.list_avail.refresh()

	# Install dictionary
	def on_btn_right_clicked(self, widget, selection):
		(model, l_iter) = selection.get_selected()
		if l_iter is None:
			return

		fname = model.get_filename(l_iter)

		#Check duplicate
		ff = os.path.join(self.conf.sl_dicts_dir, fname[:-4])
		if os.path.isfile(ff):
			ghlp.show_error(self, _("Dictionary already installed!"))
			return

		#Check permissions
		if not is_path_writable(self.conf.sl_dicts_dir):
			ghlp.show_error(self, _("You do not have permissions!"))
			return

		ghlp.change_cursor(gdk.Cursor(gdk.WATCH))

		event = threading.Event()
		installer = DictInstaller(fname, event)
		installer.connect(self.on_installer_change)

		self.pg = ghlp.ProgressDialog(self, "Installation...", "Connecting...")
		self.pg.connect("response", lambda x, y: (y == -6 and installer.cancel()))
		self.pg.show_all()

		thread = threading.Thread(target = self.__wait_connection, args = (event, self.pg))
		thread.start()
		installer.start()

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
		dlg.destroy()
		if response == gtk.RESPONSE_YES:
			#Remove dictionary
			path = os.path.join(self.conf.sl_dicts_dir, fname)
			try:
				os.unlink(path)
			except OSError, oserr:
				msg = oserr.strerror
				ghlp.show_error(self, _("An error happened while erasing dictionary!\n%s\n%s") % (msg, path))
			else:
				model.remove(l_iter)
				self.sync_used_dicts()

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

class AvailDataModel(gtk.ListStore):
	def __init__(self):
		gtk.ListStore.__init__(self, str, str, str)
		gobject.idle_add(self.__load)

	def __load(self):
		self.clear()
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

	def download_repo_file(self, event):
		try:
			import socket
			socket.setdefaulttimeout(5)

			doc = urllib2.urlopen(FTP_REPO_URL)
		except IOError, e:
			print str(e)
		else:
			fp = open(REPO_FILE, "w")
			fp.write(doc.read())
			fp.close()
			doc.close()
		event.set()

	def refresh(self):
		ghlp.change_cursor(gdk.Cursor(gdk.WATCH))

		event = threading.Event()
		thread = threading.Thread(target = self.download_repo_file, args = (event,))
		thread.start()

		while not event.isSet():
			event.wait(0.1)
			while gtk.events_pending():
				gtk.main_iteration(False)

		self.__load()
		ghlp.change_cursor(None)

	def get_filename(self, model_iter):
		dname, dtarget = self.get(model_iter, COL_A_NAME, COL_A_TARGET)
		return (dname + "." + dtarget + ".bz2")

class InstDataModel(gtk.ListStore):
	def __init__(self):
		gtk.ListStore.__init__(self, bool, bool, str, str)
		gobject.idle_add(self.__load)

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
			dname, dtarget = libsl.filename_parse(fname)
			self.append_row(used, spy, dname, dtarget)

	def append_row(self, used, spy, name, target):
		l_iter = self.append()
		self.set(l_iter, COL_I_USED, used, COL_I_SPY, spy,
						COL_I_NAME, name, COL_I_TARGET, target)
	
class DictInstallerEvent:
	def __init__(self, state = 0, msg = None, data = None):
		self.state = state # 0 - Notify, 1 - Error, 2 - Done
		self.msg = msg
		self.data = data

class DictInstaller(threading.Thread):
	def __init__(self, filename, event, name="DictInstaller"):
		threading.Thread.__init__(self, name=name)

		self.__filename = filename
		self.__event = event
		self.__cancelled = False
		self.__callbacks = []
		self.conf = SlogConf()

	def __fire_state_change(self, event):
		for cb in self.__callbacks:
			gobject.idle_add(cb, event)

	def __notification(self, msg, data):
		if msg is not None:
			print msg
		event = DictInstallerEvent(state = 0, msg = msg, data = data)
		self.__fire_state_change(event)
			
	# Finished with Done or Error
	def __finish(self, state, msg):
		print msg
		self.__event.set()
		event = DictInstallerEvent(state = state, msg = msg, data = self.__filename)
		self.__fire_state_change(event)

		print "Cleanup..."
		shutil.rmtree(SL_TMP_DIR)

	def url_hook_report(self, blocks, bytes_in_block, file_size):
		if self.__cancelled:
			raise IOError()

		if not self.__event.isSet():
			self.__event.set()
			self.__notification("Downloading...", 0)

		if file_size:
			progress = 100.0 * float(blocks*bytes_in_block)/float(file_size)
		else:
			progress = 100.0

		if progress > 100.0:
			progress = 100.0

		self.__notification(None, progress)

	def cancel(self):
		self.__notification("Cancelled, wait...", -1)
		self.__cancelled = True

	def connect(self, callback):
		self.__callbacks.append(callback)

	def run(self):
		if not os.path.exists(SL_TMP_DIR):
			os.mkdir(SL_TMP_DIR)

		try:
			import socket
			socket.setdefaulttimeout(5)

			file_dist = os.path.join(SL_TMP_DIR, self.__filename)
			url_dict = FTP_DICTS_URL +"/" + self.__filename
			urllib.urlretrieve(url_dict, file_dist, self.url_hook_report)

		except IOError, ioerr:
			state = 1
			if self.__cancelled:
				msg = "Download cancelled!"
				state = 3
			else:
				t = ioerr.strerror
				msg = "Network error while trying to get url: %s\n%s" % (url_dict, t)

			self.__finish(state, msg)
			return

		self.__notification("Decompressing...", -1)
		fname_raw_dict = os.path.join(SL_TMP_DIR, self.__filename[:-4])
		fp = open(fname_raw_dict, "wb")
		bz2f = BZ2File(file_dist)
		try:
			fp.write(bz2f.read())
		except EOFError, msg:
			ghlp.show_error(self, str(msg))
		else:
			self.__filename = self.__filename[:-4]
		finally:
			bz2f.close()
			fp.close()

		self.__notification("Indexating...", -1)
		file_idx = fname_raw_dict + ".res"
		file_inst = os.path.join(self.conf.sl_dicts_dir, self.__filename)
		libsl.indexating(fname_raw_dict)

		self.__notification("Finishing...", -1)
		shutil.copyfile(file_idx, file_inst)

		self.__finish(2, "Installation finished!")

