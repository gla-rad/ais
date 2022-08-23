/* -*- c++ -*- */
/*
 * Copyright 2022 GLA Research & Development Directorate.
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

#ifndef INCLUDED_AISTX_UDP_SOURCE_VB_H
#define INCLUDED_AISTX_UDP_SOURCE_VB_H

#include <gnuradio/aistx/api.h>
#include <gnuradio/sync_block.h>

namespace gr {
  namespace aistx {

    /*!
     * \brief <+description of block+>
     * \ingroup aistx
     *
     */
    class AISTX_API udp_source_vb : virtual public gr::sync_block
    {
     public:
      typedef std::shared_ptr<udp_source_vb> sptr;

      /*!
       * \brief Return a shared_ptr to a new instance of aistx::udp_source_vb.
       *
       * To avoid accidental use of raw pointers, aistx::udp_source_vb's
       * constructor is in a private implementation
       * class. aistx::udp_source_vb::make is the public interface for
       * creating new instances.
       */
      static sptr make(size_t itemsize, const std::string& host, int port, int payload_size, bool eof);
    };

  } // namespace aistx
} // namespace gr

#endif /* INCLUDED_AISTX_UDP_SOURCE_VB_H */
