from serial import Serial
import time

# Interface to steering servo and power controller
#    Input values:
#        Steering: from -500 (full left) to +500 (full right)
#        Power:    from -500 (full reverse) to +500 (full forward)
#
#        All values are further constained to limit steering and
#        (especially) power.
STEER_MAX = 500
POWER_MAX = 150
STEER_TRIM = 40
AUTOPILOT_POWER_GAIN = 1.0

class PowerSteering:

    def __init__(self, port_name, baud_rate, logger, speedometer):
        self._running = False
        self.logger = logger
        self.speedometer = speedometer
        self.logger.write("PowerSteering: started.")
        self.power = 0
        self.steering = 0
        self.new_values = False
        self.autopilot_on = False
        self.speed = 0
        self.direction = 0
	power_value = 0

	self.Serial = Serial(port_name, baud_rate, timeout=None)

    def stop(self):
        self.logger.write("PowerSteering: stop")
        self.set_power_and_steering(0, 0)

    def set_power_and_steering(self, power_value, steer_value, autopilot = False):
        self.logger.write("PowerSteering: power %d, steer %d" %
                          (power_value, steer_value))
        self.autopilot_on = autopilot
                          
        # Condition values past
        if steer_value > STEER_MAX - STEER_TRIM:
            steer_value = STEER_MAX - STEER_TRIM
        elif steer_value < -STEER_MAX - STEER_TRIM:
            steer_value = -STEER_MAX - STEER_TRIM
        if power_value > POWER_MAX:
            power_value = POWER_MAX
        elif power_value < -POWER_MAX:
            power_value = -POWER_MAX
        self.power = power_value
        self.steering = steer_value
        self.new_values = True
    
    def set_speed_and_direction(self, speed, direction):
        self.logger.write("Powersteering: speed %f, direction %d" %
                           (speed, direction))
        self.autopilot_on = True
        self.speed = speed
        self.direction = direction
        
    def terminate(self):
        self.set_power_and_steering(0, 0)
        time.sleep(1)
        self._running = False
        
        
    def run(self):
        self._running = True
        self.logger.write("PowerSteering: running")
        while (self._running == True):
            if self.autopilot_on == True:
                current_speed = self.speedometer.get_speed()
		#Adjust Power for new Values  
                self.power += int((self.speed - current_speed) * AUTOPILOT_POWER_GAIN)
                self.set_power_and_steering(self.power, self.steering, autopilot = True)
            if self.new_values == True:
                steer_value = 1500+self.steering+STEER_TRIM
                power_value = 1500+self.power
    	        commandstring = str(int(steer_value)) + "," + str(int(power_value))
                self.Serial.write(str(int(steer_value)) + "," + str(int(power_value)) + "\n")
                self.Serial.flush()
                self.new_values = False
                time.sleep(0.1) 
