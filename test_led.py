# Think Create Learn
# www.thinkcreatelearn.co.uk
#
# ROSI led tester

# ======================================================================================================
# Imports
# ======================================================================================================
from rosi import RosiRobot

# ======================================================================================================
# Main program
# ======================================================================================================

robot = RosiRobot()
robot.start()

led = robot.Led(channel=0)      # create an led on output channel 0

led.on()
robot.wait(seconds=5)
led.off()

robot.finish()
