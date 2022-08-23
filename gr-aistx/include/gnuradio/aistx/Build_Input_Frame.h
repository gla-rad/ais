/* -*- c++ -*- */
/*
 * Copyright 2022 GLA Research & Development Directorate.
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

#ifndef INCLUDED_AISTX_BUILD_INPUT_FRAME_H
#define INCLUDED_AISTX_BUILD_INPUT_FRAME_H

#include <gnuradio/aistx/api.h>
#include <gnuradio/block.h>

namespace gr {
  namespace aistx {

    /*!
     * \brief <+description of block+>
     * \ingroup aistx
     *
     */
    class AISTX_API Build_Input_Frame : virtual public gr::block
    {
     public:
      typedef std::shared_ptr<Build_Input_Frame> sptr;

      /*!
       * \brief Return a shared_ptr to a new instance of aistx::Build_Input_Frame.
       *
       * To avoid accidental use of raw pointers, aistx::Build_Input_Frame's
       * constructor is in a private implementation
       * class. aistx::Build_Input_Frame::make is the public interface for
       * creating new instances.
       */
      static sptr make(bool repeat, bool enable_NRZI);
    };

  } // namespace aistx
} // namespace gr

#endif /* INCLUDED_AISTX_BUILD_INPUT_FRAME_H */
