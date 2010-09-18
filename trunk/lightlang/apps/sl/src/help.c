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

#include "config.h"
#include "const.h"
#include "options.h"

#include "help.h"


void help(void)
{
	version();
	putchar('\n');
	printf("Search options:\n");
	printf("\t-%c <word> | --%s <word>\n", OPT_SHORT_SEARCH_USUALLY, OPT_SEARCH_USUALLY);
	printf("\t-%c <word> | --%s <word>\n", OPT_SHORT_SEARCH_FIRST_CONCURRENCE, OPT_SEARCH_FIRST_CONCURRENCE);
	printf("\t-%c <word> | --%s <word>\n", OPT_SHORT_SEARCH_WORD_COMBINATIONS, OPT_SEARCH_WORD_COMBINATIONS);
	printf("\t-%c <word> | --%s <word>\n", OPT_SHORT_SEARCH_LIST, OPT_SEARCH_LIST);
	printf("\t-%c <word> | --%s <word>\n", OPT_SHORT_SEARCH_ILL_DEFINED, OPT_SEARCH_ILL_DEFINED);
	printf("\t-%c <package:word> | --%s <package:word>\n", OPT_SHORT_SEARCH_SOUND, OPT_SEARCH_SOUND);
	printf("Dicts Management options:\n");
	printf("\t--%s <dict>\n", OPT_DICT_CONNECT);
	printf("\t--%s <dict>\n", OPT_DICT_DISCONNECT);
	printf("\t--%s\n", OPT_DICT_PRINT_DICTS_LIST);
	printf("\t--%s <dict>\n", OPT_DICT_PRINT_DICT_INFO);
	printf("\t--%s <list|of|dicts>\n", OPT_DICT_USE_LIST);
	printf("\t--%s <file>\n", OPT_DICT_PRINT_INDEX);
	printf("Misc options:\n");
	printf("\t-%c <count> | --%s=<count>\n", OPT_SHORT_MISC_MAX_TRANSLATE_COUNT, OPT_MISC_MAX_TRANSLATE_COUNT);
	printf("\t-%c <percent> | --%s=<percent>\n", OPT_SHORT_MISC_ILL_DEFINED_SEARCH_PERCENT, OPT_MISC_ILL_DEFINED_SEARCH_PERCENT);
	printf("\t-%c | --%s\n", OPT_SHORT_MISC_SHOW_TIME, OPT_MISC_SHOW_TIME);
	printf("Settings options:\n");
	printf("\t--%s=<%s|%s|%s>\n", OPT_SETTINGS_OUTPUT_FORMAT, OPT_ARG_HTML_OUTPUT_FORMAT, OPT_ARG_TEXT_OUTPUT_FORMAT, OPT_ARG_NATIVE_OUTPUT_FORMAT);
	printf("\t--%s=<%s|%s>\n", OPT_SETTINGS_USE_ESCS, OPT_ARG_YES, OPT_ARG_NO);
	printf("\t--%s=<%s|%s>\n", OPT_SETTINGS_USE_CSS, OPT_ARG_YES, OPT_ARG_NO);
	printf("Information options:\n");
	printf("\t-%c | --%s\n", OPT_SHORT_INFO_HELP, OPT_INFO_HELP);
	printf("\t-%c | --%s\n", OPT_SHORT_INFO_VERSION, OPT_INFO_VERSION);
	printf("\t-%c | --%s\n", OPT_SHORT_INFO_DEBUG, OPT_INFO_DEBUG);
	printf("Environment:\n");
	printf("\tHOME\n");
	printf("\tCOLUMNS\n");
	putchar('\n');
	printf("Develper e-mail:\t\"%s\"\n", DEVELOPER_MAIL);
	printf("Bugtrack e-mail:\t\"%s\"\n", BUGTRACK_MAIL);
	printf("Offers e-mail:\t\t\"%s\"\n", OFFERS_MAIL);
	printf("Home page address:\t\"%s\"\n", HOME_PAGE_ADDRESS);
	putchar('\n');
}

void version(void)
{
	printf("%s-%s, Copyright (C) 2007-2016 Devaev Maxim, %s\n", MYNAME, VERSION, DEVELOPER_MAIL);
}

void debug(void)
{
	printf("Program name: %s\n", MYNAME);
	printf("Program version: %s\n", VERSION);
	printf("Package version: %s\n", PACKAGE_VERSION);

#ifdef __DATE__
	printf("Date of compilation: %s\n", __DATE__);
#endif

#ifdef __TIME__
	printf("Time of compilation: %s\n", __TIME__);
#endif

#ifdef __VERSION__
	printf("GCC version: %s\n", __VERSION__);
#endif

#if __STDC_VERSION__ == 199901L
	printf("C standard: C99\n");
#else
	printf("C standard: Not C99\n");
#endif

#ifdef __OPTIMIZE__
	printf("Optimize: Yes\n");
#else
	printf("Optimize: No\n");
#endif

#ifdef __CFLAGS
	printf("CFLAGS: %s\n", CFLAGS);
#endif

#if defined(linux) || defined(__linux) || defined(__linux__)
	printf("System: Linux\n");
#elif defined(__FreeBSD__)
	printf("System: FreeBSD\n");
#elif defined(__NetBSD__)
	printf("System: NetBSD\n");
#elif defined(__OpenBSD__)
	printf("System: OpenBSD\n");
#elif defined(__DragonFly__)
	printf("System: DragonFlyBSD\n");
#elif defined(sun) || defined(__sun)
	printf("System: Solaris\n");
#elif defined(__CYGWIN__)
	printf("System: Cygwin o_O ?!?\n");
#else
	printf("System: Other\n");
#endif

#if defined(__i386) || defined(__i386__)
	printf("Architecture: i386\n");
#elif defined(__x86_64) || defined(__x86_64__)
	printf("Architecture: x86_64\n");
# if defined(__amd64) || defined(__amd64__)
	printf("Architecture: AMD64\n");
# endif
#else
	printf("Architecture: Other\n");
#endif

	putchar('\n');

	printf("Audio player: %s\n", AUDIO_PLAYER_PROG);
	printf("datarootdir: %s\n", DATA_ROOT_DIR);
}

