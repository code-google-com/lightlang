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
*	manager.h - funkcii administrirovaniya slovarey.			*
*										*
********************************************************************************/


#define _GNU_SOURCE

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <wchar.h>
#include <wctype.h>
#include <unistd.h>
#include <dirent.h>
#include <fcntl.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <errno.h>

#include "const.h"
#include "settings.h"
#include "mstring.h"

#include "manager.h"

/********************************************************************************
*										*
*	install_dict() - funkciya ustanovki slovarya.				*
*										*
********************************************************************************/
int install_dict(const char *in_dict_path)
{
	//////////////////////////////////
	char	*dict_name;		// Imya slovarya
	char	*out_dict_path;		// Vyhodnogy puti k slovaryu
	char	*ptr;			// Ukazatel
	size_t	out_dict_path_len;	// Dlina vyhodnogo puti k slovaryu
	//////////////////////////////////


	// Opredelyaem imya slovarya ...
	if ( (ptr = strrchr(in_dict_path, '/')) == NULL )
		dict_name = (char *) in_dict_path;
	else
		dict_name = ptr + 1;
	// dict_name = (char *) in_dict_path;
	// Eta strochka potencialno opasnaya, poskolku <in_dict_path> - konstanta,
	// a <dict_name> - net. Tut bylo ispolzovano privedenie tipov, chtoby
	// izbavitsya ot preduprejdeniya kompilyatora.

	// Opredelyaem dlinu puti ...
	out_dict_path_len = (strlen(ALL_DICTS_DIR) + strlen(dict_name) + 16) * sizeof(char);

	// Vydelyaem pamyat dlya puti ...
	if ( (out_dict_path = (char *) malloc(out_dict_path_len)) == NULL )
	{
		fprintf(stderr, "%s: memory error (%s, file %s, line %d), please report to \"%s\"\n",
			MYNAME, strerror(errno), __FILE__, __LINE__, BUGTRACK_MAIL);
		return -1;
	}

	// Sozdaem put dlya vyhodnogo fila ...
	sprintf(out_dict_path, "%s/%s", ALL_DICTS_DIR, dict_name);

	// Kopiruem ...
	printf("%s: installation of \"%s\" is starting...\n", MYNAME, in_dict_path);
	if ( copy_file(in_dict_path, out_dict_path) != 0 )
	{
		free(out_dict_path);
		return -1;
	}
	printf("%s: done\n", MYNAME);

	free(out_dict_path);
	return 0;
}

/********************************************************************************
*										*
*	remove_dict() - udalyaet slovar iz sistemy.				*
*										*
********************************************************************************/
int remove_dict(const char *dict_name)
{
	//////////////////////////
	char	*dict_path;	// Put k slovaryu
	size_t	dict_path_len;	// Dlina puti k slovaryu
	//////////////////////////

	// Vychislyaem dlinu puti k slovaryu ...
	dict_path_len = (strlen(ALL_DICTS_DIR) + strlen(dict_name) + 16) * sizeof(char);

	// Vydelyaem pamyat dlya puti k slovaryu ...
	if ( (dict_path = (char *) malloc(dict_path_len)) == NULL )
	{
		fprintf(stderr, "%s: memory error (%s, file %s, line %d), please report to \"%s\"\n",
			MYNAME, strerror(errno), __FILE__, __LINE__, BUGTRACK_MAIL);
		return -1;
	}

	// Formiruem put ...
	sprintf(dict_path, "%s/%s", ALL_DICTS_DIR, dict_name);

	// Udalyaem slovar ...
	printf("%s: removing dict \"%s\"...\n", MYNAME, dict_name);
	if ( unlink(dict_path) != 0 )
	{
		fprintf(stderr, "%s: cannot remove dict \"%s\": %s\n", MYNAME, dict_name, strerror(errno));

		free(dict_path);
		return -1;
	}
	printf("%s: done\n", MYNAME);

	free(dict_path);
	return 0;
}

