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
# $ sudo pip install pyserial
# $ sudo pip install pyais
#
# Usage Examples:
# $ sudo ./ser_ais_validator --port=/dev/ttyS0 --baud=38400

import threading
import time
import curses
import re
import socket
import serial
import time
import hashlib
import requests
import base64

from datetime import datetime

# Terminal Dashboard Library
from curses import wrapper

# Python AIS Library Import
from pyais import AISMessage, NMEAMessage

class MsgEntry:
    """
        A structure to contain the received AIS messages and their relevant
        data, such as the reception time.
    """
    msg: AISMessage
    data: str
    time: float

    def __init__(self, msg: AISMessage, data: str, time: float):
        self.msg = msg
        self.data = data
        self.time = time

class FragmentEntry:
    """
        A structure to contain the various AIS message fragements received 
        while their are being reconstructed.
    """
    msgId: int
    fragmentIndex: int
    data: str

    def __init__(self, id: int, index: int, data: str):
        self.msgId = id
        self.fragmentId = index
        self.data = data

class SerialThread (threading.Thread):
    """
        The definition of the serial thread that read the data from the 
        specified serial port. Then it filters out only the AIVDM sentences
        and places them to the loaded messages list.
    """
    ais_fields = ['type','mmsi','dest_mmsi','name','aid_type','lat','lon','valid']

    def __init__(self, name: str, ser: serial.Serial, screen, vhost: str, fwdhost: str, fwdport: str):
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
        self.vhost = vhost

        # Initialise a forwarding operation if requested
        self.fwd_host = fwdhost
        self.fwd_port = int(fwdport) if fwdport else None
        self.fwd_socket =  socket.socket(socket.AF_INET, socket.SOCK_DGRAM) if fwdhost and fwdport else None

        # Terminal window parameters
        self.counter = 0
        self.max_lines = 40
        self.max_columns = 116

        # lines, columns, start line, start column
        self.header_window = curses.newwin(9, self.max_columns, 0, 0)
        self.ais_window = curses.newwin(self.max_lines, self.max_columns, 9, 0)
        self.info_window = curses.newwin(2, self.max_columns, 9 + self.max_lines, 0)

        # Initialise the header window
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE)
        self.header_window.addstr(0, 0, self.max_columns*'#')
        self.header_window.addstr(1, 0, '#' + '© GLA Research & Development Directorate'.center(self.max_columns - 2) + '#')
        self.header_window.addstr(2, 0, '#' + "SERIAL AIS MESSAGE VALIDATOR".center(self.max_columns - 2) + '#')
        self.header_window.addstr(3, 0, '#' + f"Currently monitoring serial port {self.ser.port}".center(self.max_columns - 2) + '#')
        self.header_window.addstr(4, 0, self.max_columns*'#')
        self.header_window.addstr(6, 0, '|-----------------------------------------------------------------------------------------------------------------|')
        self.header_window.addstr(7, 0, '| Type | Source MMSI | Dest MMSI |      Name      |          Aid Type          | Latitude | Longitude | Verified  |')
        self.header_window.addstr(8, 0, '|-----------------------------------------------------------------------------------------------------------------|')

        # Print the window to the screen
        self.screen.clear()
        self.screen.refresh()
        self.header_window.refresh()
        self.ais_window.refresh()
        self.info_window.refresh()

    def run (self):
        """
            The main operation of the Serial Thread, where the input from the
            serial port is received.
        """
        while not self.die:
            reading = self.ser.readline().decode()
            reading = re.sub('\r\n', '', reading)
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
            self.info_window.clear()

        # Only plot AIVDM data
        if data.startswith('!AIVDM'):
            try:
                # Initialise with an empty message object
                message = None

                # Try to pick up message sequences but checking the fragment count
                msgParts = data.split(',')

                # For valid NMEA sentences 
                if len(msgParts) == 7:
                    # Decode the message according to whether it has fragments or not
                    sequenceNo = int(msgParts[1])
                    if sequenceNo > 1:
                        msgId = int(msgParts[3])
                        fragmentId = int(msgParts[2])

                        # Initialise the entry if it does not exist
                        if msgId not in self.fragDict:
                            self.fragDict[msgId] = []

                        # Append the received message into the array if it seems OK
                        if len(list(filter(lambda msg: msg.fragmentId == fragmentId, self.fragDict[msgId]))) == 0:
                            self.fragDict[msgId].append(FragmentEntry(msgId, fragmentId, data))

                        # Note to the user that a sequence was picked up
                        if len(self.fragDict[msgId]) == sequenceNo:
                            message = NMEAMessage.assemble_from_iterable(
                                messages=list(
                                    map(lambda msg: NMEAMessage(msg.data.encode('utf-8')), self.fragDict[msgId])
                                )
                            ).decode()

                            # Signature messages should always be 64 bytes long so 64 * 8 = 512 bits
                            if "data" in message.content and len(message.content["data"]) in [512, 514]:
                                self.handle_authorization_message(message.content)

                            # And delete the fragment entry
                            del self.fragDict[msgId]
                    else:
                        # Decode the message
                        message = NMEAMessage.assemble_from_iterable(
                                messages=[NMEAMessage(data.encode('utf-8'))]
                            ).decode()

                    # Only print the non data messages, cause data might have signatures
                    if message and type(message) == AISMessage: #and message['type'] not in [6, 8]:
                        # If successful and this is not a data message, add the message
                        # into a map, we might need to validate it
                        self.msgDict[self.counter] = MsgEntry(message, data, self.timestampCalculation(message.content))
                        # Now print the message fields in the dashboard
                        for field in self.ais_fields:
                            self.print_ais_field(message.content, field, self.counter%(self.max_lines-1))
                        # And increase the line counter
                        self.counter += 1

            except Exception as error:
                self.showError(error)

        # And update the window
        self.ais_window.refresh()
        
    def handle_authorization_message(self, message: dict):  
        # Look for a message that matches the signature
        for index in range(len(self.msgDict)-1, -1, -1):
            messageEntry = self.msgDict[index]
            nmeaMessage = messageEntry.msg.nmea
            nmeaLength = int(len(nmeaMessage.bit_array)) - int(nmeaMessage.fill_bits)

            # Get the device MMSI from the message content
            mmsi = messageEntry.msg.content['mmsi']

            # Only check for signature messages that come from the same mmsi
            # if mmsi != message['mmsi']:
            #     continue

            # Calculate the hash to be verified
            hashValue = hashlib.sha256()
            hashValue.update(nmeaMessage.bit_array[:nmeaLength].tobytes() + messageEntry.time.to_bytes(8, 'big'))            
            
            # Build the HTTP call to verify the message
            url = f'http://{self.vhost}/api/signatures/mmsi/verify/{mmsi}'
            content = base64.b64encode(hashValue.digest()).decode('ascii')
            signature = base64.b64encode(self.bitstring_to_bytes(message["data"][0:508] + message["data"][510:514])).decode('ascii')
            payload = f"{{\"content\": \"{content}\", \"signature\": \"{signature}\"}}"
            headers = {'content-type': 'application/json'}

            # Try to verify
            try:
                response = requests.post(url, data=payload, headers=headers)
                if response.ok:
                    self.print_ais_field({"verified":"Yes"}, "verified", index)

                    #Forward the message is a forwarding port is found
                    if self.fwd_host and self.fwd_port:
                        self.fwd_socket.sendto(bytes(messageEntry.data + '\r\n', "utf-8"), (self.fwd_host, self.fwd_port))

                    break
            except Exception as error:
                pass # Nothing to do, verification just failed

            # Only try once for now - just the last message
            break

    def timestampCalculation(self, message: dict):
        # Figure out the current time (but no nanos)
        now = datetime.now().replace(microsecond=0)

        # If the message doesn't have a second, just return the now time
        if 'second' not in message:
            return int(now.timestamp())

        # Replace the seconds with the ones specified in the message to get the TX
        # Be careful, cause if the second int the message is over 60, then we 
        # assume it was encoded with 00 second
        if message['second']< 60:
            txTimestamp = now.replace(second=message['second'])
        else:
            txTimestamp = now.replace(second=0)

        # If the minute is different, then it must be the previous one
        if txTimestamp > now:
            txTimestamp.replace(minute=txTimestamp.minute-1)

        # And return the vau
        return int(txTimestamp.timestamp())
    
    def bitstring_to_bytes(self, s: str):
        return int(s, 2).to_bytes((len(s) + 7) // 8, byteorder='big')

    def print_ais_field(self, message: dict, field: str, line: int):
        value = str(message[field] if field in message else ' ')
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
        output = str(infoMsg)[0:min(self.max_columns-7,len(str(infoMsg)))]
        padding = self.max_columns-7
        self.info_window.addstr(0, 0, f'Info: {output:<{padding}}')
        self.info_window.refresh()

    def showError(self, errorMsg):
        output = str(errorMsg)[0:min(self.max_columns-8,len(str(errorMsg)))]
        padding = self.max_columns-8
        self.info_window.addstr(1, 0, f'Error: {output:<{padding}}')
        self.info_window.refresh()

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
    parser.add_option("--vhost", help="The verification server hostname", default="localhost:8764")
    parser.add_option("--fwdhost", help="The host to forward verified messages", default="localhost")
    parser.add_option("--fwdport", help="The post to forward verified messages", default=None)
    
    # Parse the options
    (options, args) = parser.parse_args()

    # Open the serial port
    serial_port = serial.Serial(options.port, options.baud, timeout=0, parity=serial.PARITY_NONE, rtscts=1)

    # And start the serial thread
    s_thread = SerialThread('Serial Port Thread', serial_port, screen, options.vhost, options.fwdhost, options.fwdport)
    s_thread.start()
    try:
        while serial_port.is_open:
            time.sleep(1)
    except KeyboardInterrupt:
        s_thread.join()
        serial_port.close()

if __name__ == '__main__':
    wrapper(main)


