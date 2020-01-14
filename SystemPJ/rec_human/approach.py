import tello
import numpy as np
import cv2
import sys
import time
import datetime
import math as m
from tello.py import  TELLO

sys.path.append('./ProcessVoice')
sys.path.append('./ProcessImage')
sys.path.append('./Rechuman')

# Center Cordinates detect_videoのフレームと同じならいらぬ
#ドローンステータス　アプローチ
drone.status == 'approach'

CX = 320
CY = 240

#moving_methodで顔特定しているので認識は無視
# Reference Distance
L0 = 100
S0 = 25600

# Base Distance
LB = 120

# Initialize Tracker
def tracker_init(frame):
    global bbox
    rc = 1
    w_cur = 0
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x,y,w,h) in faces:
        if w >= w_cur:
            bbox = (x,y,w,h)
            w_cur = w
        bbox = (x,y,w,h)
    if w_cur > 0:
        rc = 0
    return rc

# Create Tracker
def tracker_create(tracker_type):
    global tracker
    if tracker_type == 'BOOSTING':
        tracker = cv2.TrackerBoosting_create()
    if tracker_type == 'MIL':
        tracker = cv2.TrackerMIL_create()
    if tracker_type == 'KCF':
        tracker = cv2.TrackerKCF_create()
    if tracker_type == 'TLD':
        tracker = cv2.TrackerTLD_create()
    if tracker_type == 'MEDIANFLOW':
        tracker = cv2.TrackerMedianFlow_create()
    if tracker_type == 'GOTURN':
        tracker = cv2.TrackerGOTURN_create()


if __name__ == '__main__':

    drone = tello.Tello()
    addr = 'udp://' + LOCAL_IP + ':' + str(LOCAL_PORT_VIDEO) + '?overrun_nonfatal=1&fifo_size=50000000'
    cap = cv2.VideoCapture(addr)

    # Set Cascade Classifier
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    # Initialize Tracker
    tracker_types = ['BOOSTING', 'MIL','KCF', 'TLD', 'MEDIANFLOW', 'GOTURN']
    tracker_type = tracker_types[4]
    tracker_create(tracker_type)
    bbox = (320, 240, 105, 105)
    tracking = 0

    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret == True:
            # Key '9' enable/disable tracking
            if drone.is_tracking:
                if drone.is_detect:

                    if tracking == 0 or tracking == 2:
                        rc = tracker_init(frame)
                        if rc == 0:
                            if tracking == 0:
                                ret = tracker.init(frame, bbox)
                            else:
                                tracker_create(tracker_type)
                                ret = tracker.init(frame, bbox)
                            tracking = 1
                            drone.tracking_interval = 0.1
                    else:
                        ret, bbox = tracker.update(frame)
                        # Draw bounding box
                        if ret:
                            p1 = (int(bbox[0]), int(bbox[1]))
                            p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
                            cv2.rectangle(frame, p1, p2, (255,0,0), 2, 1)
                        else :
                            print("Tracking failure detected")
                            tracking = 2
                            drone.tracking_interval = 2

                    drone.is_detect = False

                try:
                    x = int(bbox[0])
                    y = int(bbox[1])
                    w = int(bbox[2])
                    h = int(bbox[3])
                    if w > 0:
                        d = round(L0 * m.sqrt(S0 / (w * h)))
                        dx = x + w/2 - CX
                        dy = y + h/2 - CY
                    else:
                        d = LB
                    cv2.putText(frame, ' D:' + str(d) + 'cm X:' + str(dx) + 'px Y:' + str(dy) + 'px', (360, 710), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 1, cv2.LINE_AA)
                    cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
                    if drone.is_autopilot:
                        if (d - LB) > 10:
                            drone.pitch = drone.STICK_HOVER + drone.STICK_L
                        elif (d - LB) < -10:
                            drone.pitch = drone.STICK_HOVER - drone.STICK_L
                        else:
                            drone.pitch = drone.STICK_HOVER
                        if dx > 55:
                            drone.roll = drone.STICK_HOVER + drone.STICK_L
                        elif dx < -55:
                            drone.roll = drone.STICK_HOVER - drone.STICK_L
                        else:
                            drone.roll = drone.STICK_HOVER
                        if dy > 32:
                            drone.thr = drone.STICK_HOVER - drone.STICK_L
                        elif dy < -32:
                            drone.thr = drone.STICK_HOVER + drone.STICK_L
                        else:
                            drone.thr = drone.STICK_HOVER
                except Exception:
                    break
            else:
                tracking = 0
            cv2.putText(frame, 'Tracking:' + str(drone.is_tracking) + ' AutoPilot:' + str(drone.is_autopilot), (5, 710), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 1, cv2.LINE_AA)
            cv2.imshow("frame", frame)
            k = cv2.waitKey(1)
            if drone.stop_drone:
                print('stop: ' + str(drone.stop_drone))
                time.sleep(1)
                break
    cap.release()
    cv2.destroyAllWindows()
#この後対話の状態に移る
