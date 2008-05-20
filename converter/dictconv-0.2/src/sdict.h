/***************************************************************************
 *   Copyright (C) 2006-2007 by Raul Fernandes                             *
 *   rgfbr@yahoo.com.br                                                    *
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 *   This program is distributed in the hope that it will be useful,       *
 *   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
 *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
 *   GNU General Public License for more details.                          *
 *                                                                         *
 *   You should have received a copy of the GNU General Public License     *
 *   along with this program; if not, write to the                         *
 *   Free Software Foundation, Inc.,                                       *
 *   51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.          *
 ***************************************************************************/
#ifndef SDICT_H
#define SDICT_H

#include <string>
#include <fstream>
#include <vector>

using namespace std;

typedef unsigned char uchar;

    struct entry {
      string headword;
      ulong offset;
    };

//#ifndef NOPTIMIZE
    typedef vector<entry> Dictionary;
//#endif
    /**
@author Raul Fernandes
*/
class Sdict{
public:
    Sdict( const char* );

    ~Sdict();

    const char *search( const char * );
    inline bool isOk() const { return m_isOk; };
    inline uint size() const { return m_size; };
    inline const char *filename() const { return m_filename.c_str(); };
    inline const char *title() const { return m_title.c_str(); };
    inline const char *copyright() const { return m_copyright.c_str(); };
    inline const char *version() const { return m_version.c_str(); };
    inline const char *inlang() const { return m_inlang; };
    inline const char *outlang() const { return m_outlang; };

    Dictionary dic;
    Dictionary dump() { return dic; };

protected:
    string Inflate( const string & );

    ifstream file;
    bool m_isOk;
    uint m_size;
    string m_filename;
    string m_title;
    string m_copyright;
    string m_version;
    char m_inlang[3];
    char m_outlang[3];
    ushort m_compress;
    ushort m_idxlevels;
    uint m_shortidxlen;
    uint m_shortidx;
    uint m_fullidx;
    uint m_articles;
};

#endif // SDICT_H
