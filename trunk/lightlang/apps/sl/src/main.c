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
#include <limits.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <getopt.h>
#include <ctype.h>
#include <time.h>
#include <unistd.h>
#include <dirent.h>
#include <errno.h>

#include "config.h"
#include "const.h"
#include "settings.h"
#include "find.h"
#include "manager.h"
#include "mstring.h"
#include "options.h"
#include "info.h"

/********************************* ** Macro ************************************/
#define HTML_OUTPUT_FORMAT	"html"
#define TEXT_OUTPUT_FORMAT	"text"
#define NATIVE_OUTPUT_FORMAT	"native"

/********************************** Functions **********************************/
static int get_percent(const char *percent_str);
static void set_max_translate_count(const char *str);
static void set_output_format(const char *str);
static void set_use_terminal_escapes_flag(const char *str);

static int xfind_word(const char *word, const regimen_t regimen, const int percent, const char *dicts_list);

static FILE *get_next_dict_fp_from_dir(char **dict_name, DIR *dicts_dp);
static FILE *get_next_dict_fp_from_list(char **dict_name, const char *dicts_list);

/********************************************************************************
********************************************************************************/
int main(int argc, char **argv)
{
	//////////////////////////////////////////////////
	bool	use_default_function_flag = true;	// Flag ispolzovaniya defoltnoy funkcii
	bool	show_time_flag = false;			// Flag opcii pokazyvaniya vremeni
	char	*dicts_list = NULL;			// Spisok ispolzuemyh slovarey
	clock_t	begin_time_label, end_time_label;	// Vremennye otmetki
	int	ill_defined_percent = OPTIMUM_PERCENT;	// Procent dlya nechetkogo poiska
	int	ch;					// Schityvaemaya opciya
	int	ec = 0;					// Schetchik oshibok
	//////////////////////////////////////////////////

	struct option long_options[] = {
		{OPT_FIND_USUALY,		required_argument,	NULL,	'u'}, // +
		{OPT_FIND_FIRST_CONCURRENCE,	required_argument,	NULL,	'f'}, // +
		{OPT_FIND_WORD_COMBINATIONS,	required_argument,	NULL,	'c'}, // +
		{OPT_FIND_LIST,			required_argument,	NULL,	'l'}, // +
		{OPT_FIND_ILL_DEFINED,		required_argument,	NULL,	'i'}, // +
		{OPT_FIND_SOUND,		required_argument,	NULL,	's'}, // +

		{OPT_DICT_CONNECT,		required_argument,	NULL,	'0'}, // -
		{OPT_DICT_DISCONNECT,		required_argument,	NULL,	'1'}, // -
		{OPT_DICT_PRINT_INFO,		no_argument,		NULL,	'2'}, // -
		{OPT_DICT_INSTALL,		required_argument,	NULL,	'3'}, // -
		{OPT_DICT_UNINSTALL,		required_argument,	NULL,	'4'}, // -
		{OPT_DICT_USE_LIST,		required_argument,	NULL,	'5'}, // -
		{OPT_DICT_PRINT_INDEX,		required_argument,	NULL,	'6'}, // -

		{OPT_MISC_MAX_TRANSLATE_COUNT,	required_argument,	NULL,	'm'}, // +
		{OPT_MISC_PERCENT,		required_argument,	NULL,	'p'}, // +
		{OPT_MISC_SHOW_TIME,		no_argument,		NULL,	't'}, // +
		{OPT_SETTINGS_OUTPUT_FORMAT,	required_argument,	NULL,	'7'}, // -
		{OPT_SETTINGS_USE_ESCS,		required_argument,	NULL,	'8'}, // -

		{OPT_INFO_HELP,			no_argument,		NULL,	'h'}, // +
		{OPT_INFO_VERSION,		no_argument,		NULL,	'v'}, // +
		{OPT_INFO_DEBUG,		no_argument,		NULL,	'd'}, // +

		{0, 0, 0, 0}
	};


	begin_time_label = clock();

	if ( init_settings() != 0 )
	{
		fprintf(stderr, "%s: cannot init settings\n", MYNAME);
		return 1;
	}

	while ( (ch = getopt_long(argc, argv, ":u:f:c:l:i:s:m:p:thvd", long_options, NULL)) != -1 )
	{
		switch (ch)
		{
			case 'u' : ec += xfind_word(optarg, usualy_regimen, 0, dicts_list);
					use_default_function_flag = false;	break;

			case 'f' : ec += xfind_word(optarg, first_concurrence_regimen, 0, dicts_list);
					use_default_function_flag = false;	break;

			case 'c' : ec += xfind_word(optarg, word_combinations_regimen, 0, dicts_list);
					use_default_function_flag = false;	break;

			case 'l' : ec += xfind_word(optarg, list_regimen, 0, dicts_list);
					use_default_function_flag = false;	break;

			case 'i' : ec += xfind_word(optarg, ill_defined_regimen, ill_defined_percent, dicts_list);
					use_default_function_flag = false;	break;

			case 's' : ec += find_sound(optarg);
					use_default_function_flag = false;	break;

			case '0' : ec += connect_dict(optarg);
					use_default_function_flag = false;	break;

			case '1' : ec += disconnect_dict(optarg);
					use_default_function_flag = false;	break;

			case '2' : ec += print_info();
					use_default_function_flag = false;	break;

			case '3' : ec += install_dict(optarg);
					use_default_function_flag = false;	break;

			case '4' : ec += uninstall_dict(optarg);
					use_default_function_flag = false;	break;

			case '5' : dicts_list = optarg;
					use_default_function_flag = false;	break;

			case '6' : ec += print_index(optarg);
					use_default_function_flag = false;	break;

			case 'm' : set_max_translate_count(optarg);
					use_default_function_flag = false;	break;

			case 'p' : ill_defined_percent = get_percent(optarg);
					use_default_function_flag = false;	break;

			case '7' : set_output_format(optarg);
					use_default_function_flag = false;	break;

			case '8' : set_use_terminal_escapes_flag(optarg);
					use_default_function_flag = false;	break;

			case 't' : show_time_flag = true;
					use_default_function_flag = false;	break;

			case 'h' : help();
					use_default_function_flag = false;	break;

			case 'v' : version();
					use_default_function_flag = false;	break;

			case 'd' : debug();
					use_default_function_flag = false;	break;

			case ':' : fprintf(stderr, "%s: option \"-%c\" requires an argument: ignored\n", MYNAME, optopt);
					++ec;					break;

			case '?' :
			default : fprintf(stderr, "%s: option \"-%c\" is invalid: ignored\n", MYNAME, optopt);
					use_default_function_flag = false;	break;
		}
	}

	if ( (argc == 2) && use_default_function_flag )
		xfind_word(argv[1], usualy_regimen, 0, NULL);
	else if ( (argc != 2) && use_default_function_flag )
	{
		fprintf(stderr, "%s: bad usage, try \"%s --help\"\n", MYNAME, MYNAME);
		++ec;
	}

	if ( close_settings() != 0 )
		fprintf(stderr, "%s: cannot close settings\n", MYNAME);

	if ( show_time_flag )
	{
		end_time_label = clock();

		if ( (begin_time_label != -1) && (end_time_label != -1) )
			printf("%s: CPU time used: %.2f sec\n",
				MYNAME,	(double)(((double)(end_time_label -
					begin_time_label))/CLOCKS_PER_SEC) );
	}

	return abs(ec);
}

