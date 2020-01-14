#動作
import socket
import time import sleep
import paho.mqtt.client as mqtt
import curses
import threading
import sys
import main.py
from tello.py import Tello

#人認識　predictのと被るのは除外
import cv2
from absl import app, flags, logging
from absl.flags import FLAGS

import boto3
import json
import ask_sdk_core.utils as ask_utils
from detect_video.py import VideoCapture, drow_outputs(:, (:), human)

from ask_sdk_model import Response

sys.path.append('./ProcessVoice')
sys.path.append('./ProcessImage')
sys.path.append('./Rechuman')

#動作の本体
#上空でホバリングした後から回転し、人を見つける(誰と対話するか)までを記述
#人検出は一定以上の大きさにする　周回して無理なら閾値下げる
#以下その繰り返し

self.tracking_interval = 1 #顔認識のインターバル(s)
def _timer_detect(self):
    self.is_detect = True
    if not self.stop_drone:
        t = Timer(self.tracking_interval, self._timer_detect)
        t.start()

szs1 = ndarray.shape(drow_outputs)
szs2 = ndarray.shape(VideoCapture)
szs = (szs1(:,1)*szs1(:,2))/(szs2(:,1)*szs2(:,2))
#人間のサイズが一定比以上になればok

for szs <= 0.01
    sent = sock.sendto(b'cw 360', tello_address)
    sleep(0.3)
    szs = szs + 0.001

if szs > 0.01
    sent = sock.sendto(b'cw 1', tello_address)

#人を決定した後はapproach.pyに投げる　追跡することで接近を可能にする
drone.status == 'approach'
