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

#include "search_output.h"
#include "search_output_text.h"


//void print_begin_page_text(char *word)
//{
//}

//void print_end_page_text(void)
//{
//}

void print_separator_text(void)
{
	int count;
	extern settings_t settings;


	for (count = 0; count < settings.max_terminal_line_len; ++count)
		putchar('-');
	putchar('\n');
}

void print_newline_text(void)
{
	putchar('\n');
}

void print_header_text(const char *dict_name, const wchar_t *word_wc)
{
	int count;
	extern settings_t settings;


	print_separator_text();

	if ( strlen(dict_name) >= settings.max_terminal_line_len ) {
		puts(dict_name);
	}
	else {
		for (count = 0; count < (settings.max_terminal_line_len - strlen(dict_name)) / 2; ++count)
			putchar('=');
		putchar(' ');

		if ( settings.use_terminal_escapes_flag )
			printf("\033[1m");

		for (++count; *dict_name; ++dict_name, ++count) {
			if ( *dict_name == '_' )
				putchar(' ');
			else
				putchar(*dict_name);
		}

		if ( settings.use_terminal_escapes_flag )
			printf("\033[0m");

		putchar(' ');
		for (++count; count < settings.max_terminal_line_len; ++count)
			putchar('=');

		putchar('\n');
	}

	print_separator_text();

	printf("\n\t<< %ls >>\n\n", word_wc);
}

void print_list_item_text(const wchar_t *word_wc, const int word_number)
{
	extern settings_t settings;


	if ( settings.use_terminal_escapes_flag )
		printf(" \033[1m(%d)\033[0m %ls\n", word_number, word_wc);
	else
		printf(" (%d) %ls\n", word_number, word_wc);
}

void print_translate_text(const char *str, const int word_number)
{
	wchar_t str_ch_wc;
	size_t str_offset = 0;
	mbstate_t mb_state;

	int block_count = 0;
	int char_count = 0;
	int count = 0;

	bool strong_font_flag = false;
	bool green_font_flag = false;
	bool underline_font_flag = false;
	bool word_link_font_flag = false;
	bool sound_link_font_flag = false;
	bool shield_flag = false;

	extern settings_t settings;


	memset(&mb_state, 0, sizeof(mb_state));

	if ( settings.use_terminal_escapes_flag )
		printf("   \033[1m(%d)\033[0m ", word_number);
	else
		printf("   (%d) ", word_number);

	for (; (str_offset = mbrtowc(&str_ch_wc, str, sizeof(wchar_t), &mb_state)) > 0; str += str_offset) {
		if ( str_ch_wc == L'\n' ) {
			shield_flag = false;
			continue;
		}

		if ( str_ch_wc == L'\\' && !shield_flag ) {
			shield_flag = true;
			continue;
		}

		if ( shield_flag ) {
			switch ( str_ch_wc ) {
				case L'[' : {
					if ( settings.use_terminal_escapes_flag ) {
						printf("\033[1m");
						strong_font_flag = true;
					}
					break;
				}
				case L']' : {
					if ( settings.use_terminal_escapes_flag ) {
						 printf("\033[0m");
						if ( green_font_flag )
							printf("\033[32m");
						if ( underline_font_flag )
							printf("\033[4m");
						strong_font_flag = false;
					}
					break;
				}

				case L'<' : {
					if ( settings.use_terminal_escapes_flag ) {
						printf("\033[32m");
						green_font_flag = true;
					}
					break;
				}
				case L'>' : {
					if ( settings.use_terminal_escapes_flag ) {
						printf("\033[0m");
						if ( strong_font_flag )
							printf("\033[1m");
						if ( underline_font_flag )
							printf("\033[4m");
						green_font_flag = false;
					}
					break;
				}

				case L'{' : {
					block_count += 3;
					char_count = block_count;
					putchar('\n');
					for (count = 0; count < block_count; ++count)
						putchar(' ');
					break;
				}
				case L'}' : {
					block_count -= 3;
					if ( block_count < 0 )
						block_count = 0;
					char_count = block_count;
					break;
				}

				case L'_' : {
					if ( settings.use_terminal_escapes_flag ) {
						if ( !underline_font_flag ) {
							printf("\033[4m");
							underline_font_flag = true;
						}
						else {
							printf("\033[24m");
							underline_font_flag = false;
						}
					}
					break;
				}

				case L'@' : {
					if ( settings.use_terminal_escapes_flag ) {
						if ( !word_link_font_flag ) {
							printf("\033[4m");
							word_link_font_flag = true;
						}
						else {
							printf("\033[24m");
							word_link_font_flag = false;
						}
					}
					break;
				}

				case L's' : {
					if ( settings.use_terminal_escapes_flag ) {
						if ( !sound_link_font_flag ) {
							printf("[\033[4msnd:\"");
							sound_link_font_flag = true;
						}
						else {
							printf("\"\033[24m]");
							sound_link_font_flag = false;
						}
					}
					break;
				}

				case L'\\' : {
					putchar('\\');
					break;
				}

				case L'n' : {
					putchar('\n');
					break;
				}

				case L't' : {
					putchar('\t');
					break;
				}
			}

			shield_flag = false;
			continue;
		}

		if ( char_count > (int) ((float) settings.max_terminal_line_len * TERMINAL_TEXT_PART) && str_ch_wc == L' ' && !isdigit(*(str + 1)) ) {
			putchar('\n');
			for (count = 0; count < block_count + 3; ++count)
				putchar(' ');
			char_count = block_count + 3;
		}

		printf("%lc", str_ch_wc); // putwchar() - DON'T WORK!

		++char_count;
	}

	if ( settings.use_terminal_escapes_flag )
		printf("\033[0m"); // Reset terminal settings

	putchar('\n');
}

