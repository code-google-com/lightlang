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
#include <sys/types.h>
#include <sys/stat.h>
#include <dirent.h>
#include <errno.h>

#include "const.h"
#include "settings.h"
#include "string.h"

#include "manager.h"

static int print_dir(const char *dicts_dir);


int connect_dict(const char *dict_name)
{
	char *src_dict_path;
	char *dest_dict_path;
	size_t src_dict_path_len;
	size_t dest_dict_path_len;
	extern settings_t settings;


	src_dict_path_len = (strlen(ALL_DICTS_DIR) + strlen(dict_name) + 16) * sizeof(char);
	dest_dict_path_len = (strlen(settings.user_dicts_dir) + strlen(dict_name) + 16) * sizeof(char);

	if ( (src_dict_path = (char *) malloc(src_dict_path_len)) == NULL ) {
		fprintf(stderr, "%s: memory error (%s, file %s, line %d), please report to \"%s\"\n",
			MYNAME, strerror(errno), __FILE__, __LINE__, BUGTRACK_MAIL);
		return -1;
	}

	if ( (dest_dict_path = (char *) malloc(dest_dict_path_len)) == NULL ) {
		fprintf(stderr, "%s: memory error (%s, file %s, line %d), please report to \"%s\"\n",
			MYNAME, strerror(errno), __FILE__, __LINE__, BUGTRACK_MAIL);

		free(src_dict_path);

		return -1;
	}

	sprintf(src_dict_path, "%s/%s", ALL_DICTS_DIR, dict_name);
	sprintf(dest_dict_path, "%s/%s", settings.user_dicts_dir, dict_name);

	printf("%s: connecting dict \"%s\"...\n", MYNAME, dict_name);
	if ( access(src_dict_path, F_OK) != 0 ) {
		fprintf(stderr, "%s: cannot connect dict \"%s\": %s\n", MYNAME, dict_name, strerror(errno));

		free(src_dict_path);
		free(dest_dict_path);

		return -1;
	}
	if ( symlink(src_dict_path, dest_dict_path) != 0 ) {
		fprintf(stderr, "%s: cannot connect dict \"%s\": %s\n", MYNAME, dict_name, strerror(errno));

		free(src_dict_path);
		free(dest_dict_path);

		return -1;
	}
	printf("%s: done\n", MYNAME);

	free(src_dict_path);
	free(dest_dict_path);

	return 0;
}

int disconnect_dict(const char *dict_name)
{
	char *dict_path;
	size_t dict_path_len;
	extern settings_t settings;


	dict_path_len = (strlen(settings.user_dicts_dir) + strlen(dict_name) + 16) * sizeof(char);

	if ( (dict_path = (char *) malloc(dict_path_len)) == NULL ) {
		fprintf(stderr, "%s: memory error (%s, file %s, line %d), please report to \"%s\"\n",
			MYNAME, strerror(errno), __FILE__, __LINE__, BUGTRACK_MAIL);
		return -1;
	}

	sprintf(dict_path, "%s/%s", settings.user_dicts_dir, dict_name);

	printf("%s: disconnecting dict \"%s\"...\n", MYNAME, dict_name);
	if ( unlink(dict_path) != 0 ) {
		fprintf(stderr, "%s: cannot disconnect dict \"%s\": %s\n", MYNAME, dict_name, strerror(errno));

		free(dict_path);

		return -1;
	}
	printf("%s: done\n", MYNAME);

	free(dict_path);

	return 0;
}

int print_dicts_list(void)
{
	extern settings_t settings;


	printf("%s: established dicts:\n", MYNAME);
	if ( print_dir(ALL_DICTS_DIR) != 0 )
		return -1;

	printf("%s: connected dicts:\n", MYNAME);
	if ( print_dir(settings.user_dicts_dir) != 0 )
		return -1;

	return 0;
}


static int print_dir(const char *dicts_dir)
{
	DIR *dicts_dp;
	struct dirent *dicts_dp_ent;
	struct stat dict_st;
	char *dict_path;
	size_t dict_path_len;
	int count = 0;


	if ( (dicts_dp = opendir(dicts_dir)) == NULL ) {
		fprintf(stderr, "%s: cannot open folder \"%s\": %s\n", MYNAME, dicts_dir, strerror(errno));
		return -1;
	}

	while ( (dicts_dp_ent = readdir(dicts_dp)) != NULL ) {
		if ( dicts_dp_ent->d_name[0] == '.' )
			continue;

		dict_path_len = (strlen(dicts_dir) + strlen(dicts_dp_ent->d_name) + 16) * sizeof(char);

		if ( (dict_path = (char *) malloc(dict_path_len)) == NULL ) {
			fprintf(stderr, "%s: memory error (%s, file %s, line %d), please report to \"%s\"\n",
				MYNAME, strerror(errno), __FILE__, __LINE__, BUGTRACK_MAIL );

			if ( closedir(dicts_dp) != 0 )
				fprintf(stderr, "%s: cannot close folder \"%s\": %s\n", MYNAME, dicts_dir, strerror(errno));

			return -1;
		}

		sprintf(dict_path, "%s/%s", dicts_dir, dicts_dp_ent->d_name);

		if ( lstat(dict_path, &dict_st) != 0 ) {
			fprintf(stderr, "%s: cannot get information about dict \"%s\": %s\n", MYNAME, dicts_dp_ent->d_name, strerror(errno));

			if ( closedir(dicts_dp) != 0 )
				fprintf(stderr, "%s: cannot close folder \"%s\": %s\n", MYNAME, dicts_dir, strerror(errno));

			free(dict_path);

			return -1;
		}

		dict_st.st_mode &= S_IFMT;
		if ( (dict_st.st_mode & S_IFLNK) != S_IFLNK && (dict_st.st_mode & S_IFREG) != S_IFREG ) {
			free(dict_path);
			continue;
		}

		++count;

		printf(" (%d)\t%s\n", count, dicts_dp_ent->d_name);

		free(dict_path);
	}

	if ( closedir(dicts_dp) != 0 )
		fprintf(stderr, "%s: cannot close folder \"%s\": %s\n", MYNAME, dicts_dir, strerror(errno));

	return 0;
}

