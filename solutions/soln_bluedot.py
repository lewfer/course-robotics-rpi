# Think Create Learn
# www.thinkcreatelearn.co.uk
#
# ROSI bluedot remote control sample solution
#
# Uses Bluedot Android app to control a robot

# ======================================================================================================
# Imports
# ======================================================================================================
from rosi import RosiRobot, RosiException 

from bluedot import BlueDot


# ======================================================================================================
# Global variables
# ======================================================================================================

# Variable to indicate if we are still running
running = True

# ======================================================================================================
# Functions
# ======================================================================================================

# ------------------------------------------------------------------------------------------------------
# Function for Blue Dot.  Is called when we move our finger on the blue dot.
# ------------------------------------------------------------------------------------------------------
def bd_move(pos):
    if (pos.y < 0.1 and pos.y>-0.1):
        if (pos.x < -0.8):
            # Finger at far left - we want to spin the robot left
            robot.turnMotors(-100, 100)
            
        elif (pos.x > 0.8):
            # Finger at far right - we want to spin the robot right
            robot.turnMotors(100, -100)
            
        elif pos.x < 0.1 and pos.x > -0.1:
            # Finger in middle
            robot.stop()
    else:
        # Finger somewhere else
        
        y = pos.y
        x = pos.x
        # We want to move the robot according to the joystick positions
            
        # y is 1.0 for full forward, -1.0 for full backward and 0.0 for stop.  
        # x is 1.0 for full right, -1.0 for full left and 0.0 for straight.        

        # Work out motor speed based on forward-backward axis
        leftMotorSpeed = y * 100
        rightMotorSpeed = y * 100

        # Adjust motor speed based on right-left axis
        if x < 0:  
            # Turning left, slow the left motor down
            leftMotorSpeed = leftMotorSpeed - leftMotorSpeed * -x  
        elif x > 0:  
            # Turning right, slow the right motor down
            rightMotorSpeed = rightMotorSpeed - rightMotorSpeed * x
                
        # Turn motors
        robot.turnMotors(int(leftMotorSpeed), int(rightMotorSpeed))

# ------------------------------------------------------------------------------------------------------
# Function for Blue Dot.  Is called when we lift our finger from the blue dot
# ------------------------------------------------------------------------------------------------------
def bd_stop():
    robot.stop()

# ------------------------------------------------------------------------------------------------------
# Function for Blue Dot.  Placeholder for any action we want to take on a double-press on the blue dot.
# ------------------------------------------------------------------------------------------------------
def bd_double_press():
    robot.stop()


# ======================================================================================================
# Main program
# ======================================================================================================
try:
    robot = RosiRobot()
    robot.start()
    robot.printSettings()

    bd = BlueDot()
    bd.when_pressed = bd_move
    bd.when_moved = bd_move
    bd.when_released = bd_stop 
    bd.when_double_pressed = bd_double_press

    while running:
        robot.wait(0.1)


except RosiException as e:
    print(e.value)

