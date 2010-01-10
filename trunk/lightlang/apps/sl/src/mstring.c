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
*	mstring.c - strokovye funkcii dlya obychnyh i rasshirennyh strok.	*
*										*
********************************************************************************/

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

#include "mstring.h"

/********************************************************************************
*										*
*	del_nl() - udalenie iz obychnoy stroki simvola perevoda stroki.		*
*										*
********************************************************************************/
void del_nl(char *str)
{
	for(; (*str); str++)
		if ( (*str) == '\n' )
		{
			(*str) = '\0';
			break;
		}
}

/********************************************************************************
*										*
*	lowstr_wc() - opuskanie rasshirennoy stroki v nijniy registr.		*
*										*
********************************************************************************/
void lowstr_wc(wchar_t *str_wc)
{
	for (; (*str_wc); str_wc++)
		(*str_wc) = towlower(*str_wc);
}

/********************************************************************************
*										*
*	get_first_low_wc() - poluchenie pervogo rasshirennogo simvola		*
*		stroki <str> v nijnem registre.					*
*										*
********************************************************************************/
wchar_t get_first_low_wc(const char *str)
{
	//////////////////
	wchar_t	ch_wc;	// Rasshirennyy simvol
	//////////////////


	if ( mbrtowc(&ch_wc, str, sizeof(wchar_t), NULL) < 0 )
	{
		fprintf(stderr, "%s: cannot convert (char*) to (wchar_t)(1): %s\n", MYNAME, strerror(errno));
		return L'\0';
	}

	return towlower(ch_wc);
}

/********************************************************************************
*										*
*	strnlowcpy_wc() - konvertiruet <str> v <str_wc>, opuskaya pri etom	*
*		v nijniy registr.						*
*										*
********************************************************************************/
wchar_t *strnlowcpy_wc(wchar_t *str_wc, const char *str, size_t count)
{
	//////////////////////////////////////////
	wchar_t		*ptr_str_wc = str_wc;	// Ukazatel na rasshirennuyu stroku
	size_t		str_offset = 0;		// Smeshenie ukazatelya
	mbstate_t	mbstate;		// Status sdviga
	//////////////////////////////////////////


	memset(&mbstate, 0, sizeof(mbstate));

	for (; ((str_offset = mbrtowc(ptr_str_wc, str, sizeof(wchar_t), &mbstate)) > 0) && count;
		++ptr_str_wc, str += str_offset, --count)
		(*ptr_str_wc) = towlower(*ptr_str_wc);

	(*ptr_str_wc) = L'\0';
	if ( (str_offset == (size_t)(-1)) || (str_offset == (size_t)(-2)) )
	{
		str_wc[0] = L'\0';
		return NULL;
	}
	else return str_wc;
}

/********************************************************************************
*										*
*	strnlowcpy_filter_wc() - filtruet <count> simvolov stroki <str>,	*
*		konvertiruya v rasshirennuyu stroku i pomeshyaet v <str_wc>.	*
*										*
********************************************************************************/
wchar_t *strnlowcpy_filter_wc(wchar_t *str_wc, const char *str, size_t count)
{
	//////////////////////////////////////////
	wchar_t		*ptr_str_wc = str_wc;	// Ukazatel na rasshirennuyu stroku
	size_t		str_offset = 0;		// Smeshenie ukazatelya
	mbstate_t	mbstate;		// Status sdviga
	//////////////////////////////////////////


	memset(&mbstate, 0, sizeof(mbstate));

	for (; ((str_offset = mbrtowc(ptr_str_wc, str, sizeof(wchar_t), &mbstate)) > 0) && count;
		++ptr_str_wc, str += str_offset, --count)
	{
		(*ptr_str_wc) = towlower(*ptr_str_wc);

		if ( ptr_str_wc == str_wc ) continue;
		if ( ((*(ptr_str_wc - 1)) == L' ') && (*(ptr_str_wc) == L' ') )
		{
			(*(ptr_str_wc - 1)) = L'\0';
			return str_wc;
		}
	}

	str_wc[0] = L'\0';
	return NULL;
}

/********************************************************************************
*										*
*	strcmp_all_wc() - sravnenie dvuh rasshirennyh strok.			*
*										*
********************************************************************************/
int strcmp_all_wc(const wchar_t *str1_wc, const wchar_t *str2_wc)
{
	for (; (*str1_wc) && (*str2_wc); str1_wc++, str2_wc++)
		if ( (*str1_wc) != (*str2_wc) ) return 1;
	if ( !(*str1_wc) && !(*str2_wc) ) return 0;
	return 1;
}

/********************************************************************************
*										*
*	strcmp_noend_wc() - sravnenie dvuh rasshirennyh strok s propuskom	*
*		okonchaniya pervogo slova.					*
*										*
********************************************************************************/
int strcmp_noend_wc(const wchar_t *str1_wc, const wchar_t *str2_wc)
{
	for (; (*str1_wc) && (*str2_wc); str1_wc++, str2_wc++)
		if ( (*str1_wc) != (*str2_wc) ) return 1;
	if ( !(*str2_wc) ) return 0;
	return 1;
}

/********************************************************************************
*										*
*	strcmp_jump_wc() - nechetkoe sravnenie slov po procentu			*
*		nesovpadayushih simvolov.					*
*										*
*		Funkciya ispolzuet algoritm pryjkov.				*
*										*
********************************************************************************/
int strcmp_jump_wc(const wchar_t *str1_wc, const wchar_t *str2_wc, const int percent)
{
	//////////////////////////////////
	size_t	str1_wc_len;		// Dlina pervoy rasshirennoy stroki
	size_t	str2_wc_len;		// Dlina vtoroy rasshirennoy stroki
	int	error_count = 0;	// Schetchik nesovpadeniy
	int	search_exact;		// Jestkost poiska
	//////////////////////////////////


	// Vychislyaem dliny rasshirenyh strok
	str1_wc_len = wcslen(str1_wc);
	str2_wc_len = wcslen(str2_wc);

	// Vychislyaem jestkost poiska po procentu
	// nesovpadayushih simvolov
	search_exact = ((int)str1_wc_len * percent) / 100;

	// Pri ravnoy dline slov
	if ( str1_wc_len == str2_wc_len )
	{
		for (; (*str1_wc); str1_wc++, str2_wc++)
		{
			if ( (*str1_wc) != (*str2_wc) ) ++error_count;

			if ( error_count > search_exact ) return 1;
		}

		return 0;
	}
	else if ( str1_wc_len < str2_wc_len )
	{
		for (; (*str1_wc); str1_wc++, str2_wc++)
		{
			if ( (*str1_wc) == (*str2_wc) ) continue;
			else if ( (*str1_wc) == (*(str2_wc + 1)) )
			{
				++error_count;
				++str2_wc;
			}
			else ++error_count;

			if ( (error_count + (str2_wc_len - str1_wc_len)) > search_exact )
				return 1;
		}

		if ( (error_count + (str2_wc_len - str1_wc_len)) <= search_exact )
			return 0;
		else return 1;
	}
	else
	{
		for (; (*str2_wc); str1_wc++, str2_wc++)
		{
			if ( (*str1_wc) == (*str2_wc) ) continue;
			else if ( (*(str1_wc + 1)) == (*str2_wc) )
			{
				++error_count;
				++str1_wc;
			}
			else ++error_count;

			if ( (error_count + (str1_wc_len - str2_wc_len)) > search_exact )
				return 1;
		}

		if ( (error_count + (str1_wc_len - str2_wc_len)) <= search_exact )
			return 0;
		else return 1;
	}
}

/********************************************************************************
*********************************************************************************
********************************************************************************/
