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
import json
import time

from curses import wrapper
from pyais import NMEAMessage, decode_msg
from pyais.exceptions import UnknownMessageException, InvalidNMEAMessageException

class MsgEntry:
    msg: NMEAMessage
    time: float

    def __init__(self, msg: NMEAMessage, time: float):
        self.msg = msg
        self.time = time

class FragmentEntry:
    msgId: int
    fragmentIndex: int
    data: str

    def __init__(self, id: int, index: int, data: str):
        self.msgId = id
        self.fragmentIndex = index
        self.data = data


class SerialThread (threading.Thread):
    """
        The definition of the serial thread that read the data from the 
        specified serial port. Then it filters out only the AIVDM sentences
        and places them to the loaded messages list.
    """
    ais_fields = ['type','mmsi','dest_mmsi','name','aid_type','lat','lon','valid']

    def __init__(self, name, ser, screen):
        """
            The Serial Thread Constructor.
        """
        threading.Thread.__init__(self)
        self.name = name
        self.ser = ser
        self.die = False
        self.screen = screen
        self.msgDict = dict()
        self.fragDict = dict()

        # Terminal window parameters
        self.counter = 0
        self.max_lines = 40
        self.max_columns = 120

        # lines, columns, start line, start column
        self.header_window = curses.newwin(9, self.max_columns, 0, 0)
        self.ais_window = curses.newwin(self.max_lines, self.max_columns, 9, 0)

        # Initialise the header window
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE)
        self.header_window.addstr(0, 0, self.max_columns*'#')
        self.header_window.addstr(1, 0, '#' + '© GLA Research & Development Directorate'.center(self.max_columns - 2) + '#')
        self.header_window.addstr(2, 0, '#' + "SERIAL AIS MESSAGE VALIDATOR".center(self.max_columns - 2) + '#')
        self.header_window.addstr(3, 0, '#' + f"Currently monitoring serial port {self.ser.port}".center(self.max_columns - 2) + '#')
        self.header_window.addstr(4, 0, self.max_columns*'#')
        self.header_window.addstr(6, 0, '|-----------------------------------------------------------------------------------------------------------------|')
        self.header_window.addstr(7, 0, '| Type | Source MMSI | Dest MMSI |      Name      |          AID Type          | Latitude | Longitude | Validated |')
        self.header_window.addstr(8, 0, '|-----------------------------------------------------------------------------------------------------------------|')

        # Print the window to the screen
        self.screen.clear()
        self.screen.refresh()
        self.header_window.refresh()
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
        # Reset the line counter
        if self.counter >= self.max_lines:
            self.counter = 0
            self.msgDict.clear()
            self.ais_window.clear()
        # Only plot AIVDM data
        if data.startswith('!AIVDM'):
            try:
                message = None
                # Try to pick up message sequences but checking the fragment count
                msgParts = data.split(',')
                sequenceNo = int(msgParts[1])
                if sequenceNo > 1:
                    msgId = int(msgParts[3])
                    fragmentId = int(msgParts[2])
                    if msgId not in self.fragDict:
                        self.fragDict[msgId] = []
                    self.fragDict[msgId].append(FragmentEntry(msgId, fragmentId, re.sub('\r\n', '', data)))
                    
                    # Note to the user that a sequence was picked up
                    if fragmentId == sequenceNo:
                        self.showInfo('A sequence was picked up!')
                        message = NMEAMessage.assemble_from_iterable(
                            messages=list(
                                map(lambda msg: NMEAMessage(bytes(msg.data, "utf8")), self.fragDict[msgId])
                            )
                        ).decode()
                        # And delete the fragment entry
                        del self.fragDict[msgId]
                else:
                    # Decode the message
                    message = decode_msg(re.sub('\r\n', '', data))

                # Only print the non data messages, cause data might have signatures
                if message: #and message['type'] not in [6, 8]:
                    # If successful and this is not a data message, add the message
                    # into a map, we might need to validate it
                    self.msgDict[data] = MsgEntry(message, int(time.time()))
                    # Now print the message fields in the dashboard
                    for field in self.ais_fields:
                        self.print_ais_field(message, field, self.counter%(self.max_lines-1))
                    # And increase the line counter
                    self.counter += 1

            except Exception as error:
                self.showError(str(error))

        # And update the window
        self.ais_window.refresh()

    def print_ais_field(self, message, field, line):
       value = str(message[field]) if field in message else ' '
       start = 0
       length = 0
       if(field == 'type'):
           start = 0
           length = 4
       elif(field == 'mmsi'):
           start = 7
           length = 11
       elif(field == 'dest_mmsi'):
           start = 21
           length = 9
       elif(field == 'name'):
           start = 33
           length = 16
       elif(field == 'aid_type'):
           start = 50
           length = 26
       elif(field == 'lat'):
           start = 79
           length = 8
       elif(field == 'lon'):
           start = 90
           length = 9
       else:
           start = 102
           length = 9
       value = value[0:length] if len(value) > length else value
       self.ais_window.addstr(line, start, f'| {value:<{length}} |')

    def showInfo(self, infoMsg):
        self.ais_window.addstr(self.max_lines-1, 0, 'Info: ' + infoMsg[0:min(self.max_columns-7,len(infoMsg))])

    def showError(self, errorMsg):
        self.ais_window.addstr(self.max_lines-1, 0, 'Error: ' + errorMsg[0:min(self.max_columns0-8,len(errorMsg))])

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
    parser.add_option("--port", help="The serial port to read the data from", default="/dev/ttyUSB0")
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


