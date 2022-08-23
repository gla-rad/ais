/* -*- c++ -*- */
/*
 * Copyright 2022 GLA Research & Development Directorate.
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

#include "DebugME_impl.h"
#include <gnuradio/io_signature.h>

namespace gr {
namespace aistx {

DebugME::sptr DebugME::make(size_t itemsize)
{
    return gnuradio::make_block_sptr<DebugME_impl>(itemsize);
}


/*
 * The private constructor
 */
DebugME_impl::DebugME_impl(size_t itemsize)
    : gr::block("DebugME",
                gr::io_signature::make(
                    1 /* min inputs */, 1 /* max inputs */, itemsize),
                gr::io_signature::make(
                    0 /* min outputs */, 0 /*max outputs */, 0))
{
}

/*
 * Our virtual destructor.
 */
DebugME_impl::~DebugME_impl() {}

void DebugME_impl::forecast(int noutput_items, gr_vector_int& ninput_items_required)
{
    /* <+forecast+> e.g. ninput_items_required[0] = noutput_items */
}

int DebugME_impl::general_work(int noutput_items,
                               gr_vector_int& ninput_items,
                               gr_vector_const_void_star& input_items,
                               gr_vector_void_star& output_items)
{
    // char / byte
    if (d_itemsize == 1) {
        const unsigned char* in = (const unsigned char*)input_items[0];
        for (int i = 0; i < ninput_items[0]; ++i)
            printf("\\x%.2X", in[i]);
    }
    // float
    else if (d_itemsize == 4) {
        const float* in = (const float*)input_items[0];
        for (int i = 0; i < ninput_items[0]; ++i)
            printf("\\%.0f", in[i]);
    }
    // complex
    else
        printf("Complexes not supported yet!");

    std::cout << std::endl;

    // Do <+signal processing+>
    // Tell runtime system how many input items we consumed on
    // each input stream.
    consume_each(noutput_items);

    // Tell runtime system how many output items we produced.
    return 0;
}

} /* namespace aistx */
} /* namespace gr */
