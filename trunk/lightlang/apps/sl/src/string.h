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


#ifndef STRING_H
# define STRING_H

# define _GNU_SOURCE

# include <wchar.h>

void delete_newline(char *str);
void tolower_str_wc(wchar_t *str_wc);

wchar_t get_first_lower_wc(const char *str);
wchar_t *strncpy_lower_wc(wchar_t *str_wc, const char *str, size_t count);
wchar_t *strncpy_lower_filter_wc(wchar_t *str_wc, const char *str, size_t count);

int strcmp_full_wc(const wchar_t *str1_wc, const wchar_t *str2_wc);
int strcmp_noend_wc(const wchar_t *str1_wc, const wchar_t *str2_wc);
int strcmp_jump_wc(const wchar_t *str1_wc, const wchar_t *str2_wc, const int percent);

#endif // STRING_H

