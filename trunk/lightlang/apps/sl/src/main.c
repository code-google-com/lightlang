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
#include <string.h>
#include <stdlib.h>
#include <stdbool.h>
#include <getopt.h>
#include <ctype.h>
#include <time.h>
#include <unistd.h>
#include <errno.h>

#include "config.h"
#include "const.h"
#include "settings.h"
#include "linear_index.h"
#include "search.h"
#include "managed_search.h"
#include "manager.h"
#include "options.h"
#include "help.h"


int main(int argc, char **argv)
{
	bool use_default_function_flag = true;
	bool show_time_flag = false;
	char *dicts_list = NULL;
	clock_t begin_time_label, end_time_label;
	regimen_t regimen = usually_regimen; // GCC warning fix
	int opt;
	int error_count = 0;

	struct option long_options[] = {
		{OPT_SEARCH_USUALLY,			required_argument,	NULL,	'u'}, // +
		{OPT_SEARCH_FIRST_CONCURRENCE,		required_argument,	NULL,	'f'}, // +
		{OPT_SEARCH_WORD_COMBINATIONS,		required_argument,	NULL,	'c'}, // +
		{OPT_SEARCH_LIST,			required_argument,	NULL,	'l'}, // +
		{OPT_SEARCH_ILL_DEFINED,		required_argument,	NULL,	'i'}, // +
		{OPT_SEARCH_SOUND,			required_argument,	NULL,	's'}, // +

		{OPT_DICT_CONNECT,			required_argument,	NULL,	'0'}, // -
		{OPT_DICT_DISCONNECT,			required_argument,	NULL,	'1'}, // -
		{OPT_DICT_PRINT_DICTS_LIST,		no_argument,		NULL,	'2'}, // -
		{OPT_DICT_PRINT_DICT_INFO,		required_argument,	NULL,	'3'}, // -
		{OPT_DICT_USE_LIST,			required_argument,	NULL,	'5'}, // -
		{OPT_DICT_PRINT_INDEX,			required_argument,	NULL,	'6'}, // -

		{OPT_MISC_MAX_TRANSLATE_COUNT,		required_argument,	NULL,	'm'}, // +
		{OPT_MISC_ILL_DEFINED_SEARCH_PERCENT,	required_argument,	NULL,	'p'}, // +
		{OPT_MISC_SHOW_TIME,			no_argument,		NULL,	't'}, // +
		{OPT_SETTINGS_OUTPUT_FORMAT,		required_argument,	NULL,	'7'}, // -
		{OPT_SETTINGS_USE_ESCS,			required_argument,	NULL,	'8'}, // -
		{OPT_SETTINGS_USE_CSS,			required_argument,	NULL,	'9'}, // -

		{OPT_INFO_HELP,				no_argument,		NULL,	'h'}, // +
		{OPT_INFO_VERSION,			no_argument,		NULL,	'v'}, // +
		{OPT_INFO_DEBUG,			no_argument,		NULL,	'd'}, // +

		{0, 0, 0, 0}
	};


	begin_time_label = clock();

	if ( init_settings() != 0 ) {
		fprintf(stderr, "%s: cannot init settings\n", MYNAME);
		return 1;
	}

	while ( (opt = getopt_long(argc, argv, ":u:f:c:l:i:s:m:p:thvd", long_options, NULL)) != -1 ) {
		switch ( opt ) {
			case 'u' :
			case 'f' :
			case 'c' :
			case 'l' :
			case 'i' : {
				switch ( opt ) {
					case 'u' : regimen = usually_regimen; break;
					case 'f' : regimen = first_concurrence_regimen; break;
					case 'c' : regimen = word_combinations_regimen; break;
					case 'l' : regimen = list_regimen; break;
					case 'i' : regimen = ill_defined_regimen; break;
				}
				error_count += managed_find_word(optarg, regimen, dicts_list);
				use_default_function_flag = false;
				break;
			}

			case 's' : {
				error_count += find_sound(optarg);
				use_default_function_flag = false;
				break;
			}

			case '0' : {
				error_count += connect_dict(optarg);
				use_default_function_flag = false;
				break;
			}

			case '1' : {
				error_count += disconnect_dict(optarg);
				use_default_function_flag = false;
				break;
			}

			case '2' : {
				error_count += print_dicts_list();
				use_default_function_flag = false;
				break;
			}

			case '3' : {
				error_count += print_dict_info(optarg);
				use_default_function_flag = false;
				break;
			}

			case '5' : {
				dicts_list = optarg;
				use_default_function_flag = false;
				break;
			}

			case '6' : {
				error_count += build_linear_index(optarg);
				use_default_function_flag = false;
				break;
			}

			case 'm' : {
				set_settings_max_translate_count(optarg);
				use_default_function_flag = false;
				break;
			}

			case 'p' : {
				set_settings_ill_defined_search_percent(optarg);
				use_default_function_flag = false;
				break;
			}

			case '7' : {
				set_settings_output_format(optarg);
				use_default_function_flag = false;
				break;
			}

			case '8' : {
				set_settings_use_terminal_escapes_flag(optarg);
				use_default_function_flag = false;
				break;
			}

			case '9' : {
				set_settings_use_css_flag(optarg);
				use_default_function_flag = false;
				break;
			}

			case 't' : {
				show_time_flag = true;
				use_default_function_flag = false;
				break;
			}

			case 'h' : {
				help();
				use_default_function_flag = false;
				break;
			}

			case 'v' : {
				version();
				use_default_function_flag = false;
				break;
			}

			case 'd' : {
				debug();
				use_default_function_flag = false;
				break;
			}

			case ':' : {
				fprintf(stderr, "%s: option \"-%c\" requires an argument: ignored\n", MYNAME, optopt);
				--error_count;
				break;
			}

			case '?' :
			default : {
				fprintf(stderr, "%s: option \"-%c\" is invalid: ignored\n", MYNAME, optopt);
				use_default_function_flag = false;
				break;
			}
		}
	}

	if ( argc == 2 && use_default_function_flag ) {
		error_count += managed_find_word(argv[1], usually_regimen, NULL);
	}
	else if ( argc != 2 && use_default_function_flag ) {
		fprintf(stderr, "%s: bad usage, try \"%s --help\"\n", MYNAME, MYNAME);
		--error_count;
	}

	if ( close_settings() != 0 )
		fprintf(stderr, "%s: warning: cannot close settings\n", MYNAME);

	if ( show_time_flag ) {
		end_time_label = clock();

		if ( begin_time_label != -1 && end_time_label != -1 )
			fprintf(stderr, "%s: search time: %.2f sec\n", MYNAME, ((double) (end_time_label - begin_time_label)) / CLOCKS_PER_SEC);
	}

	return abs(error_count);
}

