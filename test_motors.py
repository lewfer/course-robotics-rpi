# Think Create Learn
# www.thinkcreatelearn.co.uk
#
# ROSI motor tester


# ======================================================================================================
# Imports
# ======================================================================================================
from rosi import RosiRobot

# ======================================================================================================
# Main program
# ======================================================================================================
robot = RosiRobot()
robot.start()              # start the robot

robot.turnMotors(50,50)    # turn the left and right motors at 50%
print("Turning both motors")
robot.wait(5)              # wait for 5 seconds

robot.turnMotors(50,0 )    # turn the left motor at 50%
print("Turning left motor")
robot.wait(5)              # wait for 5 seconds

robot.turnMotors(0,50)     # turn the right motor at 50%
print("Turning right motor")
robot.wait(seconds=5)      # wait for 5 seconds       

robot.stop()               # stop the robot
robot.finish()             # clean up

