# -*- coding:utf8 -*-
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from datetime import datetime
import ast
import time
import json
import sys
# telloの制御テストをしたいならコメント外す
# sys.path.append('../')
# from tello import Tello

# For certificate based connection
myMQTTClient = AWSIoTMQTTClient('device001') # 適当な値でOK
myMQTTClient.configureEndpoint('a2v7apez3ta34e-ats.iot.ap-northeast-1.amazonaws.com', 8883) # 管理画面で確認
myMQTTClient.configureCredentials('rootCA.pem', 'ddeb0c550f-private.pem.key', 'ddeb0c550f-certificate.pem.crt') #各種証明書(公開してはならない)
myMQTTClient.configureOfflinePublishQueueing(-1) # Infinite offline Publish queueing
myMQTTClient.configureDrainingFrequency(2) # Draining: 2 Hz
myMQTTClient.configureConnectDisconnectTimeout(10) # 10 sec
myMQTTClient.configureMQTTOperationTimeout(5) # 5 sec
myMQTTClient.connect()


# tello = Tello('', 8889, command_timeout=.01)  # Telloインスタンスを作成
# tello.send_command('command') # SDKモードを開始

def customCallback(client, userdata, message):
    payload = message.payload
    print('Received a new message: ')
    print(payload)
    print('from topic: ')
    print(message.topic)
    print('--------------\n\n')
    # command = payload[0]
    # dic = ast.literal_eval(payload)
    # tello.send_command(dic['message'])


myMQTTClient.subscribe("test/pub", 1, customCallback) # AWS IoTCore test/pub チャネルをサブスクライブ
print('Started Subscription')
while True:
    time.sleep(1)

