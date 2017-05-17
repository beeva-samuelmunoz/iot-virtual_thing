# -*- coding: utf-8 -*-
"""Thing simulator.
"""

import random
import threading
import time

class VirtualThing(threading.Thread):

    def __init__(self, thing_id):
        """Virtual thing constructor

        Parameters
        ----------
        thing_id: str
            Identificator for the device.
        """
        self.id = thing_id
        self.setup_function = lambda : None
        self.loop_function = lambda : None
        self.loop_function_sleep = False
        self.reboot_p = 0
        self.alive = False
        # SEND
        self.send_function = lambda x: None
        self.send_loss_p = 0
        # BATTERY
        self.battery_v_max = 900
        self.battery_v_now = 900
        self.battery_v_min = -1
        super(VirtualThing, self).__init__()


    def set_send(self, send_function, loss_p=0):
        self.send_function = send_function
        self.send_loss_p = loss_p


    def set_battery(self, v_max, v_min):
        # TODO
        pass

    def set_reboot_p(self, reboot_p):
        self.reboot_p = reboot_p

    def set_setup(self, setup_function):
        self.setup_function = setup_function

    def set_loop(self, loop_function, sleep_seconds):
        self.loop_function = loop_function
        self.loop_function_sleep = sleep_seconds



    def run(self):
        """Start the thing.
        """
        time_init = time.time()
        self.setup_function(self)
        #TODO: runtime affects battery
        # time.time()-time_init
        self.alive = True
        while self.alive:
            time_init = time.time()
            self.loop_function(self)
            #TODO: runtime affects battery
            # time.time()-time_init
            if self.loop_function_sleep: # Supose battery consumption is 0
                time.sleep(self.loop_function_sleep)
            # Device reboots
            if random.random()<self.reboot_p:
                time_init = time.time()
                self.setup_function(self)
                #TODO: runtime affects battery
                # time.time()-time_init


    def stop(self):
        """Stop the thing
        """
        self.alive = False



    #
    ### Inner functions
    #
    def send(self, msg):
        """Send a message.

        Parameters
        ----------
        msg: str
            Message to send.

        Returns
        -------
        retval: bool
            Wether or not the message was sent.
        """
        #TODO:
        # Decrease battery level
        if random.random()>=self.send_loss_p:
            self.send_function(self, msg)