/********************************************************************************
*										*
*	connect_dict() - podklyuchaet ukazannyy slovar.				*
*										*
*		Funkciya sozdaet ssylku iz sistemnogo kataloga so slovaryami	*
*		v polzovatelskiy katalog.					*
*										*
********************************************************************************/
int connect_dict(const char *dict_name)
{
	//////////////////////////////////////////////////
	char	*in_dict_path, *out_dict_path;		// Puti k slovaryam
	size_t	in_dict_path_len, out_dict_path_len;	// Dlina putey
	extern settings_t settings;			// Parametry sistemy
	//////////////////////////////////////////////////


	// Vychislyaem dliny putey ...
	in_dict_path_len = (strlen(ALL_DICTS_DIR) + strlen(dict_name) + 16) * sizeof(char);
	out_dict_path_len = (strlen(settings.user_dicts_dir) + strlen(dict_name) + 16) * sizeof(char);

	// Vydelyaem pamyat ...
	if ( (in_dict_path = (char *) malloc(in_dict_path_len)) == NULL )
	{
		fprintf(stderr, "%s: memory error (%s, file %s, line %d), please report to \"%s\"\n",
			MYNAME, strerror(errno), __FILE__, __LINE__, BUGTRACK_MAIL);
		return -1;
	}

	if ( (out_dict_path = (char *) malloc(out_dict_path_len)) == NULL )
	{
		fprintf(stderr, "%s: memory error (%s, file %s, line %d), please report to \"%s\"\n",
			MYNAME, strerror(errno), __FILE__, __LINE__, BUGTRACK_MAIL);

		free(in_dict_path);
		return -1;
	}

	// Formiruem puti ...
	sprintf(in_dict_path, "%s/%s", ALL_DICTS_DIR, dict_name);
	sprintf(out_dict_path, "%s/%s", settings.user_dicts_dir, dict_name);

	// Podkluchem slovar. Snachala nado proverit,
	// Sushestvuet li sistemnyy slovar.
	printf("%s: connecting dict \"%s\"...\n", MYNAME, dict_name);
	if ( access(in_dict_path, F_OK) != 0 )
	{
		fprintf(stderr, "%s: cannot connect dict \"%s\": %s\n", MYNAME, dict_name, strerror(errno));

		free(in_dict_path);
		free(out_dict_path);
		return -1;
	}

	// Sozdaem ssylku
	if ( symlink(in_dict_path, out_dict_path) != 0 )
	{
		fprintf(stderr, "%s: cannot connect dict \"%s\": %s\n", MYNAME, dict_name, strerror(errno));

		free(in_dict_path);
		free(out_dict_path);
		return -1;
	}
	printf("%s: done\n", MYNAME);

	free(in_dict_path);
	free(out_dict_path);
	return 0;
}

/********************************************************************************
*										*
*	disconnect_dict() - otkluchaet slovar (udalyaet ssylku).		*
*										*
********************************************************************************/
int disconnect_dict(const char *dict_name)
{
	//////////////////////////////////
	char	*dict_path;		// Put k slovaryu
	size_t	dict_path_len;		// Dlina puti
	extern settings_t settings;	// Parametry sistemy
	//////////////////////////////////


	// Vychislyaem dlinu puti ...
	dict_path_len = (strlen(settings.user_dicts_dir) + strlen(dict_name) + 16) * sizeof(char);

	// Vydelyaem pamyat ...
	if ( (dict_path = (char *) malloc(dict_path_len)) == NULL )
	{
		fprintf(stderr, "%s: memory error (%s, file %s, line %d), please report to \"%s\"\n",
			MYNAME, strerror(errno), __FILE__, __LINE__, BUGTRACK_MAIL);
		return -1;
	}

	// Formiruem put ...
	sprintf(dict_path, "%s/%s", settings.user_dicts_dir, dict_name);

	// Otkluchaem slovar ...
	printf("%s: disconnecting dict \"%s\"...\n", MYNAME, dict_name);
	if ( unlink(dict_path) != 0 )
	{
		fprintf(stderr, "%s: cannot disconnect dict \"%s\": %s\n", MYNAME, dict_name, strerror(errno));

		free(dict_path);
		return -1;
	}
	printf("%s: done\n", MYNAME);

	free(dict_path);
	return 0;
}

