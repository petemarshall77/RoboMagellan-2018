#This is the Monte test program

import time
import traceback

from robot import Robot

robot = Robot()
robot.initialize()
robot.wait_for_gps()
robot.wait_for_start_switch()

try:
     robot.set_speed_and_direction(1.5, 200)
     time.sleep(30)
     robot.set_speed_and_direction(1.5, 20)
     time.sleep(30)
#     robot.set_speed_and_direction(1.5, 200)
#     time.sleep(30)
#     robot.set_speed_and_direction(1.5, 20)
#     time.sleep(30)
#    time.sleep(10)
#    robot.set_power_and_steering(40,-250)
#    time.sleep(2)
#    robot.set_power_and_steering(80,0)
#    time.sleep(20)
#    robot.set_power_and_steering(60,250)
#    time.sleep(4)
#    robot.set_power_and_steering(80,0)
#    time.sleep(10)
#    robot.set_power_and_steering(60,250)
#    time.sleep(3)
#    robot.set_power_and_steering(80,0)
#    time.sleep(6)
#    robot.set_power_and_steering(0,0)

except:
    robot.logger.write(traceback.format_exc())

robot.terminate()
