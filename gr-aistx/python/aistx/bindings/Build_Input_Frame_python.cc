/*
 * Copyright 2022 Free Software Foundation, Inc.
 *
 * This file is part of GNU Radio
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 */

/***********************************************************************************/
/* This file is automatically generated using bindtool and can be manually edited  */
/* The following lines can be configured to regenerate this file during cmake      */
/* If manual edits are made, the following tags should be modified accordingly.    */
/* BINDTOOL_GEN_AUTOMATIC(0)                                                       */
/* BINDTOOL_USE_PYGCCXML(0)                                                        */
/* BINDTOOL_HEADER_FILE(Build_Input_Frame.h)                                        */
/* BINDTOOL_HEADER_FILE_HASH(deee2400aa0ebec8255974b59328763b)                     */
/***********************************************************************************/

#include <pybind11/complex.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;

#include <gnuradio/aistx/Build_Input_Frame.h>
// pydoc.h is automatically generated in the build directory
#include <Build_Input_Frame_pydoc.h>

void bind_Build_Input_Frame(py::module& m)
{

    using Build_Input_Frame    = gr::aistx::Build_Input_Frame;


    py::class_<Build_Input_Frame, gr::block, gr::basic_block,
        std::shared_ptr<Build_Input_Frame>>(m, "Build_Input_Frame", D(Build_Input_Frame))

        .def(py::init(&Build_Input_Frame::make),
           D(Build_Input_Frame,make)
        )
        



        ;




}








