# Think Create Learn
# www.thinkcreatelearn.co.uk
#
# ROSI line following sample solution
# 
# Follows a line on the ground using the light sensors

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
    robot.numLightSensors = 3

    # These will be set to the desired speed
    leftMotorSpeed = 0
    rightMotorSpeed = 0

    # Keep a count of how many loops since we last saw the line
    cantSeeLineCount = 0

    # Loop until we can't see the line for 50 continous counts
    while cantSeeLineCount<50:
        # Read from the line sensor 
        reading = robot.readLightSensor()
        left = reading[0]
        centre = reading[1]
        right = reading[2]

        # Execute the logic to keep the robot on the line                                          
        if (centre and not left and not right):
            # We are over the line - go straight
            leftMotorSpeed = 50
            rightMotorSpeed = 50
            cantSeeLineCount = 0 
        elif (left and not centre and not right):
            # We can see the line to the left - turn full left
            leftMotorSpeed = -50
            rightMotorSpeed = 50
            cantSeeLineCount = 0 
        elif (right and not centre and not left):
            # We can see the line to the right - turn full right
            leftMotorSpeed = 50
            rightMotorSpeed = -50
            cantSeeLineCount = 0 
        elif (left and centre and not right):
            # We can see the line to the left and centre - turn a bit left
            leftMotorSpeed = -40
            rightMotorSpeed = 40
            cantSeeLineCount = 0  
        elif (right and centre and not left):
            # We can see the line to the right and centre - turn a bit right
            leftMotorSpeed = 40
            rightMotorSpeed = -40
            cantSeeLineCount = 0
        elif (not left and not centre and not right):
            # We can't see the line at all - proceed in the same direction slowly, and if we still can't see the line go back until we can
            if (cantSeeLineCount==0):
                leftMotorSpeed *= 0.8 
                rightMotorSpeed *= 0.8 
            cantSeeLineCount += 1            
            if (cantSeeLineCount>4):
                leftMotorSpeed = -30  
                rightMotorSpeed = -30    
        elif (left and right and not centre):
            # We can see the line on both sides but not the centre - rotate
            leftMotorSpeed = -50
            rightMotorSpeed = 50 
            cantSeeLineCount = 0
        elif (left and centre and right):
            # We can see the line on all sensors - rotate
            leftMotorSpeed = -50 
            rightMotorSpeed = 50 
            cantSeeLineCount = 0 

        robot.turnMotors(leftMotorSpeed, rightMotorSpeed)
        robot.wait(0.1)

    robot.finish()

except RosiException as e:
    print(e.value)
except KeyboardInterrupt:
    robot.finish()    
    
