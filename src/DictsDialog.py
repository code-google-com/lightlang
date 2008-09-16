# -*- mode: python; coding: utf-8; -*-

import os, shutil, stat
import gtk, gobject
import gtk.gdk as gdk
import gtk.glade
import pango
import urllib, urllib2
import threading
import xml.sax

from bz2 import BZ2File
import libsl

from slog.common import *
import slog.gui_helper as ghlp
from slog.config import SlogConf
from slog.dhandler import DictHandler
from slog.proxy import Proxy

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

(
	DL_STATE_INFO,
	DL_STATE_ERROR,
	DL_STATE_DONE,
	DL_STATE_CANCEL
) = range (4)

def is_path_writable(path):
	""" Функция возвращет True если пользователь имеет
		права на запись в каталог, иначе False
	"""

	if os.path.exists(path):
		s = os.stat(path)
		mode = s[stat.ST_MODE] & 0777
	else:
		return False

	if mode & 02:
		return True
	elif s[stat.ST_GID] == os.getgid() and mode & 020:
		return True
	elif s[stat.ST_UID] == os.getuid() and mode & 0200:
		return True

	return False

class DictsDialog():
	def __init__(self, parent):

		gladefile = os.path.join(DATA_DIR, "slog.glade")
		self.wtree = gtk.glade.XML(gladefile, "dictsDialog", domain="slog")
		self.wtree.signal_autoconnect(self)
		self.dialog = self.wtree.get_widget("dictsDialog")

		self.conf = SlogConf()

		self.list_avail = AvailDataModel()
		#self.avail_filter = self.list_avail.filter_new()

		tree_avail = self.wtree.get_widget("tableAvailDicts")
		tree_avail.set_model(self.list_avail)
		self.__avail_selection = tree_avail.get_selection()

		cell = gtk.CellRendererText()
		cell.set_property("ellipsize", pango.ELLIPSIZE_END)
		column = gtk.TreeViewColumn(_("Name"), cell, text=COL_A_NAME)
		column.set_sizing(gtk.TREE_VIEW_COLUMN_AUTOSIZE)
		column.set_expand(True)
		column.set_resizable(True)
		column.set_sort_column_id(COL_A_NAME)
		column.set_reorderable(True)
		tree_avail.append_column(column)

		column = gtk.TreeViewColumn(_("Target"), gtk.CellRendererText(), text=COL_A_TARGET)
		column.set_sort_column_id(COL_A_TARGET)
		column.set_reorderable(True)
		tree_avail.append_column(column)

		column = gtk.TreeViewColumn(_("Size"), gtk.CellRendererText(), text=COL_A_SIZE)
		column.set_sort_column_id(COL_A_SIZE)
		column.set_reorderable(True)
		tree_avail.append_column(column)
		self.list_avail.set_sort_column_id(COL_A_TARGET, gtk.SORT_ASCENDING)

		self.list_inst = InstDataModel()
		self.list_inst.connect("row-changed", self.on_row_changed)
		self.list_inst.connect("row-inserted", self.on_row_inserted)
		tree_inst = self.wtree.get_widget("tableInstDicts")
		tree_inst.set_model(self.list_inst)
		self.__inst_selection = tree_inst.get_selection()

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

		cell = gtk.CellRendererText()
		cell.set_property("ellipsize", pango.ELLIPSIZE_END)
		column = gtk.TreeViewColumn(_("Name"), cell, text=COL_I_NAME)
		column.set_sizing(gtk.TREE_VIEW_COLUMN_AUTOSIZE)
		column.set_expand(True)
		column.set_resizable(True)
		column.set_sort_column_id(COL_I_NAME)
		column.set_reorderable(True)
		tree_inst.append_column(column)

		column = gtk.TreeViewColumn(_("Target"), gtk.CellRendererText(), text=COL_I_TARGET)
		column.set_sort_column_id(COL_I_TARGET)
		column.set_reorderable(True)
		tree_inst.append_column(column)

	def run(self):
		self.dialog.run()

	def destroy(self):
		self.dialog.destroy()

	def __wait_connection(self, event, progressbar):
		""" Функция выполняющася в отдельном потоке, изменяет
			состояние компонента progressbar, пока не возникнет 
			событие event
		"""
		while not event.isSet():
			progressbar.pulse()
			event.wait(0.1)
			while gtk.events_pending():
				gtk.main_iteration(False)

	def on_installer_change(self, event):
		"""	Обработчик событий возникающих при установке словаря.
		"""
		if event.state == DL_STATE_INFO:
			if event.msg is not None:
				self.pg.set_task(event.msg)
				self.pg.set_message("")
			if event.data != -1:
				self.pg.set_message("%d%%" % event.data)
				self.pg.set_progress(event.data)
			else:
				self.pg.pulse()

		elif event.state == DL_STATE_ERROR:
			gobject.idle_add(ghlp.show_error, self.dialog, event.msg)

		elif event.state == DL_STATE_DONE:
			dname, dtarget = libsl.filename_parse(event.data)
			self.list_inst.append_row(True, False, dname, dtarget)

		if event.state in (DL_STATE_ERROR, DL_STATE_DONE, DL_STATE_CANCEL):
			self.pg.destroy()
			ghlp.change_cursor(None)

		while gtk.events_pending():
			gtk.main_iteration(False)

	# Get list available dictionaries from FTP
	def on_btn_fresh_clicked(self, widget, data=None):
		self.list_avail.refresh()

	# Install dictionary
	def on_btn_right_clicked(self, widget, data=None):
		(model, l_iter) = self.__avail_selection.get_selected()
		if l_iter is None:
			return

		fname = model.get_filename(l_iter)

		#Check duplicate
		ff = os.path.join(self.conf.sl_dicts_dir, fname[:-4])
		if os.path.isfile(ff):
			ghlp.show_error(self.dialog, _("Dictionary already installed!"))
			return

		#Check permissions
		if not is_path_writable(self.conf.sl_dicts_dir):
			ghlp.show_error(self.dialog, _("You do not have permissions!"))
			return

		ghlp.change_cursor(gdk.Cursor(gdk.WATCH))

		event = threading.Event()
		installer = DictInstaller(fname, event)
		installer.connect(self.on_installer_change)

		self.pg = ghlp.ProgressDialog(self.dialog, "Installation...", "Connecting...")
		self.pg.connect("response", lambda x, y: (y == -6 and installer.cancel()))
		self.pg.show_all()

		thread = threading.Thread(target = self.__wait_connection, args = (event, self.pg))
		thread.start()
		installer.start()

	# Remove installed dictionary
	def on_btn_left_clicked(self, widget, data=None):
		(model, l_iter) = self.__inst_selection.get_selected()
		if l_iter is None:
			return
		dname, dtarget = model.get(l_iter, COL_I_NAME, COL_I_TARGET)
		fname = dname + "." + dtarget

		#Check permissions
		if not is_path_writable(self.conf.sl_dicts_dir):
			ghlp.show_error(self.dialog, _("You do not have permissions!"))
			return

		#Question user to delete dictionary
		dlg = gtk.MessageDialog(self.dialog,
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
				ghlp.show_error(self.dialog, _("An error happened while erasing dictionary!\n%s\n%s") % (msg, path))
			else:
				model.remove(l_iter)

	def on_btn_up_clicked(self, widget, data=None):
		(model, iter) = self.__inst_selection.get_selected()
		if iter is None:
			return
		model.move_after(iter, None)

	def on_btn_down_clicked(self, widget, data=None):
		(model, l_iter) = self.__inst_selection.get_selected()
		if l_iter is None:
			return

		next_iter = model.iter_next(l_iter)
		if next_iter is None:
			return

		model.move_after(l_iter, next_iter)
		gobject.idle_add(self.reorder_list_dicts, model)

	def on_item_toggled(self, cell, path, model):
		""" Обработчик события нажатия на галочку в таблице
			установленных словарей		
		"""
		column = cell.get_data("column")
		l_iter = model.get_iter((int(path),))
		used = model.get_value(l_iter, column)
		used = not used
		model.set(l_iter, column, used)

	def reorder_list_dicts(self, model):
		""" Процедура выполняющая синхронизацию таблицы установленных
			словарей с файлом конфигурации
		"""
		d_list = []
		l_iter = model.get_iter_first()
		while l_iter:
			used, spy, dname, dtarget, = model.get(l_iter, *range(4))
			fname = dname + "." + dtarget
			if used == spy and spy == False:
				pass
			else:
				d_list.append([fname, used, spy])
			l_iter = model.iter_next(l_iter)

		self.conf.sl_dicts = d_list

	def on_row_inserted(self, model, path, r_iter, data=None):
		""" Обработчик события изменения порядка установленных словарей
		"""
		gobject.idle_add(self.reorder_list_dicts, model)

	def on_row_changed(self, model, path, r_iter, data=None):
		""" Обработчик события изменения свойства либо used либо spy
			установленного словаря
		"""
		used, spy, name, target = model.get(r_iter, COL_I_USED, COL_I_SPY, COL_I_NAME, COL_I_TARGET)
		fname = name + "." + target
		self.conf.set_sl_dict_state(fname, used, spy)


class AvailDataModel(gtk.ListStore):
	def __init__(self):
		gtk.ListStore.__init__(self, str, str, int)
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
								COL_A_TARGET, dtarget, COL_A_SIZE, int(dsize))

	def download_repo_file(self, event):
		try:
			import socket
			socket.setdefaulttimeout(5)

			conf = SlogConf()
			proxy = Proxy(conf)
			downloader = proxy.get_ftp_downloader()
			downloader.retrieve(FTP_REPO_URL, REPO_FILE)

		except IOError, e:
			print str(e)
		finally:
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
		self.conf = SlogConf()
		self.__load()

	def __load(self):
		""" Загрузить список установленных словарей в таблицу
		"""
		#Cписок словарей на файловой системе в директории sl_dicts_dir
		fs_list = []
		try:
			fs_list = [f for f in os.listdir(self.conf.sl_dicts_dir) if os.path.isfile(os.path.join(self.conf.sl_dicts_dir, f))]
		except OSError, msg:
			print str(msg)

		# Список словарей сохранненый в конфигурационом файле
		for rec in self.conf.sl_dicts:
			fname, used, spy = rec
			if fname not in fs_list:
				print "Dictionary <%s> not exists in directory" % fname
				continue
			else:
				fs_list.remove(fname)

			dname, dtarget = libsl.filename_parse(fname)
			self.append_row(used, spy, dname, dtarget)

		# Добавляем словари которые не подключены
		for fname in fs_list:
			d_struct = libsl.filename_parse(fname)
			if d_struct is not None:
				self.append_row(False, False, d_struct[0], d_struct[1])

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
		event = DictInstallerEvent(state = DL_STATE_INFO, msg = msg, data = data)
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

		progress = min(100.0, progress)
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

			conf = SlogConf()
			proxy = Proxy(conf)
			downloader = proxy.get_ftp_downloader()

			file_dist = os.path.join(SL_TMP_DIR, self.__filename)
			url_dict = FTP_DICTS_URL +"/" + self.__filename
			downloader.retrieve(url_dict, file_dist, self.url_hook_report)

		except IOError, ioerr:
			state = DL_STATE_ERROR
			if self.__cancelled:
				msg = "Download cancelled!"
				state = DL_STATE_CANCEL
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
		except IOError, ioerr:
			state = DL_STATE_ERROR
			if self.__cancelled:
				msg = "Cancelled!"
				state = DL_STATE_CANCEL
			else:
				t = ioerr.strerror
				msg = "IO error while decompressing\n%s" % t

			self.__finish(state, msg)
			return

		except EOFError, msg:
			ghlp.show_error(self.dialog, str(msg))
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

		self.__finish(DL_STATE_DONE, "Installation finished!")

