# -*- mode: python; coding: utf-8; -*-

import os
import re
import tempfile


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
		"\\[" : "<span style='font-weight: bold'>",
		"\\]" : "</span>",
		"\\(" : "<span style='font-style: italic'>",
		"\\)" : "</span>",
		"\\{" : "<dl><li>",
		"\\}" : "</li></dl>",
		"\\<" : "<span style='color:#0A7700'>",
		"\\>" : "</span>",
	}
	tmp = multiple_replace(adict, text)
	tmp = re.sub(r"\\s(.*?)\\s", " <a href=\"#sl"+r"\1"+"\"><span style='font-size: 150%'>"+u"\u266B"+"</span></a> ", tmp)
	body = re.sub(r"\\_(.*?)\\_", r"<u>\1</u>", tmp)

	dictionary = os.path.basename(filename)

	header = "<br/>" \
		"<p style='background-color: #DFEDFF; font-weight: bold; text-align: center'>" \
		"%s</p><br/>" % dictionary

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

		if utf8_word[0] != r_word[0]:
			if break_flag:
				break
			else:
				continue
		else:
			break_flag = True

		if mode == 0: # list
			if r_word.startswith(utf8_word):
				lines.append(r_word)
		elif mode == 1: #match
			if r_word == utf8_word:
				html = sl_to_html(utf8_str, filename)
				lines.append(html)

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
	indexating("/tmp/Sokrat-Mova.ru-en")

