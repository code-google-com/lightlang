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

/********************************************************************************
*										*
*	search.h - funkcii poiskovoy sistemy programmy.				*
*										*
********************************************************************************/

#ifndef SEARCH_H
# define SEARCH_H

# define _GNU_SOURCE

# include <stdlib.h>
# include <stdbool.h>
# include <wchar.h>

/*********************************** Macro *************************************/
# define ALL_SOUNDS_DIR		__PREFIX "/share/sl/sounds"

# define AUDIO_POSTFIX		".ogg"

# define MAX_WORD_SIZE		256
/*********************************** Types *************************************/
typedef enum {
	usually_regimen,
	first_concurrence_regimen,
	word_combinations_regimen,
	list_regimen,
	ill_defined_regimen
} regimen_t;

/********************************* Functions ***********************************/
int find_word(const char *word, const regimen_t regimen, const int percent, const char *dict_name, FILE *dict_fp);
int find_sound(const char *word);

static long read_index(const wchar_t ch_wc, FILE *dict_fp);

void print_begin_page(const char *word);
void print_end_page(void);
static void print_separator(void);
static void print_header(const char *dict_name);

static void print_list_item(const wchar_t *word_wc, const int word_number);
static void print_translate(const char *str, const int number);

#endif

/********************************************************************************
*********************************************************************************
********************************************************************************/
