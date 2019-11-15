# import alarm
import argparse
import os
import switch
from aws import iotclient
from os import path

# ALLOWED_MODES = ["alarm", "switch"]

parser = argparse.ArgumentParser()
parser.add_argument("-e", "--endpoint", action="store", required=True, dest="host", help="Your AWS IoT custom endpoint")
parser.add_argument("-r", "--rootCA", action="store", required=True, dest="rootCAPath", help="Root CA file path")
parser.add_argument("-c", "--cert", action="store", required=True, dest="certificatePath", help="Certificate file path")
parser.add_argument("-k", "--key", action="store", required=True, dest="privateKeyPath", help="Private key file path")
parser.add_argument("-m", "--mode", action="store", dest="mode", default="alarm" ,help="Operation modes: %s"%str(ALLOWED_MODES))

args = parser.parse_args()
host = args.host
rootCAPath = args.rootCAPath
certificatePath = args.certificatePath
privateKeyPath = args.privateKeyPath

if args.mode not in ALLOWED_MODES:
    parser.error("Unknown --mode option %s. Must be one of %s" % (args.mode, str(ALLOWED_MODES)))
    exit(2)

clientId = "client_" + args.mode

mqtt_client = iotclient.MQTTClient(clientId, host, rootCAPath, certificatePath, privateKeyPath)

if args.mode == "alarm":
    alarm_obj = alarm.Alarm()
    mqtt_client.subscribe("remote/alarm", alarm_obj.stop)
    alarm_obj.play(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'alarm.wav'))
    mqtt_client.unsubscribe("remote/alarm")
elif args.mode == "switch":
    switch.watch()
    mqtt_client.publish("remote/alarm", "stop")