/********************************************************************************
*										*
*	get_percent() - preobrazuet stroku v procenty.				*
*										*
********************************************************************************/
static int get_percent(const char *percent_str)
{
	//////////////////
	int percent;	// Procent
	//////////////////


	if ( !isdigit(percent_str[0]) )
	{
		fprintf(stderr, "%s: bad argument \"%s\": ignored\n",
			MYNAME, percent_str );
		return 40;
	}

	if ( (percent = atoi(percent_str)) > 100 )
	{
		fprintf(stderr, "%s: argument \"%s\": 0 <= arg <= 100: ignored\n",
			MYNAME, percent_str );
		return 40;
	}

	return percent;
}

/********************************************************************************
*										*
*	set_max_translate_count() - ustanavlivayet maximum perevodov		*
*										*
********************************************************************************/
static void set_max_translate_count(const char *str)
{
	//////////////////////////////////
	extern settings_t settings;	// Parametry sistemy
	//////////////////////////////////

	if ( !isdigit(str[0]) )
	{
		fprintf(stderr, "%s: bad argument \"%s\": ignored\n",
			MYNAME, str);
		return;
	}

	settings.max_translate_count = atoi(str);
}

/********************************************************************************
*										*
*	set_output_format() - ustanavlivaet format vyvoda.			*
*										*
********************************************************************************/
static void set_output_format(const char *str)
{
	//////////////////////////////////
	extern settings_t settings;	// Parametry sistemy
	//////////////////////////////////


	if ( !strcmp(str, HTML_OUTPUT_FORMAT) )
		settings.output_format = html_output_format;
	else if ( !strcmp(str, TEXT_OUTPUT_FORMAT) )
		settings.output_format = text_output_format;
	else if ( !strcmp(str, NATIVE_OUTPUT_FORMAT) )
		settings.output_format = native_output_format;
	else fprintf(stderr, "%s: unknown format \"%s\": ignored\n", MYNAME, str);
}

