# Copyright 2020 Free Software Foundation, Inc.
#
# This file is part of GNU Radio
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

########################################################################
# Check if there is C++ code at all
########################################################################
if(NOT aistx_sources)
    MESSAGE(STATUS "No C++ sources... skipping python bindings")
    return()
endif(NOT aistx_sources)

########################################################################
# Check for pygccxml
########################################################################
GR_PYTHON_CHECK_MODULE_RAW(
    "pygccxml"
    "import pygccxml"
    PYGCCXML_FOUND
    )

include(GrPybind)

########################################################################
# Python Bindings
########################################################################

list(APPEND aistx_python_files
    Build_Frame_python.cc
    DebugME_python.cc
    nrz_to_nrzi_python.cc
    python_bindings.cc)

GR_PYBIND_MAKE_OOT(aistx
   ../../..
   gr::aistx
   "${aistx_python_files}")

# copy bindings extension for use in QA test module
add_custom_command(TARGET aistx_python POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E copy $<TARGET_FILE:aistx_python>
    ${PROJECT_BINARY_DIR}/test_modules/gnuradio/aistx/
)

install(TARGETS aistx_python DESTINATION ${GR_PYTHON_DIR}/gnuradio/aistx COMPONENT pythonapi)
