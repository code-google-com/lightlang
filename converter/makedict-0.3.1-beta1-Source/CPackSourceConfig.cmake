# This file will be configured to contain variables for CPack. These variables
# should be set in the CMake list file of the project before CPack module is
# included. Example variables are:
#   CPACK_GENERATOR                     - Generator used to create package
#   CPACK_INSTALL_CMAKE_PROJECTS        - For each project (path, name, component)
#   CPACK_CMAKE_GENERATOR               - CMake Generator used for the projects
#   CPACK_INSTALL_COMMANDS              - Extra commands to install components
#   CPACK_INSTALL_DIRECTORIES           - Extra directories to install
#   CPACK_PACKAGE_DESCRIPTION_FILE      - Description file for the package
#   CPACK_PACKAGE_DESCRIPTION_SUMMARY   - Summary of the package
#   CPACK_PACKAGE_EXECUTABLES           - List of pairs of executables and labels
#   CPACK_PACKAGE_FILE_NAME             - Name of the package generated
#   CPACK_PACKAGE_ICON                  - Icon used for the package
#   CPACK_PACKAGE_INSTALL_DIRECTORY     - Name of directory for the installer
#   CPACK_PACKAGE_NAME                  - Package project name
#   CPACK_PACKAGE_VENDOR                - Package project vendor
#   CPACK_PACKAGE_VERSION               - Package project version
#   CPACK_PACKAGE_VERSION_MAJOR         - Package project version (major)
#   CPACK_PACKAGE_VERSION_MINOR         - Package project version (minor)
#   CPACK_PACKAGE_VERSION_PATCH         - Package project version (patch)

# There are certain generator specific ones

# NSIS Generator:
#   CPACK_PACKAGE_INSTALL_REGISTRY_KEY  - Name of the registry key for the installer
#   CPACK_NSIS_EXTRA_UNINSTALL_COMMANDS - Extra commands used during uninstall
#   CPACK_NSIS_EXTRA_INSTALL_COMMANDS   - Extra commands used during install


SET(CPACK_CMAKE_GENERATOR "Unix Makefiles")
SET(CPACK_GENERATOR "TGZ;TZ")
SET(CPACK_IGNORE_FILES "/CVS/;/\\.svn/;\\.swp$;\\.#;/#")
SET(CPACK_INSTALLED_DIRECTORIES "/home/liksys/projects/lightlang/converter/makedict-0.3.1-beta1-Source;/")
SET(CPACK_INSTALL_CMAKE_PROJECTS "")
SET(CPACK_MODULE_PATH "/home/liksys/projects/lightlang/converter/makedict-0.3.1-beta1-Source/cmake")
SET(CPACK_NSIS_DISPLAY_NAME "makedict 0.3.1-beta1")
SET(CPACK_OUTPUT_CONFIG_FILE "/home/liksys/projects/lightlang/converter/makedict-0.3.1-beta1-Source/CPackConfig.cmake")
SET(CPACK_PACKAGE_DESCRIPTION_FILE "/home/liksys/projects/lightlang/converter/makedict-0.3.1-beta1-Source/README")
SET(CPACK_PACKAGE_DESCRIPTION_SUMMARY "Converter from any dictionary format to any")
SET(CPACK_PACKAGE_FILE_NAME "makedict-0.3.1-beta1-Source")
SET(CPACK_PACKAGE_INSTALL_DIRECTORY "makedict 0.3.1-beta1")
SET(CPACK_PACKAGE_INSTALL_REGISTRY_KEY "makedict 0.3.1-beta1")
SET(CPACK_PACKAGE_NAME "makedict")
SET(CPACK_PACKAGE_VENDOR "Evgeniy Dushistov <dushistov@mail.ru>")
SET(CPACK_PACKAGE_VERSION "0.3.1-beta1")
SET(CPACK_PACKAGE_VERSION_MAJOR "0")
SET(CPACK_PACKAGE_VERSION_MINOR "3")
SET(CPACK_PACKAGE_VERSION_PATCH "1-beta1")
SET(CPACK_RESOURCE_FILE_LICENSE "/usr/share/cmake/Templates/CPack.GenericLicense.txt")
SET(CPACK_RESOURCE_FILE_README "/usr/share/cmake/Templates/CPack.GenericDescription.txt")
SET(CPACK_RESOURCE_FILE_WELCOME "/usr/share/cmake/Templates/CPack.GenericWelcome.txt")
SET(CPACK_SOURCE_GENERATOR "TGZ;TZ")
SET(CPACK_SOURCE_IGNORE_FILES "/CVS/;/\\.svn/;\\.swp$;\\.#;/#")
SET(CPACK_SOURCE_INSTALLED_DIRECTORIES "/home/liksys/projects/lightlang/converter/makedict-0.3.1-beta1-Source;/")
SET(CPACK_SOURCE_OUTPUT_CONFIG_FILE "/home/liksys/projects/lightlang/converter/makedict-0.3.1-beta1-Source/CPackSourceConfig.cmake")
SET(CPACK_SOURCE_PACKAGE_FILE_NAME "makedict-0.3.1-beta1-Source")
SET(CPACK_SOURCE_TOPLEVEL_TAG "Linux-Source")
SET(CPACK_STRIP_FILES "")
SET(CPACK_SYSTEM_NAME "Linux")
SET(CPACK_TOPLEVEL_TAG "Linux-Source")
