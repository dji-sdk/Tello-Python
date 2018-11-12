#!/bin/sh

echo 'Uninstalling the Tello Video Stream module'

cd .. 
cd ..
sudo pip uninstall opencv-python -y
sudo pip uninstall cmake -y
sudo pip uninstall pip -y

sudo apt-get remove libboost-all-dev -y
sudo apt-get remove libavcodec-dev -y
sudo apt-get remove libswscale-dev -y
sudo apt-get remove python-numpy -y
sudo apt-get remove python-matplotlib -y
sudo apt-get remove python-pil.imagetk -y

sudo apt-get remove python-pip -y
sudo apt-get remove python2.7 -y

sudo apt-get update -y

rm ./libh264decoder.so
rm -r ./h264decoder/build
echo 'Uninstallation Done!'
