#!/bin/sh

echo 'Compiling and Installing the Tello Video Stream module'
echo 'You might need to enter your password'

cd .. 
cd ..
sudo apt-get update -y

# install python 2.7
sudo apt-get install python2.7 python-pip -y
sudo pip install --upgrade pip

#switch to python2.7
sudo update-alternatives --install /usr/bin/python python /usr/bin/python2 150 
sudo update-alternatives --install /usr/bin/python python /usr/bin/python3 100

sudo apt-get update -y

# install cmake
#sudo apt-get install cmake -y
sudo pip install cmake

# install dependencies
sudo apt-get install libboost-all-dev -y
sudo apt-get install libavcodec-dev -y
sudo apt-get install libswscale-dev -y
sudo apt-get install python-numpy -y
sudo apt-get install python-matplotlib -y
sudo pip install opencv-python
sudo apt-get install python-imaging-tk

# pull and build h264 decoder library
cd h264decoder
mkdir build
cd build
cmake ..
make

# copy source .so file to tello.py directory
cp libh264decoder.so ../../

echo 'Compilation and Installation Done!'
