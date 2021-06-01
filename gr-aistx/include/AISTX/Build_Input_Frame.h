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

#ifndef INCLUDED_AISTX_BUILD_INPUT_FRAME_H
#define INCLUDED_AISTX_BUILD_INPUT_FRAME_H

#include <AISTX/api.h>
#include <gnuradio/block.h>

namespace gr {
  namespace AISTX {

    /*!
     * \brief <+description of block+>
     * \ingroup AISTX
     *
     */
    class AISTX_API Build_Input_Frame : virtual public gr::block
    {
     public:
      typedef boost::shared_ptr<Build_Input_Frame> sptr;

      /*!
       * \brief Return a shared_ptr to a new instance of AISTX::Build_Input_Frame.
       *
       * To avoid accidental use of raw pointers, AISTX::Build_Input_Frame's
       * constructor is in a private implementation
       * class. AISTX::Build_Input_Frame::make is the public interface for
       * creating new instances.
       */
      static sptr make(bool repeat, bool enable_NRZI);
    };

  } // namespace AISTX
} // namespace gr

#endif /* INCLUDED_AISTX_BUILD_INPUT_FRAME_H */

