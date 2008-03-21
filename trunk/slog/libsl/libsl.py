# -*- mode: python; coding: utf-8; -*-

import os
import re

DICTS_DIR = "/home/renat/opt/lightlang/share/sl/dicts"

def multiple_replace(adict, text):
	#Create a regular expression from all of the dictionary keys
	regex = re.compile("|".join(map(re.escape, adict.keys())))
	# For each match, look up the corresponding value in the dictionary
	return regex.sub(lambda match: adict[match.group(0)], text)

def sl_to_html(text):

	adict = {
		"\\[" : "<strong>",
		"\\]" : "</strong>",
		"\\(" : "<em>",
		"\\)" : "</em>",
		"\\{" : "<dl><dd>",
		"\\}" : "</dd></dl>",
		"\\<" : "<font color=\"#0A7700\">",
		"\\>" : "</font>",
	}
	tmp = multiple_replace(adict, text)
	tmp = re.sub(r"\\s(.*?)\\s", "&nbsp;<a href=\"#sl"+r"\1"+"\">"+u"\u266B"+"</a>&nbsp;", tmp)
	body = re.sub(r"\\_(.*?)\\_", r"<u>\1</u>", tmp)

	header = "<html><head><meta http-equiv=\"Content-Type\" content=\"text/html; charset=UTF-8\"></head><body>"
	footer = "</body></html>"
	
	return header+body+footer

def get_index(filename, char):
		
	pos = -1
	in_tag = False

	fp = open(filename, "r")

	for line in fp:
		if (line[0] == "#") or (line[0] == "\n"):
			continue
		if line.startswith("[noindex]"):
			print >> stderr, "Bad index in %s" % filename
			pos = -1
			break
		if line.startswith("[index]"):
			in_tag = True
			continue
		if not in_tag:
			continue
		if line.startswith("[/index]"):
			break

		wchar = line.split()[0]
		pos = int(line.split()[1])
		
		if wchar == char:
			break

	fp.close()
	return pos

def get_word(line):
	ret = ""
	i = line.find("  ")
	if i != -1:
		ret = line[:i]
	return ret
	
def find_word(word, mode, dictionary):
	if word == "":
		return []

	lines = []
	word_wc = word.lower().rstrip().encode("utf-8")
	filename = os.path.join(DICTS_DIR, dictionary)

	pos = get_index(filename, word_wc[0])
	if pos < 0:
		return lines;

	fp = open(filename, "r")
	fp.seek(pos)

	break_flag = False
	for line in fp:
		if (line[0] == "#") or (line[0] == "\n"):
			continue

		str_wc = line.lower().encode("utf-8")
		gw = get_word(str_wc)
		if gw == "":
			continue

		if word_wc[0] != gw[0]:
			if break_flag:
				break
			else:
				continue
		else:
			break_flag = True

		if mode == 0: # list
			if gw.startswith(word_wc):
				lines.append(gw)
		elif mode == 1: #match
			if gw == word_wc:
				html = sl_to_html(str_wc)
				#print html
				lines.append(html)
		
	fp.close()
	return lines

#Return list with installed dictionaries
def get_installed_dicts():
	return os.listdir(DICTS_DIR)
