// SL - system of electronic dictionaries for Linux
// Copyright (C) 2007-2016 Devaev Maxim
//
// This file is part of SL.
//
// This program is free software; you can redistribute it and/or
// modify it under the terms of the GNU General Public License
// as published by the Free Software Foundation; either version 2
// of the License, or (at your option) any later version.
//
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with this program; if not, write to the Free Software
// Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.


#define _GNU_SOURCE

#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <wchar.h>
#include <wctype.h>
#include <ctype.h>
#include <langinfo.h>
#include <sys/types.h>
#include <errno.h>

#include "config.h"
#include "const.h"
#include "settings.h"
#include "string.h"

#include "search_output.h"


void print_begin_page_html(const char *word)
{
	extern settings_t settings;


	printf("<html>\n"
		"<!-- Lisa, I Love You!!! -->\n"
		"<!--      ___  ___       -->\n"
		"<!--     /   \\/   \\      -->\n"
		"<!--    (          )     -->\n"
		"<!--     \\        /      -->\n"
		"<!--      \\      /       -->\n"
		"<!--        \\  /         -->\n"
		"<!--         \\/          -->\n"
		"<!-- ******************* -->\n"
		"<head>\n"
		"\t<title>%s</title>\n"
		"\t<meta name=\"GENERATOR\" content=\"SL Engine\">\n"
		"\t<meta name=\"AUTHOR\" content=\"Devaev Maxim aka Liksys\">\n"
		"\t<meta http-equiv=\"Content-Type\" content=\"text/html; charset=%s\">\n"
		"\t<style type=\"text/css\">\n", word, settings.locale_encoding);

	if ( settings.use_css_flag ) {
		printf("\t\t.dict_header_background {background-color: #DFEDFF;}\n"
			"\t\t.dict_header_font {font-size: large; font-style: italic; font-weight: bold;}\n"
			"\t\t.word_header_font {font-size: normal; color: #494949;}\n"
			"\t\t.list_item_number_font {font-style: italic;}\n"
			"\t\t.article_number_font {font-style: italic; font-weight: bold;}\n"
			"\t\t.strong_font {font-weight: bold;}\n"
			"\t\t.italic_font {font-style: italic;}\n"
			"\t\t.green_font {color: #0A7700;}\n"
			"\t\t.underline_font {font-decoration: underline;}\n"
			"\t\t.word_link_font {color: #DFEDFF; font-decoration: underline;}\n"
			"\t\t.sound_link_font {font-size: normal;}\n"
			"\t\t.info_font {font-style: italic;}\n");	
	}

	printf("\t</style>\n"
		"</head>\n"
		"<body>\n"
		"<!-- translate -->\n");
}

void print_end_page_html(void)
{
	printf("</body>\n</html>\n");
}

void print_separator_html(void)
{
	printf("\t<hr>\n");
}

void print_newline_html(void)
{
	printf("<br>\n");
}

void print_header_html(const char *dict_name, const wchar_t *word_wc)
{
	printf("\t<table border=\"0\" width=\"100%%\"><tr><td align=\"center\" class=\"dict_header_background\"><font class=\"dict_header_font\">");
	for (; *dict_name; ++dict_name) {
		if ( *dict_name == '_' )
			putchar(' ');
		else
			putchar(*dict_name);
	}
	printf("</font></td></tr></table>\n");

	printf("\t<font class=\"word_header_font\">&nbsp;&nbsp;&nbsp;%ls</font>\n", word_wc);
}

void print_list_item_html(const wchar_t *word_wc, const int word_number)
{
	printf("\t(<font class=\"list_item_number_font\">%d</font>) <a href=\"#i_%ls\">%ls</a><br>\n", word_number, word_wc, word_wc);
}

void print_translate_html(const char *str, const int word_number)
{
	int strong_font_count = 0;
	int italic_font_count = 0;
	int green_font_count = 0;
	int block_count = 0;

	bool underline_font_flag = false;
	bool word_link_font_flag = false;
	bool sound_link_font_flag = false;
	bool shield_flag = false;


	printf("\t<dl><dd>\n\t\t(<font class=\"article_number_font\">%d</font>) ", word_number);
	++block_count;

	for (; *str; ++str) {
		if ( *str == '\n' ) {
			shield_flag = false;
			continue;
		}

		if ( *str == '\\' && !shield_flag ) {
			shield_flag = true;
			continue;
		}

		if ( shield_flag ) {
			switch ( *str ) {
				case '[' : {
					printf("<font class=\"strong_font\">");
					++strong_font_count;
					break;
				}
				case ']' : {
					if ( strong_font_count > 0 ) {
						printf("</font>");
						--strong_font_count;
					}
					break;
				}

				case '(' : {
					printf("<font class=\"italic_font\">");
					++italic_font_count;
					break;
				}
				case ')' : {
					if ( italic_font_count > 0 ) {
						printf("</font>");
						--italic_font_count;
					}
					break;
				}

				case '<' : {
					printf("<font class=\"green_font\">");
					++green_font_count;
					break;
				}
				case '>' : {
					if ( green_font_count > 0 ) {
						printf("</font>");
						--green_font_count;
					}
					break;
				}

				case '{' : {
					printf("<dl><dd>");
					++block_count;
					break;
				}
				case '}' : {
					if ( block_count > 0 ) {
						printf("</dd></dl>");
						--block_count;
					}
					break;
				}

				case '_' : {
					if ( !underline_font_flag ) {
						printf("<font class=\"underline_font\">");
						underline_font_flag = true;
					}
					else {
						printf("</font>");
						underline_font_flag = false;
					}
					break;
				}

				case '@' : {
					if ( !word_link_font_flag ) {
						printf("<font class\"word_link_font\">");
						word_link_font_flag = true;
					}
					else {
						printf("</font>");
						word_link_font_flag = false;
					}
					break;
				}

				case 's' : {
					if ( !sound_link_font_flag ) {
						printf("&nbsp;[&nbsp;<a class=\"sound_link_font\"href=\"#s_");
						sound_link_font_flag = true;
					}
					else {
						printf("\">&#9836;</a>&nbsp;]&nbsp;");
						sound_link_font_flag = false;
					}
					break;
				}

				case '\\' : {
					putchar('\\');
					break;
				}

				case 'n' : {
					printf("<br>");
					break;
				}

				case 't' : {
					printf("&nbsp;&nbsp;&nbsp;");
					break;
				}
			}

			shield_flag = false;
			continue;
		}

		if ( *str == '\"' )
			printf("&quot;");
		else if ( *str == '&' )
			printf("&amp;");
		else if ( *str == '<' )
			 printf("&lt;");
		else if ( *str == '>' )
			printf("&gt;");
		else
			putchar(*str);
	}

	for (; strong_font_count > 0; --strong_font_count)
		printf("</font>");
	for (; italic_font_count > 0; --italic_font_count)
		printf("</font>");
	for (; green_font_count > 0; --green_font_count)
		 printf("</font>");
	if ( underline_font_flag )
		printf("</font>");
	if ( word_link_font_flag )
		printf("</font>");
	if ( sound_link_font_flag )
		printf("\">&#9836;</a>&nbsp;]&nbsp;");
	for (; block_count > 0; --block_count)
		printf("</dd></dl>");

	putchar('\n');
}

