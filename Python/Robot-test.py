#This is the Monty test program

import time
import traceback

from robot import Robot

robot = Robot()
robot.initialize()
robot.wait_for_gps()
robot.wait_for_start_switch()

try:
    robot.drive_to_cone(33.778575000000004, 118.41897833333333, 2.0)
    time.sleep(5)
    robot.backup_to_waypoint(33.778373333333334, 118.41907333333333)
    robot.drive_to_cone(33.778373333333334, 118.41907333333333, 2.0)
    time.sleep(5)
    robot.backup_to_waypoint(33.77823333333333, 118.41864833333334)
    robot.drive_to_cone(33.77823333333333, 118.41864833333334, 2.0)
    time.sleep(5)
    robot.backup_to_waypoint(33.77842833333333, 118.41898333333333)
    robot.drive_to_cone(33.77842833333333, 118.41898333333333, 2.0)

#    time.sleep(3)
#    robot.backup_to_waypoint(33.778481666666664, 118.41900333333334)
#    robot.drive_to_waypoint(33.778481666666664, 118.41900333333334, 2.0)
#    robot.powersteering.set_power_and_steering(0, 0)
#    time.sleep(3)
#    robot.backup_to_compass(0)
#    robot.set_speed_and_direction(1.5, 200)
#    time.sleep(30)
#    robot.set_speed_and_direction(1.5, 20)
#    time.sleep(30)
#    robot.set_speed_and_direction(1.5, 200)
#    time.sleep(30)
#    robot.set_speed_and_direction(1.5, 20)
#    time.sleep(30)
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