/********************************************************************************
*										*
*	set_use_terminal_escapes_flag() - ustanavlivaet razrechenie na		*
*		ispolzovanie ESC-posledovatelnostey.				*
*										*
********************************************************************************/
static void set_use_terminal_escapes_flag(const char *str)
{
	//////////////////////////////////
	extern settings_t settings;	// Parametry sistemy
	//////////////////////////////////

	if ( !strcmp(str, "yes") )
		settings.use_terminal_escapes_flag = true;
	else if ( !strcmp(str, "no") )
		settings.use_terminal_escapes_flag = false;
	else fprintf(stderr, "%s: unknown replay \"%s\", please use"
		" \"yes\" or \"no\": ignored\n", MYNAME, str);
}

/********************************************************************************
*										*
*	xfind_word() - obolochka dlya funkcii find_word().			*
*										*
********************************************************************************/
static int xfind_word(const char *word, const regimen_t regimen, const int percent, const char *dicts_list)
{
	//////////////////////////////////////////
	DIR	*dicts_dp;			// Ukazatel na katalog slovarey
	FILE	*dict_fp;			// Ukazatel na slovar
	char	*dict_name;			// Imya slovarya
	bool	no_translate_flag = true;	// Flag otsutstviya perevoda
	bool	no_dicts_flag = true;		// Flag otsutstviya slovarey
	extern settings_t settings;		// Parametry sistemy
	//////////////////////////////////////////


	print_begin_page(word);

	if ( dicts_list == NULL )
	{
		if ( (dicts_dp = opendir(settings.user_dicts_dir)) == NULL )
		{
			fprintf(stderr, "%s: cannot open dict folder \"%s\": %s\n",
				MYNAME, settings.user_dicts_dir, strerror(errno) );
			return -1;
		}

		while ( (dict_fp = get_next_dict_fp_from_dir(&dict_name, dicts_dp)) != NULL )
		{
			if ( find_word(word, regimen, percent, dict_name, dict_fp) )
				no_translate_flag = false;

			if ( fclose(dict_fp) != 0 )
				fprintf(stderr, "%s: cannot close dict \"%s\": %s\n",
					MYNAME, dict_name, strerror(errno) );

			no_dicts_flag = false;
		}

		if ( no_translate_flag && (regimen == usualy_regimen) )
		{
			rewinddir(dicts_dp);

			while ( (dict_fp = get_next_dict_fp_from_dir(&dict_name, dicts_dp)) != NULL )
			{
				if ( find_word(word, first_concurrence_regimen, percent, dict_name, dict_fp) )
					no_translate_flag = false;

				if ( fclose(dict_fp) != 0 )
					fprintf(stderr, "%s: cannot close dict \"%s\": %s\n",
						MYNAME, dict_name, strerror(errno) );
			}
		}

		if ( closedir(dicts_dp) == -1 )
			fprintf(stderr, "%s: cannot close dict folder \"%s\": %s\n",
				MYNAME, settings.user_dicts_dir, strerror(errno) );
	}
	else
	{
		while ( (dict_fp = get_next_dict_fp_from_list(&dict_name, dicts_list)) != NULL )
		{
			if ( find_word(word, regimen, percent, dict_name, dict_fp) )
				no_translate_flag = false;

			if ( fclose(dict_fp) != 0 )
				fprintf(stderr, "%s: cannot close dict \"%s\": %s\n",
					MYNAME, dict_name, strerror(errno) );

			no_dicts_flag = false;
		}

		if ( no_translate_flag && (regimen == usualy_regimen) )
		{
			while ( (dict_fp = get_next_dict_fp_from_list(&dict_name, dicts_list)) != NULL )
			{
				if ( find_word(word, first_concurrence_regimen, percent, dict_name, dict_fp) )
					no_translate_flag = false;

				if ( fclose(dict_fp) != 0 )
					fprintf(stderr, "%s: cannot close dict \"%s\": %s\n",
						MYNAME, dict_name, strerror(errno) );
			}
		}
	}

	if ( no_translate_flag )
		if ( settings.output_format == html_output_format )
			fprintf(stderr, "\t<em>This word is not found</em><br>\n");
		else if ( settings.output_format == text_output_format )
			fprintf(stderr, "%s: this word is not found\n", MYNAME);
		else if ( settings.output_format == native_output_format )
			fprintf(stderr, "%s: this word is not found\n", MYNAME);

	if ( no_dicts_flag )
		if ( settings.output_format == html_output_format )
			fprintf(stderr, "\t<em>No dict is connected</em><br>\n");
		else if ( settings.output_format == text_output_format )
			fprintf(stderr, "%s: no dict is connected\n", MYNAME);
		else if ( settings.output_format == native_output_format )
			fprintf(stderr, "%s: no dict is connected\n", MYNAME);

	print_end_page();

	return 0;
}

