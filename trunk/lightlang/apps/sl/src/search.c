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
#include "linear_index.h"
#include "search_output.h"

#include "search.h"

static int find_word_unified(const char *word, const regimen_t regimen, const char *dict_name, FILE *dict_fp);
static int find_word_combinations(const char *word, const char *dict_name, FILE *dict_fp);


int find_word(const char *word, const regimen_t regimen, const char *dict_name, FILE *dict_fp)
{
	switch ( regimen ) {
		case usually_regimen :
		case first_concurrence_regimen :
		case list_regimen :
		case ill_defined_regimen : return find_word_unified(word, regimen, dict_name, dict_fp);
		case word_combinations_regimen : return find_word_combinations(word, dict_name, dict_fp);
	}

	return 0;
}

int find_sound(const char *word)
{
	wchar_t *word_wc;
	wchar_t *lang_wc_ptr;
	wchar_t *word_wc_ptr;
	wchar_t *word_token_wc;
	wchar_t *word_token_wc_state;
	char *play_command;
	size_t word_wc_len;
	size_t play_command_len;


	if ( (word_wc_len = strlen(word)) < 1 )
		return 0;
	word_wc_len = (word_wc_len + 16) * sizeof(wchar_t);


	if ( (word_wc = (wchar_t *) malloc(word_wc_len)) == NULL ) {
		fprintf(stderr, "Cannot allocate memory (%s:%d): %s\n", __FILE__, __LINE__, strerror(errno));
		return -1;
	}

	strncpy_lower_wc(word_wc, word, word_wc_len);

	if ( (word_wc_ptr = wcschr(word_wc, ':')) == NULL ) { // lang:word
		fprintf(stderr, "A word must be given in the format \"language:word\"\n");
		free(word_wc);
		return -1;
	}

	lang_wc_ptr = word_wc;
	*word_wc_ptr = L'\0';
	++word_wc_ptr;

	for (word_token_wc = wcstok(word_wc_ptr, L" -./\\()", &word_token_wc_state); word_token_wc;
		word_token_wc = wcstok(NULL, L" -./\\()", &word_token_wc_state)) {

		play_command_len = ( (strlen(AUDIO_PLAYER_PROG) + strlen(ALL_SOUNDS_DIR) + strlen(AUDIO_POSTFIX)) * sizeof(char) +
			(wcslen(lang_wc_ptr) + wcslen(word_token_wc)) * sizeof(wchar_t) + 32 );

		if ( (play_command = (char *) malloc(play_command_len)) == NULL ) {
			fprintf(stderr, "Cannot allocate memory (%s:%d): %s\n", __FILE__, __LINE__, strerror(errno));
			continue;
		}

		sprintf(play_command, "%s %s/%ls/%lc/%ls%s", AUDIO_PLAYER_PROG, ALL_SOUNDS_DIR, lang_wc_ptr,
			word_token_wc[0], word_token_wc, AUDIO_POSTFIX);

		system(play_command);

		free(play_command);
	}

	free(word_wc);

	return 0;
}


