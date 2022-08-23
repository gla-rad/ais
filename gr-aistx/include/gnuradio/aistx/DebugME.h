/* -*- c++ -*- */
/*
 * Copyright 2022 GLA Research & Development Directorate.
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

#ifndef INCLUDED_AISTX_DEBUGME_H
#define INCLUDED_AISTX_DEBUGME_H

#include <gnuradio/aistx/api.h>
#include <gnuradio/block.h>

namespace gr {
  namespace aistx {

    /*!
     * \brief <+description of block+>
     * \ingroup aistx
     *
     */
    class AISTX_API DebugME : virtual public gr::block
    {
     public:
      typedef std::shared_ptr<DebugME> sptr;

      /*!
       * \brief Return a shared_ptr to a new instance of aistx::DebugME.
       *
       * To avoid accidental use of raw pointers, aistx::DebugME's
       * constructor is in a private implementation
       * class. aistx::DebugME::make is the public interface for
       * creating new instances.
       */
      static sptr make(size_t itemsize);
    };

  } // namespace aistx
} // namespace gr

#endif /* INCLUDED_AISTX_DEBUGME_H */
