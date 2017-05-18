# -*- coding: utf-8 -*-
"""Test functions to inject into thing.
"""

import random
import time

#
### Functions
#
def setup(device):
    time.sleep(random.randint(0,10))  # Wait some time before starting
    device.counter = 0  # Create a new variable
    print("[THING {}]  ----------->     Set Up.".format(device.id))

def loop (device):
    device.send("[THING {}]  Loop:{}, battery:{}".format(
        device.id, device.counter, device.battery
    ))
    device.counter += 1

def send(device, message):
    print(message)
