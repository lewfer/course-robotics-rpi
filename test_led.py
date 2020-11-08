# Think Create Learn
# www.thinkcreatelearn.co.uk
#
# ROSI led tester

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

    led = robot.Led(channel=0)      # create an led on output channel 0

    led.on()
    robot.wait(seconds=5)
    led.off()
    
    robot.finish()

except RosiException as e:
    print(e.value)
except KeyboardInterrupt:
    robot.finish()    