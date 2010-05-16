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


#ifndef SETTINGS_H
# define SETTINGS_H

# define _GNU_SOURCE

#include <stdbool.h>


# define USER_DICTS_SUBDIR ".sl"

# define DEFAULT_MAX_TERMINAL_LINE_LEN 80
# define DEFAULT_MAX_TRANSLATE_COUNT 50
# define DEFAULT_ILL_DEFINED_SEARCH_PERCENT 40


typedef enum {
	html_output_format,
	text_output_format,
	native_output_format
} output_format_t;

typedef struct {
	char *user_dicts_dir;
	char *locale_encoding;
	int max_terminal_line_len;
	int max_translate_count;
	int ill_defined_search_percent;
	bool use_terminal_escapes_flag;
	bool use_css_flag;
	output_format_t output_format;
} settings_t;


settings_t settings;


int init_settings(void);
int close_settings(void);


#endif // SETTINGS_H

