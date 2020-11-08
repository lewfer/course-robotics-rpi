# Think Create Learn
# www.thinkcreatelearn.co.uk
#
# ROSI analogue / potentiometer tester


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

    analogue = robot.AnalogueIn(3)      # create a button on input pin 3

    while True:
        value = analogue.read()
        print("Value is", value)
        robot.wait(seconds=1) 
    
    robot.finish()

except RosiException as e:
    print(e.value)
except KeyboardInterrupt:
    robot.finish()    