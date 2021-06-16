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

#ifndef INCLUDED_AISTX_BUILD_INPUT_FRAME_IMPL_H
#define INCLUDED_AISTX_BUILD_INPUT_FRAME_IMPL_H

#include <AISTX/Build_Input_Frame.h>

namespace gr
{
    namespace AISTX
    {

        class Build_Input_Frame_impl : public Build_Input_Frame
        {
        private:
            bool d_repeat;
            bool d_enable_NRZI;
            char *payload; // [the 01 representation of the sentence as taken from input]
            unsigned short d_len_payload;
            std::string d_udp_p_delim = "\n";
        public:
            Build_Input_Frame_impl(bool repeat, bool enable_NRZI);
            ~Build_Input_Frame_impl();

            void create_payload(const char *sentence);
            void dump_buffer(const char *b, int buffer_size);
            char *int2bin(int a, char *buffer, int buf_size);
            int stuff(const char *in, char *out, int l_in);
            void pack(int orig_ascii, char *ret, int bits_per_byte);
            void nrz_to_nrzi(char *data, int length);
            void reverse_bit_order(char *data, int length);
            unsigned long unpack(char *buffer, int start, int length);
            void compute_crc(char *buffer, char *ret, unsigned int len);
            void byte_packing(char *input_frame, unsigned char *out_byte, unsigned int len);

            // Where all the action really happens
            void forecast(int noutput_items, gr_vector_int &ninput_items_required);

            int general_work(int noutput_items,
                             gr_vector_int &ninput_items,
                             gr_vector_const_void_star &input_items,
                             gr_vector_void_star &output_items);
        };

    } // namespace AISTX
} // namespace gr

#endif /* INCLUDED_AISTX_BUILD_INPUT_FRAME_IMPL_H */
