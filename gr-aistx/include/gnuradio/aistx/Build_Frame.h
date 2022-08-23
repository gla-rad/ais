/* -*- c++ -*- */
/*
 * Copyright 2022 GLA Research & Development Directorate.
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

#ifndef INCLUDED_AISTX_BUILD_FRAME_H
#define INCLUDED_AISTX_BUILD_FRAME_H

#include <gnuradio/aistx/api.h>
#include <gnuradio/sync_block.h>

namespace gr {
  namespace aistx {

    /*!
     * \brief <+description of block+>
     * \ingroup aistx
     *
     */
    class AISTX_API Build_Frame : virtual public gr::sync_block
    {
     public:
      typedef std::shared_ptr<Build_Frame> sptr;

      /*!
       * \brief Return a shared_ptr to a new instance of aistx::Build_Frame.
       *
       * To avoid accidental use of raw pointers, aistx::Build_Frame's
       * constructor is in a private implementation
       * class. aistx::Build_Frame::make is the public interface for
       * creating new instances.
       */
      static sptr make(const char *sentence, bool repeat, bool enable_NRZI);
    };

  } // namespace aistx
} // namespace gr

#endif /* INCLUDED_AISTX_BUILD_FRAME_H */
