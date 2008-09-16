#!/usr/bin/env python
# -*- mode: python; coding: utf-8; -*-

from ftplib import FTP

FTP_LL_HOST = "etc.edu.ru"
FTP_LL_DIR = "pub/soft/for_linux/lightlang/dicts/"

xml_buf = []

def ftp_dir_callback(dir_entry):
	dir_info = dir_entry.split()

	fmode = dir_info[0]
	if fmode[0:1] == "d":
		return

	fname = dir_info[8]
	fsize = dir_info[4]

	i = fname.find(".")
	j = fname.find(".", i+1)
	dname = fname[:i]
	target = fname[i+1:j]

	xml_buf.append("<dictionary file=\"%s\">" % fname)
	xml_buf.append("<name>%s</name>" % dname)
	xml_buf.append("<target>%s</target>" % target)
	xml_buf.append("<size>%s</size>" % fsize)
	xml_buf.append("</dictionary>")

def connect():
	ftp = FTP(FTP_LL_HOST)
	ftp.login()
	ftp.cwd(FTP_LL_DIR)
	ftp.dir(ftp_dir_callback)
	ftp.quit()

if __name__ == "__main__":

	xml_buf.append("<?xml version=\"1.0\" encoding=\"UTF-8\"?>")
	xml_buf.append("<repository author=\"Renat\">")

	connect()

	xml_buf.append("</repository>")
	print "\n".join(xml_buf)
