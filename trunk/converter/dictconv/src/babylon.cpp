/***************************************************************************
 *   Copyright (C) 2007 by Raul Fernandes and Karl Grill                   *
 *   rgbr@yahoo.com.br                                                     *
 *   Modified by Lightlang Project
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

#include "babylon.h"
// #include <fstream>

#include<stdlib.h>
#include<stdio.h>
#include<cstring>

#include <iconv.h>

#include <QString>
#include <QTextCodec>

Babylon::Babylon( std::string filename )
{
	m_filename = filename;
	file = NULL;
}


Babylon::~Babylon()
{
}


bool Babylon::open()
{
	FILE *f;
	unsigned char buf[6];
	int i;

	f = fopen( m_filename.c_str(), "r" );
	if( f == NULL )
		return false;

	i = fread( buf, 1, 6, f );

	/* First four bytes: BGL signature 0x12340001 or 0x12340002 (big-endian) */
	if( i < 6 || memcmp( buf, "\x12\x34\x00", 3 ) || buf[3] == 0 || buf[3] > 2 )
		return false;

	/* Calculate position of gz header */

	i = buf[4] << 8 | buf[5];

	if( i < 6 )
		return false;

	if( fseek( f, i, SEEK_SET ) ) /* can't seek - emulate */
			for(int j=0;j < i - 6;j++) fgetc( f );

	if( ferror( f ) || feof( f ) )
		return false;

	/* we need to flush the file because otherwise some nfs mounts don't seem
	 * to properly update the file position for the following reopen */

	fflush( f );

	file = gzdopen( dup( fileno( f ) ), "r" );
	if( file == NULL )
		return false;

	fclose( f );

	return true;
}


void Babylon::close()
{
	 gzclose( file );
}


bool Babylon::readBlock( bgl_block &block )
{
	if( gzeof( file ) || file == NULL )
		return false;

	block.length = bgl_readnum( 1 );
	block.type = block.length & 0xf;
	if( block.type == 4 ) return false; // end of file marker
	block.length >>= 4;
	block.temp = block.length;
	block.length = block.length < 4 ? bgl_readnum( block.length + 1 ) : block.length - 4 ;
	if( block.length )
	{
		block.data = (char *)malloc( block.length );
		gzread( file, block.data, block.length );
	}

	return true;
}


unsigned int Babylon::bgl_readnum( int bytes )
{
	unsigned char buf[4];
	unsigned val = 0;

	if ( bytes < 1 || bytes > 4 ) return (0);

	gzread( file, buf, bytes );
	for(int i=0;i<bytes;i++) val= (val << 8) | buf[i];
	return val;
}


bool Babylon::read()
{
	if( file == NULL ) return false;

	bgl_block block;
	uint pos;
	uint type;
	std::string headword;
	std::string definition;

	m_numEntries = 0;
	while( readBlock( block ) )
	{
		headword.clear();
		definition.clear();
		switch( block.type )
		{
			case 1:
			case 10:
			case 11:
				// Only count entries
				m_numEntries++;
				break;
			case 3:
				pos = 2;
				switch( block.data[1] )
				{
					case 1:
						headword.reserve( block.length - 2 );
						for(uint a=0;a<block.length-2;a++) headword += block.data[pos++];
						m_title = headword;
						break;
					case 2:
						headword.reserve( block.length - 2 );
						for(uint a=0;a<block.length-2;a++) headword += block.data[pos++];
						m_author = headword;
						break;
					case 3:
						headword.reserve( block.length - 2 );
						for(uint a=0;a<block.length-2;a++) headword += block.data[pos++];
						m_email = headword;
						break;
					case 4:
						headword.reserve( block.length - 2 );
						for(uint a=0;a<block.length-2;a++) headword += block.data[pos++];
						m_copyright = headword;
						break;
					case 7:
						headword = bgl_language[block.data[5]];
						m_sourceLang = headword;
						break;
					case 8:
						headword = bgl_language[block.data[5]];
						m_targetLang = headword;
						break;
					case 9:
						headword.reserve( block.length - 2 );
						for(uint a=0;a<block.length-2;a++) headword += block.data[pos++];
						m_description = headword;
						break;
					case 17:
						type = (uint)block.data[4] & 0xff;
						switch (type){
							case 128:
								m_defaultCharset = "UTF-8";
								break;
							//case 0:
								//break;
							default:
								break;
						}
					case 26:
						if (m_defaultCharset == "UTF-8")
							break;
						type = (uint)block.data[2];
						if( type > 64 ) type -= 65;
						m_sourceCharset = bgl_charset[type];
						break;
					case 27:
						if (m_defaultCharset == "UTF-8")
							break;
						type = (uint)block.data[2];
						if( type > 64 ) type -= 65;
						m_targetCharset = bgl_charset[type];
						if (m_defaultCharset == ""){
							m_defaultCharset = bgl_charset[type];
						}
						break;
					default:
						break;
				}
				break;
			default:
				;
		}
		if( block.length ) free( block.data );
	}
	gzseek( file, 0, SEEK_SET );

	convertToUtf8( m_title, DEFAULT_CHARSET );
	convertToUtf8( m_author, DEFAULT_CHARSET );
	convertToUtf8( m_email, DEFAULT_CHARSET );
	convertToUtf8( m_copyright, DEFAULT_CHARSET );
	convertToUtf8( m_description, DEFAULT_CHARSET );
	return true;
}

