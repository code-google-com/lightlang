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


#ifndef MANAGER_H
# define MANAGER_H

# define _GNU_SOURCE

# include "config.h"


# define ALL_DICTS_DIR DATA_ROOT_DIR "/sl/dicts"


int connect_dict(const char *dict_name);
int disconnect_dict(const char *dict_name);

int print_dicts_list(void);
int print_dict_info(const char *dict_name);


#endif // MANAGER_H

