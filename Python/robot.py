#
# MONTY III - Main Robot class
#
from threading import Thread
import time

from logger import Logger
from powersteering import PowerSteering
from speedometer import Speedometer
from compasswitch import Compasswitch
from gps import GPS
from camera import Camera
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
        self.compasswitch = Compasswitch(ports['compasswitch'], 9600, self.logger)
        self.powersteering = PowerSteering(ports['chias'], 9600, self.logger, self.speedometer, self.compasswitch)
        self.gps = GPS(ports['gps'], 4800, self.logger)
        self.camera = Camera(9788, self.logger)
       
    def initialize(self):
        self.logger.write("Robot: initializing")
        self.logger.display("Initializing...")
        self.speedometer_thread = Thread(target = self.speedometer.run)
        self.compasswitch_thread = Thread(target = self.compasswitch.run)
        self.powersteering_thread = Thread(target = self.powersteering.run)
        self.gps_thread = Thread(target = self.gps.run)
        self.camera_thread = Thread(target = self.camera.run)
	self.compasswitch_thread.start()
        self.speedometer_thread.start()
        self.powersteering_thread.start()
	self.gps_thread.start()
	self.camera_thread.start()
       
    def terminate(self):
        self.logger.write("Robot: terminating")
        self.logger.display("Terminating...")
        self.speedometer.terminate()
        self.compasswitch.terminate()
        self.powersteering.terminate()
        self.gps.terminate()
        self.camera.terminate()
       
    def wait_for_start_switch(self):
        self.logger.write("Press start")
        self.logger.display("Press start")
        while self.compasswitch.start_switch == False:
            pass
        self.logger.write("Button Pressed")
        self.logger.display("Button Pressed")
            
    def wait_for_gps(self):
        self.logger.display("Waiting for GPS")
        self.logger.write("Waiting for GPS")
        while self.gps.got_fix() == False:
            pass
        
    def set_power_and_steering(self, power_value, steer_value):
        self.powersteering.set_power_and_steering(power_value, steer_value)

    def set_speed_and_direction(self, speed, direction):
	self.powersteering.set_speed_and_direction(speed, direction)
