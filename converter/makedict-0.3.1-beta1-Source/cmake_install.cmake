# Install script for directory: /home/liksys/projects/lightlang/converter/makedict-0.3.1-beta1-Source

# Set the install prefix
IF(NOT DEFINED CMAKE_INSTALL_PREFIX)
  SET(CMAKE_INSTALL_PREFIX "/usr/local")
ENDIF(NOT DEFINED CMAKE_INSTALL_PREFIX)
STRING(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
IF(NOT CMAKE_INSTALL_CONFIG_NAME)
  IF(BUILD_TYPE)
    STRING(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  ELSE(BUILD_TYPE)
    SET(CMAKE_INSTALL_CONFIG_NAME "")
  ENDIF(BUILD_TYPE)
  MESSAGE(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
ENDIF(NOT CMAKE_INSTALL_CONFIG_NAME)

# Set the component getting installed.
IF(NOT CMAKE_INSTALL_COMPONENT)
  IF(COMPONENT)
    MESSAGE(STATUS "Install component: \"${COMPONENT}\"")
    SET(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  ELSE(COMPONENT)
    SET(CMAKE_INSTALL_COMPONENT)
  ENDIF(COMPONENT)
ENDIF(NOT CMAKE_INSTALL_COMPONENT)

# Install shared libraries without execute permission?
IF(NOT DEFINED CMAKE_INSTALL_SO_NO_EXE)
  SET(CMAKE_INSTALL_SO_NO_EXE "0")
ENDIF(NOT DEFINED CMAKE_INSTALL_SO_NO_EXE)

FILE(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/bin" TYPE EXECUTABLE FILES "/home/liksys/projects/lightlang/converter/makedict-0.3.1-beta1-Source/CMakeFiles/CMakeRelink.dir/makedict")
FILE(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/man/man1" TYPE FILE FILES "/home/liksys/projects/lightlang/converter/makedict-0.3.1-beta1-Source/docs/makedict.1")
FILE(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/makedict-codecs" TYPE FILE PERMISSIONS OWNER_READ OWNER_EXECUTE GROUP_EXECUTE GROUP_READ WORLD_EXECUTE WORLD_READ FILES "/home/liksys/projects/lightlang/converter/makedict-0.3.1-beta1-Source/src/mueller7_parser.py")
FILE(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/makedict-codecs" TYPE FILE PERMISSIONS OWNER_READ OWNER_EXECUTE GROUP_EXECUTE GROUP_READ WORLD_EXECUTE WORLD_READ FILES "/home/liksys/projects/lightlang/converter/makedict-0.3.1-beta1-Source/src/apresyan.py")
FILE(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/makedict-codecs" TYPE FILE PERMISSIONS OWNER_READ GROUP_READ WORLD_READ FILES "/home/liksys/projects/lightlang/converter/makedict-0.3.1-beta1-Source/src/mdparser.py")
IF(CMAKE_INSTALL_COMPONENT)
  SET(CMAKE_INSTALL_MANIFEST "install_manifest_${CMAKE_INSTALL_COMPONENT}.txt")
ELSE(CMAKE_INSTALL_COMPONENT)
  SET(CMAKE_INSTALL_MANIFEST "install_manifest.txt")
ENDIF(CMAKE_INSTALL_COMPONENT)
FILE(WRITE "/home/liksys/projects/lightlang/converter/makedict-0.3.1-beta1-Source/${CMAKE_INSTALL_MANIFEST}" "")
FOREACH(file ${CMAKE_INSTALL_MANIFEST_FILES})
  FILE(APPEND "/home/liksys/projects/lightlang/converter/makedict-0.3.1-beta1-Source/${CMAKE_INSTALL_MANIFEST}" "${file}\n")
ENDFOREACH(file)