/********************************************************************************
*										*
*	print_info() - pechataet informaciyu o sostoyanii slovarey.		*
*										*
********************************************************************************/
int print_info(void)
{
	//////////////////////////////////
	extern settings_t settings;	// Parametry sistemy
	//////////////////////////////////


	// Pokazat ustanovlennye slovari
	printf("%s: established dicts:\n", MYNAME);
	if ( print_dir(ALL_DICTS_DIR) != 0 ) return -1;

	// Pokazat polzovatelskie slovari
	printf("%s: connected dicts:\n", MYNAME);
	if ( print_dir(settings.user_dicts_dir) != 0 ) return -1;

	return 0;
}

/********************************************************************************
*										*
*	print_index() - vyvodit index dlya fila-slovarya.			*
*										*
********************************************************************************/
int print_index(const char *dict_path)
{
	//////////////////////////
	char	*str = NULL;	// Chitaemaya stroka
	size_t	str_len = 0;	// Dlina chitaemoy stroki
	wchar_t	ch_wc = L'\0';	// Simvol
	long	pos;		// Index
	FILE	*dict_fp;	// Ukazatel-na-file
	char	*ptr;		// Ukazatel na dva probela
	//////////////////////////


	// Otkryvaem file slovarya
	if ( (dict_fp = fopen(dict_path, "r")) == NULL )
	{
		fprintf(stderr, "%s: cannot open file \"%s\": %s\n", MYNAME, dict_path, strerror(errno));
		return -1;
	}

	// Sostavlyaem tablicu indexov
	// puts("# Embedded SL Index Creator");
	puts("[index]");
	while ( true )
	{
		// Poluchaem smeshenie fila
		if ( (pos = ftell(dict_fp)) == -1 ) break;

		// Chitaem sleduyushuyu stroku
		if ( getline(&str, &str_len, dict_fp) == -1 ) break;

		// Propuskaem pustye stroki i kamenty
		if ( (str[0] == '#') || (str[0] == '\n') ) continue;

		// Filtruem ...
		if ( (ptr = strstr(str, "  ")) != NULL )
			(*ptr) = '\0';
		else continue;

		// Sravnivaem predydushiy simvol i tekushiy
		if ( towlower(ch_wc) != get_first_low_wc(str) )
		{
			ch_wc = get_first_low_wc(str);
			printf("%lc %ld\n", ch_wc, pos);
		}
	}
	puts("[/index]");

	free(str);

	if ( fclose(dict_fp) != 0 )
		fprintf(stderr, "%s: cannot close file \"%s\": %s\n", MYNAME, dict_path, strerror(errno));

	return 0;
}

/********************************************************************************
*										*
*	copy_file() - kopiruet fily iz <in_file_path> v <out_file_path>.	*
*										*
********************************************************************************/
static int copy_file(const char *in_file_path, const char *out_file_path)
{
	//////////////////////////////////////////
	int	in_file_fd, out_file_fd;	// Deskriptory filov
	char	buf[BUFSIZ];			// Razmer buffera
	ssize_t	rcount, wcount;			// Schetchiki chteniya/zapisi
	//////////////////////////////////////////

	if ( (in_file_fd = open(in_file_path, O_RDONLY)) == -1 )
	{
		fprintf(stderr, "%s: cannot open in file \"%s\": %s\n",	MYNAME, in_file_path, strerror(errno));
		return -1;
	}

	if ( (out_file_fd = open(out_file_path, O_WRONLY|O_CREAT|O_TRUNC, 0644)) == -1 )
	{
		fprintf(stderr, "%s: cannot open out file \"%s\": %s\n", MYNAME, out_file_path, strerror(errno));

		if ( close(in_file_fd) != 0 )
			fprintf(stderr, "%s: close error in file \"%s\": %s\n", MYNAME, in_file_path, strerror(errno));

		return -1;
	}

	while ( (rcount = read(in_file_fd, (char *) buf, sizeof(buf) )) > 0 )
	{
		wcount = write(out_file_fd, (char *) buf, rcount );

		if (rcount != wcount)
		{
			fprintf(stderr, "%s: read/write error: %s\n", MYNAME, strerror(errno));

			if ( close(in_file_fd) != 0 )
				fprintf(stderr, "%s: close error in file \"%s\": %s\n", MYNAME, in_file_path, strerror(errno));

			if ( close(out_file_fd) != 0 )
				fprintf(stderr, "%s: close error out file \"%s\": %s\n", MYNAME, out_file_path, strerror(errno));

			return -1;
		}
	}

	if ( close(in_file_fd) != 0 )
		fprintf(stderr, "%s: close error in file \"%s\": %s\n", MYNAME, in_file_path, strerror(errno));

	if ( close(out_file_fd) != 0 )
		fprintf(stderr, "%s: close error out file \"%s\": %s\n", MYNAME, out_file_path, strerror(errno));

	return 0;
}

