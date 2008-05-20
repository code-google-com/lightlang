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

#include "plaintextdictbuilder.h"

PlainTextDictBuilder::PlainTextDictBuilder( std::string filename )
{
  m_filename = filename;
  m_entriescount = 0;
}


PlainTextDictBuilder::~PlainTextDictBuilder()
{
}

bool PlainTextDictBuilder::addHeadword( std::string headword, std::string definition, std::vector<std::string> alternates )
{
  m_entriescount++;
  dic.insert( make_pair( headword, definition ) );
  return true;
}

bool PlainTextDictBuilder::finish()
{
  m_wordcount = m_entriescount;

  file.open( m_filename.c_str() );
  if( !file.is_open() )
  {
    return false;
  }

  dictionary::iterator iter;
  for( iter = dic.begin(); iter != dic.end(); ++iter ) {
    file.write( iter->first.data(), iter->first.length() );
    file.put( '\t' );
    file.write( iter->second.data(), iter->second.length() );
    file.put( '\n' );
  }
  file.close();

  return true;
}
