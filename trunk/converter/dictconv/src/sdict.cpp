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
#include "sdict.h"

#include <zlib.h>

#define CHUNK 0xffffL

Sdict::Sdict( const char *filename )
{
  uint size;
  char block[256];
  uint titlePos;
  uint copyrightPos;
  uint versionPos;

  m_filename = filename;

  // dct file
  file.open( m_filename.c_str() );
  if( !file.is_open() )
  {
    m_isOk = false;
    return;
  }

  // Read the header
  file.readsome( block, 43 );
  m_inlang[0] = block[4];
  m_inlang[1] = block[5];
  m_inlang[2] = block[6];
  m_outlang[0] = block[7];
  m_outlang[1] = block[8];
  m_outlang[2] = block[9];
  m_compress = (uchar)block[10] & '\x0f';
  if( m_compress > 1 ){
    // Don't support bzip compression
    m_isOk = false;
    return;
  }
  m_idxlevels = (uchar)block[10] >> 4;
  m_size = (uchar)block[11] | (uchar)block[12] << 8 | (uchar)block[13] << 16 | (uchar)block[14] << 24;
  m_shortidxlen = (uchar)block[15] | (uchar)block[16] << 8 | (uchar)block[17] << 16 | (uchar)block[18] << 24;
  titlePos = (uchar)block[19] | (uchar)block[20] << 8 | (uchar)block[21] << 16 | (uchar)block[22] << 24;
  copyrightPos = (uchar)block[23] | (uchar)block[24] << 8 | (uchar)block[25] << 16 | (uchar)block[26] << 24;
  versionPos = (uchar)block[27] | (uchar)block[28] << 8 | (uchar)block[29] << 16 | (uchar)block[30] << 24;
  m_shortidx = (uchar)block[31] | (uchar)block[32] << 8 | (uchar)block[33] << 16 | (uchar)block[34] << 24;
  m_fullidx = (uchar)block[35] | (uchar)block[36] << 8 | (uchar)block[37] << 16 | (uchar)block[38] << 24;
  m_articles = (uchar)block[39] | (uchar)block[40] << 8 | (uchar)block[41] << 16 | (uchar)block[42] << 24;

  // Read title
  file.seekg( titlePos );
  file.readsome( block, 4 );
  size = (uchar)block[0] | (uchar)block[1] << 8 | (uchar)block[2] << 16 | (uchar)block[3] << 24;
  if( m_compress == 1 )
  {
    size -= 2;
    file.get();
    file.get();
  }
  file.readsome( block, size );
  block[size] = '\0';
  if( m_compress == 0 ) m_title = block;
  else{
    m_title = Inflate( block );
  }

  // Read copyright
  file.seekg( copyrightPos );
  file.readsome( block, 4 );
  size = (uchar)block[0] | (uchar)block[1] << 8 | (uchar)block[2] << 16 | (uchar)block[3] << 24;
  if( m_compress == 1 )
  {
    size -= 2;
    file.get();
    file.get();
  }
  file.readsome( block, size );
  block[size] = '\0';
  if( m_compress == 0 ) m_copyright = block;
  else{
    m_copyright = Inflate( block );
  }

  // Read version
  file.seekg( versionPos );
  file.readsome( block, 4 );
  size = (uchar)block[0] | (uchar)block[1] << 8 | (uchar)block[2] << 16 | (uchar)block[3] << 24;
  if( m_compress == 1 )
  {
    size -= 2;
    file.get();
    file.get();
  }
  file.readsome( block, size );
  block[size] = '\0';
  if( m_compress == 0 ) m_version = block;
  else{
    m_version = Inflate( block );
  }

  dic.clear();
  struct entry entry;

  file.seekg( m_fullidx );
  dic.reserve( m_size );
  for(uint a = 0;a<m_size;a++)
  {
    file.readsome( block, 8 );
    entry.offset = (uchar)block[4] | (uchar)block[5] << 8 | (uchar)block[6] << 16 | (uchar)block[7] << 24;
    size = (uchar)block[0] | (uchar)block[1] << 8;
    size -= 8;
    file.readsome( block, size );
    block[size] = '\0';
    file.tellg();
    entry.headword = block;
    dic.push_back( entry );
  }

  file.close();

  m_isOk = true;
}


Sdict::~Sdict()
{
}


/*!
    \fn Sdict::search( const char *word )
 */
const char *Sdict::search( const char *word )
{
  std::string result;
  uint size;
  char block[256];

  // Find the headword in index file
  Dictionary::const_iterator it;
  for ( it = dic.begin(); it != dic.end(); ++it )
  {
    if( (*it).headword == word ) break;
  }

  if( it != dic.end() )
  {
    file.open( m_filename.c_str() );
    if( !file.is_open() ) return "";

    file.seekg( m_articles + (*it).offset );
    file.readsome( block, 4 );
    size = (uchar)block[0] | (uchar)block[1] << 8 | (uchar)block[2] << 16 | (uchar)block[3] << 24;
    if( m_compress == 1 )
    {
      size -= 2;
      file.get();
      file.get();
    }
    std::string article;
    article.reserve( size );
    for(uint a=0;a<size;a++) article += file.get();
    file.close();

    result = word;
    result += '\n';
    if( m_compress == 0 ) result += article;
    else{
      result += Inflate( article );
    }
    return result.c_str();
  }
  return "";
}


std::string Sdict::Inflate( const std::string &data )
{
    int ret;
    z_stream strm;
    char out[CHUNK];
    for(uint a = 0;a<CHUNK;a++) out[a] = '\0';
    std::string result;

    // Inicialization of zlib
    strm.zalloc = Z_NULL;
    strm.zfree = Z_NULL;
    strm.opaque = Z_NULL;
    strm.avail_in = 0;
    strm.next_in = Z_NULL;
    ret = inflateInit2( &strm, -MAX_WBITS );
    if (ret != Z_OK)
      return "";

      // Compressed data
      strm.avail_in = data.size();
      strm.next_in = (Bytef*)data.c_str();

      /* run inflate() on input until output buffer not full */
      do {
        strm.avail_out = CHUNK;
        strm.next_out = (Bytef*)out;
        ret = inflate(&strm, Z_SYNC_FLUSH);
        switch (ret) {
          case Z_NEED_DICT:
            ret = Z_DATA_ERROR;     /* and fall through */
          case Z_DATA_ERROR:
          case Z_MEM_ERROR:
            (void)inflateEnd(&strm);
            return ""; // Error
        }
        result += out;
      } while (strm.avail_out == 0);

    /* clean up and return */
    ret = inflateEnd(&strm);
    return result;
}
