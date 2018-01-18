import usb_probe
from time import asctime
from serial import Serial

class Logger:

    def __init__(self):
        # Open the log file
        filename = "log/%s.%s" % (asctime(), 'log')
        self.file = open(filename, 'w')
        print("Log file opened.")

        # Open the lcd display
        self.serial = Serial(usb_probe.probe()['lcd-display'], 9600)
        self.serial.write("Monty is alive!\n\n")

    def write(self, message):
        datastring = "%s: %s\n" % (asctime(), message)
        print(datastring.rstrip())
        self.file.write(datastring)

    def display(self, text):
        self.serial.write("%s\n" % text)

    def __del__(self):
        self.file.close()
        print "Log file closed."
