# -*- coding: utf8 -*-
#
# XSL - graphical interface for SL
# Copyright (C) 2007-2016 Devaev Maxim
#
# This file is part of XSL.
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

from PyQt4 import Qt
import Const
import Config

#####
GoogleTranslateHost = "translate.google.com"

#####
class GoogleTranslate(Qt.QObject) :
	def __init__(self, parent = None) :
		Qt.QObject.__init__(self, parent)

		self.http = Qt.QHttp()
		self.http_request_id = -1
		self.http_abort_flag = False

		self.http_output = Qt.QByteArray()

		self.timer = Qt.QTimer()
		self.timer.setInterval(30000)

		#####

		self.connect(self.http, Qt.SIGNAL("stateChanged(int)"), self.setStatus)
		self.connect(self.http, Qt.SIGNAL("requestFinished(int, bool)"), self.requestFinished)
		self.connect(self.http, Qt.SIGNAL("readyRead(const QHttpResponseHeader &)"), self.setText)

		self.connect(self.timer, Qt.SIGNAL("timeout()"), self.abort)


	### Public ###

	def translate(self, sl, tl, text) :
		self.http_abort_flag = True
		self.http.abort()
		self.http_abort_flag = False

		self.processStartedSignal()

		self.clearRequestSignal()

		self.http.clearPendingRequests()
		self.http_output.clear()

		self.wordChangedSignal(self.tr("Google Translate"))
		self.textChangedSignal(self.tr("<em>Please wait...</em>"))

		text = Qt.QString.fromLocal8Bit(str(Qt.QUrl.toPercentEncoding(text)))

		http_request_header = Qt.QHttpRequestHeader("GET",
			"/translate_t?sl="+sl+"&tl="+tl+"&text="+text)
		http_request_header.setValue("Host", GoogleTranslateHost)
		http_request_header.setValue("User-Agent", "Mozilla/5.0")

		self.http.setHost(GoogleTranslateHost)
		self.http_request_id = self.http.request(http_request_header)

		self.timer.start()

	def abort(self) :
		self.statusChangedSignal(Qt.QString())
		self.textChangedSignal(self.tr("<em>Aborted</em>"))

		self.http_abort_flag = True
		self.http.abort()
		self.http_abort_flag = False


	### Private ###

	def setStatus(self, state) :
		if state == Qt.QHttp.Unconnected :
			self.statusChangedSignal(Qt.QString())
		elif state == Qt.QHttp.HostLookup :
			self.statusChangedSignal(self.tr("Looking up host..."))
		elif state == Qt.QHttp.Connecting :
			self.statusChangedSignal(self.tr("Connecting..."))
		elif state == Qt.QHttp.Sending :
			self.statusChangedSignal(self.tr("Sending request..."))
		elif state == Qt.QHttp.Reading :
			self.statusChangedSignal(self.tr("Reading data..."))
		elif state == Qt.QHttp.Connected :
			self.statusChangedSignal(self.tr("Connected"))
		elif state == Qt.QHttp.Closing :
			self.statusChangedSignal(self.tr("Closing connection..."))

	def setText(self) :
		self.http_output.append(self.http.readAll())

		codec = Qt.QTextCodec.codecForName("UTF-8")
		text = codec.toUnicode(self.http_output.data())

		index = text.indexOf("<div id=result_box dir=")
		if index != -1 :
			text = text.mid(index)

		index = text.indexOf("</div>")
		if index != -1 :
			# FIXME: string hack
			text = text[29:index]

		self.textChangedSignal(text)

	def requestFinished(self, request_id, error_flag) :
		if request_id != self.http_request_id :
			return

		if error_flag and not self.http_abort_flag :
			Qt.QMessageBox.warning(None, Const.MyName,
				self.tr("HTTP error: %1\nPress \"Yes\" to ignore")
					.arg(self.http.errorString()),
				Qt.QMessageBox.Yes)

		self.timer.stop()

		self.processFinishedSignal()


	### Signals ###

	def processStartedSignal(self) :
		self.emit(Qt.SIGNAL("processStarted()"))

	def processFinishedSignal(self) :
		self.emit(Qt.SIGNAL("processFinished()"))

	def clearRequestSignal(self) :
		self.emit(Qt.SIGNAL("clearRequest()"))

	def wordChangedSignal(self, word) :
		self.emit(Qt.SIGNAL("wordChanged(const QString &)"), word)

	def textChangedSignal(self, text) :
		self.emit(Qt.SIGNAL("textChanged(const QString &)"), text)

	def statusChangedSignal(self, text) :
		self.emit(Qt.SIGNAL("statusChanged(const QString &)"), text)
