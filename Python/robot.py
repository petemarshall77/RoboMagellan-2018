#
# MONTY III - Main Robot class
#
from threading import Thread
import time

from logger import Logger
from powersteering import PowerSteering
from speedometer import Speedometer
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
        self.speedometer = Speedometer(ports['speedometer'], 9600, self.logger)
        self.powersteering = PowerSteering(ports['chias'], 9600, self.logger, self.speedometer)
       
    def initialize(self):
        self.logger.write("Robot: initializing")
        self.logger.display("Initializing...")
        self.speedometer_thread = Thread(target = self.speedometer.run)
        self.powersteering_thread = Thread(target = self.powersteering.run)
	self.speedometer_thread.start()
	self.powersteering_thread.start()
       
    def terminate(self):
        self.logger.write("Robot: terminating")
        self.logger.display("Terminating...")
        self.speedometer.terminate()
        self.powersteering.terminate()
       
    def wait_for_start_switch(self):
        time.sleep(5) #TODO: implement this
        
    def set_power_and_steering(self, power_value, steer_value):
        self.powersteering.set_power_and_steering(power_value, steer_value)

    def set_speed_and_direction(self, speed, direction):
	self.powersteering.set_speed_and_direction(speed, direction)
