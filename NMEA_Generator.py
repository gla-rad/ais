#!/usr/bin/env python3
#
# NMEA Generator to produce NMEA sentences from binary AIVDM sentences.
#
# Copyright 2021 -- GLA Research & Development DIrectorate
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# Usage Examples:
# ./NMEA_Generator.py --data=001000000011101011110111001110011000100000000000010000010100100001100101011011000110110001101111001000000101011101101111011100100110110001100100
# ./NMEA_Generator.py --data=`./AIVDM_Encoder.py --type=21 --mmsi=123456789 --lon=51.9474 --lat=1.2555 --aid_type=20 --vsize=1x1`
#

def nmea_generator(payload):
        # Converts the binary payload to a text string (NMEA) payload, thsi to allow checking and composing a NEMA sentence        
        CharTable =[["0", "@", "000000"], ["1", "A", "000001"], ["2", "B", "000010"], ["3", "C", "000011"], ["4", "D", "000100"], ["5", "E", "000101"],
                    ["6", "F", "000110"], ["7", "G", "000111"], ["8", "H", "001000"], ["9", "I", "001001"], [":", "J", "001010"], [";", "K", "001011"],
                    ["<", "L", "001100"], ["=", "M", "001101"], [">", "N", "001110"], ["?", "O", "001111"], ["@", "P", "010000"], ["A", "Q", "010001"],
                    ["B", "R", "010010"], ["C", "S", "010011"], ["D", "T", "010100"], ["E", "U", "010101"], ["F", "V", "010110"], ["G", "W", "010111"],
                    ["H", "X", "011000"], ["I", "Y", "011001"], ["J", "Z", "011010"], ["K", "[", "011011"], ["L", "\\", "011100"], ["M", "]", "011101"],
                    ["N", "^", "011110"], ["O", "_", "011111"], ["P", " ", "100000"], ["Q", "!", "100001"], ["R", "\"", "100010"], ["S", "#", "100011"],
                    ["T", "$", "100100"], ["U", "%", "100101"], ["V", "&", "100110"], ["W", "'", "100111"], ["`", "(", "101000"], ["a", ")", "101001"],
                    ["b", "*", "101010"], ["c", "+", "101011"], ["d", ",", "101100"], ["e", "-", "101101"], ["f", ".", "101110"], ["g", "/", "101111"],
                    ["h", "0", "110000"], ["i", "1", "110001"], ["j", "2", "110010"], ["k", "3", "110011"], ["l", "4", "110100"], ["m", "5", "110101"],
                    ["n", "6", "110110"], ["o", "7", "110111"], ["p", "8", "111000"], ["q", "9", "111001"], ["r", ":", "111010"], ["s", ";", "111011"],
                    ["t", "<", "111100"], ["u", "=", "111101"], ["v", ">", "111110"], ["w", "?", "111111"]]

        MESSAGE_BIN = payload + '011000' # Added X at the end as this decodes I less char.
        #print (MESSAGE_BIN)
        MESSENC = ""
        LEN = 952 #28 6-byte words = 168 bits   #######XXXXXXXX Changed to 952 as this is the max length of msg8
        P = 0
        # Starting encoding binary string to 6-byte word:
        while P <= LEN:
            TMPSTR = MESSAGE_BIN[(6*P):(6*P+6)]
            #print (TMPSTR)
            P += 1
            for PAIR in CharTable:
                if PAIR[2] == TMPSTR:
                    MESSENC += PAIR[0]
        #print (MESSENC)     #Prints the payload text string

        # Next line fakes a NEMA message using the above text string
        #  Really want to generate binary for the entire message (not just the payload) and convert that to NEMA sting
        #  that way we would get a propper message without having to fake it.
        FakeMessageMaker = ('AIVDM,1,1,,A,' + MESSENC + ',0')
        CS = checksum(FakeMessageMaker)
        FakeMessage = ("!" + FakeMessageMaker + '*' + CS)
        print(FakeMessage)
        return(FakeMessage)


# Checksum for NEMA sentences
def checksum(s):
    c = 0
    for ch in s:
        c ^= ord(ch)
    c = hex(c).upper()[2:]
    return c


def main():
    from optparse import OptionParser

    desc="""Use this tool to generate the NMEA sentance from a binary AIVDM sentence."""
    parser = OptionParser(description=desc)
    parser.add_option("--data",help="The binary data to generate the NMEA setence from", default="")

    (options, args) = parser.parse_args()
    if not options.data:
        parser.error("Binary data not specified: -h for help.")

    nmea_generator(options.data)


if __name__ == "__main__":
    main()