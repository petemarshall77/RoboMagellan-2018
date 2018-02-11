#This is the Monte test program

import time
import traceback

from robot import Robot

robot = Robot()
robot.initialize()
robot.wait_for_start_switch()

try:
    time.sleep(3600)

except:
    robot.logger.write(traceback.format_exc())

robot.terminate()
