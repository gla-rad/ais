/* -*- c++ -*- */
/*
 * Copyright 2021 gr-AISTX author.
 *
 * This is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3, or (at your option)
 * any later version.
 *
 * This software is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this software; see the file COPYING.  If not, write to
 * the Free Software Foundation, Inc., 51 Franklin Street,
 * Boston, MA 02110-1301, USA.
 */

#ifndef INCLUDED_AISTX_NRZ_TO_NRZI_H
#define INCLUDED_AISTX_NRZ_TO_NRZI_H

#include <AISTX/api.h>
#include <gnuradio/block.h>

namespace gr {
  namespace AISTX {

    /*!
     * \brief <+description of block+>
     * \ingroup AISTX
     *
     */
    class AISTX_API nrz_to_nrzi : virtual public gr::block
    {
     public:
      typedef boost::shared_ptr<nrz_to_nrzi> sptr;

      /*!
       * \brief Return a shared_ptr to a new instance of AISTX::nrz_to_nrzi.
       *
       * To avoid accidental use of raw pointers, AISTX::nrz_to_nrzi's
       * constructor is in a private implementation
       * class. AISTX::nrz_to_nrzi::make is the public interface for
       * creating new instances.
       */
      static sptr make();
    };

  } // namespace AISTX
} // namespace gr

#endif /* INCLUDED_AISTX_NRZ_TO_NRZI_H */

