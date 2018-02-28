from serial import Serial
import time, math, traceback

# MONTY III interface to compass modeule and bump and start switches
#    Input:  from compasswitch.ino, compass X and Y values, switch states
#    Output: heading value, switch states

class Compasswitch:

    def __init__(self, port_name, baud_rate, logger):
        self._running = False
        self.logger = logger
        self.logger.write("Compasswitch: starting")
        self.serial = Serial(port_name, baud_rate, timeout=None)
        time.sleep(3)  # wait for Arduino to reset
        self.compassX = 0
        self.compassY = 0
        self.heading  = 0
        self.bump_switch = False
        self.start_switch = False

    def terminate(self):
        self._running = False

    def run(self):
        self._running = True
        self.logger.write("Compasswitch: running")
        while (self._running == True):
            if self.serial.inWaiting() > 0:
                try:
                    data = self.serial.readline().rstrip()
                    self.compassX = float(data.split(',')[0])
                    self.compassY = float(data.split(',')[1])
                    angle = math.atan2(self.compassY, self.compassX)
                    if angle > 0.0:
                        self.heading = 360 - angle * 180 / math.pi
                    else:
                        self.heading = -angle * 180 / math.pi
                    self.heading = 1.13 * self.heading - 15.5 #TODO:recalibrate
                    self.logger.display(self.heading)
		    if int(data.split(',')[2]) == 1:
                        self.bump_switch = True
                    else:
                        self.bump_switch = False
                    if int(data.split(',')[3]) == 1:
                        self.start_switch = True
                    else:
                        self.start_switch = False
                except:
                    pass  # ignore errors - more data will arrive very soon!

        self.logger.write("Compasswitch: terminated")


