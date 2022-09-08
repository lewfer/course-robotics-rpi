# Think Create Learn
# www.thinkcreatelearn.co.uk
#
# ROSI line following sensor tester

# ======================================================================================================
# Imports
# ======================================================================================================
from rosi import RosiRobot

# ======================================================================================================
# Main program
# ======================================================================================================
print("Press Ctrl-C to stop")

robot = RosiRobot()
robot.start()

robot.numLightSensors = 1

while True:
    # Read from the line sensor 
    reading = robot.readLightSensor()

    # Print out what we see
    print(reading)
    
    robot.wait(seconds=0.1)

robot.finish()
