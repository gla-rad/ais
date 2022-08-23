/* -*- c++ -*- */
/*
 * Copyright 2022 GLA Research & Development Directorate.
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

#ifndef INCLUDED_AISTX_NRZ_TO_NRZI_H
#define INCLUDED_AISTX_NRZ_TO_NRZI_H

#include <gnuradio/aistx/api.h>
#include <gnuradio/block.h>

namespace gr {
  namespace aistx {

    /*!
     * \brief <+description of block+>
     * \ingroup aistx
     *
     */
    class AISTX_API nrz_to_nrzi : virtual public gr::block
    {
     public:
      typedef std::shared_ptr<nrz_to_nrzi> sptr;

      /*!
       * \brief Return a shared_ptr to a new instance of aistx::nrz_to_nrzi.
       *
       * To avoid accidental use of raw pointers, aistx::nrz_to_nrzi's
       * constructor is in a private implementation
       * class. aistx::nrz_to_nrzi::make is the public interface for
       * creating new instances.
       */
      static sptr make();
    };

  } // namespace aistx
} // namespace gr

#endif /* INCLUDED_AISTX_NRZ_TO_NRZI_H */
