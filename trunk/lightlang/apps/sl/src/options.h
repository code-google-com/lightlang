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


#ifndef OPTIONS_H
# define OPTIONS_H

# define _GNU_SOURCE


# define OPT_SEARCH_USUALLY "usually"
# define OPT_SEARCH_FIRST_CONCURRENCE "first-concurrence"
# define OPT_SEARCH_WORD_COMBINATIONS "word-combinations"
# define OPT_SEARCH_LIST "list"
# define OPT_SEARCH_ILL_DEFINED "ill-defined"
# define OPT_SEARCH_SOUND "sound"

# define OPT_DICT_CONNECT "connect"
# define OPT_DICT_DISCONNECT "disconnect"
# define OPT_DICT_PRINT_DICTS_LIST "print-dicts-list"
# define OPT_DICT_USE_LIST "use-list"
# define OPT_DICT_PRINT_INDEX "print-index"

# define OPT_MISC_ILL_DEFINED_SEARCH_PERCENT "percent"
# define OPT_MISC_MAX_TRANSLATE_COUNT "max-translate-count"
# define OPT_MISC_SHOW_TIME "show-time"

# define OPT_SETTINGS_OUTPUT_FORMAT "output-format"
# define OPT_SETTINGS_USE_ESCS "use-terminal-escapes"
# define OPT_SETTINGS_USE_CSS "use-css"

# define OPT_INFO_HELP "help"
# define OPT_INFO_VERSION "version"
# define OPT_INFO_DEBUG "debug"

# define OPT_SHORT_SEARCH_USUALLY 'u'
# define OPT_SHORT_SEARCH_FIRST_CONCURRENCE 'f'
# define OPT_SHORT_SEARCH_WORD_COMBINATIONS 'c'
# define OPT_SHORT_SEARCH_LIST 'l'
# define OPT_SHORT_SEARCH_ILL_DEFINED 'i'
# define OPT_SHORT_SEARCH_SOUND 's'

# define OPT_SHORT_MISC_MAX_TRANSLATE_COUNT 'm'
# define OPT_SHORT_MISC_ILL_DEFINED_SEARCH_PERCENT 'p'
# define OPT_SHORT_MISC_SHOW_TIME 't'

# define OPT_SHORT_INFO_HELP 'h'
# define OPT_SHORT_INFO_VERSION 'v'
# define OPT_SHORT_INFO_DEBUG 'd'

# define OPT_ARG_YES "yes"
# define OPT_ARG_NO "no"

# define OPT_ARG_HTML_OUTPUT_FORMAT "html"
# define OPT_ARG_TEXT_OUTPUT_FORMAT "text"
# define OPT_ARG_NATIVE_OUTPUT_FORMAT "native"


void set_settings_max_translate_count(const char *str);
void set_settings_ill_defined_search_percent(const char *str);
void set_settings_output_format(const char *str);
void set_settings_use_terminal_escapes_flag(const char *str);
void set_settings_use_css_flag(const char *str);


#endif // OPTIONS_H

