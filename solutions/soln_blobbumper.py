# Think Create Learn
# www.thinkcreatelearn.co.uk
#
# ROSI blob (light sensor) bumper sample solution
#
# Turns around when it sees a black blob on the ground


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
    print("Press Ctrl-C to stop")
    robot.numLightSensors = 1
    robot.tracingOn()

    while True:
        if robot.lightSensorSeeingBlob():
            robot.stop()
            robot.turnMotors(-100,-100)  # full speed backward
            robot.backwardDistance(100,centimetres=15)
            robot.spinAngle(180)            
        else:
            robot.turnMotors(100,100)  # full speed forward
        
        robot.wait(0.1)

    robot.finish()

except RosiException as e:
    print(e.value)
except KeyboardInterrupt:
    robot.finish()    
    
