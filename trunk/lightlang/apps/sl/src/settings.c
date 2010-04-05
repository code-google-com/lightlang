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
#include <string.h>
#include <stdbool.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <sys/ioctl.h>
#include <locale.h>
#include <langinfo.h>
#include <errno.h>

#include "const.h"

#include "settings.h"

static int init_settings_locale(void);
static int init_settings_user_dicts_dir(void);
static int init_settings_locale_encoding(void);
static int init_settings_max_terminal_line_len(void);
static int init_settings_use_terminal_escapes_flag(void);


int init_settings(void)
{
	extern settings_t settings;


	if ( init_settings_locale() != 0 )
		return -1;
	if ( init_settings_user_dicts_dir() != 0 )
		return -1;

	init_settings_locale_encoding();
	init_settings_max_terminal_line_len();
	init_settings_use_terminal_escapes_flag();

	settings.max_translate_count = DEFAULT_MAX_TRANSLATE_COUNT;
	settings.ill_defined_search_percent = DEFAULT_ILL_DEFINED_SEARCH_PERCENT;
	settings.output_format = text_output_format;
	settings.use_css_flag = true;

	return 0;
}

int close_settings(void)
{
	extern settings_t settings;


	free(settings.user_dicts_dir);

	return 0;
}


static int init_settings_locale(void)
{
	if ( setlocale(LC_ALL, "") == NULL && setlocale(LC_CTYPE, "") == NULL ) {
		fprintf(stderr, "%s: init: cannot change locale: %s\n", MYNAME, strerror(errno));
		return -1;
	}

	return 0;
}

static int init_settings_user_dicts_dir(void)
{
	char *home_dir;
	size_t user_dicts_dir_len;
	extern settings_t settings;


	if ( (home_dir = getenv("HOME")) == NULL ) {
		fprintf(stderr, "%s: cannot \"$HOME\" value: %s\n", MYNAME, strerror(errno));
		return -1;
	}

	user_dicts_dir_len = (strlen(home_dir) + strlen(USER_DICTS_SUBDIR) + 16) * sizeof(char);

	if ( (settings.user_dicts_dir = (char *) malloc(user_dicts_dir_len)) == NULL ) {
		fprintf(stderr, "%s: memory error (%s, file %s, line %d), please report to \"%s\"\n",
			MYNAME, strerror(errno), __FILE__, __LINE__, BUGTRACK_MAIL );
		return -1;
	}

	sprintf(settings.user_dicts_dir, "%s/%s", home_dir, USER_DICTS_SUBDIR);

	if ( access(settings.user_dicts_dir, F_OK) != 0 ) {
		if ( mkdir(settings.user_dicts_dir, 0755) != 0 ) {
			fprintf(stderr, "%s: cannot create user dicts folder \"%s\": %s\n", MYNAME, settings.user_dicts_dir, strerror(errno));
			return -1;
		}
	}

	return 0;
}

static int init_settings_locale_encoding(void)
{
	extern settings_t settings;


	if ( (settings.locale_encoding = nl_langinfo(CODESET)) == NULL )
		settings.locale_encoding = "";

	return 0;
}

static int init_settings_max_terminal_line_len(void)
{
	char *max_terminal_line_len_str;
	struct winsize win_size;
	extern settings_t settings;


	if ( (max_terminal_line_len_str = getenv("COLUMNS")) != NULL ) {
		if ( (settings.max_terminal_line_len = atoi(max_terminal_line_len_str)) != 0 )
			return 0;
	}

	if ( ioctl(1, TIOCGWINSZ, &win_size) == 0 ) {
		settings.max_terminal_line_len = win_size.ws_col;
		return 0;
	}

	settings.max_terminal_line_len = DEFAULT_MAX_TERMINAL_LINE_LEN;

	return 0;
}

static int init_settings_use_terminal_escapes_flag(void)
{
	extern settings_t settings;

	/**************************************
	*       _,,,_   _,,,,,,,_   ___       *
	*     .'     `.' _,,,,,,_`.'   `,     *
	*     ;        ,'  _    _`.     ;     *
	*     ;        ;  (D)  (D);     ;     *
	*     t        ;      ^   ;     ;     *
	*      \        L_   `-' ,'     j     *
	*       `.    ,' J`"r==r' `.   /      *
	*         `--' ,'   t  |\   `-'       *
	*            ,' /7   \_/ \_           *
	*           (,,J/      |\,,)          *
	*               \____ _L              *
	*               (,,,,),,)             *
	**************************************/

	settings.use_terminal_escapes_flag = (bool) isatty(1);

	return 0;
}

