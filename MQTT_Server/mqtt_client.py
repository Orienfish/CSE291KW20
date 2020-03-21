#!/usr/bin/python3

'''
A data collection script running on RPi broker.
Save all subscribed data into certain folders.
'''
import paho.mqtt.client as mqtt
import os
import sys
from datetime import datetime

dir_path = os.path.dirname(os.path.realpath(__file__))
file_path = dir_path + '/data/adp_data.txt'
refer_path = dir_path + '/data/refer_data.txt'
broker_IP = '192.168.4.1'
broker_port = 61613

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("photon/#") # subscribe to all data

def on_message(client, userdata, msg):
    # save data
    print("Received from pi broker:" + msg.topic + " " + str(msg.payload))
    if msg.topic == 'photon/data':
        fname = file_path
    elif msg.topic == 'photon/refer':
        fname = refer_path
    with open(fname, 'a+') as f:
        data = msg.payload.decode('utf-8') 
        time_str = str(datetime.now().time())
        f.write('{},{}'.format(time_str, data));

def main():
    print("data file is {}".format(file_path))
    # if file exists, delete it
    if os.path.exists(file_path):
        os.remove(file_path)

    client = mqtt.Client("data_collection")
    client.connect(broker_IP, broker_port, 60)
    client.on_connect = on_connect
    client.on_message = on_message
    client.loop_forever() # nonblocking version

if __name__ == '__main__':
    main()
