# Think Create Learn
# www.thinkcreatelearn.co.uk
#
# ROSI analogue / potentiometer tester


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

analogue = robot.AnalogueIn(3)      # create a button on input pin 3

while True:
    value = analogue.read()
    print("Value is", value)
    robot.wait(seconds=1) 

robot.finish()
