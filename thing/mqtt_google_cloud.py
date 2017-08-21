# -*- coding: utf-8 -*-
"""Temperatures over MQTT
Implemented with one client in order not to open so many sockets as threads.
"""

import json
import random
import time
import datetime

import paho.mqtt.client as mqtt
import jwt


#	
### CONFIGURATION
#

MQTT_IP = "mqtt.googleapis.com"
MQTT_PORT = 8883


#
### Functions
#

def setup(device):
    time.sleep(random.randint(0,10))
    device.counter = 0
    print("[THING {}]  ----------->     Set Up.".format(device.id))


def loop (device):
    device.send(
        json.dumps({
            "device_id": device.id,
            "counter": device.counter,
            "temperature": random.gauss(25,15),
            "battery": device.battery
        }),
        "virtual_things"
    )
    device.counter += 1

def send(device, message, topic):
    print(message)
   
    topic = "/devices/[device name]/events"

    mqtt_client.publish(topic, payload=message, qos=0, retain=False)


def create_jwt(project_id, private_key_file, algorithm):
  """Create a JWT (https://jwt.io) to establish an MQTT connection."""
  token = {
      'iat': datetime.datetime.utcnow(),
      'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
      'aud': project_id
  }
  with open(private_key_file, 'r') as f:
    private_key = f.read()
  print 'Creating JWT using {} from private key file {}'.format(
      algorithm, private_key_file)
  return jwt.encode(token, private_key, algorithm=algorithm)



#
### Configuration
#
mqtt_client = mqtt.Client(client_id='projects/[project id]/locations/[location]/registries/[device registry name]/devices/[device name]')
mqtt_client.username_pw_set(username='unused', password=create_jwt('[project id]','[private key path]','ES256'))
mqtt_client.tls_set("[google authority .pem path (included in repo)]")


mqtt_client.connect(MQTT_IP, MQTT_PORT, keepalive=60)

