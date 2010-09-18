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
#include "search_output_html.h"
#include "search_output_text.h"
#include "search_output_native.h"


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

void print_newline(void)
{
	extern settings_t settings;


	switch ( settings.output_format ) {
		case html_output_format : print_newline_html(); break;
		case text_output_format : print_newline_text(); break;
		case native_output_format : print_newline_native(); break;
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