/********************************************************************************
*										*
*	print_dir() - pechataet soderjimoe ukazannogo kataloga			*
*										*
********************************************************************************/
static int print_dir(const char *dicts_dir) // private
{
	//////////////////////////////////
	DIR		*dicts_dp;	// Ukazatel na katalog so slovaryami
	struct dirent	*dicts_dp_ent;	// Element kataloga
	struct stat	dict_st;	// Informaciya o file slovarya
	char		*dict_path;	// Put k slovaryu
	size_t		dict_path_len;	// Dlina puti k slovaryu
	int		count = 0;	// Schetchik elementov
	//////////////////////////////////


	// Otkryvaem katalog so slovaryami ...
	if ( (dicts_dp = opendir(dicts_dir)) == NULL )
	{
		fprintf(stderr, "%s: cannot open folder \"%s\": %s\n", MYNAME, dicts_dir, strerror(errno));
		return -1;
	}

	// Chitaem ...
	while ( (dicts_dp_ent = readdir(dicts_dp)) != NULL )
	{
		// Skrytye fily otseivaem
		if ( dicts_dp_ent->d_name[0] == '.' ) continue;

		// Vychislyaem dlinu puti k slovaryu ...
		dict_path_len = (strlen(dicts_dir) + strlen(dicts_dp_ent->d_name) + 16) * sizeof(char);

		// Vydelyaem pamyat ...
		if ( (dict_path = (char *) malloc(dict_path_len)) == NULL )
		{
			fprintf(stderr, "%s: memory error (%s, file %s, line %d), please report to \"%s\"\n",
				MYNAME, strerror(errno), __FILE__, __LINE__, BUGTRACK_MAIL );

			if ( closedir(dicts_dp) != 0 )
				fprintf(stderr, "%s: cannot close folder \"%s\": %s\n", MYNAME, dicts_dir, strerror(errno));

			return -1;
		}

		// Formiruem put k slovaryu ...
		sprintf(dict_path, "%s/%s", dicts_dir, dicts_dp_ent->d_name);

		// Poluchaem informaciyu o slovare
		if ( lstat(dict_path, &dict_st) != 0 )
		{
			fprintf(stderr, "%s: cannot get information about dict \"%s\": %s\n", MYNAME, dicts_dp_ent->d_name, strerror(errno));

			if ( closedir(dicts_dp) != 0 )
				fprintf(stderr, "%s: cannot close folder \"%s\": %s\n", MYNAME, dicts_dir, strerror(errno));

			free(dict_path);
			return -1;
		}

		// Tolko obychnye fily ili ssylki
		dict_st.st_mode &= S_IFMT;
		if ( ((dict_st.st_mode & S_IFLNK) != S_IFLNK) && ((dict_st.st_mode & S_IFREG) != S_IFREG) )
		{
			free(dict_path);
			continue;
		}

		++count;

		// Raspechataem ...
		printf(" (%d)\t%s\n", count, dicts_dp_ent->d_name);

		free(dict_path);
	}

	if ( closedir(dicts_dp) != 0 )
		fprintf(stderr, "%s: cannot close folder \"%s\": %s\n", MYNAME, dicts_dir, strerror(errno));

	return 0;
}

/********************************************************************************
*********************************************************************************
********************************************************************************/
