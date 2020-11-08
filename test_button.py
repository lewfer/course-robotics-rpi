# Think Create Learn
# www.thinkcreatelearn.co.uk
#
# ROSI button tester

# ======================================================================================================
# Imports
# ======================================================================================================
from rosi import RosiRobot, RosiException 

# ======================================================================================================
# Main program
# ======================================================================================================
try:
    print( 'Press CTRL+C to quit')

    robot = RosiRobot()

    robot.start()

    button = robot.Button(0)           # create a button on input pin 0

    while True:
        if (button.isPressed()):
            print("Pressed")
        else:
            print("Not pressed")  
        robot.wait(seconds=0.1)        # allow some time for Ctrl-C
    
    robot.finish()

except RosiException as e:
    print(e.value)
except KeyboardInterrupt:
    robot.finish()    