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


import json

import Qt
import Const
import Config
import Locale
import LangsList


##### Public classes #####
class GoogleTranslate(Qt.QObject) :
	def __init__(self, parent = None) :
		Qt.QObject.__init__(self, parent)

		#####

		self._http = Qt.QHttp()
		self._http_request_id = -1
		self._http_abort_flag = False

		self._http_output = Qt.QByteArray()

		self._timer = Qt.QTimer()
		self._timer.setInterval(30000)

		self._sl = Qt.QString()
		self._tl = Qt.QString()

		#####

		self.connect(self._http, Qt.SIGNAL("stateChanged(int)"), self.setStatus)
		self.connect(self._http, Qt.SIGNAL("requestFinished(int, bool)"), self.requestFinished)
		self.connect(self._http, Qt.SIGNAL("readyRead(const QHttpResponseHeader &)"), self.setText)

		self.connect(self._timer, Qt.SIGNAL("timeout()"), self.abort)


	### Public ###

	def translate(self, sl, tl, text) :
		self._http_abort_flag = True
		self._http.abort()
		self._http_abort_flag = False

		self.processStartedSignal()

		self.clearRequestSignal()

		self._http.clearPendingRequests()
		self._http_output.clear()

		self.wordChangedSignal(tr("Google Translate"))
		self.textChangedSignal(tr("<font class=\"info_font\">Please wait...</font>"))

		text = text.trimmed()

		self._sl = sl
		self._tl = tl

		###

		if text.startsWith("http:", Qt.Qt.CaseInsensitive) :
			site = ( Qt.QString("http://translate.google.com/translate?js=y&prev=_t&hl=%1&ie=UTF-8&sl=%2&tl=%3&u=%4")
				.arg(Locale.mainLang()).arg(sl).arg(tl).arg(text) )
			Qt.QDesktopServices.openUrl(Qt.QUrl(site))
			self.textChangedSignal(tr("<font class=\"word_header_font\">Link of site \"%1\" translation"
				" was opened in your browser</font><hr><br><a href=\"%2\">%2</a>").arg(text).arg(site))
			self.processFinishedSignal()
			return

		###

		text = Qt.Qt.escape(text)
		text.replace("\"", "&quot;")
		text.replace("\n", "<br>")

		text = Qt.QString.fromLocal8Bit(str(Qt.QUrl.toPercentEncoding(text)))
		text = Qt.QByteArray().append("q="+text)

		http_request_header = Qt.QHttpRequestHeader("POST",
			Qt.QString("/ajax/services/language/translate?v=1.0&type=html&langpair=%1%7C%2").arg(sl).arg(tl), 1, 1)
		http_request_header.setValue("Host", "ajax.googleapis.com")
		http_request_header.setValue("User-Agent", "Mozilla/5.0")
		http_request_header.setValue("Accept", "*/*")
		http_request_header.setValue("Content-Type", "application/x-www-form-urlencoded")
		http_request_header.setContentLength(text.length())
		http_request_header.setValue("Connection", "close")

		self._http.setHost("ajax.googleapis.com")
		self._http_request_id = self._http.request(http_request_header, text)

		self._timer.start()

	def abort(self) :
		self._http_abort_flag = True
		self._http.abort()
		self._http_abort_flag = False

		self.statusChangedSignal(Qt.QString())
		self.textChangedSignal(tr("<font class=\"info_font\">Aborted</font>"))


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
		self._http_output.append(self._http.readAll())

	def requestFinished(self, request_id, error_flag) :
		if request_id != self._http_request_id :
			return

		if error_flag and not self._http_abort_flag :
			Qt.QMessageBox.warning(None, Const.MyName,
				tr("HTTP error: %1\nPress \"Yes\" to ignore").arg(self._http.errorString()),
				Qt.QMessageBox.Yes)

		self._timer.stop()

		###

		text = Qt.QTextCodec.codecForName("UTF-8").toUnicode(self._http_output.data())

		###

		try :
			json_dict = json.loads(unicode(text).encode("utf-8"))
		except :
			json_dict = None

		if json_dict != None :
			if json_dict.has_key("responseData") and json_dict.has_key("responseStatus") and json_dict.has_key("responseDetails") :
				responce_data = json_dict["responseData"]
				responce_status = json_dict["responseStatus"]
				responce_details = json_dict["responseDetails"]

				if responce_data != None :
					if responce_data.has_key("detectedSourceLanguage") :
						sl_name = tr("%1 (guessed)").arg(LangsList.langName(responce_data["detectedSourceLanguage"]))
					else :
						sl_name = LangsList.langName(self._sl)
					tl_name = LangsList.langName(self._tl)

					text = ( tr("<font class=\"word_header_font\">Translated: %1 &#187; %2</font><hr>%3")
						.arg(sl_name).arg(tl_name).arg(Qt.QString(responce_data["translatedText"])) )
				else :
					text = ( tr("<font class=\"word_header_font\">Invalid server responce</font><hr>Code: %1<br>Message: %2")
						.arg(responce_status).arg(responce_details) )
			else :
				text = ( tr("<font class=\"word_header_font\">Invalid server responce</font><hr>Raw JSON: %1")
					.arg(Qt.QString(unicode(json_dict).encode("utf-8"))) )

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

