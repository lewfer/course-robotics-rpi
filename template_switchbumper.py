# Think Create Learn
# www.thinkcreatelearn.co.uk
#
# ROSI switch bumper template

# ======================================================================================================
# Imports
# ======================================================================================================
from rosi import RosiRobot, RosiException 


# ======================================================================================================
# Main program
# ======================================================================================================

robot = RosiRobot()
robot.start()

button = robot.Button(0)           # create a button on input pin 0

while True:
    if (button.isPressed()):
        robot.stop()               # stop
    else:
        robot.turnMotors(100,100)  # full speed forward

    robot.wait(0.1) 

robot.finish()
