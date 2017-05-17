# -*- coding: utf-8 -*-
"""Virtual Thing example.
"""

import time
import random

from virtual_thing import VirtualThing
from thing import test, mqtt_temp

if __name__=="__main__":
    workers = []
    n = 10
    functions = mqtt_temp
    #functions = test
    for i in range(n):
        thing = VirtualThing(str(i))
        thing.set_setup(functions.setup)
        thing.set_loop(functions.loop, sleep_seconds=random.randint(1,3))
        thing.set_send(functions.send, loss_p=0.1)
        thing.set_reboot_p(0.05)
        workers.append(thing)
    print "Press <ENTER> to launch {} workers.".format(len(workers))
    print "Press <ENTER> again to stop workers."
    _ = raw_input()
    for thing in workers:
        thing.start()
    _ = raw_input()
    print "Stopping workers."
    for thing in workers:
        thing.stop()
    for w in workers:
        w.join()
