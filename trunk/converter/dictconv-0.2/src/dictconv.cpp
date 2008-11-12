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

#include "babylonreader.h"
#include "plaintextdictbuilder.h"
#include "sdictreader.h"

#include <stdio.h>
#include <string>

void usage( const char *program )
{
  printf( "Usage: %s [-hvr] -o OUTPUT_FILE INPUT_FILE\n", program );
  printf( "\n" );
  printf( "Convert INPUT_FILE dictionary to OUTPUT_FILE dictionary.\n");
  printf( "The extension of file determines the dictionary type.\n");
  printf( "\n" );
  printf( "  -o  OUTPUT_FILE\tpath to target dictionary\n");
  printf( "  INPUT_FILE\t\tpath to source dictionary\n");
  printf( "  -h\t\t\tprint help message and exit\n" );
  printf( "  -?\t\t\tprint help message and exit\n");
  printf( "  -v\t\t\tshows the version information and exit\n" );
  printf( "  -r\t\t\tEnable .BGL's resources extraction\n" );
  printf( "\n" );
  printf( "INPUT_FILE can be:\n" );
  printf( "  Babylon Glossary (.bgl)\n" );
  printf( "  Sdictionary dictionary (.dct)\n" );
  printf( "\n" );
  printf( "OUTPUT_FILE can be:\n" );
  printf( "  PlainText dictionary (.dic)\n" );
  printf( "\n" );

  exit( 1 );
}


void version()
{
  printf( "Dictconv 0.2\n" );
  printf( "Copyright (C) 2007 Raul Fernandes <rgfbr@yahoo.com.br>.\n" );
  printf( "This is free software. You may redistribute copies of it under the terms of\n" );
  printf( "the GNU General Public License <http://www.gnu.org/licenses/gpl.html>.\n" );
  printf( "There is NO WARRANTY; not even for MERCHANTABILITY or FITNESS FOR A\n" );
  printf( "PARTICULAR PURPOSE.\n" );

  exit( 0 );
}


int main(int argc, char ** argv)
{
  // Options
  std::string infile;
  std::string outfile;
  bool quiet = false;

  int c;
  int babylon_resEnabled = 0;
  while( ( c = getopt( argc, argv, "-o:hqvr" ) ) != -1 )
  {
    switch( c )
    {
      case 1:
        infile = optarg;
        break;
      case 'o':
        outfile = optarg;
        break;
      case 'r':
        babylon_resEnabled = 1;
        break;
      case 'v':
        version();
      case '?':
      case 'h':
      default:
        usage( argv[0] );
    }
  }
  if( outfile.empty() || infile.empty() ) usage( argv[0] );

  // Builder
  DictBuilder *builder;
  if( outfile.compare( outfile.length() - 4, 4, ".dic") == 0 || outfile.compare( outfile.length() - 4, 4, ".DIC") == 0 ) builder = new PlainTextDictBuilder( outfile );
  else{
    printf( "You should specify a valid output file.\n" );
    exit( 1 );
  }

  // Reader
  DictReader *reader;
  if( infile.compare( infile.length() - 4, 4, ".bgl" ) == 0 || infile.compare( infile.length() - 4, 4, ".BGL" ) == 0 ) reader = new BabylonReader( infile, builder, babylon_resEnabled + 1 );
  else if( infile.compare( infile.length() - 4, 4, ".dct" ) == 0 || infile.compare( infile.length() - 4, 4, ".DCT" ) == 0 ) reader = new SdictReader( infile, builder );
  else{
    printf( "You should specify a valid input file.\n" );
    exit( 1 );
  }

  if( !reader->convert() )
  {
    printf( "Error converting %s\n", outfile.c_str() );
    exit(1);
  }

  builder->finish();

  printf( "\n\n\nResults\n" );
  printf( "File: %s\n", builder->filename().c_str() );
  printf( "Title: %s\n", builder->title().c_str() );
  printf( "Author: %s\n", builder->author().c_str() );
  printf( "Email: %s\n", builder->email().c_str() );
  printf( "Version: %s\n", builder->version().c_str() );
  printf( "License: %s\n", builder->license().c_str() );
  printf( "Description: %s\n", builder->description().c_str() );
  printf( "Original Language: %s\n", builder->origLang().c_str() );
  printf( "Destination Language: %s\n", builder->destLang().c_str() );
  printf( "Headwords: %d\n", builder->headwords() );
  printf( "Words: %d\n", builder->words() );
  printf( "\n" );
}
