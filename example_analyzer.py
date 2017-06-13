# -*- coding: utf-8 -*-
"""Virtual Thing example.
"""

from collections import defaultdict
import json
import threading
import time

import paho.mqtt.client as mqtt

#
### CONFIGURATION
#

MQTT_IP = "localhost"
MQTT_PORT = 1883

BATTERY_THRESHOLD = 3.01  # Volts
TIME_THRESHOLD = 10  # Seconds

stop = False
devices = defaultdict(lambda : {
    'counter': -1,
    'timestamp': 0,
})

# Check dead things

def check_dead_things(check_seconds=2):
    time.sleep(2*TIME_THRESHOLD)
    while not stop:
        now = time.time()
        for k,v in devices.iteritems():
            if now-v["timestamp"]>=TIME_THRESHOLD and ("dead" not in v):
                print("[ANALYZER] Dead\tDevice({})\tLast message({})".format(
                    k,v["timestamp"]
                ))
                v["dead"] = True
        time.sleep(check_seconds)

# MQTT Callbacks

def on_connect(mosq, obj, rc):
    print("[MQTT] Connected")

def on_message(mosq, obj, msg):
    # print("[MQTT] Topic:{}\t\tMessage:{}".format(msg.topic, msg.payload))
    data = False
    try:
        data = json.loads(msg.payload)
    except Exception:
        print("[ANALYZER] Wrong JSON payload: {}".format(msg.payload))
    if data:
        ## Check for counter missmatches
        new_counter = data["counter"]
        new_time = time.time()
        # Device reseted
        if (new_counter-1)<devices[data["device_id"]]["counter"]:
            print("[ANALYZER] RESETED\tDevice({})\tCounter({} -> {})".format(
                data["device_id"],
                devices[data["device_id"]]["counter"],
                new_counter
            ))
        # Message lost
        if devices[data["device_id"]]["counter"]<(new_counter-1):
            print("[ANALYZER] LOST MESSAGES\tDevice({})\tCounter({} -> {})".format(
                data["device_id"],
                devices[data["device_id"]]["counter"],
                new_counter
            ))
        ## Check for battery alerts
        if data["battery"]<BATTERY_THRESHOLD:
            print("[ANALYZER] Battery level is critical\tDevice({})".format(
                data["device_id"]
            ))
        devices[data["device_id"]]["counter"] = new_counter
        devices[data["device_id"]]["timestamp"] = new_time


def on_publish(mosq, obj, mid):
    pass

def on_subscribe(mosq, obj, mid, granted_qos):
    print("[MQTT] Subscribed {}".format(mid))

def on_log(mosq, obj, level, string):
    print(string)

# MQTT Object
mqttc = mqtt.Client()
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_publish = on_publish
mqttc.on_subscribe = on_subscribe
# Connect
mqttc.connect(MQTT_IP, MQTT_PORT,60)

# Start subscribe, with QoS level 0
mqttc.subscribe("virtual_things", 0)


print("Press <ENTER> to launch the analyzer.")
print("Press <ENTER> again to stop.")
thread_dead = threading.Thread(target=check_dead_things)
_ = raw_input()
mqttc.loop_start()
thread_dead.start()
_ = raw_input()
stop = True
mqttc.loop_stop(force=False)
thread_dead.join()
