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
/* BINDTOOL_HEADER_FILE(DebugME.h)                                        */
/* BINDTOOL_HEADER_FILE_HASH(1fffe89f84ead16b08749e8c27960288)                     */
/***********************************************************************************/

#include <pybind11/complex.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;

#include <gnuradio/aistx/DebugME.h>
// pydoc.h is automatically generated in the build directory
#include <DebugME_pydoc.h>

void bind_DebugME(py::module& m)
{

    using DebugME = ::gr::aistx::DebugME;


    py::class_<DebugME, gr::block, gr::basic_block, std::shared_ptr<DebugME>>(
        m, "DebugME", D(DebugME))

        .def(py::init(&DebugME::make), py::arg("itemsize"), D(DebugME, make))


        ;
}
