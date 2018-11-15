# Tello-SimplePoseRecognition

This is an example using the Tello SDK v1.3.0.0 and above to receive video stream from Tello camera and do real-time body pose recognition processing on PC. You're welcome to fork/clone/copy this example and let Tello fly creatively.

 - Written in Python 2.7
 - Tello SDK v1.3.0.0 and above(with h.264 video streaming)
 - This example includes a simple UI build with Tkinter to interact with Tello
 - Interactive control of Tello based on human movement is achieved via body pose recognition module.

## Prerequisites

- Python2.7
- pip
- Python OpenCV
- Numpy 
- PIL
- libboost-python
- Tkinter
- homebrew(for mac)
- Python h264 decoder
    - <https://github.com/DaWelter/h264decoder>

## Installation

In order to facilitate you to install python2.7 and various dependencies, we have written a one-click installation script for windows, Linux and macos. You can choose to run this script for the one-click installation, or you can download python2.7 and related libraries and dependencies online. If you have questions about the actions that the script performs, you can open the script with an editor and look up the comments for each instruction in the script. In addition, we have additionally written an uninstall script that cleans and restores all downloaded and configured content from the one-click installation script.

- **Windows**

    Go to the "install\Windows" folder,select and run the correct  "windows_install.bat" according to your computer operating system bits. 

- **Linux (Ubuntu 14.04 and above)**

    Go to the "install\Linux" folder in command line, run
    
    ```
    chmod +x linux_install.sh
    ./linux_install.sh
    ```

- **Mac**

   1. Make sure you have the latest Xcode command line tools installed. If not, you might need to update your OS X and XCode to the latest version in order to compile the h264 decoder module
   2. Go to the "install\Mac" folder folder in command line, run
   
  ```
     chmod a+x ./mac_install.sh
     ./mac_install.sh
  ```
    
    If you see no errors during installation, you are good to go!

## Get the Model

You can get the pose recognition model by run the script named "getModels.bat" or "getModels.bat"(according to your os type) under the path of "./model/".And it will take some time to download the model.


## Run the project
- **Step1**. Turn on Tello and connect your computer device to Tello via wifi.


- **Step2**. Open project folder in terminal. Run:
    
    ```
    python main.py
    ```

- **Step3**. A UI will show up, you can now:

    - Watch live video stream from the Tello camera;
    - Take snapshot and save jpg to local folder;
    - Open Command Panel, which allows you to:
        - Take Off
            - After you click this button, tello will receive the takeoff command from computer. If the battery is low, it will not take off and will give a corresponding reminder. When the tello completes the takeoff command (about 1.2 meters), in order to make the arms of the person controlling the tello can enter the field of the tello's front camera completely, the tello will fly up again for about 0.5 meters to compensate for the height. In this process,if the wifi communication between the tello and the computer is interrupted or lost, the tello will execute the land command.If tello move up again sucessfully,the thread that sends command of 'command' every 5 seconds will be started to prevent tello from landing. In order to let tello fly up to a really proper height,you should put the tello on the ground at 
            the beginning. 
        - Land
        - Flip (in forward, backward, left and right direction)
        - Control Tello using keyboard inputs:
            - **[key-Up]** move forward 20cm
            - **[key-Down]** move backward 20cm
            - **[key-Left]** move left 20 cm
            - **[key-Right]** move right 20 cm
            - **[key-w]** move up 20cm
            - **[key-s]** move down 20cm
            - **[key-a]** rotate counter-clockwise by 30 degree
            - **[key-d]** rotate clockwise by 30 degree
        -  You can also adjust the **distance** and **degree** via the trackbar and hit the "reset distance" or "reset degree" button to customize your own control.
    
    - Turn on **Pose Recognition** mode. A 17-joints skeleton based on your body will appear on the screen. Raise your arm UP or FLAT (like a "Y" or "T"), Tello will move forward 0.5 meters. Raise both your arm DOWN (your body be like '/|\'), Tello will move back 0.5 meters.Raise your arm bending(your body be like 'v|v'),Tello will land.
    

## Project Description

### tello.py - class Tello

Wrapper class to interact with Tello drone.
Modified from <https://github.com/microlinux/tello>

The object starts 2 threads:

 1. thread for receiving command response from Tello
 2. thread for receiving video stream

You can use **read()** to read the last frame from Tello camera, and pause the video by setting **video_freeze(is_freeze=True)**.

### tello_control_ui.py - class TelloUI

Modified from: https://www.pyimagesearch.com/2016/05/30/displaying-a-video-feed-with-opencv-and-tkinter/

Build with Tkinter. Display video, control video play/pause and control Tello using buttons and arrow keys.
The object starts 4 threads:

 1. thread for sending command 'command' to Tello every 5s; Starts after take off. This prevents Tello from landing automatically if no commands are sent within 15s.
 2. thread for starting a Tello automatically takeoff process.After open the Command Panel and click the Takeoff button,this
thread will be started.Computer will send the 'takeoff' command and check a series of response from Tello.If the corresponding response is received by computer,the thread will send a 'moveup'command to control Tello to a suitable height.Finally,the thread
will start the sending commang thread to preventing Tello from landing automatically.
 3. thread for displaying video.This thread will read the video stream from the h264decoder software module,with the format of frame.If the pose recognition mode are open,a 17-joints skeleton will be draw on the image.
 4. thread for initializing the photo image object.This thread is only enabled on Macos.It's a short-term solution to some compatibility problems between Macos and some plugins such as Tkinter and PIL.

### tello_pose.py - class Tello_Pose
Code modifed from:https://github.com/spmallick/learnopencv/tree/master/OpenPose
Using pre-trained caffe model from <https://github.com/CMU-Perceptual-Computing-Lab/openpose>.

Detect Body Pose and draw a 17-joints skeleton. Analyze pose by calculating angles between joints.

### h264decoder - class libh264decoder

From <https://github.com/DaWelter/h264decoder>.

A c++ based class that decodes raw h264 data. This module interacts with python language via python-libboost library, and its decoding functionality is based on ffmpeg library. 

After compilation, a libh264decoder.so or libh264decoder.pyd file will be placed in the working directory so that the main python file can reference it. 

If you have to compile it from source,with Linux or Mac,you can:

```
cd h264decoder
mkdir build
cd build
cmake ..
make
cp libh264decoder.so ../../
```
With Windows,you can create a project through visual studio, add files in h264decoder and dependencies such as ffmpeg and libboost, compile the project and generate a libh264decoder.pyd file.We have generated a libh264decoder.pyd and put it in the "\h264decoder\Windows"foleder so that you can copy put it to "python/site-package".


