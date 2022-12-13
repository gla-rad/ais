find_package(PkgConfig)

PKG_CHECK_MODULES(PC_GR_AISTX gnuradio-aistx)

FIND_PATH(
    GR_AISTX_INCLUDE_DIRS
    NAMES gnuradio/aistx/api.h
    HINTS $ENV{AISTX_DIR}/include
        ${PC_AISTX_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    GR_AISTX_LIBRARIES
    NAMES gnuradio-aistx
    HINTS $ENV{AISTX_DIR}/lib
        ${PC_AISTX_LIBDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/lib
          ${CMAKE_INSTALL_PREFIX}/lib64
          /usr/local/lib
          /usr/local/lib64
          /usr/lib
          /usr/lib64
          )

include("${CMAKE_CURRENT_LIST_DIR}/gnuradio-aistxTarget.cmake")

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(GR_AISTX DEFAULT_MSG GR_AISTX_LIBRARIES GR_AISTX_INCLUDE_DIRS)
MARK_AS_ADVANCED(GR_AISTX_LIBRARIES GR_AISTX_INCLUDE_DIRS)
