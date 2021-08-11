#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Top Block
# GNU Radio version: 3.8.1.0

from gnuradio import analog
from gnuradio import blocks
from gnuradio import digital
from gnuradio import gr
from gnuradio.filter import firdes
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import uhd
import time
import AISTX

class top_block(gr.top_block):

    def __init__(self, sentence0='010101000001110101101111001101000101011100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000010110111111010010100001110110111001011110111000000000000000000000000000000000000011110000000000000000000', sentence1='000001000011010011111011010111100011101111100000000000010100000000000101100010011111100000011101110100110011010010001101110111101111111111001100000000000000000000000000'):
        gr.top_block.__init__(self, "Top Block")

        ##################################################
        # Parameters
        ##################################################
        self.sentence0 = sentence0
        self.sentence1 = sentence1

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 326531
        self.channel_select = channel_select = 2
        self.bit_rate = bit_rate = 9600

        ##################################################
        # Blocks
        ##################################################
        self.uhd_usrp_sink_0 = uhd.usrp_sink(
            ",".join(('', "")),
            uhd.stream_args(
                cpu_format="fc32",
                args='',
                channels=list(range(0,1)),
            ),
            '',
        )
        self.uhd_usrp_sink_0.set_center_freq(uhd.tune_request_t(162000000, 25000), 0)
        self.uhd_usrp_sink_0.set_gain(10, 0)
        self.uhd_usrp_sink_0.set_antenna('TX/RX', 0)
        self.uhd_usrp_sink_0.set_samp_rate(samp_rate)
        self.uhd_usrp_sink_0.set_time_now(uhd.time_spec(time.time()), uhd.ALL_MBOARDS)
        self.digital_gmsk_mod_0_0 = digital.gmsk_mod(
            samples_per_symbol=int(samp_rate/bit_rate),
            bt=0.4,
            verbose=False,
            log=False)
        self.digital_gmsk_mod_0 = digital.gmsk_mod(
            samples_per_symbol=int(samp_rate/bit_rate),
            bt=0.4,
            verbose=False,
            log=False)
        self.blocks_selector_0 = blocks.selector(gr.sizeof_gr_complex*1,channel_select,0)
        self.blocks_selector_0.set_enabled(True)
        self.blocks_multiply_xx_0_0 = blocks.multiply_vcc(1)
        self.blocks_multiply_xx_0 = blocks.multiply_vcc(1)
        self.blocks_multiply_const_vxx_0_1_0 = blocks.multiply_const_cc(0.9)
        self.blocks_multiply_const_vxx_0_1 = blocks.multiply_const_cc(0.9)
        self.blocks_multiply_const_vxx_0_0 = blocks.multiply_const_cc(0.45)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_cc(0.45)
        self.blocks_add_xx_0 = blocks.add_vcc(1)
        self.analog_sig_source_x_0_0 = analog.sig_source_c(samp_rate, analog.GR_SIN_WAVE, 25000, 1, 0, 0)
        self.analog_sig_source_x_0 = analog.sig_source_c(samp_rate, analog.GR_SIN_WAVE, -25000, 1, 0, 0)
        self.AISTX_Build_Frame_1 = AISTX.Build_Frame(sentence1, True, False)
        self.AISTX_Build_Frame_0 = AISTX.Build_Frame(sentence0, True, False)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.AISTX_Build_Frame_0, 0), (self.digital_gmsk_mod_0, 0))
        self.connect((self.AISTX_Build_Frame_1, 0), (self.digital_gmsk_mod_0_0, 0))
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_multiply_xx_0, 1))
        self.connect((self.analog_sig_source_x_0_0, 0), (self.blocks_multiply_xx_0_0, 1))
        self.connect((self.blocks_add_xx_0, 0), (self.blocks_selector_0, 2))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_add_xx_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0_0, 0), (self.blocks_add_xx_0, 1))
        self.connect((self.blocks_multiply_const_vxx_0_1, 0), (self.blocks_selector_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0_1_0, 0), (self.blocks_selector_0, 1))
        self.connect((self.blocks_multiply_xx_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.blocks_multiply_xx_0, 0), (self.blocks_multiply_const_vxx_0_1, 0))
        self.connect((self.blocks_multiply_xx_0_0, 0), (self.blocks_multiply_const_vxx_0_0, 0))
        self.connect((self.blocks_multiply_xx_0_0, 0), (self.blocks_multiply_const_vxx_0_1_0, 0))
        self.connect((self.blocks_selector_0, 0), (self.uhd_usrp_sink_0, 0))
        self.connect((self.digital_gmsk_mod_0, 0), (self.blocks_multiply_xx_0, 0))
        self.connect((self.digital_gmsk_mod_0_0, 0), (self.blocks_multiply_xx_0_0, 0))

    def get_sentence0(self):
        return self.sentence0

    def set_sentence0(self, sentence0):
        self.sentence0 = sentence0

    def get_sentence1(self):
        return self.sentence1

    def set_sentence1(self, sentence1):
        self.sentence1 = sentence1

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.analog_sig_source_x_0.set_sampling_freq(self.samp_rate)
        self.analog_sig_source_x_0_0.set_sampling_freq(self.samp_rate)
        self.uhd_usrp_sink_0.set_samp_rate(self.samp_rate)

    def get_channel_select(self):
        return self.channel_select

    def set_channel_select(self, channel_select):
        self.channel_select = channel_select
        self.blocks_selector_0.set_input_index(self.channel_select)

    def get_bit_rate(self):
        return self.bit_rate

    def set_bit_rate(self, bit_rate):
        self.bit_rate = bit_rate


def argument_parser():
    parser = ArgumentParser()
    parser.add_argument(
        "-s", "--sentence0", dest="sentence0", type=str, default='010101000001110101101111001101000101011100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000010110111111010010100001110110111001011110111000000000000000000000000000000000000011110000000000000000000',
        help="Set Sentence 0 [default=%(default)r]")
    parser.add_argument(
        "-d", "--sentence1", dest="sentence1", type=str, default='000001000011010011111011010111100011101111100000000000010100000000000101100010011111100000011101110100110011010010001101110111101111111111001100000000000000000000000000',
        help="Set Sentence 1 [default=%(default)r]")
    return parser


def main(top_block_cls=top_block, options=None):
    if options is None:
        options = argument_parser().parse_args()
    tb = top_block_cls(sentence0=options.sentence0, sentence1=options.sentence1)

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()
        sys.exit(0)

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    tb.start()
    tb.wait()


if __name__ == '__main__':
    main()
