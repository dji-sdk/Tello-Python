
#!/bin/sh



echo 'Compiling and Installing the Tello Video Stream module'

echo 'You might need to enter your password'

# go to /sample_code folder
cd ..
cd ..

# install Homebrew

/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"

brew update



# install pip

#sudo easy_install pip

curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
sudo python get-pip.py

# install cmake

brew install cmake



# install dependencies

brew install boost

brew install boost-python

brew install ffmpeg

brew install tcl-tk

sudo pip install numpy --ignore-installed

sudo pip install matplotlib --ignore-installed

sudo pip install pillow --ignore-installed

sudo pip install opencv-python --ignore-installed



# pull and build h264 decoder library

cd h264decoder


mkdir build

cd build

cmake ..

make



# copy source .so file to tello.py directory

cp libh264decoder.so ../../



echo 'Compilation and Installation Done!'
