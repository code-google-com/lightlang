/***************************************************************************
 *   Copyright (C) 2007 by Raul Fernandes                                  *
 *   rgfernandes@yahoo.com                                                 *
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

#include "dictdbuilder.h"

#include <iostream>

DictdBuilder::DictdBuilder( std::string filename )
{
  m_idxfilename = filename;
  m_dictfilename = filename;
  m_dictfilename = m_dictfilename.substr( 0, m_dictfilename.length() - 6 ) + ".dict";
  m_entriescount = 0;
}


DictdBuilder::~DictdBuilder()
{
}

bool DictdBuilder::addHeadword( std::string word, std::string def, std::vector<std::string> /*alternates*/ )
{
  m_entriescount++;
  struct entry entry;
  std::string definition = def;
  entry.position = m_definition.length();
  entry.size = definition.length();
  std::string headword;

  headword = word;
  dic.insert( make_pair( headword, entry ) );

  // TODO: syn file
  /*
  // Alternate forms
  std::vector<std::string>::iterator iter;
  for(iter = alternates.begin();iter != alternates.end(); iter++)
  {
  dic.insert( make_pair( *iter, entry ) );
}*/

  m_definition += definition;
  return true;
}

bool DictdBuilder::finish()
{
  m_wordcount = dic.size();


  //////////////////
  // Index file
  /////////////////

  file.open( m_idxfilename.c_str() );
  if( !file.is_open() )
  {
    return false;
  }

  dictionary::iterator iter;
  const char *result;
  for( iter = dic.begin(); iter != dic.end(); ++iter ) {
    file.write( iter->first.data(), iter->first.length() );
    file.put( '\t' );
    result = b64_encode( iter->second.position );
    file.write( result, strlen( result ) );
    file.put( '\t' );
    result = b64_encode( iter->second.size );
    file.write( result, strlen( result ) );
    file.put( '\n' );
  }
  file.close();


  //////////////////
  // Dict file
  /////////////////

  file.open( m_dictfilename.c_str() );
  if( !file.is_open() )
  {
    return false;
  }
  file.write( m_definition.data(), m_definition.length() );
  file.close();

  return true;
}

// Copied from libmaa/base64.c file in dictd sources
// available at http://www.dict.org/
const char* DictdBuilder::b64_encode( unsigned long val )
{
  unsigned char b64_list[] = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";
  static char result[7];
  int i;

  result[0] = b64_list[ (val & 0xc0000000) >> 30 ];
  result[1] = b64_list[ (val & 0x3f000000) >> 24 ];
  result[2] = b64_list[ (val & 0x00fc0000) >> 18 ];
  result[3] = b64_list[ (val & 0x0003f000) >> 12 ];
  result[4] = b64_list[ (val & 0x00000fc0) >>  6 ];
  result[5] = b64_list[ (val & 0x0000003f)       ];
  result[6] = 0;

  for(i = 0; i < 5; i++)
    if (result[i] != b64_list[0])
      return result + i;

  return result + 5;
}
