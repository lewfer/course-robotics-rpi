# Think Create Learn
# www.thinkcreatelearn.co.uk
#
# ROSI ultrasonic tester

# ======================================================================================================
# Imports
# ======================================================================================================
from rosi import RosiRobot
import math

# ======================================================================================================
# Main program
# ======================================================================================================
print( 'Press CTRL+C to quit')

robot = RosiRobot()
robot.start()

global_sonarLastDistances = []

# Keep running until told to stop
while True:
    distance = round(robot.readSonarDistance(),2)
    print(distance)
    robot.wait(seconds=0.5)

robot.finish()


