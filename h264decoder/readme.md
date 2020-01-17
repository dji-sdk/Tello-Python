H264 Decoder Python Module
==========================

The aim of this project is to provide a simple decoder for video
captured by a Raspberry Pi camera. At the time of this writing I only
need H264 decoding, since a H264 stream is what the RPi software 
delivers. Furthermore flexibility to incorporate the decoder in larger
python programs in various ways is desirable.

The code might also serve as example for libav and boost python usage.


Files
-----
* `h264decoder.hpp`, `h264decoder.cpp` and `h264decoder_python.cpp` contain the module code.

* Other source files are tests and demos.


Requirements
------------
* cmake for building
* libav
* boost python


Todo
----

* Add a video clip for testing and remove hard coded file names in demos/tests.


License
-------
The code is published under the Mozilla Public License v. 2.0. 
