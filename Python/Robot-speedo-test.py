#This is the Monte test program

import time
import traceback

from robot import Robot

robot = Robot()
robot.initialize()
robot.wait_for_gps()
robot.wait_for_start_switch()

while True:
    robot.logger.display("C: %d" %robot.compasswitch.get_heading())
#robot.set_speed_and_direction(2, 100)

#try:
#    while True:
#        robot.logger.write("Speed = %0.5f, Acceleration = %0.5f" % robot.speedometer.get_speed_and_acceleration())
#        robot.logger.display("V=%0.2f A=%0.2f" % robot.speedometer.get_speed_and_acceleration()) 
#        time.sleep(0.2)

#except:
#    robot.logger.write(traceback.format_exc())

robot.terminate()