/********************************************************************************
*										*
*	get_next_dict_fp_from_dir() - vozvrashyaet sleduyushiy ukazatel na	*
*		slovar, izvlekaya ego iz kataloga.				*
*										*
********************************************************************************/
static FILE *get_next_dict_fp_from_dir(char **dict_name, DIR *dicts_dp)
{
	//////////////////////////////////////////
	static struct dirent	*dicts_dp_ent;	// Ukazatel na element kataloga
	struct stat		dict_st;	// Parametry slovarya
	FILE			*dict_fp;	// Ukazatel na slovar
	char			*dict_path;	// Put k slovaryu
	size_t			dict_path_len;	// Dlina puti k slovaryu
	extern settings_t	settings;	// Parametry sistemy
	//////////////////////////////////////////


	while ( (dicts_dp_ent = readdir(dicts_dp)) != NULL )
	{
		if ( dicts_dp_ent->d_name[0] == '.' ) continue;

		dict_path_len = (strlen(settings.user_dicts_dir) +
			strlen(dicts_dp_ent->d_name) + 16) * sizeof(char);

		if ( (dict_path = (char *) malloc(dict_path_len)) == NULL )
		{
			fprintf(stderr, "%s: memory error (%s, file %s, line %d), please report to \"%s\"\n",
				MYNAME, strerror(errno), __FILE__, __LINE__, BUGTRACK_MAIL );
			return NULL;
		}

		sprintf(dict_path, "%s/%s", settings.user_dicts_dir, dicts_dp_ent->d_name);

		if ( lstat(dict_path, &dict_st) != 0 )
		{
			fprintf(stderr, "%s: cannot get information about dict \"%s\": %s\n",
				MYNAME, dicts_dp_ent->d_name, strerror(errno) );

			free(dict_path);
			continue;
		}

		dict_st.st_mode &= S_IFMT;
		if ( ((dict_st.st_mode & S_IFLNK) != S_IFLNK) && ((dict_st.st_mode & S_IFREG) != S_IFREG) )
		{
			free(dict_path);
			continue;
		}

		if ( (dict_fp = fopen(dict_path, "r")) == NULL )
		{
			fprintf(stderr, "%s: cannot open dict \"%s\": %s\n",
				MYNAME, dicts_dp_ent->d_name, strerror(errno) );

			free(dict_path);
			continue;
		}

		(*dict_name) = dicts_dp_ent->d_name;

		free(dict_path);
		return dict_fp;
	}

	return NULL;
}

/********************************************************************************
*										*
*	get_next_dict_fp_from_list() - vozvrashyaet sleduyushiy ukazatel na	*
*		slovar, izvlekaya ego iz spiska.				*
*		Vnimanie!!! Nikakih funkciy dlya perevoda spiska na nachalo,	*
*		tipa rewind() - ne nujno! Eto proishodit avtomaticheski.	*
*										*
********************************************************************************/
static FILE *get_next_dict_fp_from_list(char **dict_name, const char *dicts_list)
{
	//////////////////////////////////////////////////////////////////
	FILE		*dict_fp;					// Ukazatel na slovar
	char		dict_path[strlen(ALL_DICTS_DIR) + PATH_MAX +16];// Put k slovaryu
	static char	dicts_list_item[PATH_MAX];			// Elemet spiska
	static size_t	count1 = 0;					// Schetchik po spisku
	size_t		count2;						// Schetchik po elementu spiska
	//////////////////////////////////////////////////////////////////


	while ( true )
	{
		if ( !dicts_list[count1] )
		{
			// Esli posledniy raz byl konec spiska - to perevodim schetchik na nachalo
			// i vozvrashyaem NULL, chtoby ne zaciklit poisk, pri sleduyushem obrashenii
			// rasparsivanie nachnetsya snachala
			count1 = 0;
			return NULL;
		}
		else for (; dicts_list[count1] == '|'; count1++); // Propusk razdeliteley

		for (count2 = 0; dicts_list[count1] && (dicts_list[count1] != '|')
			&& (count2 < PATH_MAX -1); count1++, count2++)
			dicts_list_item[count2] = dicts_list[count1]; // Parsim
		dicts_list_item[count2] = '\0';

		sprintf(dict_path, "%s/%s", ALL_DICTS_DIR, dicts_list_item); // Formiruem put k slovaryu

		if ( (dict_fp = fopen(dict_path, "r")) == NULL )
		{ // Otkryvaem slovar
			fprintf(stderr, "%s: cannot open dict \"%s\": %s\n",
				MYNAME, dicts_list_item, strerror(errno) );
			continue;
		}

		(*dict_name) = dicts_list_item; // Imya slovarya

		return dict_fp;
	}
}
/********************************************************************************
*********************************************************************************
********************************************************************************/