bgl_entry Babylon::readEntry(int resEnabled){
	bgl_entry entry;

	if( file == NULL )
	{
		entry.headword = "";
		return entry;
	}

	bgl_block block;
	uint len, pos;
	std::string headword;
	std::string definition;
	std::vector<std::string> alternates;
	std::string alternate;


	while( readBlock( block ) )
	{
		switch( block.type )
		{
			case 1:
			case 10:
			case 11:
				if ((block.temp == 1) && (block.type == 11))
				break; //headword's too long
				alternate.clear();
				headword.clear();
				definition.clear();
				pos = 0;

				// Headword
				len = 0;
				if (block.type == 11){
					 pos += 3;
					 len = (unsigned char)block.data[pos++] << 8;
					 len |= block.data[pos++];
				} else{
					 len = (unsigned char)block.data[pos++];
				}

				headword.reserve( len );
				for(uint a=0;a<len;a++) headword += block.data[pos++];
				convertToUtf8( headword, SOURCE_CHARSET );

				// Definition
				len = 0;
				if (block.type == 11){
					 pos += 3;
					 uint alter_num = block.data[pos];
					 for (uint a = 0; a < alter_num; a++){
						pos = pos + 4 + ((unsigned char)block.data[pos + 3] << 8) + block.data[pos + 4];
					 }
					 pos += 2;
					 for (uint a = 0; a < block.temp+1; a++){
						len = (len << 8) | (unsigned char)block.data[pos++];
					 }
				} else {
					 len = (unsigned char)block.data[pos++] << 8;
					 len |= (unsigned char)block.data[pos++];
				}
				definition.reserve( len );
				for(uint a=0; a<len; a++){
					if( (unsigned char)block.data[pos] == 0x0a )
					{
						definition += '\n';
						pos++;
					}else if( block.data[pos] == 0x14 ){
							if ( a < len - 3 && block.data[pos+1] == 0x02 ) definition = partOfSpeech[(unsigned char)block.data[pos+2] - 0x30] + " " + definition;
							pos += len - a;
							break;
					}else definition += block.data[pos++];
				}
				convertToUtf8( definition, TARGET_CHARSET );

				// Alternate forms
				while( pos != block.length ){
					len = (unsigned char)block.data[pos++];
					alternate.reserve( len );
					for(uint a=0;a<len;a++) alternate += block.data[pos++];
					convertToUtf8( alternate, SOURCE_CHARSET );
					alternates.push_back( alternate );
					alternate.clear();
				}

				entry.headword = headword;
				entry.definition = definition;
				entry.alternates = alternates;
				return entry;
				break;

			case 2:
				if (resEnabled == 2){
					headword.clear();
					pos = 0;
					len = 0;
					len = (unsigned char)block.data[pos++];

					headword.reserve(len);
					for (uint a=0; a < len; a++) headword +=block.data[pos++];
					len = block.length - len;
					resfile.open( headword.c_str() );
					if ( resfile.is_open() ){
						for ( uint a=0; a<len; a++ ) resfile.write( &block.data[pos++], sizeof( block.data[pos++] ) );
					}

					resfile.close();
				}
				break;
			default:
				;
		}
		if( block.length ) free( block.data );
	}
	entry.headword = "";
	return entry;
}

void Babylon::convertToUtf8( std::string &s, uint type )
{
	if( s.size() < 1 ) return;
	if( type > 2 ) return;

	std::string charset;
	switch( type )
	{
		case DEFAULT_CHARSET:
			if( m_defaultCharset.size() > 0 ) charset = m_defaultCharset;
			else charset = m_sourceCharset;
			break;
		case SOURCE_CHARSET:
			if( m_sourceCharset.size() > 0 ) charset = m_sourceCharset;
			else charset = m_defaultCharset;
			break;
		case TARGET_CHARSET:
			if( m_targetCharset.size() > 0 ) charset = m_targetCharset;
			else charset = m_defaultCharset;
			break;
		default:
			;
	}

	iconv_t cd = iconv_open( "UTF-8", charset.c_str() );
	if( cd == (iconv_t)(-1) )
	{
		printf( "Error openning iconv library\n" );
		exit(1);
	}

	char *inbuf, *outbuf, *defbuf;
	size_t inbufbytes, outbufbytes;

	inbufbytes = s.size();
	outbufbytes = s.size() * 6;
	inbuf = (char*)s.data();
	outbuf = (char*)malloc( outbufbytes + 1 );
	memset( outbuf, '\0', outbufbytes + 1 );
	defbuf = outbuf;
	size_t test;
	while (inbufbytes) {
		test = iconv(cd, &inbuf, &inbufbytes, &outbuf, &outbufbytes);
		if ( test == size_t(-1)) {
			/*inbuf++;
			inbufbytes--;*/
			if ((charset == "SHIFT_JISX0213") && (inbuf[0] == char(0x81))){
				inbuf[1] = 0x45;
			} else{
				break;
			}
		}
	}
	if (test == size_t(-1)){
		QTextCodec *codec = (charset == "SHIFT_JISX0213") ? QTextCodec::codecForName("SHIFT_JIS") : QTextCodec::codecForName(charset.c_str());
		QString decodedString = (codec->toUnicode(s.c_str())).toUtf8();
		s = decodedString.toStdString();
	} else{
		s = std::string( defbuf );
	}

	free( defbuf );
	iconv_close( cd );
}
