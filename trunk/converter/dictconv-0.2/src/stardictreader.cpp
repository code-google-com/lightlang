/***************************************************************************
 *   Copyright (C) 2007 by Raul Fernandes                                  *
 *   rgbr@yahoo.com.br                                                     *
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

#include "stardictreader.h"
#include "stardict.h"
#include "dictbuilder.h"

#include <stdio.h>

StarDictReader::StarDictReader( std::string filename, DictBuilder *builder )
{
  m_stardict = new StarDict( filename.c_str() );
  m_builder = builder;
}


bool StarDictReader::convert()
{
  m_builder->setTitle( m_stardict->bookname() );
  m_builder->setAuthor( m_stardict->author() );
  m_builder->setDescription( m_stardict->description() );
  //m_builder->setVersion( m_stardict->version() );

  std::vector<std::string> list = m_stardict->dump();

  std::vector<std::string>::const_iterator it;
  std::string result;
  for ( it = list.begin(); it != list.end(); ++it )
  {
    result = m_stardict->search( (*it).c_str() );
    m_builder->addHeadword( (*it).c_str(), result.c_str() );
    printf( "." );
  }
  printf( "\n" );

  return true;
}
