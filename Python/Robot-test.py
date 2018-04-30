#This is the Monty test program

import time
import traceback

from robot import Robot

robot = Robot()
robot.initialize()
robot.wait_for_gps()
robot.wait_for_start_switch()

try:
#    robot.drive_to_cone(37.65958166666667, 121.88643, 2.0)
#    robot.powersteering.set_speed(-1)
#    time.sleep(5)
#    robot.drive_to_cone(37.65955833333334, 121.88587833333334, 2.0)

    robot.drive_to_waypoint(37.65972, 121.8872, 2.0)
    robot.drive_to_waypoint(37.65976166666667, 121.88675833333333, 2.0)
    robot.drive_to_waypoint(37.65994333333333, 121.88664666666666, 2.0)
    robot.drive_to_waypoint(37.659971666666664, 121.8865, 2.0)
    robot.drive_to_cone(37.660016666666664, 121.88650666666666, 2.0, gps_accuracy = 3.0)

#    robot.drive_to_cone(37.660035, 121.88625, 2.0)
#    time.sleep(5)
#    robot.backup_to_waypoint(37.66003833333333, 121.88595333333333)
#    robot.drive_to_waypoint(37.66003833333333, 121.88595333333333, 2.0)
#    
#    robot.drive_to_waypoint(37.659958333333336, 121.88544166666667, 2.0)
#
#    robot.drive_to_cone(37.659976666666665, 121.88566333333333, 2.0)
#    time.sleep(5)
#    robot.backup_to_compass(160)
#    time.sleep(3)
#    robot.drive_to_cone(37.66005, 121.88590333333333, 2.0)
    #time.sleep(5)
    #robot.backup_to_waypoint(33.77842833333333, 118.41898333333333)
    #robot.drive_to_cone(33.77842833333333, 118.41898333333333, 2.0)

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
