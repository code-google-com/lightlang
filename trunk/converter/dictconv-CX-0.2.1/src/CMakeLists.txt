FIND_PACKAGE(ZLIB)

FIND_PATH(XML2_INCLUDE_DIR libxml/xmlreader.h
  /usr/local/include/libxml2
  /usr/include/libxml2
)

SET(XML2_NAMES xml2)
FIND_LIBRARY(XML2_LIBRARY
  NAMES ${XML2_NAMES}
  PATHS /usr/lib /usr/local/lib
)

IF (XML2_INCLUDE_DIR AND XML2_LIBRARY)
   SET(XML2_FOUND TRUE)
    SET( XML2_LIBRARIES ${XML2_LIBRARY} )
ELSE (XML2_INCLUDE_DIR AND XML2_LIBRARY)
   SET(XML2_FOUND FALSE)
   SET( XML2_LIBRARIES )
ENDIF (XML2_INCLUDE_DIR AND XML2_LIBRARY)

INCLUDE_DIRECTORIES(${ZLIB_INCLUDE_DIR} ${XML2_INCLUDE_DIR})

add_executable(dictconv dictconv.cpp babylon.cpp babylonreader.cpp dictdbuilder.cpp freedictreader.cpp plaintextdictbuilder.cpp sdict.cpp sdictreader.cpp stardict.cpp stardictreader.cpp stardictbuilder.cpp)
TARGET_LINK_LIBRARIES(dictconv ${ZLIB_LIBRARIES} ${XML2_LIBRARY})

INSTALL(TARGETS dictconv
        RUNTIME DESTINATION bin)
