# Tello-Python

## Introduction

This is a collection of python-based sample code that interact with the Ryze Tello drone.

## Project Description

This toolkit contains three sample programs based on tello sdk and python2.7,including Single_Tello_Test, Tello_Video, and Tello_Video (With_Pose_Recognition). There is also a program file named tello_state.py.

- **Single_Tello_Test**

 In Single_Tello_Test,You can design a series of command combinations by writing a txt script to let tello execute a series of actions you have designed. This program can also be used as a command set test tool for tello.

- **Tello_Video**

 In Tello_Video，You can receive the video stream data from tello, decode the video through the h264 decoding library, and display it on a GUI interface based on Tkinter and PIL. In addition, it also supports a control panel that can operate tello. This sample code provides an example of receiving and processing and getting the correct video data. The source code of the h264 decoding library is also provided in the package, which can be used for your reference.

- **Tello_Video(With_Pose_Recognition)**

 Tello_Video_With_Pose_Recognition is an application version modified from Tello_Video.It uses the decoded video data，and everytime extract a single frame image for pose recognition operation , and binds the specific posture and aircraft control commands to realize the pose control of Tello.This code is mainly used as an application case for utilizing the decoded video data of tello for image processing.

- **Tello_state.py**

 Tello_state.py can read the various status data of tello, and can be used as a tool to debug and view the status of tello.

## Environmental configuration

The sample codes above are based on python2.7.There is no need to install additional third-party libraries for running Single_Tello_Test and tello_state.py.For Tello_Video and Tello_Video (With_Pose_Recognition), you need to install a series of third-party libraries. Therefore, in these two folders, a one-click installation script (based on windows32/64, linux and macos) is provided, which can facilitate you with installing all relevant dependencies.

Specific to the content and description of each package, you can refer to the readme file in the related folder. 
 
## Contact Information

If you have any questions about this sample code and the installation, please feel free to contact me. You can communicate with me by sending e-mail to sdk@ryzerobotics.com.
And recently we have committed a new FAQ file under the 'Tello-Python'.If you have any questions,you can firstly refer to it .

## About Multi-Tello-Formation

Please refer to github repository https://github.com/TelloSDK/Multi-Tello-Formation.
This is a python program that enable the function of multi-tello swarms. 



