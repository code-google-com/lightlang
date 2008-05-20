/***************************************************************************
 *   Copyright (C) 2007 by Raul Fernandes                                  *
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

#ifndef _FREEDICTREADER_H_
#define _FREEDICTREADER_H_

#include "dictreader.h"

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <libxml/xmlmemory.h>
#include <libxml/parser.h>

#include <string>

class DictBuilder;

/**
@author Raul Fernandes
 */
class FreedictReader : public DictReader
{
  public:
    FreedictReader( std::string filename, DictBuilder *builder );
    bool convert();
    int parseEntry( xmlDocPtr doc, xmlNodePtr cur );
    xmlNodePtr getChildElement( xmlNodePtr node, const char *name );
    xmlNodePtr firstChildElement( xmlNodePtr node );
    xmlNodePtr nextElement( xmlNodePtr node );
    inline DictBuilder* product() const { return m_builder; };
    inline std::string filename() const { return filename(); };

  protected:
    DictBuilder *m_builder;
    std::string m_filename;
};

#endif // _FREEDICTREADER_H_
