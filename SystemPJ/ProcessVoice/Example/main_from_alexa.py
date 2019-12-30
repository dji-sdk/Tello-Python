# -*- coding:utf8 -*-
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from datetime import datetime
from tello import Tello
import ast
import time
import json
import sys

# For certificate based connection
myMQTTClient = AWSIoTMQTTClient('device001') # 適当な値でOK
myMQTTClient.configureEndpoint('a1qhwdmvn9jp9z-ats.iot.ap-northeast-1.amazonaws.com', 8883) # 管理画面で確認
myMQTTClient.configureCredentials('rootCA.pem', 'fef0460c44-private.pem.key', 'fef0460c44-certificate.pem.crt') #各種証明書(公開してはならない)
myMQTTClient.configureOfflinePublishQueueing(-1) # Infinite offline Publish queueing
myMQTTClient.configureDrainingFrequency(2) # Draining: 2 Hz
myMQTTClient.configureConnectDisconnectTimeout(10) # 10 sec
myMQTTClient.configureMQTTOperationTimeout(5) # 5 sec
myMQTTClient.connect()


tello = Tello() # Telloインスタンスを作成
tello.send_command('command') # SDKモードを開始

def customCallback(client, userdata, message):
    payload = message.payload
    print('Received a new message: ')
    print(payload)
    print('from topic: ')
    print(message.topic)
    print('--------------\n\n')
    # command = payload[0]
    dic = ast.literal_eval(payload)
    tello.send_command(dic['message'])


myMQTTClient.subscribe("test/pub", 1, customCallback) # AWS IoTCore test/pub チャネルをサブスクライブ
while True:
    time.sleep(1)

