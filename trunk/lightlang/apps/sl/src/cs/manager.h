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

#ifndef MANAGER_H
# define MANAGER_H

# define _GNU_SOURCE

# include "config.h"

/*********************************** Macro *************************************/
# define ALL_DICTS_DIR __PREFIX "/share/sl/dicts"

/********************************* Functions ***********************************/
int install_dict(const char *in_dict_path);	// Ustanavlivaet slovar
int uninstall_dict(const char *dict_name);	// Udalyaet slovar

int connect_dict(const char *dict_name);	// Podkluchaet slovar
int disconnect_dict(const char *dict_name);	// Otkluchaet slovar

int print_info(void);				// Pechataet infu o slovaryah

int print_index(const char *dict_path);		// Pechataet index slovarya


static int copy_file(const char *in_file_path, const char *out_file_path);
static int print_dir(const char *dicts_dir);	// Pechataet soderjimoe kataloga

#endif

/********************************************************************************
*********************************************************************************
********************************************************************************/
