from serial import Serial

# MONTY III: GPS interface
#   writes current GPS coordinates to self.latitude and self,longitude,
#   or 0.0, 0.0 if no GPS fix available

class GPS:

    def __init__(self, port_name, baud_rate, logger):
        self._running = False
        self.logger = logger
        self.logger.write("GPS: starting")
        self.serial = Serial(port_name, baud_rate)
        self.latitude = 0.0
        self.longitude = 0.0

    def terminate(self):
        self._running = False

    def got_fix(self):
        if self.latitude != 0.0 and self.longitude != 0.0:
            return True
        else:
            return False

    def run(self):
        self._running = True
        self.logger.write("GPS: running")
        while (self._running == True):
            if self.serial.inWaiting() > 0:
                data = self.serial.readline().rstrip()
                if data[0:6] == "$GPRMC":
                    fields = data.split(',')
                    if fields[2] == 'A':
                        self.latitude = int(fields[3][0:2]) + (float(fields[3][2:]) / 60.0) #ASSUMES TWO DIGIT LATITUDE
                        self.longitude = int(fields[5][0:3]) + (float(fields[5][3:]) / 60.0) #ASSUMES THREE DIGIT LONGITUDE
                    else:
                        self.latitude = 0.0
                        self.longitude = 0.0

        self.logger.write("GPS: terminated")
