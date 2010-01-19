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
*	info.c - spravochnaya informaciya ob SL.				*
*										*
********************************************************************************/

#define _GNU_SOURCE

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>

#include "config.h"
#include "const.h"
#include "options.h"

#include "info.h"

/********************************************************************************
*										*
*	help() - vyvodit kratkuyu spravku na ekran.				*
*										*
********************************************************************************/
void help(void)
{
	version();
	putchar('\n');
	printf("Search options:\n");
	printf("\t-u <word> | --%s <word>\n", OPT_SEARCH_USUALLY);
	printf("\t-f <word> | --%s <word>\n", OPT_SEARCH_FIRST_CONCURRENCE);
	printf("\t-c <word> | --%s <word>\n", OPT_SEARCH_WORD_COMBINATIONS);
	printf("\t-l <word> | --%s <word>\n", OPT_SEARCH_LIST);
	printf("\t-i <word> | --%s <word>\n", OPT_SEARCH_ILL_DEFINED);
	printf("\t-s <package:word> | --%s <package:word>\n", OPT_SEARCH_SOUND);
	printf("Dict Management options:\n");
	printf("\t--%s <dict>\n", OPT_DICT_CONNECT);
	printf("\t--%s <dict>\n", OPT_DICT_DISCONNECT);
	printf("\t--%s\n", OPT_DICT_PRINT_INFO);
	printf("\t--%s <file>\n", OPT_DICT_INSTALL);
	printf("\t--%s <dict>\n", OPT_DICT_REMOVE);
	printf("\t--%s <list|of|dicts>\n", OPT_DICT_USE_LIST);
	printf("\t--%s <file>\n", OPT_DICT_PRINT_INDEX);
	printf("Misc options:\n");
	printf("\t-m <count> | --%s=<count>\n", OPT_MISC_MAX_TRANSLATE_COUNT);
	printf("\t-p <percent> | --%s=<percent>\n", OPT_MISC_PERCENT);
	printf("\t-t | --%s\n", OPT_MISC_SHOW_TIME);
	printf("Settings options:\n");
	printf("\t--%s=<html|text|native>\n", OPT_SETTINGS_OUTPUT_FORMAT);
	printf("\t--%s=<yes|no>\n", OPT_SETTINGS_USE_ESCS);
	printf("\t--%s=<yes|no>\n", OPT_SETTINGS_USE_CSS);
	printf("Information options:\n");
	printf("\t-h | --%s\n", OPT_INFO_HELP);
	printf("\t-v | --%s\n", OPT_INFO_VERSION);
	printf("\t-d | --%s\n", OPT_INFO_DEBUG);
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

/********************************************************************************
*										*
*	version() - pechataet versiyu programmy.				*
*										*
********************************************************************************/
void version(void)
{
	printf("%s-%s, Copyright (C) 2007-2016 Devaev Maxim, %s\n",
		MYNAME, VERSION, DEVELOPER_MAIL);
}

/********************************************************************************
*										*
*	debug() - pechataet otladochnuyu informaciyu.				*
*										*
********************************************************************************/
void debug(void)
{
	printf("Program name\t\t:\t%s\n", MYNAME);
	printf("Program version\t\t:\t%s\n", VERSION);
	printf("Package version\t\t:\t%s\n", PACKAGE_VERSION);

#ifdef __DATE__
	printf("Date of compilation\t:\t%s\n", __DATE__);
#endif

#ifdef __TIME__
	printf("Time of compilation\t:\t%s\n", __TIME__);
#endif

	putchar('\n');

#ifdef __VERSION__
	printf("GCC version\t\t:\t%s\n", __VERSION__);
#endif

#if __STDC_VERSION__ == 199901L
	puts("C standard\t\t:\tC99");
#else
	puts("C standard\t\t:\tNot C99");
#endif

#ifdef __OPTIMIZE__
	puts("Optimize\t\t:\tYes");
#else
	puts("Optimize\t\t:\tNo");
#endif

#ifdef __CFLAGS
	printf("CFLAGS\t\t\t:\t%s\n", CFLAGS);
#endif

#if defined(linux) || defined(__linux) || defined(__linux__)
	puts("System\t\t\t:\tLinux");
#elif defined(__FreeBSD__)
	puts("System\t\t\t:\tFreeBSD");
#elif defined(__NetBSD__)
	puts("System\t\t\t:\tNetBSD");
#elif defined(__OpenBSD__)
	puts("System\t\t\t:\tOpenBSD");
#elif defined(__DragonFly__)
	puts("System\t\t\t:\tDragonFlyBSD");
#elif defined(sun) || defined(__sun)
	puts("System\t\t\t:\tSolaris");
#elif defined(__CYGWIN__)
	puts("System\t\t\t:\tCygwin o_O ?!?");
#else
	puts("System\t\t\t:\tOther");
#endif

#if defined(__i386) || defined(__i386__)
	puts("Architecture\t\t:\ti386");
#elif defined(__x86_64) || defined(__x86_64__)
	puts("Architecture\t\t:\tx86_64");
# if defined(__amd64) || defined(__amd64__)
	puts("Architecture\t\t:\tAMD64");
# endif
#else
	puts("Architecture\t\t:\tOther");
#endif

	putchar('\n');

	printf("Audio player\t\t:\t%s\n", AUDIO_PLAYER_PROG);
	printf("prefix\t\t\t:\t%s\n", PREFIX);
	printf("datarootdir\t\t:\t%s\n", DATA_ROOT_DIR);

	putchar('\n');
}

/********************************************************************************
*********************************************************************************
********************************************************************************/
