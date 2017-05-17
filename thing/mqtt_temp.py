# -*- coding: utf-8 -*-
"""Temperatures over MQTT
Implemented with one client in order not to open so many sockets as threads.
"""

import json
import random
import time

import paho.mqtt.client as mqtt


#
### CONFIGURATION
#

MQTT_IP = "localhost"
MQTT_PORT = 1883


#
### Functions
#

def setup(device):
    time.sleep(random.randint(0,10))
    device.counter = 0
    print("[THING {}]  ----------->     Set Up.".format(device.id))


def loop (device):
    device.send(json.dumps({
        "device_id": device.id,
        "counter": device.counter,
        "measure": "temperature",
        "value": random.gauss(25,15)
    }))
    device.counter += 1

def send(device, message):
    print(message)
    mqtt_client.publish("virtual_things", payload=message, qos=0, retain=False)

#
### Configuration
#
mqtt_client = mqtt.Client()
mqtt_client.connect(MQTT_IP, MQTT_PORT, keepalive=60)
