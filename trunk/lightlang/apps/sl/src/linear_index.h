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


#ifndef LINEAR_INDEX_H
# define LINEAR_INDEX_H

# define _GNU_SOURCE


# define BEGIN_INDEX_BLOCK "[index]"
# define END_INDEX_BLOCK "[/index]"
# define NO_INDEX_BLOCK "[noindex]"


long get_linear_index_pos(const wchar_t ch_wc, FILE *dict_fp);

int build_linear_index(const char *dict_path);


#endif // LINEAR_INDEX_H

