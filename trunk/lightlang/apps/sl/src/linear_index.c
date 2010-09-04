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
#include <sys/types.h>
#include <errno.h>

#include "const.h"
#include "string.h"

#include "linear_index.h"


long get_linear_index_pos(const wchar_t ch_wc, FILE *dict_fp)
{
	char *str = NULL;
	size_t str_len = 0;

	wchar_t str_ch_wc;
	long index_pos = 0;
	bool begin_index_block_flag = false;


	while ( getline(&str, &str_len, dict_fp) != -1 ) {
		if ( str[0] == '#' || str[0] == '\n' )
			continue;

		delete_newline(str);

		if ( !strcmp(str, NO_INDEX_BLOCK) )
			break;

		if ( !strcmp(str, BEGIN_INDEX_BLOCK) ) {
			begin_index_block_flag = true;
			continue;
		}

		if ( !begin_index_block_flag )
			continue;
		if ( !strcmp(str, END_INDEX_BLOCK) )
			break;

		if ( sscanf(str, "%lc %ld", &str_ch_wc, &index_pos) != 2 ) {
			fprintf(stderr, "Warning: bad index \"%s\": ignored\n", str);
			continue;
		}

		if ( towlower(str_ch_wc) == towlower(ch_wc) )
			break;

	}

	free(str);

	return index_pos;
}

int build_linear_index(const char *dict_path)
{
	char *str = NULL;
	size_t str_len = 0;

	wchar_t str_ch_wc = L'\0';
	long index_pos;
	FILE *dict_fp;
	char *double_space_ptr;


	if ( (dict_fp = fopen(dict_path, "r")) == NULL ) {
		fprintf(stderr, "Cannot open dict file \"%s\": %s\n", dict_path, strerror(errno));
		return -1;
	}

	puts(BEGIN_INDEX_BLOCK);
	while ( true ) {
		if ( (index_pos = ftell(dict_fp)) == -1 )
			break;

		if ( getline(&str, &str_len, dict_fp) == -1 )
			break;

		if ( str[0] == '#' || str[0] == '\n' )
			continue;

		if ( (double_space_ptr = strstr(str, "  ")) != NULL )
			*double_space_ptr = '\0';
		else
			continue;


		if ( towlower(str_ch_wc) != get_first_lower_wc(str) ) {
			str_ch_wc = get_first_lower_wc(str);
			printf("%lc %ld\n", str_ch_wc, index_pos);
		}
	}
	puts(END_INDEX_BLOCK);

	free(str);

	if ( fclose(dict_fp) != 0 )
		fprintf(stderr, "Cannot close dict file \"%s\": %s\n", dict_path, strerror(errno));

	return 0;
}

