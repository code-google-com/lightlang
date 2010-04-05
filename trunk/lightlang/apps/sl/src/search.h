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


#ifndef SEARCH_H
# define SEARCH_H

# define _GNU_SOURCE

# include <stdlib.h>
# include <stdbool.h>


# define ALL_SOUNDS_DIR DATA_ROOT_DIR "/sl/sounds"
# define AUDIO_POSTFIX ".ogg"
# define MAX_WORD_SIZE 256


typedef enum {
		usually_regimen,
		first_concurrence_regimen,
		word_combinations_regimen,
		list_regimen,
		ill_defined_regimen
	} regimen_t;


int find_word(const char *word, const regimen_t regimen, const char *dict_name, FILE *dict_fp);
int find_sound(const char *word);


#endif // SEARCH_H

