# AIS BlackToolkit - GLA Research & Development Version

This repository contains some work on the AIS BlackToolkit performed by the 
Research &  Development Directorate of the General Lighthouse Authorities of UK 
and Ireland (GLAs). It is a fork of the original code but it has been upgraded 
to work with GNURadio-3.8 and additional functionality for constructing AIS
Message 6, 8 and 21 has been developed. An additional script for reading the
AIS messages through a serial interface is included.

## Installation
Before using the repository make sure that you have corrently installed 
GNURadion 3.8 into your system.

You can then follow the instructions found in the [README](./gr-aistx/README.md) 
file of the gr-aistx directory to install the GNURadio AIS Frame Builder module.

## General Information
This top level directory of the repository contains the following:
* gr-aistx - The GNURadio AIS Frame Builder module
* gr-ais.py - A GNURadio Companio design to send fixed AIS messages
* gr-ais-udp.py - A GNURadio Companio design to send ASI messages through a UDP port
* AIVDM_Encoder.py - An AIVDM encoder supporting the main message types
* AIVDM_pre.pl - Preprocessor / user interface (by Gary C. Kessler)
* unpacker.c - An NMEA sentence generator script based on C
* unpacker.pl - A Perm verion of the generator script (by Gary C. Kessler)
* unpacker.py - A Python verion of the generator script (by GRAD)
* ser_ais_validator.py - A python script to read AIS messages of a serial port and validate them

## The Serial AIS Validator
This is a custom project that the GLA Research & Development Directorate is
working on. Authentication messages are transmitted in addition to the
original AIS messages. The 'ser_ais_validator.py' is able to distinguish them
and use them to verify that the received messages are actually authentic.

Before using the validator script, you will need to install certain Python 
packages using pip. Note that the script is only compatible with Python3.

```
$ sudo pip install pyserial
$ sudo pip install pyais
$ sudo pip install ecdsa
```

The validator script is runs on a serial port since this is the easiest 
way to connect to a standard AIS receiver. For GNURadio implementations you 
will need to improvise I'm afraid!

To achieve this simple run the validator script by providing the serial port
to listen to. Probably you will need sudo rights to access the port.

```bash
$ sudo ./ser_ais_validator.py --port=/dev/ttyUSB0 --baud=38400
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to
discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

See [LICENSE](./LICENSE) for more information.

## Contact
Nikolaos Vastardis - Nikolaos.Vastardis@gla-rad.org


