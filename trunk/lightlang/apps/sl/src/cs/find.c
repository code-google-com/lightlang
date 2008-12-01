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
*	find.c - funkcii poiska i vyvoda perevoda v texte ili HTML.		*
*										*
********************************************************************************/

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
#include "mstring.h"

#include "find.h"

/********************************************************************************
*										*
*	find_word() - poisk slov. Prinimaet v kachestve argumentov slovo,	*
*		rejim poiska (sm. types.h/reg_t), procent simvolov (dlya	*
*		nechetkogo poiska, v drugih sluchayah = 0), imya slovarya	*
*		i ukazatel n file slovarya.					*
*										*
*		Vozvrashyaet kolichestvo naydennyh slov.			*
*										*
********************************************************************************/
int find_word(const char *word, const regimen_t regimen, const int percent, const char *dict_name, FILE *dict_fp)
{
	//////////////////////////////////////////////////
	wchar_t		word_wc[MAX_WORD_SIZE];		// Rasshirennaya stroka (slovo)
	wchar_t		str_wc[MAX_WORD_SIZE];		// Filtrovannaya rashirennaya stroka
	wchar_t		*token_str_wc, *state_str_wc;	// Ukazateli dlya poiska slovosochetaniy
	char		*str = NULL;			// Chitaemaya iz fila stroka
	size_t		str_len = 0;			// Dlina chitaemoy stroki
	long		pos;				// Smeshenie v file (index)
	int		translate_count = 0;		// Schetchik kolichestva sovpadeniy
	bool		break_end_flag = false;		// Flag propuska konca fila
	bool		first_translate_flag = true;	// Flag pervogo perevoda v file
	extern settings_t settings;			// Nastroyki sistemy
	//////////////////////////////////////////////////


	if ( strlen(word) < 1 ) return 0;
	if ( strnlowcpy_wc(word_wc, word, MAX_WORD_SIZE -1) == NULL )
	{
		fprintf(stderr, "%s: cannot convert (char*) to (wchar_t*): %s\n", MYNAME);
		return -1;
	}

	if ( regimen == usualy_regimen )
	{
		pos = read_index(word_wc[0], dict_fp);
		if ( pos > 0 )
		{
			if ( fseek(dict_fp, pos, SEEK_SET) != 0 )
				fprintf(stderr, "%s: cannot seek: incorrect index \"%lc %ld\": %s: ignored\n",
					MYNAME, word_wc[0], pos, strerror(errno) );
		}
		else if ( pos == 0 ) return 0;
		else rewind(dict_fp);

		while ( getline(&str, &str_len, dict_fp) != -1 )
		{
			if ( (str[0] == '#') || (str[0] == '\n') ) continue;

			if ( (str_wc[0] = get_first_low_wc(str)) == L'\0' ) continue;

			if ( (word_wc[0] != str_wc[0]) && break_end_flag ) break;
			if ( word_wc[0] != str_wc[0] ) continue;
			if ( word_wc[0] == str_wc[0] ) break_end_flag = true;

			if ( strnlowcpy_filter_wc(str_wc, str, MAX_WORD_SIZE -1) == NULL )
			{
				if ( break_end_flag ) break_end_flag = false;
				continue;
			}

			if ( !strcmp_all_wc(str_wc, word_wc) )
			{
				++translate_count;

				if ( first_translate_flag )
				{
					print_separator();
					print_header(dict_name);

					if ( settings.output_format == html_output_format )
						printf("\t<em><font color=\"#494949\" size=\"+1\">"
							"&nbsp;&nbsp;&nbsp;%ls</font></em><br>\n", word_wc);
					else if ( settings.output_format == text_output_format )
						printf("\n\t<< %ls >>\n", word_wc);
					// native format pass

					first_translate_flag = false;
				}
				print_translate(str, translate_count);

				if ( translate_count >= settings.max_translate_count ) break;
			}
		}

		free(str);
		return translate_count;
	}

	else if ( regimen == first_concurrence_regimen ) // Poisk do pervogo sovpadeniya
	{
		pos = read_index(word_wc[0], dict_fp);
		if ( pos > 0 )
		{
			if ( fseek(dict_fp, pos, SEEK_SET) != 0 )
				fprintf(stderr, "%s: cannot seek: incorrect index \"%lc %ld\": %s: ignored\n",
					MYNAME, word_wc[0], pos, strerror(errno) );
		}
		else if ( pos == 0 ) return 0;
		else rewind(dict_fp);

		while ( getline(&str, &str_len, dict_fp) != -1 )
		{
			if ( (str[0] == '#') || (str[0] == '\n') ) continue;

			if ( (str_wc[0] = get_first_low_wc(str)) == L'\0' ) continue;

			if ( (word_wc[0] != str_wc[0]) && break_end_flag ) break;
			if ( word_wc[0] != str_wc[0] ) continue;
			if ( word_wc[0] == str_wc[0] ) break_end_flag = true;

			if ( strnlowcpy_filter_wc(str_wc, str, MAX_WORD_SIZE -1) == NULL )
			{
				if ( break_end_flag) break_end_flag = false;
				continue;
			}

			if ( !strcmp_noend_wc(str_wc, word_wc) )
			{
				++translate_count;

				if ( first_translate_flag )
				{
					print_separator();
					print_header(dict_name);

					if ( settings.output_format == html_output_format )
						printf("\t<em><font color=\"#494949\" size=\"+1\">"
							"&nbsp;&nbsp;&nbsp;%ls</font></em><br>\n", word_wc);
					else if ( settings.output_format == text_output_format )
						printf("\n\t<< %ls >>\n", word_wc);
					// native format pass

					first_translate_flag = false;
				}
				print_translate(str, translate_count);

				break;
			}
		}

		free(str);
		return translate_count;
	}

	else if ( regimen == word_combinations_regimen ) // Poisk po slovosochetaniyam
	{
		while ( getline(&str, &str_len, dict_fp) != -1 )
		{
			if ( (str[0] == '#') || (str[0] == '\n') ) continue;

			if ( strnlowcpy_filter_wc(str_wc, str, MAX_WORD_SIZE -1) == NULL )
				continue;

			for (token_str_wc = wcstok(str_wc, L" -./\\", &state_str_wc);
				token_str_wc; token_str_wc = wcstok(NULL, L" -./\\", &state_str_wc))
			{
				if ( word_wc[0] != token_str_wc[0] ) continue;

				if ( !strcmp_all_wc(token_str_wc, word_wc) )
				{
					++translate_count;

					if ( first_translate_flag )
					{
						print_separator();
						print_header(dict_name);

						if ( settings.output_format == html_output_format )
							printf("\t<em><font color=\"#494949\" size=\"+1\">"
								"&nbsp;&nbsp;&nbsp;%ls</font></em><br>\n", word_wc);
						else if ( settings.output_format == text_output_format )
							printf("\n\t<< %ls >>\n", word_wc);
						// native format pass

						first_translate_flag = false;
					}
					print_translate(str, translate_count);

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

	else if ( regimen == list_regimen )
	{
		pos = read_index(word_wc[0], dict_fp);
		if ( pos > 0 )
		{
			if ( fseek(dict_fp, pos, SEEK_SET) != 0 )
				fprintf(stderr, "%s: cannot seek: incorrect index \"%lc %ld\": %s: ignored\n",
					MYNAME, word_wc[0], pos, strerror(errno) );
		}
		else if ( pos == 0 ) return 0;
		else rewind(dict_fp);

		while ( getline(&str, &str_len, dict_fp) != -1 )
		{
			if ( (str[0] == '#') || (str[0] == '\n') ) continue;

			if ( (str_wc[0] = get_first_low_wc(str)) == L'\0' ) continue;

			if ( (word_wc[0] != str_wc[0]) && break_end_flag ) break;
			if ( word_wc[0] != str_wc[0] ) continue;
			if ( word_wc[0] == str_wc[0] ) break_end_flag = true;

			if ( strnlowcpy_filter_wc(str_wc, str, MAX_WORD_SIZE -1) == NULL )
			{
				if ( break_end_flag ) break_end_flag = false;
				continue;
			}

			if ( !strcmp_noend_wc(str_wc, word_wc) )
			{
				++translate_count;

				if ( first_translate_flag )
				{
					print_separator();
					print_header(dict_name);
					print_separator();

					if ( settings.output_format == html_output_format )
						printf("\t<em><font color=\"#494949\" size=\"+1\">"
							"&nbsp;&nbsp;&nbsp;%ls</font></em><br>\n", word_wc);
					else if ( settings.output_format == text_output_format )
						printf("\n\t<< %ls >>\n", word_wc);
					// native format pass

					first_translate_flag = false;
				}
				print_list_item(str_wc, translate_count);

				if ( translate_count >= settings.max_translate_count ) break;
			}
		}

		if ( translate_count != 0 ) print_separator();

		free(str);
		return translate_count;

	}

	else if ( regimen == ill_defined_regimen ) // Nechetkiy poisk
	{
		while ( getline (&str, &str_len, dict_fp) != -1 )
		{
			if ( (str[0] == '#') || (str[0] == '\n') ) continue;

			if ( strnlowcpy_filter_wc(str_wc, str, MAX_WORD_SIZE -1) == NULL )
				continue;

			if ( !strcmp_jump_wc(str_wc, word_wc, percent) )
			{
				++translate_count;

				if ( first_translate_flag )
				{
					print_separator();
					print_header(dict_name);
					print_separator();

					if ( settings.output_format == html_output_format )
						printf("\t<em><font color=\"#494949\" size=\"+1\">"
							"&nbsp;&nbsp;&nbsp;%ls</font></em><br>\n", word_wc);
					else if ( settings.output_format == text_output_format )
						printf("\n\t<< %ls >>\n", word_wc);
					// native format pass

					first_translate_flag = false;
				}
				print_list_item(str_wc, translate_count);

				if ( translate_count >= settings.max_translate_count ) break;
			}
		}

		if ( translate_count != 0 ) print_separator();

		free(str);
		return translate_count;
	}

	else return -1; // Neizvestnyy metod poiska :)
}

/********************************************************************************
*										*
*	find_sound() - poisk zvuka. Prosto zapuskaet komandu PLAYER_PROG	*
*		dlya slova.							*
*										*
********************************************************************************/
int find_sound(const char *word)
{
	//////////////////////////////////////////////////
	wchar_t	*word_wc;				// Slovo v rasshyrennyh simvolah
	wchar_t	*token_word_wc, *state_token_word_wc;	// Razbivki
	wchar_t	*lang_wc;				// Yazyk
	char	*play_command;				// Komanda
	size_t	word_wc_len;				// Dlina slova
	size_t	lang_wc_len;				// Dlina yazyka :-)
	size_t	play_command_len;			// Dlina komandy
	bool	first_token_flag = true;		// Flag pervogo tokena
	//////////////////////////////////////////////////


	if ( (word_wc_len = strlen(word)) < 1 ) return 0;
	word_wc_len = (word_wc_len + 16) * sizeof(wchar_t);

	if ( (word_wc = (wchar_t *) malloc(word_wc_len)) == NULL )
	{
		fprintf(stderr, "%s: memory error (%s, file %s, line %d), please report to \"%s\"\n",
			MYNAME, strerror(errno), __FILE__, __LINE__, BUGTRACK_MAIL );

		return -1;
	}

	strnlowcpy_wc(word_wc, word, word_wc_len);

	for (token_word_wc = wcstok(word_wc, L" -./\\:", &state_token_word_wc);
		token_word_wc; token_word_wc = wcstok(NULL, L" -./\\:", &state_token_word_wc))
	{
		if ( first_token_flag )
		{
			lang_wc_len = (wcslen(token_word_wc) + 16) * sizeof(wchar_t);

			if ( (lang_wc = (wchar_t *) malloc(lang_wc_len)) == NULL )
			{
				fprintf(stderr, "%s: memory error (%s, file %s, line %d), please report to \"%s\"\n",
					MYNAME, strerror(errno), __FILE__, __LINE__, BUGTRACK_MAIL );

				free(word_wc);
				return -1;
			}

			wcscpy(lang_wc, token_word_wc);
			//wcsncpy(lang_wc, token_word_wc, wcslen(token_word_wc) -1);
			//memmove(lang_wc, token_word_wc, lang_wc_len);

			first_token_flag = false;
			continue;
		}

		play_command_len = (strlen(AUDIO_PLAYER_PROG) + strlen(ALL_SOUNDS_DIR) +
			wcslen(token_word_wc) * sizeof(wchar_t) + strlen(AUDIO_POSTFIX) + 32) * sizeof(char);

		if ( (play_command = (char *) malloc(play_command_len)) == NULL )
		{
			fprintf(stderr, "%s: memory error (%s, file %s, line %d), please report to \"%s\"\n",
				MYNAME, strerror(errno), __FILE__, __LINE__, BUGTRACK_MAIL );

			free(word_wc);
			if ( !first_token_flag ) free(lang_wc);
			return -1;
		}

		sprintf(play_command, "%s %s/%ls/%lc/%ls%s", AUDIO_PLAYER_PROG, ALL_SOUNDS_DIR,
			lang_wc, token_word_wc[0], token_word_wc, AUDIO_POSTFIX);

		system(play_command);

		free(play_command);
	}

	free(word_wc);
	if ( !first_token_flag ) free(lang_wc);
	return 0;
}

/********************************************************************************
*										*
*	read_index() - chitaet dannye ob indexe iz slovarya i vozvrashyaet	*
*		index dlya ukazannogo simvola.					*
*										*
********************************************************************************/
static long read_index(const wchar_t ch_wc, FILE *dict_fp)
{
	//////////////////////////////////////////
	char	*str = NULL;			// Chitaemaya stroka
	wchar_t	ch_str_wc;			// Pervyy rasshirennyy simvol chitaemoy stroki
	size_t	str_len = 0;			// Dlina chitaemoy stroki
	long	pos = 0;			// Index
	bool	begin_read_flag = false;	// Flag nachala chteniya
	//////////////////////////////////////////


	// Chitaem file ...
	while ( getline(&str, &str_len, dict_fp) != -1 )
	{
		if ( (str[0] == '#') || (str[0] == '\n') ) continue;

		del_nl(str);

		if ( !strcmp(str, "[noindex]") )
		{
			free(str);
			return -1;
		}
		if ( !strcmp(str, "[index]") )
		{
			begin_read_flag = true;
			continue;
		}
		if ( !begin_read_flag ) continue;
		if ( !strcmp(str, "[/index]") ) break;

		if ( sscanf(str, "%lc %ld", &ch_str_wc, &pos) != 2 )
		{
			fprintf(stderr, "%s: warning: bad index: \"%s\": ignored\n",
				MYNAME, str);
			continue;
		}

		if ( towlower(ch_str_wc) == towlower(ch_wc) ) break;
	}

	free(str);
	return pos;
}

/********************************************************************************
*										*
*	print_begin_page() - pechatat nachalo stranicy.				*
*										*
********************************************************************************/
void print_begin_page(const char *word)
{
	//////////////////////////////////
	extern settings_t settings;	// Parametry sistemy
	//////////////////////////////////

	if ( settings.output_format == html_output_format )
	{
		printf("<html>\n"
			"<!-- Lisa, I Love You!!! -->\n"
			"<!--      ___  ___       -->\n"
			"<!--     /   \\/   \\      -->\n"
			"<!--    (          )     -->\n"
			"<!--     \\        /      -->\n"
			"<!--      \\      /       -->\n"
			"<!--        \\  /         -->\n"
			"<!--         \\/          -->\n"
			"<!-- ------------------- -->\n"
			"<head>\n"
			"\t<title>%s</title>\n"
			"\t<meta name=\"GENERATOR\" content=\"SL Engine\">\n"
			"\t<meta name=\"AUTHOR\" content=\"Devaev Maxim aka Liksys\">\n"
			"\t<meta http-equiv=\"Content-Type\" content=\"text/html; charset=%s\">\n"
			"</head>\n"
			"<body>\n"
			"<!-- translate --->\n", word, settings.locale_encoding);
	}
}

/********************************************************************************
*										*
*	print_end_page() - pechataet konec stranicy.				*
*										*
********************************************************************************/
void print_end_page(void)
{
	//////////////////////////////////
	extern settings_t settings;	// Parametry sistemy
	//////////////////////////////////


	if ( settings.output_format == html_output_format )
		printf("</body>\n</html>\n");
}

/********************************************************************************
*										*
*	print_separator() - pechataet razdelitel.				*
*										*
********************************************************************************/
static void print_separator(void)
{
	//////////////////////////////////
	int	count;			// Schetchik
	extern settings_t settings;	// Parametry sistemy
	//////////////////////////////////


	if ( settings.output_format == html_output_format )
		fputs("\t<hr>\n", stdout);
	else if ( settings.output_format == text_output_format )
	{
		for (count = 0; count < settings.max_terminal_line_len; count++)
			putchar('-');
		putchar('\n');
	}
	// native format pass
}

/********************************************************************************
*										*
*	print_header() - pechataet vyrovnennyy po centru zagolovok.		*
*										*
********************************************************************************/
static void print_header(const char *dict_name)
{
	//////////////////////////////////
	int	count;			// Schetchik
	extern settings_t settings;	// Parametry sistemy
	//////////////////////////////////


	if ( settings.output_format == html_output_format )
	{
		printf("\t<table border=\"0\" width=\"100%\"><tr><td bgcolor=\"#DFEDFF\"><h2 align=\"center\"><em>");
		for (; (*dict_name); dict_name++)
			if ( (*dict_name) == '_' ) putchar(' ');
			else putchar(*dict_name);
		printf("</em></h2></td></tr></table>\n");
	}
	else if ( settings.output_format == text_output_format )
	{
		if ( strlen(dict_name) >= settings.max_terminal_line_len )
			puts(dict_name);
		else
		{
			for (count = 0; count < ((settings.max_terminal_line_len
				- strlen(dict_name)) / 2); count++)
				putchar('=');
			putchar(' ');
			if ( settings.use_terminal_escapes_flag ) printf("\033[1m");
			for (++count; (*dict_name); dict_name++, count++)
				if ( (*dict_name) == '_' ) putchar(' ');
				else putchar(*dict_name);
			if ( settings.use_terminal_escapes_flag ) printf("\033[0m");
			putchar(' ');
			for (++count; count < settings.max_terminal_line_len; count++)
				putchar('=');
			putchar('\n');
		}
	}
	// native format pass
}

/********************************************************************************
*										*
*	print_list_item() - pechataet element spiska slov.			*
*										*
********************************************************************************/
static void print_list_item(const wchar_t *word_wc, const int word_number)
{
	//////////////////////////////////////////
	static long	link_count = 0l;	// Schetchik ssylok
	extern settings_t settings;		// Parametry sistemy
	//////////////////////////////////////////


	if ( settings.output_format == html_output_format )
	{
		printf("\t(<em>%d</em>) <a name=\"z_%ls\"></a><a href=\"#z_%ls\">%ls</a><br>\n",
			word_number, word_wc, word_wc, word_wc);
		++link_count;
	}
	else if ( settings.output_format == text_output_format )
	{
		if ( settings.use_terminal_escapes_flag )
			printf(" \033[1m(%d)\033[0m %ls\n", word_number, word_wc);
		else printf(" (%d) %ls\n", word_number, word_wc);
	}
	else if ( settings.output_format == native_output_format )
		printf("%ls\n", word_wc);
}

/********************************************************************************
*										*
*	print_translate() - pechataet otformatirovannyy perevod.		*
*										*
********************************************************************************/
static void print_translate(const char *str, const int word_number)
{
	//////////////////////////////////////////
	int	strong_font_count = 0;		// Schetchik jirnogo teksta
	int	italic_font_count = 0;		// Schetchik kursivnogo teksta
	int	green_font_count = 0;		// Schetchik zelenogo teksta
	int	blocks_count = 0;		// Schetchik blokov
	int	char_count = 0;			// Schetchik simvolov
	int	count = 0;			// Schetchik dlya blokov
	bool	underline_text_flag = false;	// Flag podcherknutogo teksta
	bool	word_link_text_flag = false;	// Flag ssylki-teksta
	bool	sound_link_text_flag = false;	// Flas ssyli-zvuka
	bool	shiel_flag = false;		// Flag ekranirovaniya
	static long		link_count = 0l;// Shetchik ssylok
	extern settings_t	settings;	// Parametry sistemy
	//////////////////////////////////////////


	if ( word_number == 1 ) print_separator();

	if ( settings.output_format == html_output_format )
	{
		printf("\t<dl><dd>\n\t\t<strong><em>(%d)</em></strong> ", word_number);

		for (; (*str); str++)
		{
			if ( (*str) == '\n' )
			{
				shiel_flag = false; // fignya ;-)
				continue;
			}

			if ( ((*str) == '\\') && !shiel_flag )
			{
				shiel_flag = true;
				continue;
			}
			if ( shiel_flag )
			{
				switch (*str)
				{
					case '[' : printf("<strong>"); ++strong_font_count; break;
					case ']' : if ( strong_font_count > 0 )
						{ printf("</strong>"); --strong_font_count; } break;

					case '(' : printf("<em>"); ++italic_font_count; break;
					case ')' : if ( italic_font_count > 0 )
						{ printf("</em>"); --italic_font_count; } break;

					case '<' : printf("<font color=\"#0A7700\">"); ++green_font_count; break;
					case '>' : if ( green_font_count > 0 )
						{ printf("</font>"); --green_font_count; } break;

					case '{' : printf("<dl><dd>"); ++blocks_count; break;
					case '}' : if ( blocks_count > 0 )
						{ printf("</dd></dl>"); --blocks_count; } break;

					case '_' : if ( !underline_text_flag )
						{ printf("<u>"); underline_text_flag = true; }
						else { printf("</u>"); underline_text_flag = false; } break;

					case '@' : if ( !word_link_text_flag )
						{ printf("<u><font color=\"#DFEDFF\">"); word_link_text_flag = true; }
						else { printf("</font></u>"); word_link_text_flag = false; } break;

					case 's' : if ( !sound_link_text_flag )
						{ printf("&nbsp;<a href=\"#s%ld_", link_count);
						++link_count; sound_link_text_flag = true; }
						else { printf("\"><img src=\"%s/play_16.png\" "
							"align=\"absmiddle\" alt=\"[&gt;]\"></a>&nbsp;",
						ICONS_DIR); sound_link_text_flag = false; } break;

					case '\\' : putchar('\\'); break;

					case 'n' : printf("<br>"); break;

					case 't' : printf("&nbsp;&nbsp;&nbsp;"); break;

					default : break;
				}

				shiel_flag = false;
				continue;
			}

			if ( (*str) == '\"' ) printf("&quot;");
			else if ( (*str) == '&' ) printf("&amp;");
			else if ( (*str) == '<' ) printf("&lt;");
			else if ( (*str) == '>' ) printf("&gt;");
			else putchar(*str);
		}

		for (; strong_font_count > 0; strong_font_count--) printf("</strong>");
		for (; italic_font_count > 0; italic_font_count--) printf("</em>");
		for (; green_font_count > 0; green_font_count--) printf("</font>");
		for (; blocks_count > 0; blocks_count--) printf("</dd></dl>");
		if ( underline_text_flag ) { printf("</u>"); underline_text_flag = false; }
		if ( word_link_text_flag ) { printf("</font></u>"); word_link_text_flag = false; }

		printf("\n\t</dd></dl>\n");
	}
	else if ( settings.output_format == text_output_format )
	{
		if ( settings.use_terminal_escapes_flag )
			printf("   \033[1m(%d)\033[0m ", word_number);
		else printf("   (%d) ", word_number);

		for (; (*str); str++)
		{
			if ( (*str) == '\n' )
			{
				shiel_flag = false; // fignya ;-)
				continue;
			}

			if ( ((*str) == '\\') && !shiel_flag )
			{
				shiel_flag = true;
				continue;
			}
			if ( shiel_flag )
			{
				switch (*str)
				{
					case '[' : if ( settings.use_terminal_escapes_flag )
						{ printf("\033[1m"); strong_font_count = 1; } break;
					case ']' : if ( settings.use_terminal_escapes_flag )
						{
							printf("\033[0m");
							if ( green_font_count ) printf("\033[32m");
							if ( underline_text_flag ) printf("\033[4m");
							strong_font_count = 0;
						} break;

					case '<' : if ( settings.use_terminal_escapes_flag )
						{ printf("\033[32m"); green_font_count = 1; } break;
					case '>' : if ( settings.use_terminal_escapes_flag )
						{
							printf("\033[0m");
							if ( strong_font_count ) printf("\033[1m");
							if ( underline_text_flag ) printf("\033[4m");
							green_font_count = 0;
						} break;

					case '{' : blocks_count += 3; char_count = blocks_count;
						putchar('\n');
						for (count = 0; count < blocks_count; count++) putchar(' ');
						break;
					case '}' : blocks_count -= 3;
						if ( blocks_count < 0 ) blocks_count = 0;
						char_count = blocks_count;
						break;

					case '_' : if ( settings.use_terminal_escapes_flag )
						{
							if ( !underline_text_flag )
							{ printf("\033[4m"); underline_text_flag = true; }
							else { printf("\033[24m"); underline_text_flag = false; }
						} break;

					case '@' : if ( settings.use_terminal_escapes_flag )
						{
							if ( !word_link_text_flag )
							{ printf("\033[4m"); word_link_text_flag = true; }
							else { printf("\033[24m"); word_link_text_flag = false; }
						} break;

					case 's' : if ( settings.use_terminal_escapes_flag )
						{
							if ( !sound_link_text_flag )
							{ printf("[\033[4msnd:\""); sound_link_text_flag = true; }
							else { printf("\"\033[24m]"); sound_link_text_flag = false; }
						} break;

					case '\\' : putchar('\\'); break;

					case 'n' : putchar('\n'); break;

					case 't' : putchar('\t'); break;

					default : break;
				}

				shiel_flag = false;
				continue;
			}

			if ( (char_count > (int)((float)settings.max_terminal_line_len * 0.8)) &&
				((*str) == ' ') && !isdigit(*(str +1)) )
				{
					putchar('\n');
					for (count = 0; count < blocks_count +3; count++) putchar(' ');
					char_count = blocks_count +3;
				}
			putchar(*str);
			++char_count;
		}

		if ( settings.use_terminal_escapes_flag ) printf("\033[0m"); // Sbros parametrov terminala
		// Eta posledovatelnost universalmaya, ona vystavlyaet parametry
		// konsoli na defoltnye parametry. Esli kakoy-to teg okajetsya ne
		// zakrytym, to eta posledovatelnost pribet vse modifikacii i
		// sostoyanie konsoli budet vosstanovleno do ishodnogo.
		// Za podrobnostyami - smotri stranicu "man 4 console_codes".
	}
	else if ( settings.output_format == native_output_format )
		for (; (*str) && (*str) != '\n'; str++)
			putchar(*str);

	putchar('\n');
	print_separator();
}

/********************************************************************************
*********************************************************************************
********************************************************************************/
