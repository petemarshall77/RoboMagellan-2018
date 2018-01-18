#
# MONTY III - Main Robot class
#
from threading import Thread
import time

from logger import Logger
from powersteering import PowerSteering
import usb_probe

class Robot:

    def __init__(self):
        self.logger = Logger()
        self.logger.write("Robot: initializing")
        self.logger.display("Starting...")
        ports = usb_probe.probe()
        self.logger.write("Robot: found USB ports...")
        for port in ports:
            self.logger.write("       %s, %s" % (ports[port], port))
        self.powersteering = PowerSteering(ports['chias'], 9600, self.logger)
      
    def initialize(self):
        self.logger.write("Robot: initializing")
        self.logger.display("Initializing...")
       

    def terminate(self):
        self.logger.write("Robot: terminating")
        self.logger.display("Terminating...")
       
    def wait_for_start_switch(self):
        pass #TODO: implement this
        
    def set_power_and_steering(power_value, steer_value):
        self.powersteering.set_power_and_steering(power_value, steer_value)
      

      

