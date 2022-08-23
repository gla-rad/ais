/* -*- c++ -*- */
/*
 * Copyright 2022 GLA Research & Development Directorate.
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

#ifndef INCLUDED_AISTX_BUILD_FRAME_IMPL_H
#define INCLUDED_AISTX_BUILD_FRAME_IMPL_H

#include <gnuradio/aistx/Build_Frame.h>

namespace gr {
namespace aistx {

class Build_Frame_impl : public Build_Frame
{
private:
    bool d_repeat;
    bool d_enable_NRZI;
    char* d_payload; // [the 01 representation of the sentence as taken from input]
    unsigned short d_len_payload;

public:
    Build_Frame_impl(const char* sentence, bool repeat, bool enable_NRZI);
    ~Build_Frame_impl();

    void create_payload(const char* sentence);
    void dump_buffer(const char* b, int buffer_size);
    char* int2bin(int a, char* buffer, int buf_size);
    int stuff(const char* in, char* out, int l_in);
    void pack(int orig_ascii, char* ret, int bits_per_byte);
    void nrz_to_nrzi(char* data, int length);
    void reverse_bit_order(char* data, int length);
    unsigned long unpack(char* buffer, int start, int length);
    void compute_crc(char* buffer, char* ret, unsigned int len);
    void byte_packing(char* input_frame, unsigned char* out_byte, unsigned int len);

    // Where all the action really happens
    int work(int noutput_items,
             gr_vector_const_void_star& input_items,
             gr_vector_void_star& output_items);
};

} // namespace aistx
} // namespace gr

#endif /* INCLUDED_AISTX_BUILD_FRAME_IMPL_H */
