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

#include "search_output_native.h"


//void print_begin_page_native(char *word)
//{
//}

//void print_end_page_native(void)
//{
//}

void print_separator_native(void)
{
	putchar('\n');
}

void print_newline_native(void)
{
	putchar('\n');
}

void print_header_native(const char *dict_name, const wchar_t *word_wc)
{
	printf("[[%s]]\n", dict_name);
}

void print_list_item_native(const wchar_t *word_wc, const int word_number)
{
	printf("%ls\n", word_wc);
}

void print_translate_native(const char *str, const int word_number)
{
	for (; *str && *str != '\n'; ++str)
		putchar(*str);
	putchar('\n');
}

