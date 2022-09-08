# Think Create Learn
# www.thinkcreatelearn.co.uk
#
# ROSI template for line following

# ======================================================================================================
# Imports
# ======================================================================================================
from rosi import RosiRobot


# ======================================================================================================
# Main program
# ======================================================================================================
print( 'Press CTRL+C to quit')

robot = RosiRobot()

robot.start()

# Set the number of light sensors we have (1, 2 or 3)
robot.numLightSensors = 3

# Loop forever (or until Ctrl-C)
while True:
    # Read from the line sensor 
    reading = robot.readLightSensor()
    left = reading[0]
    centre = reading[1]
    right = reading[2]
    print (left, centre, right)

    # ******** DO SOMETHING HERE ********  

    robot.wait(0.1)

robot.finish()

