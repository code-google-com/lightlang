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

static void print_begin_page_html(const char *word);
//static void print_begin_page_text(const char *word);
//static void print_begin_page_native(const char *word);

static void print_end_page_html(void);
//static void print_end_page_text(void);
//static void print_end_page_native(void);

static void print_separator_html(void);
static void print_separator_text(void);
static void print_separator_native(void);

static void print_header_html(const char *dict_name, const wchar_t *word_wc);
static void print_header_text(const char *dict_name, const wchar_t *word_wc);
static void print_header_native(const char *dict_name, const wchar_t *word_wc);

static void print_list_item_html(const wchar_t *word_wc, const int word_number);
static void print_list_item_text(const wchar_t *word_wc, const int word_number);
static void print_list_item_native(const wchar_t *word_wc, const int word_number);

static void print_translate_html(const char *str, const int word_number);
static void print_translate_text(const char *str, const int word_number);
static void print_translate_native(const char *str, const int word_number);


void print_begin_page(const char *word)
{
	extern settings_t settings;


	switch ( settings.output_format ) {
		case html_output_format : print_begin_page_html(word); break;
		case text_output_format : break;
		case native_output_format : break;
//		case text_output_format : print_begin_page_text(word); break;
//		case native_output_format : print_begin_page_native(word); break;
	}
}

void print_end_page(void)
{
	extern settings_t settings;


	switch ( settings.output_format ) {
		case html_output_format : print_end_page_html(); break;
		case text_output_format : break;
		case native_output_format : break;
//		case text_output_format : print_end_page_text(); break;
//		case native_output_format : print_end_page_native(); break;
	}
}

void print_separator(void)
{
	extern settings_t settings;


	switch ( settings.output_format ) {
		case html_output_format : print_separator_html(); break;
		case text_output_format : print_separator_text(); break;
		case native_output_format : print_separator_native(); break;
	}
}

void print_header(const char *dict_name, const wchar_t *word_wc)
{
	extern settings_t settings;


	switch ( settings.output_format ) {
		case html_output_format : print_header_html(dict_name, word_wc); break;
		case text_output_format : print_header_text(dict_name, word_wc); break;
		case native_output_format : print_header_native(dict_name, word_wc); break;
	}
}

void print_list_item(const wchar_t *word_wc, const int word_number)
{
	extern settings_t settings;


	switch ( settings.output_format ) {
		case html_output_format : print_list_item_html(word_wc, word_number); break;
		case text_output_format : print_list_item_text(word_wc, word_number); break;
		case native_output_format : print_list_item_native(word_wc, word_number); break;
	}
}

void print_translate(const char *str, const int word_number)
{
	extern settings_t settings;


	switch ( settings.output_format ) {
		case html_output_format : print_translate_html(str, word_number); break;
		case text_output_format : print_translate_text(str, word_number); break;
		case native_output_format : print_translate_native(str, word_number); break;
	}
}


static void print_begin_page_html(const char *word)
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
		puts("\t\t.dict_header_background {background-color: #DFEDFF;}\n"
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
			"\t\t.info_font {font-style: italic;}");	
	}

	puts("\t</style>\n"
		"</head>\n"
		"<body>\n"
		"<!-- translate -->");
}

//static void print_begin_page_text(char *word)
//{
//}

//static void print_begin_page_native(char *word)
//{
//}


static void print_end_page_html(void)
{
	printf("</body>\n</html>\n");
}

//static void print_end_page_text(void)
//{
//}

//static void print_end_page_native(void)
//{
//}


static void print_separator_html(void)
{
	puts("\t<hr>");
}

static void print_separator_text(void)
{
	int count;
	extern settings_t settings;


	for (count = 0; count < settings.max_terminal_line_len; ++count)
		putchar('-');
	putchar('\n');
}

static void print_separator_native(void)
{
	putchar('\n');
}


static void print_header_html(const char *dict_name, const wchar_t *word_wc)
{
	print_separator_html();

	printf("\t<table border=\"0\" width=\"100%%\"><tr><td align=\"center\" class=\"dict_header_background\"><font class=\"dict_header_font\">");
	for (; *dict_name; ++dict_name) {
		if ( *dict_name == '_' )
			putchar(' ');
		else
			putchar(*dict_name);
	}
	printf("</font></td></tr></table>\n");

	print_separator_html();

	printf("\t<font class=\"word_header_font\">&nbsp;&nbsp;&nbsp;%ls</font>\n", word_wc);

	print_separator_html();
}

static void print_header_text(const char *dict_name, const wchar_t *word_wc)
{
	int count;
	extern settings_t settings;


	print_separator_text();

	if ( strlen(dict_name) >= settings.max_terminal_line_len ) {
		puts(dict_name);
	}
	else {
		for (count = 0; count < (settings.max_terminal_line_len - strlen(dict_name)) / 2; ++count)
			putchar('=');
		putchar(' ');

		if ( settings.use_terminal_escapes_flag )
			printf("\033[1m");

		for (++count; *dict_name; ++dict_name, ++count) {
			if ( *dict_name == '_' )
				putchar(' ');
			else
				putchar(*dict_name);
		}

		if ( settings.use_terminal_escapes_flag )
			printf("\033[0m");

		putchar(' ');
		for (++count; count < settings.max_terminal_line_len; ++count)
			putchar('=');

		putchar('\n');
	}

	print_separator_text();

	printf("\n\t<< %ls >>\n", word_wc);

	print_separator_text();
}

