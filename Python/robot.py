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
import utils

# Configuration
GPS_ERROR_RADIUS = 5.0

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
	
    def drive_to_waypoint(self, target_lat, target_lon, speed):
	    self.logger.write("Called drive_to_waypoint: lat=%0.5f, lon=%0.5f, speed=%0.1f" % (target_lat, target_lon, speed))
	    (distance, bearing) = utils.get_distance_and_bearing (
	                                self.gps.get_latitude(),
	                                self.gps.get_longitude(),
	                                target_lat,
	                                target_lon )
	    
	    while distance >  GPS_ERROR_RADIUS:
	        self.logger.write("Drive_to_waypoint: distance=%0.2f, bearing=%0.1f, tgt_speed=%0.2f" % (distance, bearing, speed))
	        self.logger.write("Drive_to_waypoint: actual_speed=%0.2f, power=%d" % (self.speedometer.get_speed(), self.powersteering.get_power()))
	        self.logger.display("D2W %0.1f, %05.1f" % (distance, bearing))
	        self.logger.display("D2W %0.1f, %d" % (self.speedometer.get_speed(), self.powersteering.get_power())) 
	        self.powersteering.set_speed_and_direction(speed, bearing)
	        time.sleep(0.5)
	        (distance, bearing) = utils.get_distance_and_bearing (
	                                self.gps.get_latitude(),
	                                self.gps.get_longitude(),
	                                target_lat,
	                                target_lon )
	    
	    self.logger.write("Drive_to_waypoint: arrived, distance = %o.2f" % distance)
	    
	    
    def backup_to_compass(self, target_heading, power = -100, steer = 400, accuracy = 15, timeout = 10):
        self.logger.write("Back up to Compass: target = %d , power = %d , steer = %d , accuracy = %d , timeout = %d"
                           % (target_heading, power, steer, accuracy, timeout))
        delta_angle = target_heading - self.compasswitch.get_heading()
        
        if delta_angle > 180:
            delta_angle = int(delta_angle + 360)
        elif delta_angle < -180:
            delta_angle = int(delta_angle - 360)
        else:
            delta_angle = int(delta_angle)
        
        if delta_angle > 0:
            steering = -steer
        elif delta_angle < 0:
            steering = steer
        else:
            return
            
        start_time = time.time()
        self.powersteering.set_power_and_steering(power, steering)
        while abs(target_heading - self.compasswitch.get_heading()) > accuracy:
            self.logger.display("B2C: tgt=%d cur=%d" % (target_heading, self.compasswitch.get_heading()))
            if time.time() - start_time > timeout:
                self.logger.write("B2C - Timed Out")
                break
                
        self.powersteering.set_power_and_steering(0, 0)
    
    def backup_to_waypoint(self, target_lat, target_lon):
        (distance, bearing) = utils.get_distance_and_bearing (
	                                self.gps.get_latitude(),
	                                self.gps.get_longitude(),
	                                target_lat,
	                                target_lon )
        self.backup_to_compass(bearing)
    
    
    
    
    
    
    
    
    
    
    
    
	        
	    
