/* -*- c++ -*- */
/*
 * Copyright 2022 GLA Research & Development Directorate.
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

#ifndef INCLUDED_AISTX_NRZ_TO_NRZI_IMPL_H
#define INCLUDED_AISTX_NRZ_TO_NRZI_IMPL_H

#include <gnuradio/aistx/nrz_to_nrzi.h>

namespace gr {
namespace aistx {

class nrz_to_nrzi_impl : public nrz_to_nrzi
{
private:
    // Nothing to declare in this block.

public:
    nrz_to_nrzi_impl();
    ~nrz_to_nrzi_impl();

    // Where all the action really happens
    void forecast(int noutput_items, gr_vector_int& ninput_items_required);

    int general_work(int noutput_items,
                     gr_vector_int& ninput_items,
                     gr_vector_const_void_star& input_items,
                     gr_vector_void_star& output_items);
};

} // namespace aistx
} // namespace gr

#endif /* INCLUDED_AISTX_NRZ_TO_NRZI_IMPL_H */
