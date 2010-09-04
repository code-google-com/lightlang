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
#include <ctype.h>
#include <errno.h>

#include "const.h"
#include "settings.h"

#include "options.h"


void set_settings_max_translate_count(const char *str)
{
	extern settings_t settings;


	if ( !isdigit(str[0]) ) {
		fprintf(stderr, "Bad argument \"%s\" (must be digit): ignored\n", str);
		return;
	}

	settings.max_translate_count = atoi(str);
}

void set_settings_ill_defined_search_percent(const char *str)
{
	extern settings_t settings;
	int percent;


	if ( !isdigit(str[0]) ) {
		fprintf(stderr, "Bad argument \"%s\" (must be digit): ignored\n", str);
		return;
	}

	if ( (percent = atoi(str)) > 100 ) {
		fprintf(stderr, "Argument \"%s\" not in range 0...100: ignored\n", str);
		return;
	}

	settings.ill_defined_search_percent = percent;
}

void set_settings_output_format(const char *str)
{
	extern settings_t settings;


	if ( !strcmp(str, OPT_ARG_HTML_OUTPUT_FORMAT) )
		settings.output_format = html_output_format;
	else if ( !strcmp(str, OPT_ARG_TEXT_OUTPUT_FORMAT) )
		settings.output_format = text_output_format;
	else if ( !strcmp(str, OPT_ARG_NATIVE_OUTPUT_FORMAT) )
		settings.output_format = native_output_format;
	else
		fprintf(stderr, "Unknown output format \"%s\": ignored\n", str);
}

void set_settings_use_terminal_escapes_flag(const char *str)
{
	extern settings_t settings;


	if ( !strcmp(str, OPT_ARG_YES) )
		settings.use_terminal_escapes_flag = true;
	else if ( !strcmp(str, OPT_ARG_NO) )
		settings.use_terminal_escapes_flag = false;
	else
		fprintf(stderr, "Unknown replay \"%s\", say \"%s\" or \"%s\": ignored\n", str, OPT_ARG_YES, OPT_ARG_NO);
}

void set_settings_use_css_flag(const char *str)
{
	extern settings_t settings;

	if ( !strcmp(str, OPT_ARG_YES) )
		settings.use_css_flag = true;
	else if ( !strcmp(str, OPT_ARG_NO) )
		settings.use_css_flag = false;
	else
		fprintf(stderr, "Unknown replay \"%s\", say \"%s\" or \"%s\": ignored\n", str, OPT_ARG_YES, OPT_ARG_NO);
}

