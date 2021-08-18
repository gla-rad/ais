
This directory contains a custom block for GnuRadio we called AIS Frame Builder.
It is part of the AIS BlackToolkit.
 
This block serves as generator of AIS frames and implements the full AIS stack.
It is composed of three main components covering respectively the 
application/presentation layers, the link layer and the physical layer, 
as defined in the protocol specification for AIS.

Install as described in the official out-of-tree documentation, i.e.:

$ mkdir build
$ cd build
$ cmake ../
$ make
$ sudo make install 
$ sudo ldconfig

You will need to have the appropriate dependencies installed. On an Ubuntu 20.04
system these are:

$ sudo apt install gnuradio
$ sudo apt install swig
$ sudo apt install doxygen
$ sudo apt install graphviz
$ sudo apt install libboost-all-dev
$ sudo apt install liborc-0.4-dev

On some systems the installation directory of the python3 modules will be at
the '''lib/python3/dist-packages''' which might not be picked up by python3.
To resolve this a quick hack it to link it to your current python installation
with something like:

$ sudo ln -s /usr/local/lib/python3/dist-packages/AISTX /usr/local/lib/python3.8/dist-packages/AISTX

Copyright 2013-2014 -- Embyte & Pastus

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

