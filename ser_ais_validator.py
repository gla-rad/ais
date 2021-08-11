#!/usr/bin/python3
#
# Copyright (c) 2021 GLA UK Research and Development Directive.
#
# Licensed under the Apache License, Version 2.0 (the "License"); 
# you may not use this file except in compliance with the License. 
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software 
# distributed under the License is distributed on an "AS IS" BASIS, 
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. 
# See the License for the specific language governing permissions and 
# limitations under the License.
#
# Note that for accessing the serial port you might required root rights.
# 
# First install the required packages:
# $ pip install pyserial
# $ pip install pyais
#
# Usage Examples:
# $ sudo ./ser_ais_validator --port=/dev/ttyS0 --baud=38400

import threading
import time
import curses
import re
import serial

from curses import wrapper
from pyais import NMEAMessage, decode_msg
from pyais.exceptions import UnknownMessageException, InvalidNMEAMessageException

class SerialThread (threading.Thread):
    """
        The definition of the serial thread that read the data from the 
        specified serial port. Then it filters out only the AIVDM sentences
        and places them to the loaded messages list.
    """
    
    def __init__(self, name, ser, screen):
        """
            The Serial Thread Constructor.
        """
        threading.Thread.__init__(self)
        self.name = name
        self.ser = ser
        self.die = False
        self.screen = screen

        # Terminal window parameters
        self.counter = 0
        self.max_lines = 40
        self.max_columns = 120

        # lines, columns, start line, start column
        self.ais_window = curses.newwin(self.max_lines, self.max_columns, 0, 0)
         
        # Print the window to the screen
        self.screen.clear()
        self.screen.refresh()
        self.ais_window.refresh()

    def run (self):
        """
            The main operation of the Serial Thread, where the input from the
            serial port is received.
        """
        while not self.die:
            reading = self.ser.readline().decode()
            self.handle_data(reading)
            time.sleep(0.1)
        self.ais_window.addstr(self.max_lines-1, 0, "Exiting... Please Wait...")

    def handle_data(self, data):
        """
            The serial port data input handling function. Only AIVDM sentences 
            are allows and for the time being this just prints out the data.
        """
        if data.startswith('!AIVDM'):
            self.counter += 1
            try:
                message = decode_msg(re.sub('\r\n','',data))
                self.ais_window.addstr(self.counter%(self.max_lines-1), 0, message)
            except (UnknownMessageException, InvalidNMEAMessageException) as error:
               self.ais_window.addstr(self.max_lines-1, 0, error)

    def join(self):
        """
            This function can be called when the thread is supposed to finish
            and join with the main process.
        """
        self.die = True
        super().join()

def main(screen):
    """
        The main function of the script where the input arguments are parsed and
        the serial port monitoring begins.
    """
    from optparse import OptionParser

    desc="""Use this tool to validate the AIVDM sentences received through a serial port."""
    parser = OptionParser(description=desc)
    parser.add_option("--port", help="The serial port to read the data from", default="/dev/ttyS0")
    parser.add_option("--baud", help="The serial port baud rate", default=38400)

    # Parse the options
    (options, args) = parser.parse_args()

    # Open the serial port
    serial_port = serial.Serial(options.port, options.baud, timeout=0, parity=serial.PARITY_NONE, rtscts=1)

    # And start the serial thread
    s_thread = SerialThread('Serial Port Thread', serial_port, screen)
    s_thread.start()
    try:
        while serial_port.is_open:
            time.sleep(1)
    except KeyboardInterrupt:
        s_thread.join()
        serial_port.close()

if __name__ == '__main__':
    wrapper(main)

    