static int find_word_unified(const char *word, const regimen_t regimen, const char *dict_name, FILE *dict_fp)
{
	wchar_t word_wc[MAX_WORD_SIZE];
	wchar_t str_wc[MAX_WORD_SIZE];

	char *str = NULL;
	size_t str_len = 0;

	long index_pos = -1;
	int translate_count = 0;

	bool break_end_flag = false;


	if ( strlen(word) < 1 )
		return 0;

	if ( strncpy_lower_wc(word_wc, word, MAX_WORD_SIZE - 1) == NULL ) {
		fprintf(stderr, "Cannot convert \"%s\" to (wchar_t *): %s\n", word, strerror(errno));
		return -1;
	}

	if ( regimen == usually_regimen || regimen == first_concurrence_regimen || list_regimen ) {
		index_pos = get_linear_index_pos(word_wc[0], dict_fp);
		if ( index_pos == 0 ) {
			return 0;
		}
		else if ( index_pos > 0 ) {
			if ( fseek(dict_fp, index_pos, SEEK_SET) != 0 )
				fprintf(stderr, "Seek fail on index \"%lc %ld\": %s: ignored\n", word_wc[0], index_pos, strerror(errno));
		}
		else {
			rewind(dict_fp);
		}
	}

	while ( getline(&str, &str_len, dict_fp) != -1 ) {
		if ( str[0] == '#' || str[0] == '\n' )
			continue;

		if ( (str_wc[0] = get_first_lower_wc(str)) == L'\0' )
			continue;

		if ( regimen == usually_regimen || regimen == first_concurrence_regimen || list_regimen ) {
			if ( word_wc[0] != str_wc[0] && break_end_flag )
				break;
			if ( word_wc[0] != str_wc[0] )
				continue;
			else
				break_end_flag = true;
		}

		if ( strncpy_lower_filter_wc(str_wc, str, MAX_WORD_SIZE - 1) == NULL ) {
			break_end_flag = false; // ill_defined_regimen not required this
			continue;
		}

		if ( regimen == usually_regimen ) {
			if ( !strcmp_full_wc(str_wc, word_wc) ) {
				++translate_count;

				if ( translate_count == 1 )
					print_header(dict_name, word_wc);
				print_translate(str, translate_count);

				if ( translate_count >= settings.max_translate_count )
					break;
			}
		}
		else if ( regimen == first_concurrence_regimen ) {
			if ( !strcmp_noend_wc(str_wc, word_wc) ) {
				++translate_count;

				if ( translate_count == 1 )
					print_header(dict_name, word_wc);
				print_translate(str, translate_count);

				break;
			}
		}
		else if ( regimen == list_regimen ) {
			if ( !strcmp_noend_wc(str_wc, word_wc) ) {
				++translate_count;

				if ( translate_count == 1 )
					print_header(dict_name, word_wc);
				print_list_item(str_wc, translate_count);

				if ( translate_count >= settings.max_translate_count )
					break;
			}
		}
		else if ( regimen == ill_defined_regimen ) {
			if ( !strcmp_jump_wc(str_wc, word_wc, settings.ill_defined_search_percent) ) {
				++translate_count;

				if ( translate_count == 1 )
					print_header(dict_name, word_wc);
				print_list_item(str_wc, translate_count);

				if ( translate_count >= settings.max_translate_count )
					break;
			}
		}
	}

	free(str);

	return translate_count;
}

static int find_word_combinations(const char *word, const char *dict_name, FILE *dict_fp)
{
	wchar_t word_wc[MAX_WORD_SIZE];
	wchar_t str_wc[MAX_WORD_SIZE];

	wchar_t *str_token_wc;
	wchar_t *str_token_wc_state;

	char *str = NULL;
	size_t str_len = 0;

	int translate_count = 0;


	if ( strlen(word) < 1 )
		return 0;

	if ( strncpy_lower_wc(word_wc, word, MAX_WORD_SIZE - 1) == NULL ) {
		fprintf(stderr, "Cannot convert \"%s\" to (wchar_t *): %s\n", word, strerror(errno));
		return -1;
	}

	while ( getline(&str, &str_len, dict_fp) != -1 ) {
		if ( str[0] == '#' || str[0] == '\n' )
			continue;

		if ( strncpy_lower_filter_wc(str_wc, str, MAX_WORD_SIZE - 1) == NULL )
			continue;

		for (str_token_wc = wcstok(str_wc, L" -./\\", &str_token_wc_state); str_token_wc;
			str_token_wc = wcstok(NULL, L" -./\\", &str_token_wc_state)) {
			if ( word_wc[0] != str_token_wc[0] )
				continue;

			if ( !strcmp_full_wc(str_token_wc, word_wc) ) {
				++translate_count;

				//if ( translate_count == 1 )
				//	print_header(dict_name, word_wc);
				print_translate(str, translate_count);
				//print_separator();

				if ( translate_count >= settings.max_translate_count )
					goto external_loop_break_label;

				break;
			}
		}
	}

	external_loop_break_label :

	free(str);

	return translate_count;
}

