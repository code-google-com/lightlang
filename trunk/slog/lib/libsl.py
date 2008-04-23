# -*- mode: python; coding: utf-8; -*-

import os
import re
import tempfile
import gobject

(
	SL_FIND_LIST,
	SL_FIND_MATCH,
	SL_FIND_FUZZY
) = range(3)

FUZZY_MAX_DISTANCE = 4

def get_dict_html_block(filename):
	dictionary = os.path.basename(filename)

	return "<br/>" \
		"<p style='background-color: #DFEDFF; font-weight: bold; text-align: center'>" \
		"%s</p><br/>" % dictionary


# Dictionary filename format: | Dictionary Name |.| Target |.| bz2 |
def filename_parse(fullfilename):
	fname = os.path.basename(fullfilename)
	i = fname.find(".")
	j = fname.find(".", i+1)
	dname = fname[:i]
	if j == -1:
		dtarget = fname[i+1:]
	else:
		dtarget = fname[i+1:j]
	return dname, dtarget

def multiple_replace(adict, text):
	#Create a regular expression from all of the dictionary keys
	regex = re.compile("|".join(map(re.escape, adict.keys())))
	# For each match, look up the corresponding value in the dictionary
	return regex.sub(lambda match: adict[match.group(0)], text)

def sl_to_html(text, filename):

	adict = {
		"\\[" : "<span style='font-weight: bold'> ",
		"\\]" : " </span>",
		"\\(" : "<span style='font-style: italic'> ",
		"\\)" : " </span>",
		"\\{" : "<dl><li>",
		"\\}" : "</li></dl>",
		"\\<" : "<span style='color:#0A7700'> ",
		"\\>" : " </span>",
	}
	tmp = multiple_replace(adict, text)
	href_sound = "[<a href=\"#sl"+r"\1"+"\"><span style='font-size: 150%'>"+u"\u266B"+"</span></a>]"
	tmp = re.sub(r"\\s(.*?)\\s", href_sound, tmp)
	body = re.sub(r"\\_(.*?)\\_", r"<u>\1</u>", tmp)

	header = get_dict_html_block(filename)

	return (header + body + "<br/>")

def get_index(filename, w_char):
	pos = -1
	in_tag = False

	try:
		fp = open(filename, "r")
	except IOError, ioerr:
		print str(ioerr)
		return pos

	for line in fp:
		if (line[0] == "#") or (line[0] == "\n"):
			continue
		if line.startswith("[noindex]"):
			print "Bad index in %s" % filename
			pos = -1
			break
		if line.startswith("[index]"):
			in_tag = True
			continue
		if not in_tag:
			continue
		if line.startswith("[/index]"):
			break

		f_char = line.split()[0].decode("utf-8")
		pos = int(line.split()[1])

		if w_char == f_char:
			break

	fp.close()
	return pos

# From mstring.c (c) Maxim Devaev
def strcmp_jump(a, b, percent = 40):
	errors = 0
	n, m = len(a), len(b)

	if n > m:
		a, b = b, a
		n, m = m, n

	hard_find = (n*percent)/100

	if n == m:
		for i in xrange(n):
			if a[i] != b[i]:
				errors += 1
				if errors > hard_find:
					return 1
		return 0
	else:
		j = 0
		for i in xrange(n):

			if a[i] == b[j]:
				continue
			elif a[i] == b[j+1]:
				errors += 1
				j += 1
			else:
				errors += 1

			if (errors + (m - n)) > hard_find:
				return 1

			j += 1

		if (errors + (m - n)) <= hard_find:
			return 0

	return 1

# (c) From Wikipedia 
def levenshtein(a, b):
	"""Calculates the Levenshtein distance
		between a and b. """

	n, m = len(a), len(b)

	# My optimization
	if abs(n - m) > 2:
		return FUZZY_MAX_DISTANCE + 1

	if n > m:
		# Make sure n <= m, to use O(min(n,m)) space
		a, b = b, a
		n, m = m, n

	current = range(n+1)
	for i in xrange(1, m+1):
		previous, current = current, [i]+[0]*n
		for j in xrange(1, n+1):
			add, delete = previous[j]+1, current[j-1]+1
			change = previous[j-1]
			if a[j-1] != b[i-1]:
				change = change + 1
			current[j] = min(add, delete, change)

	return current[n]

def find_word(word, mode, filename):
	if word == "":
		return []

	lines = []
	utf8_word = word.lower().rstrip().decode("utf-8")

	pos = get_index(filename, utf8_word[0])
	if pos < 0:
		return lines;

	fp = open(filename, "r")
	fp.seek(pos)

	break_flag = False
	for line in fp:
		if (line[0] == "#") or (line[0] == "\n"):
			continue

		utf8_str = line.decode("utf-8").lower()

		i = utf8_str.find(u"  ")
		if i != -1:
			r_word = utf8_str[:i]
		else:
			continue

		if mode != SL_FIND_FUZZY:
			if utf8_word[0] != r_word[0]:
				if break_flag:
					break
				else:
					continue
			else:
				break_flag = True

		if mode == SL_FIND_LIST: # list
			if r_word.startswith(utf8_word):
				lines.append(r_word)
		elif mode == SL_FIND_MATCH: #match
			if r_word == utf8_word:
				html = sl_to_html(utf8_str, filename)
				lines.append(html)
		elif mode == SL_FIND_FUZZY:
				#if levenshtein(r_word, utf8_word) < FUZZY_MAX_DISTANCE:
				if strcmp_jump(r_word, utf8_word) == 0:
					lines.append(r_word)

		# Save memory
		if len(lines) > 50:
			break

	fp.close()
	return lines

def create_index(fp):
	ch_wc = u"\0"
	index = ["[index]\n"]
	fp.seek(0)
	while True:
		pos = fp.tell()

		line = fp.readline()
		if line == "":
			break

		if (line[0] == "#") or (line[0] == "\n"):
			continue

		i = line.find("  ")
		if i == -1:
			continue

		w_str = line.decode("utf-8").lower()

		fch = w_str[0]
		if ch_wc != fch:
			ch_wc = fch
			w_str = u"%lc %ld\n" % (ch_wc, pos)
			index.append(w_str.encode("utf-8"))

	index.append("[/index]\n")
	return index

def indexating(filename):
	fp = open(filename, "r")
	index = create_index(fp)
	fp.seek(0)

	tmp = tempfile.TemporaryFile()
	tmp.writelines(index)
	for line in fp:
		tmp.write(line)
	index = create_index(tmp)
	tmp.close()

	fp.seek(0)
	filename_res = filename + ".res"
	fr = open(filename_res, "w")
	fr.writelines(index)
	for line in fp:
		fr.write(line)
	fr.close()
	fp.close()

#Unit test
if __name__ == "__main__":
	#indexating("/tmp/Sokrat-Mova.ru-en")
	dicts = ("/home/rnt/opt/lightlang/share/sl/dicts/EngFree.en-ru", "/home/rnt/opt/lightlang/share/sl/dicts/Mueller-7.en-ru")
	for fname in dicts:
		items = find_word("LightLang", SL_FIND_FUZZY, fname)
		print fname
		print items
http://dpaste.com/hold/46529/
