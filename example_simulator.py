# -*- coding: utf-8 -*-
"""Virtual Thing example.
"""

import time
import random
import sys

from virtual_thing import VirtualThing
# from thing import test as functions
from thing import mqtt_temp as functions

if __name__=="__main__":
    workers = []
    n = False
    try:
        n = int(sys.argv[1])
    except Exception:
        print("USAGE: python example.py <num_workers>")
    if n:
        for i in range(n): # Create workers
            thing = VirtualThing(str(i))
            thing.set_setup(functions.setup)
            thing.set_loop(functions.loop, sleep_seconds=random.randint(1,3))
            thing.set_send(functions.send, loss_p=0.1)
            thing.set_battery(3.3, 3.0, 500, costs={
                    "send": 2.0,
                    "compute_sg": 1.0,
                    "alive_sg": 0.1
                },
                behaviour='lineal'
            )
            thing.set_reboot_p(0.001)
            thing.set_die_p(0.00001)
            workers.append(thing)
        print "Press <ENTER> to launch {} workers.".format(len(workers))
        print "Press <ENTER> again to stop workers."
        _ = raw_input()
        for thing in workers:  # Launch workers
            thing.start()
        _ = raw_input()
        print "Stopping workers."
        for thing in workers:  # Stop workers
            thing.stop()
        for w in workers:
            w.join()
