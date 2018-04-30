from serial import Serial
import time
import traceback

# MONTY III interface to speedometer arduino
#    Input:  from speedometer.ino, rotations/second, total rotations
#    Output: speed in m/s, distance travelled in meters, via accessor functions

class Speedometer:

    def __init__(self, port_name, baud_rate, logger):
        self._running = False
        self.logger = logger
        self.logger.write("Speedometer: starting")
        self.serial = Serial(port_name, baud_rate, timeout=None)
        time.sleep(3)  # wait for Arduino to reset
        self.speed = 0
        self.last_speed = 0
        self.last_time = time.time()
        self.acceleration = 0 
        self.distance = 0

    def get_speed(self):
        return self.speed
        
    def get_speed_and_acceleration(self):
        return (self.speed, self.acceleration)

    def terminate(self):
        self._running = False

    def run(self):
        self._running = True
        self.logger.write("Speedometer: running")
        while (self._running == True):
            if self.serial.inWaiting() > 0:
                try:
                    self.last_speed = self.speed
                    
                    # Process data from Arduino
                    data = self.serial.readline().rstrip()
                    self.speed = float(data.split(',')[0]) * 0.1142
                    self.distance = float(data.split(',')[1]) * 0.1142
                    
                    # Calculate acceleration
                    self.acceleration = (self.speed - self.last_speed)/(time.time() - self.last_time)
                    self.last_time = time.time()
                    
                except:
                    self.logger.write(traceback.format_exc())

        self.logger.write("Speedometer: terminated")
