bin_PROGRAMS = dictconv
dictconv_SOURCES = dictconv.cpp babylon.cpp babylonreader.cpp dictdbuilder.cpp freedictreader.cpp plaintextdictbuilder.cpp sdict.cpp sdictreader.cpp stardict.cpp stardictreader.cpp stardictbuilder.cpp

# set the include path found by configure
INCLUDES= $(all_includes) @XML_CPPFLAGS@

# the library search path.
dictconv_LDFLAGS = $(all_libraries) -lz @XML_LIBS@
