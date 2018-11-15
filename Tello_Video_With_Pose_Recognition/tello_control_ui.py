from PIL import Image
from PIL import ImageTk
import Tkinter as tki
from Tkinter import Toplevel, Scale
import threading
import datetime
import cv2
import os
import time
from tello_pose import Tello_Pose
import platform

class TelloUI:
    """Wrapper class to enable the GUI."""

    def __init__(self,tello,outputpath):
        """
        Initial all the element of the GUI,support by Tkinter

        :param tello: class interacts with the Tello drone.

        Raises:
            RuntimeError: If the Tello rejects the attempt to enter command mode.
        """        

        self.tello = tello # videostream device
        self.outputPath = outputpath # the path that save pictures created by clicking the takeSnapshot button 
        self.frame = None  # frame read from h264decoder and used for pose recognition 
        self.thread = None # thread of the Tkinter mainloop
        self.stopEvent = None  
        
        # control variables
        self.distance = 0.1  # default distance for 'move' cmd
        self.degree = 30  # default degree for 'cw' or 'ccw' cmd
        # if the pose recognition mode is opened 
        self.pose_mode = False        
        # if the flag is TRUE,the auto-takeoff thread will stop waiting for the response from tello
        self.quit_waiting_flag = False
        
        # if the flag is TRUE,the pose recognition skeleton will be drawn on the GUI picture
        self.draw_skeleton_flag = False
        # pose recognition
        self.my_tello_pose = Tello_Pose()
        
        # record the coordinates of the nodes in the pose recognition skeleton     
        self.points = []
        #list of all the possible connections between skeleton nodes        
        self.POSE_PAIRS = [[0,1], [1,2], [2,3], [3,4], [1,5], [5,6], [6,7], [1,14], [14,8], [8,9], [9,10], [14,11], [11,12], [12,13] ]
        
        # initialize the root window and image panel
        self.root = tki.Tk()
        self.panel = None
       # self.panel_for_pose_handle_show = None

        # create buttons
        self.btn_snapshot = tki.Button(self.root, text="Snapshot!",
                                       command=self.takeSnapshot)
        self.btn_snapshot.pack(side="bottom", fill="both",
                               expand="yes", padx=10, pady=5)

        self.btn_pose = tki.Button(self.root, text="Pose Recognition Status: Off",
                                   command=self.setPoseMode)
        self.btn_pose.pack(side="bottom", fill="both",
                           expand="yes", padx=10, pady=5)

        self.btn_pause = tki.Button(self.root, text="Pause", relief="raised", command=self.pauseVideo)
        self.btn_pause.pack(side="bottom", fill="both",
                            expand="yes", padx=10, pady=5)

        self.btn_landing = tki.Button(
            self.root, text="Open Command Panel", relief="raised", command=self.openCmdWindow)
        self.btn_landing.pack(side="bottom", fill="both",
                              expand="yes", padx=10, pady=5)
        
        # start a thread that constantly pools the video sensor for
        # the most recently read frame
        self.stopEvent = threading.Event()
        self.thread = threading.Thread(target=self.videoLoop, args=())
        self.thread.start()

        # set a callback to handle when the window is closed
        self.root.wm_title("TELLO Controller")
        self.root.wm_protocol("WM_DELETE_WINDOW", self.onClose)

        # the auto-takeoff thread will start if the 'takeoff' button on command window is clicked 
        self.auto_takeoff_thread = threading.Thread(target=self._autoTakeoff)
        # the sending_command will send command to tello every 5 seconds
        self.sending_command_thread = threading.Thread(target = self._sendingCommand)
        self.get_GUI_Image_thread = threading.Thread(target = self._getGUIImage)
    def videoLoop(self):
        """
        The mainloop thread of Tkinter 
        Raises:
            RuntimeError: To get around a RunTime error that Tkinter throws due to threading.
        """
        try:
            # start the thread that get GUI image and drwa skeleton 
            time.sleep(0.5)
            self.get_GUI_Image_thread.start()
            while not self.stopEvent.is_set():                
                # read the frame for pose recognition
                self.frame = self.tello.read()                
                if self.frame is None or self.frame.size == 0:
                    continue
                # smoothing filter
                self.frame = cv2.bilateralFilter(self.frame, 5, 50, 100)  

                cmd = ''
                self.points.append(None)               
                # process pose-recognition                
                if self.pose_mode:
                    cmd,self.draw_skeleton_flag,self.points = self.my_tello_pose.detect(self.frame)
            
                # process command - map your motion to whatever Tello movement you want!
                if cmd == 'moveback':
                    self.telloMoveBackward(0.50)
                elif cmd == 'moveforward':
                    self.telloMoveForward(0.50) 
                elif cmd == 'land':
                    self.telloLanding()
                                            
        except RuntimeError, e:
            print("[INFO] caught a RuntimeError")
    
    def _getGUIImage(self):
        """
        Main operation to read frames from h264decoder and draw skeleton on 
        frames if the pose mode is opened
        """  
        # read the system of your computer
        system = platform.system()
        while not self.stopEvent.is_set():
            # read the frame for GUI show
            frame = self.tello.read()
            if frame is None or frame.size == 0:
                continue 
            if self.pose_mode:
                # Draw the detected skeleton points
                for i in range(15):
                    if self.draw_skeleton_flag == True:
                        cv2.circle(frame, self.points[i], 8, (0, 255, 255), thickness=-1, lineType=cv2.FILLED)
                        cv2.putText(frame, "{}".format(i), self.points[i], cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2,lineType=cv2.LINE_AA)       
                # Draw Skeleton
                for pair in self.POSE_PAIRS:
                    partA = pair[0]
                    partB = pair[1]
                    if self.points[partA] and self.points[partB]:
                        cv2.line(frame, self.points[partA], self.points[partB], (0, 255, 255), 2)
                        cv2.circle(frame, self.points[partA], 8, (0, 0, 255), thickness=-1, lineType=cv2.FILLED)
            
            # transfer the format from frame to image         
            image = Image.fromarray(frame)

            # we found compatibility problem between Tkinter,PIL and Macos,and it will 
            # sometimes result the very long preriod of the "ImageTk.PhotoImage" function,
            # so for Macos,we start a new thread to execute the _updateGUIImage function.
            if system =="Windows" or system =="Linux":                
                self._updateGUIImage(image)

            else:
                thread_tmp = threading.Thread(target=self._updateGUIImage,args=(image,))
                thread_tmp.start()
                time.sleep(0.03) 
           
    def _updateGUIImage(self,image):
        """
        Main operation to initial the object of image,and update the GUI panel 
        """  
        image = ImageTk.PhotoImage(image)
        # if the panel none ,we need to initial it
        if self.panel is None:
            self.panel = tki.Label(image=image)
            self.panel.image = image
            self.panel.pack(side="left", padx=10, pady=10)
        # otherwise, simply update the panel
        else:
            self.panel.configure(image=image)
            self.panel.image = image

    def _autoTakeoff(self):
        """
        Firstly,it will waiting for the response that will be sent by Tello if Tello 
        
        finish the takeoff command.If computer doesn't receive the response,it may be
        
        because tello doesn't takeoff normally,or because the UDP pack of response is
        
        lost.So in order to confirm the reason,computer will send 'height?'command to
        
        get several real-time height datas and get a average value.If the height is in
        
        normal range,tello will execute the moveup command.Otherwise,tello will land.
        
        Finally,the sending-command thread will start.
        """ 
        response = None 
        height_tmp = 0 # temp variable to content value of height
        height_val = 0 # average value of height
        cnt = 0        # effective number of height reading
        timeout = 6    # max waiting time of tello's response

        timer = threading.Timer(timeout, self._setQuitWaitingFlag)
        timer.start()        

        # waiting for the response from tello
        while response != 'ok' :
            if self.quit_waiting_flag is True:
                break
            response = self.tello.get_response()
            print "ack:%s"%response 
        timer.cancel()

        # receive the correct response
        if response == 'ok':
            self.tello.move_up(0.5)
        
        # calculate the height of tello
        else:
            for i in range(0,50):
                height_tmp = self.tello.get_height()
                try:
                    height_val = height_val + height_tmp
                    cnt = cnt + 1
                    print height_tmp,cnt
                except:
                    height_val = height_val
                
            height_val = height_val/cnt
            
            # if the height value is in normal range 
            if height_val == 9 or height_val == 10 or height_val == 11:
                self.tello.move_up(0.5)    
            else:
                self.tello.land()
        # start the sendingCmd thread       
        self.sending_command_thread.start()
            
    def _sendingCommand(self):
        """
        start a while loop that sends 'command' to tello every 5 second
        """    

        while True:
            self.tello.send_command('command')        
            time.sleep(5)

    def _setQuitWaitingFlag(self):  
        """
        set the variable as TRUE,it will stop computer waiting for response from tello  
        """       
        self.quit_waiting_flag = True        
   
    def openCmdWindow(self):
        """
        open the cmd window and initial all the button and text
        """        
        panel = Toplevel(self.root)
        panel.wm_title("Command Panel")

        # create text input entry
        text0 = tki.Label(panel,
                          text='This Controller map keyboard inputs to Tello control commands\n'
                               'Adjust the trackbar to reset distance and degree parameter',
                          font='Helvetica 10 bold'
                          )
        text0.pack(side='top')

        text1 = tki.Label(panel, text=
                          'W - Move Tello Up\t\t\tArrow Up - Move Tello Forward\n'
                          'S - Move Tello Down\t\t\tArrow Down - Move Tello Backward\n'
                          'A - Rotate Tello Counter-Clockwise\tArrow Left - Move Tello Left\n'
                          'D - Rotate Tello Clockwise\t\tArrow Right - Move Tello Right',
                          justify="left")
        text1.pack(side="top")

        self.btn_landing = tki.Button(
            panel, text="Land", relief="raised", command=self.telloLanding)
        self.btn_landing.pack(side="bottom", fill="both",
                              expand="yes", padx=10, pady=5)

        self.btn_takeoff = tki.Button(
            panel, text="Takeoff", relief="raised", command=self.telloTakeOff)
        self.btn_takeoff.pack(side="bottom", fill="both",
                              expand="yes", padx=10, pady=5)

        # binding arrow keys to drone control
        self.tmp_f = tki.Frame(panel, width=100, height=2)
        self.tmp_f.bind('<KeyPress-w>', self.on_keypress_w)
        self.tmp_f.bind('<KeyPress-s>', self.on_keypress_s)
        self.tmp_f.bind('<KeyPress-a>', self.on_keypress_a)
        self.tmp_f.bind('<KeyPress-d>', self.on_keypress_d)
        self.tmp_f.bind('<KeyPress-Up>', self.on_keypress_up)
        self.tmp_f.bind('<KeyPress-Down>', self.on_keypress_down)
        self.tmp_f.bind('<KeyPress-Left>', self.on_keypress_left)
        self.tmp_f.bind('<KeyPress-Right>', self.on_keypress_right)
        self.tmp_f.pack(side="bottom")
        self.tmp_f.focus_set()

        self.btn_landing = tki.Button(
            panel, text="Flip", relief="raised", command=self.openFlipWindow)
        self.btn_landing.pack(side="bottom", fill="both",
                              expand="yes", padx=10, pady=5)

        self.distance_bar = Scale(panel, from_=0.02, to=5, tickinterval=0.01, digits=3, label='Distance(m)',
                                  resolution=0.01)
        self.distance_bar.set(0.2)
        self.distance_bar.pack(side="left")

        self.btn_distance = tki.Button(panel, text="Reset Distance", relief="raised",
                                       command=self.updateDistancebar,
                                       )
        self.btn_distance.pack(side="left", fill="both",
                               expand="yes", padx=10, pady=5)

        self.degree_bar = Scale(panel, from_=1, to=360, tickinterval=10, label='Degree')
        self.degree_bar.set(30)
        self.degree_bar.pack(side="right")

        self.btn_distance = tki.Button(panel, text="Reset Degree", relief="raised", command=self.updateDegreebar)
        self.btn_distance.pack(side="right", fill="both",
                               expand="yes", padx=10, pady=5)

    def openFlipWindow(self):
        """
        open the flip window and initial all the button and text
        """
        
        panel = Toplevel(self.root)
        panel.wm_title("Gesture Recognition")

        self.btn_flipl = tki.Button(
            panel, text="Flip Left", relief="raised", command=self.telloFlip_l)
        self.btn_flipl.pack(side="bottom", fill="both",
                            expand="yes", padx=10, pady=5)

        self.btn_flipr = tki.Button(
            panel, text="Flip Right", relief="raised", command=self.telloFlip_r)
        self.btn_flipr.pack(side="bottom", fill="both",
                            expand="yes", padx=10, pady=5)

        self.btn_flipf = tki.Button(
            panel, text="Flip Forward", relief="raised", command=self.telloFlip_f)
        self.btn_flipf.pack(side="bottom", fill="both",
                            expand="yes", padx=10, pady=5)

        self.btn_flipb = tki.Button(
            panel, text="Flip Backward", relief="raised", command=self.telloFlip_b)
        self.btn_flipb.pack(side="bottom", fill="both",
                            expand="yes", padx=10, pady=5)
       
    def takeSnapshot(self):
        """
        save the current frame of the video as a jpg file and put it into outputpath
        """

        # grab the current timestamp and use it to construct the filename
        ts = datetime.datetime.now()
        filename = "{}.jpg".format(ts.strftime("%Y-%m-%d_%H-%M-%S"))

        p = os.path.sep.join((self.outputPath, filename))

        # save the file
        cv2.imwrite(p, cv2.cvtColor(self.frame, cv2.COLOR_RGB2BGR))
        print("[INFO] saved {}".format(filename))

    def setPoseMode(self):
        """
        Toggle the open/close of pose recognition mode
        """
        if self.pose_mode is False:
            self.pose_mode = True
            self.btn_pose.config(text='Pose Recognition Status: On')
        else:
            self.pose_mode = False
            self.btn_pose.config(text='Pose Recognition Status: Off')

    def pauseVideo(self):
        """
        Toggle the freeze/unfreze of video
        """
        if self.btn_pause.config('relief')[-1] == 'sunken':
            self.btn_pause.config(relief="raised")
            self.tello.video_freeze(False)
        else:
            self.btn_pause.config(relief="sunken")
            self.tello.video_freeze(True)

    def telloTakeOff(self):
        """
        send the takeoff command to tello,and wait for the first response,
        
        if get the 'error'response,remind the "battery low" warning.Otherwise,
        
        start the auto-takeoff thread
        """
        takeoff_response = None

        self.tello.takeoff()
        time.sleep(0.2)

        takeoff_response = self.tello.get_response()

        if takeoff_response != 'error':
            self.auto_takeoff_thread.start()       
        else:
            print "battery low,please repalce with a new one"                          

    def telloLanding(self):
        return self.tello.land()

    def telloFlip_l(self):
        return self.tello.flip('l')

    def telloFlip_r(self):
        return self.tello.flip('r')

    def telloFlip_f(self):
        return self.tello.flip('f')

    def telloFlip_b(self):
        return self.tello.flip('b')

    def telloCW(self, degree):
        return self.tello.rotate_cw(degree)

    def telloCCW(self, degree):
        return self.tello.rotate_ccw(degree)

    def telloMoveForward(self, distance):
        return self.tello.move_forward(distance)

    def telloMoveBackward(self, distance):
        return self.tello.move_backward(distance)

    def telloMoveLeft(self, distance):
        return self.tello.move_left(distance)

    def telloMoveRight(self, distance):
        return self.tello.move_right(distance)

    def telloUp(self, dist):
        return self.tello.move_up(dist)

    def telloDown(self, dist):
        return self.tello.move_down(dist)

    def updateTrackBar(self):
        self.my_tello_hand.setThr(self.hand_thr_bar.get())

    def updateDistancebar(self):
        self.distance = self.distance_bar.get()
        print 'reset distance to %.1f' % self.distance

    def updateDegreebar(self):
        self.degree = self.degree_bar.get()
        print 'reset distance to %d' % self.degree

    def on_keypress_w(self, event):
        print "up %d m" % self.distance
        self.telloUp(self.distance)

    def on_keypress_s(self, event):
        print "down %d m" % self.distance
        self.telloDown(self.distance)

    def on_keypress_a(self, event):
        print "ccw %d degree" % self.degree
        self.tello.rotate_ccw(self.degree)

    def on_keypress_d(self, event):
        print "cw %d m" % self.degree
        self.tello.rotate_cw(self.degree)

    def on_keypress_up(self, event):
        print "forward %d m" % self.distance
        self.telloMoveForward(self.distance)

    def on_keypress_down(self, event):
        print "backward %d m" % self.distance
        self.telloMoveBackward(self.distance)

    def on_keypress_left(self, event):
        print "left %d m" % self.distance
        self.telloMoveLeft(self.distance)

    def on_keypress_right(self, event):
        print "right %d m" % self.distance
        self.telloMoveRight(self.distance)

    def on_keypress_enter(self, event):
        if self.frame is not None:
            self.registerFace()
        self.tmp_f.focus_set()

    def onClose(self):
        """
        set the stop event, cleanup the camera, and allow the rest of
        
        the quit process to continue
        """
        print("[INFO] closing...")
        self.stopEvent.set()
        del self.tello
        self.root.quit()

