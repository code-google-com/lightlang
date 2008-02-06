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

#define _GNU_SOURCE

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <locale.h>
#include <langinfo.h>
#include <errno.h>

#include "const.h"

#include "settings.h"

/********************************************************************************
*										*
*	init_settings() - inicializiruet znacheniyami strukturu <settings>.	*
*										*
*		Vozvrashaet 0 v sluche uspeha i -1 pri oshibke.			*
*										*
*		Pered zaversheniem raboty programmy neobhodimo vyzvat		*
*		funkciyu close_settings() dlya ochistki struktury <settings>.	*
*										*
********************************************************************************/
int init_settings(void)
{
	//////////////////////////////////
	extern settings_t settings;	// Nastroyki sistemy
	//////////////////////////////////


	if ( init_locale() != 0 )		return -1;
	if ( init_user_dicts_dir() != 0 )	return -1;
	if ( init_locale_encoding() != 0 )	{}
	if ( init_max_terminal_line_len() != 0 ){}
	if ( init_use_terminal_escapes_flag() != 0 ){}

	settings.output_format = text_output_format;

	return 0;
}

/********************************************************************************
*										*
*	close_settings() - zakryvaet nastroyki sistemy poiska.			*
*										*
********************************************************************************/
int close_settings(void)
{
	//////////////////////////////////
	extern settings_t settings;	// Nastroyki sisteny poiska
	//////////////////////////////////


	// Osvobojdaem pamyat ...
	free(settings.user_dicts_dir);

	return 0;
}

/********************************************************************************
*										*
*	init_locale() - inicializaciya lokali.					*
*										*
********************************************************************************/
static int init_locale(void)
{
	if ( (setlocale(LC_ALL, "") == NULL) && (setlocale(LC_CTYPE, "") == NULL) )
	{
		fprintf(stderr, "%s: init: cannot change locale: %s\n",
			MYNAME, strerror(errno) );
		return -1;
	}

	return 0;
}

/********************************************************************************
*										*
*	init_user_dicts_dir() - poluchenie polzovatelskogo kataloga so		*
*		slovaryami putem polucheniya znacheniya peremennoy <$HOME>	*
*		i dobavleniya prefixa.						*
*										*
********************************************************************************/
static int init_user_dicts_dir(void)
{
	//////////////////////////////////
	char	*home_dir;		// Domashniy katalog
	size_t	user_dicts_dir_len;	// Dlina polzovatelskogo kataloga
	extern settings_t settings;	// Nastroyki sistemy
	//////////////////////////////////


	// Poluchaem domashniy katalog polzovatelya
	if ( (home_dir = getenv("HOME")) == NULL )
	{
		fprintf(stderr, "%s: cannot \"$HOME\" value: %s\n",
			MYNAME, strerror(errno) );
		return -1;
	}

	// Vychislyaem razmer pamyati, neobhodimyy dlya
	// polzovatelskogo kataloga so slovaryami
	user_dicts_dir_len = (strlen(home_dir) + strlen(USER_DICTS_SUBDIR) + 16) * sizeof(char);

	// Vydelyaem pamyat ...
	if ( (settings.user_dicts_dir = (char *) malloc(user_dicts_dir_len)) == NULL )
	{
		fprintf(stderr, "%s: memory error (%s, file %s, line %d), please report to \"%s\"\n",
			MYNAME, strerror(errno), __FILE__, __LINE__, BUGTRACK_MAIL );
		return -1;
	}

	// Sozdanie informacii o polzovatelskom kataloge slovarey
	sprintf(settings.user_dicts_dir, "%s/%s", home_dir, USER_DICTS_SUBDIR);

	if ( access(settings.user_dicts_dir, F_OK) != 0 )
		if ( mkdir(settings.user_dicts_dir, 0755) != 0 )
		{
			fprintf(stderr, "%s: cannot create user dicts folder \"%s\": %s\n",
				MYNAME, settings.user_dicts_dir, strerror(errno) );
			return -1;
		}

	return 0;
}

/********************************************************************************
*										*
*	init_locale_encoding() - poluchaet kodirovku sistemy.			*
*										*
********************************************************************************/
static int init_locale_encoding(void)
{
	//////////////////////////////////
	extern settings_t settings;	// Parametry systemy
	//////////////////////////////////

	if ( (settings.locale_encoding = nl_langinfo(CODESET)) == NULL )
		settings.locale_encoding = "";

	return 0;
}

/********************************************************************************
*										*
*	init_max_terminal_line_len() - poluchaet maximalnuyu dlinu stroki	*
*		terminala iz peremennoy <$COLUMNS>				*
*										*
********************************************************************************/
static int init_max_terminal_line_len(void)
{
	//////////////////////////////////////////
	char	*max_terminal_line_len_str;	// Strokovaya velichina dliny
	extern settings_t settings;		// Nastroyki sistemy
	//////////////////////////////////////////


	// Bez kommentariev :)
	if ( (max_terminal_line_len_str = getenv("COLUMNS")) == NULL )
	{
		settings.max_terminal_line_len = DEFAULT_MAX_TERMINAL_LINE_LEN;
		return 0;
	}

	if ( (settings.max_terminal_line_len = atoi(max_terminal_line_len_str)) == 0 )
	{
		settings.max_terminal_line_len = DEFAULT_MAX_TERMINAL_LINE_LEN;
		return 0;
	}

	return 0;
}

/********************************************************************************
*										*
*	init_use_terminal_escapes_flag(void) - inicializiruet vozmojnost	*
*		ispolzovaniya ESC-posledovatelnostay terminala			*
*										*
********************************************************************************/
static int init_use_terminal_escapes_flag(void)
{
	//////////////////////////////////
	extern settings_t settings;	// Nastroyki sistemy
	//////////////////////////////////

	if ( isatty(1) ) settings.use_terminal_escapes_flag = true;
	else settings.use_terminal_escapes_flag = false;

	return 0;
}

/********************************************************************************
*********************************************************************************
********************************************************************************/