static void print_header_native(const char *dict_name, const wchar_t *word_wc)
{
	printf("[[%s]]\n", dict_name);
}


static void print_list_item_html(const wchar_t *word_wc, const int word_number)
{
	printf("\t(<font class=\"list_item_number_font\">%d</font>) <a href=\"#i_%ls\">%ls</a><br>\n", word_number, word_wc, word_wc);
}

static void print_list_item_text(const wchar_t *word_wc, const int word_number)
{
	extern settings_t settings;


	if ( settings.use_terminal_escapes_flag )
		printf(" \033[1m(%d)\033[0m %ls\n", word_number, word_wc);
	else
		printf(" (%d) %ls\n", word_number, word_wc);
}

static void print_list_item_native(const wchar_t *word_wc, const int word_number)
{
	printf("%ls\n", word_wc);
}


static void print_translate_html(const char *str, const int word_number)
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
						printf("\">\u266B</a>&nbsp;]&nbsp;");
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
		printf("\">\u266B</a>&nbsp;]&nbsp;");
	for (; block_count > 0; --block_count)
		printf("</dd></dl>");

	putchar('\n');
}

static void print_translate_text(const char *str, const int word_number)
{
	wchar_t str_ch_wc;
	size_t str_offset = 0;
	mbstate_t mb_state;
	int block_count = 0;
	int char_count = 0;
	int count = 0;
	bool strong_font_flag = false;
	bool green_font_flag = false;
	bool underline_font_flag = false;
	bool word_link_font_flag = false;
	bool sound_link_font_flag = false;
	bool shield_flag = false;
	extern settings_t settings;


	memset(&mb_state, 0, sizeof(mb_state));

	if ( settings.use_terminal_escapes_flag )
		printf("   \033[1m(%d)\033[0m ", word_number);
	else
		printf("   (%d) ", word_number);

	for (; (str_offset = mbrtowc(&str_ch_wc, str, sizeof(wchar_t), &mb_state)) > 0; str += str_offset) {
		if ( str_ch_wc == L'\n' ) {
			shield_flag = false;
			continue;
		}

		if ( str_ch_wc == L'\\' && !shield_flag ) {
			shield_flag = true;
			continue;
		}

		if ( shield_flag ) {
			switch ( str_ch_wc ) {
				case L'[' : {
					if ( settings.use_terminal_escapes_flag ) {
						printf("\033[1m");
						strong_font_flag = true;
					}
					break;
				}
				case L']' : {
					if ( settings.use_terminal_escapes_flag ) {
						 printf("\033[0m");
						if ( green_font_flag )
							printf("\033[32m");
						if ( underline_font_flag )
							printf("\033[4m");
						strong_font_flag = false;
					}
					break;
				}

				case L'<' : {
					if ( settings.use_terminal_escapes_flag ) {
						printf("\033[32m");
						green_font_flag = true;
					}
					break;
				}
				case L'>' : {
					if ( settings.use_terminal_escapes_flag ) {
						printf("\033[0m");
						if ( strong_font_flag )
							printf("\033[1m");
						if ( underline_font_flag )
							printf("\033[4m");
						green_font_flag = false;
					}
					break;
				}

				case L'{' : {
					block_count += 3;
					char_count = block_count;
					putchar('\n');
					for (count = 0; count < block_count; ++count)
						putchar(' ');
					break;
				}
				case L'}' : {
					block_count -= 3;
					if ( block_count < 0 )
						block_count = 0;
					char_count = block_count;
					break;
				}

				case L'_' : {
					if ( settings.use_terminal_escapes_flag ) {
						if ( !underline_font_flag ) {
							printf("\033[4m");
							underline_font_flag = true;
						}
						else {
							printf("\033[24m");
							underline_font_flag = false;
						}
					}
					break;
				}

				case L'@' : {
					if ( settings.use_terminal_escapes_flag ) {
						if ( !word_link_font_flag ) {
							printf("\033[4m");
							word_link_font_flag = true;
						}
						else {
							printf("\033[24m");
							word_link_font_flag = false;
						}
					}
					break;
				}

				case L's' : {
					if ( settings.use_terminal_escapes_flag ) {
						if ( !sound_link_font_flag ) {
							printf("[\033[4msnd:\"");
							sound_link_font_flag = true;
						}
						else {
							printf("\"\033[24m]");
							sound_link_font_flag = false;
						}
					}
					break;
				}

				case L'\\' : {
					putchar('\\');
					break;
				}

				case L'n' : {
					putchar('\n');
					break;
				}

				case L't' : {
					putchar('\t');
					break;
				}
			}

			shield_flag = false;
			continue;
		}

		if ( char_count > (int) ((float) settings.max_terminal_line_len * TERMINAL_TEXT_PART) && str_ch_wc == L' ' && !isdigit(*(str + 1)) ) {
			putchar('\n');
			for (count = 0; count < block_count + 3; ++count)
				putchar(' ');
			char_count = block_count + 3;
		}

		printf("%lc", str_ch_wc); // putwchar() - DON'T WORK!

		++char_count;
	}

	if ( settings.use_terminal_escapes_flag )
		printf("\033[0m"); // Reset terminal settings

	putchar('\n');
}

static void print_translate_native(const char *str, const int word_number)
{
	for (; *str && *str != '\n'; ++str)
		putchar(*str);
	putchar('\n');
}

