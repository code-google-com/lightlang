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


import Qt
import Const
import Config
import Locale


#####
GoogleTranslateHost = "translate.google.com"


#####
def tr(str) :
	return Qt.QApplication.translate("@default", str)


#####
class GoogleTranslate(Qt.QObject) :
	def __init__(self, parent = None) :
		Qt.QObject.__init__(self, parent)

		#####

		self.http = Qt.QHttp()
		self.http_request_id = -1
		self.http_abort_flag = False

		self.http_output = Qt.QByteArray()

		self.timer = Qt.QTimer()
		self.timer.setInterval(30000)

		self.lang = Locale.mainLang()

		self.direction_regexp = Qt.QRegExp("<td id=autotrans style=.*>(<span class=.*>.*</span>.*)</td>")
		self.direction_regexp.setMinimal(True)

		self.translate_regexp = Qt.QRegExp("<div id=result_box .*>(.*)</div>")
		self.translate_regexp.setMinimal(True)

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

		self.wordChangedSignal(tr("Google Translate"))
		self.textChangedSignal(tr("<em>Please wait...</em>"))

		text = text.trimmed()

		###

		if text.startsWith("http:", Qt.Qt.CaseInsensitive) :
			Qt.QDesktopServices.openUrl(Qt.QUrl(Qt.QString("http://%1/translate?hl=%2&sl=%3&tl=%4&u=%5&client=t")
				.arg(GoogleTranslateHost).arg(self.lang).arg(sl).arg(tl).arg(text)))
			self.textChangedSignal(tr("<em>Link <strong>%1</strong> translation was opened in your browser</em>").arg(text))
			self.processFinishedSignal()
			return

		###

		text = Qt.QString.fromLocal8Bit(str(Qt.QUrl.toPercentEncoding(text)))

		http_request_header = Qt.QHttpRequestHeader("POST", (Qt.QString("/translate_t?client=t&hl=%1&sl=%2&tl=%3")
			.arg(self.lang).arg(sl).arg(tl)), 1, 1)
		http_request_header.setValue("Host", GoogleTranslateHost)
		http_request_header.setValue("User-Agent", "Mozilla/5.0")
		http_request_header.setContentLength(text.length())
		http_request_header.setValue("Connection", "Close")

		bytes = Qt.QByteArray("text=")
		bytes.append(text)

		self.http.setHost(GoogleTranslateHost)
		self.http_request_id = self.http.request(http_request_header, bytes)

		self.timer.start()

	def abort(self) :
		self.http_abort_flag = True
		self.http.abort()
		self.http_abort_flag = False

		self.statusChangedSignal(Qt.QString())
		self.textChangedSignal(tr("<em>Aborted</em>"))


	### Private ###

	def setStatus(self, state) :
		if state == Qt.QHttp.Unconnected :
			self.statusChangedSignal(Qt.QString())
		elif state == Qt.QHttp.HostLookup :
			self.statusChangedSignal(tr("Looking up host..."))
		elif state == Qt.QHttp.Connecting :
			self.statusChangedSignal(tr("Connecting..."))
		elif state == Qt.QHttp.Sending :
			self.statusChangedSignal(tr("Sending request..."))
		elif state == Qt.QHttp.Reading :
			self.statusChangedSignal(tr("Reading data..."))
		elif state == Qt.QHttp.Connected :
			self.statusChangedSignal(tr("Connected"))
		elif state == Qt.QHttp.Closing :
			self.statusChangedSignal(tr("Closing connection..."))

	def setText(self) :
		self.http_output.append(self.http.readAll())

	def requestFinished(self, request_id, error_flag) :
		if request_id != self.http_request_id :
			return

		if error_flag and not self.http_abort_flag :
			Qt.QMessageBox.warning(None, Const.MyName,
				tr("HTTP error: %1\nPress \"Yes\" to ignore").arg(self.http.errorString()),
				Qt.QMessageBox.Yes)

		self.timer.stop()

		codec = Qt.QTextCodec.codecForName("UTF-8")
		text = codec.toUnicode(self.http_output.data())

		###

		direction_index = self.direction_regexp.indexIn(text)
		translate_index = self.translate_regexp.indexIn(text)
		if direction_index > -1 and translate_index > -1 :
			text = ( Qt.QString("<font color=\"#494949\">%1</font><hr>%2")
				.arg(self.direction_regexp.cap(1)).arg(self.translate_regexp.cap(1)) )
		elif translate_index > -1 :
			text = self.translate_regexp.cap(1)

		###

		self.textChangedSignal(text)

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

