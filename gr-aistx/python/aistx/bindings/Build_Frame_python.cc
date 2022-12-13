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
/* BINDTOOL_HEADER_FILE(Build_Frame.h)                                        */
/* BINDTOOL_HEADER_FILE_HASH(907e50c6ebda30a530d6617244b764f1)                     */
/***********************************************************************************/

#include <pybind11/complex.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;

#include <gnuradio/aistx/Build_Frame.h>
// pydoc.h is automatically generated in the build directory
#include <Build_Frame_pydoc.h>

void bind_Build_Frame(py::module& m)
{

    using Build_Frame = ::gr::aistx::Build_Frame;


    py::class_<Build_Frame,
               gr::sync_block,
               gr::block,
               gr::basic_block,
               std::shared_ptr<Build_Frame>>(m, "Build_Frame", D(Build_Frame))

        .def(py::init(&Build_Frame::make),
             py::arg("sentence"),
             py::arg("repeat"),
             py::arg("enable_NRZI"),
             D(Build_Frame, make))


        ;
}
