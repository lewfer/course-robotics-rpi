# Think Create Learn
# www.thinkcreatelearn.co.uk
#
# ROSI switch bumper sample solution
#
# Moves forward until the bumper switch is hit, when it turns around


# ======================================================================================================
# Imports
# ======================================================================================================
from rosi import RosiRobot, RosiException 

# ======================================================================================================
# Main program
# ======================================================================================================
try:
    robot = RosiRobot()

    robot.start()

    button = robot.Button(0)           # create a button on input pin 0

    while True:
        if (button.isPressed()):
            robot.stop()               # stop
            robot.turnMotors(-100,-100)  # full speed backward
            robot.backwardDistance(100,centimetres=10)
            robot.spinAngle(180)
        else:
            robot.turnMotors(100,100)  # full speed forward

        robot.wait(0.1)                # allow some time for Ctrl-C
    
    robot.finish()

except RosiException as e:
    print(e.value)
except KeyboardInterrupt:
    robot.finish()    