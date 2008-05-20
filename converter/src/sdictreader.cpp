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

#include "sdictreader.h"
#include "sdict.h"
#include "dictbuilder.h"

#include <stdio.h>

SdictReader::SdictReader( std::string filename, DictBuilder *builder )
{
  m_sdict = new Sdict( filename.c_str() );
  m_builder = builder;
}


bool SdictReader::convert()
{
  m_builder->setTitle( m_sdict->title() );
  //m_builder->setAuthor( m_sdict->author() );
  //m_builder->setDescription( m_sdict->description() );
  //m_builder->setVersion( m_sdict->version() );
  m_builder->setOrigLang( m_sdict->inlang() );
  m_builder->setDestLang( m_sdict->outlang() );

  Dictionary list = m_sdict->dump();

  Dictionary::const_iterator it;
  std::string result;
  for ( it = list.begin(); it != list.end(); ++it )
  {
    result = m_sdict->search( (*it).headword.c_str() );
    m_builder->addHeadword( (*it).headword.c_str(), result.c_str() );
    printf( "." );
  }
  printf( "\n" );

  return true;
}
