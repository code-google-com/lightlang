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
*	settings.c - nastroyki sistemy poiska.					*
*										*
*		Vkluchet tip dlya hraneniya nastroek, globalnuyu peremennuyu	*
*		s nastroykami i funkcii dlya zagruzki/vygruzki nastroek.	*
*										*
********************************************************************************/

#ifndef SETTINGS_H
# define SETTINGS_H

# define _GNU_SOURCE

#include <stdbool.h>

/*********************************** Macro *************************************/
# define USER_DICTS_SUBDIR		".sl"	// Podkatalog polzovatelya

# define DEFAULT_MAX_TERMINAL_LINE_LEN	80	// Dlina stroki terminala
# define DEFAULT_MAX_TRANSLATE_COUNT	50	// Kolichestvo perevodov

/*********************************** Types *************************************/
typedef enum {				// Tip formata vyvoda
	html_output_format,		// HTML-format
	text_output_format,		// Textovyy format
	native_output_format		// Nativnyy format
} output_format_t;

typedef struct {			// Tip parametrov sistemy
	char *user_dicts_dir;		// Polzovatelskiy podkatalog slovarey
	char *locale_encoding;		// Kodirovka
	int max_terminal_line_len;	// Dlina stroki terminala
	int max_translate_count;
	bool use_terminal_escapes_flag;
	output_format_t output_format;	// Format vyvoda
} settings_t;

/******************************* Global values *********************************/
settings_t settings;			// Parametry sistemy

/********************************* Functions ***********************************/
int init_settings(void);	// Inicializiruet parametry sistemy
int close_settings(void);	// Zakryvaet parametry sistemy

static int init_locale(void);
static int init_user_dicts_dir(void);
static int init_locale_encoding(void);
static int init_max_terminal_line_len(void);
static int init_use_terminal_escapes_flag(void);

#endif

/********************************************************************************
*********************************************************************************
********************************************************************************/
