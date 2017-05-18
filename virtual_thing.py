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
        self.id = thing_id  # Identity
        self.time_start = None  # When the device starts
        self.setup_function = lambda : None
        self.loop_function = lambda : None
        self.loop_function_sleep = 0  # Delay between loops
        self.reboot_p = 0
        self.die_p = 0
        self.alive = False
        # SEND
        self.send_function = lambda x: None
        self.send_loss_p = 0
        # BATTERY
        self.battery_capacity = 0
        self.battery_used = -1
        self.battery_costs = {
            "send": 0,
            "compute_sg": 0,
            "alive_sg": 0
        }
        self.battery_used2volts = lambda x : -1  # Battery voltage
        super(VirtualThing, self).__init__()

    @property
    def battery(self):
        """Calculate the volts in the battery from the device usage.

        Returns
        -------
        retval: float
            Volts measured in the battery.
        """
        return self.battery_used2volts(self.battery_used)


    def set_send(self, send_function, loss_p=0):
        self.send_function = send_function
        self.send_loss_p = loss_p


    def set_battery(self, v_max, v_min, capacity, costs, behaviour='lineal'):
        """Set a battery for the device.

        Parameters
        ----------
        v_max: float
            Nominal voltage for the battery.
        v_min: float
            Minimumn operative voltage for the device.
        capacity: float
            Battery capacity. For example mAh
        costs: dict {"send", "compute_sg", "alive_sg"}
            send: capacity lost on a single device send operation.
            compute_sg: capacity lost per second running.
            alive_sg: capacity lost per second alive. Independent from compute_sg.
        behaviour: lambda float: float
            Mapping function from cumulative cost to remaining voltage.
        """
        functions = {
            'lineal': lambda cost_cumulative: (v_min-v_max)/capacity*cost_cumulative + v_max
        }
        self.battery_used2volts = functions[behaviour]
        self.battery_used = 0
        self.battery_capacity = capacity
        self.battery_costs = costs


    def set_reboot_p(self, reboot_p):
        """Set the probability for the device to randomly reboot.
        """
        self.reboot_p = reboot_p

    def set_die_p(self, die_p):
        """Set the probability for the device to randomly die.
        """
        self.die_p = die_p

    #
    ### A la Arduino
    #
    def set_setup(self, setup_function):
        """Set the function the device runs on boot up.
        """
        self.setup_function = setup_function

    def set_loop(self, loop_function, sleep_seconds):
        """Set the loop function for the device.
        """
        self.loop_function = loop_function
        self.loop_function_sleep = sleep_seconds


    #
    ### Operative
    #
    def run(self):
        """Start the thing.
        It takes into consideration the battery and events probabilities.
        """
        self.time_start = time.time()
        self.alive = True
        p = -1  # Device reboot == boot up
        while self.alive:
            time_loop_alive = time.time()
            # Reboot
            if p<self.reboot_p:
                time_reboot = time.time()
                self.setup_function(self)
                self.battery_used += self.battery_costs["compute_sg"]*(time.time()-time_reboot)
            # Loop
            time_loop = time.time()
            self.loop_function(self)
            self.battery_used += self.battery_costs["compute_sg"]*(time.time()-time_loop)
            # Sleep
            time.sleep(self.loop_function_sleep)
            self.battery_used += self.battery_costs["alive_sg"]*(time.time()-time_loop_alive)
            # Events
            p = random.random()
            if p<self.die_p or self.battery_used>=self.battery_capacity:  # Device dies
                self.alive = False

    def stop(self):
        """Stop the thing
        """
        self.alive = False


    #
    ### Inner functions
    #
    def send(self, *args, **kwargs):
        """Send a message. This is a wrapper over the user-defined function to
        take into account battery consumption and packet lost.

        Parameters
        ----------
        Same as user-defined function plus object itself.

        Returns
        -------
        retval: bool
            Wether or not the message was sent.
        """
        retval = False
        if random.random()>=self.send_loss_p:
            self.send_function(self, *args, **kwargs)
            retval = True
        self.battery_used += self.battery_costs["send"]
        return retval
