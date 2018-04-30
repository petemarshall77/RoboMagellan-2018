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
        self.read_time = time.time()

    def terminate(self):
        self._running = False
        
    def get_bump_switch(self):
        return self.bump_switch
        
    def get_heading(self):
        return self.heading

    def run(self):
        self._running = True
        self.logger.write("Compasswitch: running")
        while (self._running == True):
            if self.serial.inWaiting() > 0:
                try:
                    data = self.serial.readline().rstrip()
                    self.heading = float(data.split(',')[0])
                    self.heading = 0.00000738517*(self.heading**3)-0.003247*(self.heading**2)+1.249041*(self.heading)+20.93111734
                    #self.heading = -0.00002038*(self.heading**3)+0.012*(self.heading**2)-0.758*(self.heading)+42.43
                    #self.logger.display(self.heading)
                    
                    if self.heading > 360:
                        self.heading -=360
                    
                    if int(data.split(',')[1]) == 1:
                        self.bump_switch = True
                    else:
                        self.bump_switch = False
                    if int(data.split(',')[2]) == 1:
                        self.start_switch = True
                    else:
                        self.start_switch = False
                except:
                    pass  # ignore errors - more data will arrive very soon!
            else: 
                time.sleep(0.1)
            self.read_time = time.time()

        self.logger.write("Compasswitch: terminated")


