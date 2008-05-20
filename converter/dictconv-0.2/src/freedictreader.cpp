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

#include "freedictreader.h"
#include "dictbuilder.h"

#include <stdio.h>

FreedictReader::FreedictReader( std::string filename, DictBuilder *builder )
{
  m_filename = filename;
  m_builder = builder;
}


bool FreedictReader::convert()
{
  xmlDocPtr doc;
  xmlNodePtr cur, temp, temp1;
  xmlChar *key;
  int a = 0;

  // Parse the file
  doc = xmlParseFile( m_filename.c_str() );


  if( !doc )
  {
    fprintf (stderr, "Document not parsed successfully. \n");
    return false;
  }

  cur = xmlDocGetRootElement( doc );

  if( !cur )
  {
    fprintf (stderr, "empty document\n");
    xmlFreeDoc (doc);
    return false;
  }

  if( xmlStrcmp( cur->name, (const xmlChar *) "tei.2" ) &&
      xmlStrcmp( cur->name, (const xmlChar*) "TEI.2" ) )
  {
    fprintf (stderr, "document of the wrong type, root node != tei.2\n");
    xmlFreeDoc (doc);
    return false;
  }

  // Go to the first entry node
  cur = getChildElement( cur, "teiHeader" );
  if( cur )
  {
    temp = cur;

    // fileDesc
    temp1 = getChildElement( temp, "fileDesc" );

    // titleStmt
    if( temp1 ) temp = getChildElement( temp1, "titleStmt" );

    // title
    if( temp ) temp = getChildElement( temp, "title" );
    if( temp )
    {
      key = xmlNodeListGetString( doc, temp->xmlChildrenNode, 1 );
      m_builder->setTitle( (char*)key );
      xmlFree( key );
    }

    // editionStmt
    if( temp1 ) temp = getChildElement( temp1, "editionStmt" );

    // edition
    if( temp ) temp = getChildElement( temp, "edition" );
    if( temp )
    {
      key = xmlNodeListGetString( doc, temp->xmlChildrenNode, 1 );
      m_builder->setVersion( (char*)key );
      xmlFree( key );
    }

    // publicationStmt
    if( temp1 ) temp = getChildElement( temp1, "publicationStmt" );

    // publisher
    if( temp ) temp = getChildElement( temp, "publisher" );
    if( temp )
    {
      key = xmlNodeListGetString( doc, temp->xmlChildrenNode, 1 );
      m_builder->setAuthor( (char*)key );
      xmlFree( key );
    }

    // encodingDesc
    temp1 = getChildElement( cur, "encodingDesc" );

    // projectDesc
    if( temp1 ) temp = getChildElement( temp1, "projectDesc" );
    if( temp )
    {
      temp = getChildElement( temp, "p" );
      if( temp )
      {
        key = xmlNodeListGetString( doc, temp->xmlChildrenNode, 1 );
        m_builder->setDescription( (char*)key );
        xmlFree( key );
      }
    }
  }
  cur = xmlDocGetRootElement( doc );
  cur = getChildElement( cur, "text" );
  if( cur )
  {
    cur = getChildElement( cur, "body" );
    if( cur )
    {
      cur = firstChildElement( cur );

      // Parse the entry nodes
      while( cur )
      {
        if( !xmlStrcmp( cur->name, (const xmlChar *) "entry" ) )
          parseEntry( doc, cur );

        cur = nextElement( cur );
      }
    }else return false;
  }else return false;

  xmlFree (doc);

  return true;
}


int FreedictReader::parseEntry( xmlDocPtr doc, xmlNodePtr cur )
{
  std::string headword, definition;
  xmlNodePtr temp;
  xmlChar *key;

  // Flags to avoid wrong separators (, or ;)
  int is_first_trans = 1;
  int is_first_tr = 1;
  int is_first_pos = 1;

  cur = firstChildElement( cur );

  // Parse the form node
  if( cur && !xmlStrcmp (cur->name, (const xmlChar *) "form") )
  {
    temp = firstChildElement( cur );

    // Parse the orth node
    if( temp && !xmlStrcmp (temp->name, (const xmlChar *) "orth"))
    {
      key = xmlNodeListGetString (doc, temp->xmlChildrenNode, 1);
      //printf ("%s\t", key);
      headword = (char*)key;
      xmlFree( key );
    }

    if( temp ) temp = nextElement( temp );

    // Parse the pron node
    if( temp && !xmlStrcmp (temp->name, (const xmlChar *) "pron") )
    {
      key = xmlNodeListGetString (doc, temp->xmlChildrenNode, 1);
      //printf ("[%s] ", key);
      definition = "[";
      definition += (char*)key;
      definition += "] ";
      xmlFree( key );
    }
  }
  xmlFree (temp);

  // Parse the trans node
  cur = nextElement( cur );
  while (cur != NULL)
  {
    if (!xmlStrcmp (cur->name, (const xmlChar *) "trans"))
    {
      if (is_first_trans == 0)
        //printf ("; ");
        definition += "; ";
      else
        is_first_trans = 0;
      temp = cur->xmlChildrenNode;
      while (temp != NULL)
      {
        if (!xmlStrcmp (temp->name, (const xmlChar *) "tr"))
        {
          if (is_first_tr == 0)
            //printf (", ");
            definition += ", ";
          else
            is_first_tr = 0;
          key = xmlNodeListGetString (doc, temp->xmlChildrenNode, 1);
          //printf ("%s", key);
          definition += (char*)key;
          xmlFree( key );
        }
        temp = nextElement( temp );
      }
      is_first_tr = 1;
    }

// Parse the gramGrp node
    if (!xmlStrcmp (cur->name, (const xmlChar *) "gramGrp"))
    {
      temp = firstChildElement( cur );
      while( temp )
      {
        if (!xmlStrcmp (temp->name, (const xmlChar *) "pos"))
        {
          if (is_first_pos == 0)
            definition += "; ";
          else
            is_first_pos = 0;
          key = xmlNodeListGetString (doc, temp->xmlChildrenNode, 1);
          definition += "(";
          definition += (char*)key;
          definition += ".) ";
          xmlFree( key );
        }
        temp = nextElement( temp );
      }
      is_first_trans = 1;
    }

    // Parse the def node
    if (!xmlStrcmp (cur->name, (const xmlChar *) "def"))
    {
      key = xmlNodeListGetString (doc, cur->xmlChildrenNode, 1);
      definition += (char*)key;
      xmlFree( key );
    }
    cur = nextElement( cur );
  }

  m_builder->addHeadword( headword.c_str(), definition.c_str()/*, alternates*/ );

  return true;
}


xmlNodePtr FreedictReader::getChildElement( xmlNodePtr node, const char *name )
{
  node = node->xmlChildrenNode;

  while( node && ( node->type != 1 || xmlStrcmp( node->name, (xmlChar*)name ) ) )
    node = node->next;

  return node;
}


xmlNodePtr FreedictReader::firstChildElement( xmlNodePtr node )
{
  node = node->xmlChildrenNode;

  while( node && node->type != 1 )
    node = node->next;

  return node;
}


xmlNodePtr FreedictReader::nextElement( xmlNodePtr node )
{
  node = node->next;

  while( node && node->type != 1 )
      node = node->next;

  return node;
}
