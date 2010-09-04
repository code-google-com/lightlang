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
#include <ctype.h>
#include <wchar.h>
#include <wctype.h>
#include <errno.h>

#include "const.h"

#include "string.h"


void delete_newline(char *str)
{
	for (; *str && *str != '\n'; ++str);
	*str = '\0';
}

void tolower_str_wc(wchar_t *str_wc)
{
	for (; *str_wc; ++str_wc)
		*str_wc = towlower(*str_wc);
}

wchar_t get_first_lower_wc(const char *str)
{
	wchar_t str_ch_wc = L'\0';


	if ( mbrtowc(&str_ch_wc, str, sizeof(wchar_t), NULL) < 0 )
		fprintf(stderr, "Cannot convert \"%s\" to (wchar_t): %s\n", str, strerror(errno));

	return towlower(str_ch_wc);
}

wchar_t *strncpy_lower_wc(wchar_t *dest_str_wc, const char *src_str, size_t count)
{
	wchar_t *dest_str_wc_ptr = dest_str_wc;
	size_t src_str_offset = 0;
	mbstate_t mb_state;


	memset(&mb_state, 0, sizeof(mb_state));

	for (; (src_str_offset = mbrtowc(dest_str_wc_ptr, src_str, sizeof(wchar_t), &mb_state)) > 0 && count;
		++dest_str_wc_ptr, src_str += src_str_offset, --count)
		*dest_str_wc_ptr = towlower(*dest_str_wc_ptr);

	*dest_str_wc_ptr = L'\0';
	if ( src_str_offset == (size_t)(-1) || src_str_offset == (size_t)(-2) ) {
		dest_str_wc[0] = L'\0';
		return NULL;
	}

	return dest_str_wc;
}

wchar_t *strncpy_lower_filter_wc(wchar_t *dest_str_wc, const char *src_str, size_t count)
{
	wchar_t *dest_str_wc_ptr = dest_str_wc;
	size_t src_str_offset = 0;
	mbstate_t mb_state;


	memset(&mb_state, 0, sizeof(mb_state));

	for (; (src_str_offset = mbrtowc(dest_str_wc_ptr, src_str, sizeof(wchar_t), &mb_state)) > 0 && count;
		++dest_str_wc_ptr, src_str += src_str_offset, --count) {
		*dest_str_wc_ptr = towlower(*dest_str_wc_ptr);

		if ( dest_str_wc_ptr == dest_str_wc )
			continue;

		if ( *(dest_str_wc_ptr - 1) == L' ' && *dest_str_wc_ptr == L' ' ) {
			*(dest_str_wc_ptr - 1) = L'\0';
			return dest_str_wc;
		}
	}

	dest_str_wc[0] = L'\0';
	return NULL;
}

int strcmp_full_wc(const wchar_t *str1_wc, const wchar_t *str2_wc)
{
	for (; *str1_wc && *str2_wc; ++str1_wc, ++str2_wc)
		if ( *str1_wc != *str2_wc )
			return 1;

	if ( !*str1_wc && !*str2_wc )
		return 0;

	return 1;
}

int strcmp_noend_wc(const wchar_t *str1_wc, const wchar_t *str2_wc)
{
	for (; *str1_wc && *str2_wc; ++str1_wc, ++str2_wc)
		if ( *str1_wc != *str2_wc )
			return 1;

	if ( !*str2_wc )
		return 0;

	return 1;
}

int strcmp_jump_wc(const wchar_t *str1_wc, const wchar_t *str2_wc, const int percent)
{
	size_t str1_wc_len, str2_wc_len;
	int error_count = 0;
	int search_exact;


	str1_wc_len = wcslen(str1_wc);
	str2_wc_len = wcslen(str2_wc);

	search_exact = ((int)str1_wc_len * percent) / 100;

	if ( str1_wc_len == str2_wc_len ) {
		for (; *str1_wc; ++str1_wc, ++str2_wc) {
			if ( *str1_wc != *str2_wc )
				++error_count;

			if ( error_count > search_exact )
				return 1;
		}

		return 0;
	}
	else if ( str1_wc_len < str2_wc_len ) {
		for (; *str1_wc; ++str1_wc, ++str2_wc) {
			if ( *str1_wc == *str2_wc ) {
				continue;
			}
			else if ( *str1_wc == *(str2_wc + 1) ) {
				++error_count;
				++str2_wc;
			}
			else {
				++error_count;
			}

			if ( error_count + (str2_wc_len - str1_wc_len) > search_exact )
				return 1;
		}

		if ( error_count + (str2_wc_len - str1_wc_len) <= search_exact )
			return 0;
		return 1;
	}
	else {
		for (; *str2_wc; ++str1_wc, ++str2_wc) {
			if ( *str1_wc == *str2_wc ) {
				continue;
			}
			else if ( *(str1_wc + 1) == *str2_wc ) {
				++error_count;
				++str1_wc;
			}
			else {
				++error_count;
			}

			if ( error_count + (str1_wc_len - str2_wc_len) > search_exact )
				return 1;
		}

		if ( error_count + (str1_wc_len - str2_wc_len) <= search_exact )
			return 0;
		return 1;
	}

	//return 1;
}

