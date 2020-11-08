# Think Create Learn
# www.thinkcreatelearn.co.uk
#
# ROSI blob bumper template

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
    robot.numLightSensors = 1

    while True:
        if robot.lightSensorSeeingBlob():
            robot.stop()               # stop
            break                      # exit the program
        else:
            robot.turnMotors(100,100)  # full speed forward
        
        robot.wait(0.1)

    robot.finish()

except RosiException as e:
    print(e.value)
except KeyboardInterrupt:
    robot.finish()    
    
