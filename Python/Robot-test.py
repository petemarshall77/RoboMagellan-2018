#This is the Monte test program

import time
import traceback

from robot import Robot

robot = Robot()
robot.initialize()
robot.wait_for_start_switch()

try:
  robot.set_power_and_steering(1600,1500)
  time.sleep(5)
  robot.set_power_and_steering(1500,1500)

except:
    robot.logger.write(traceback.format_exc())

robot.terminate()
