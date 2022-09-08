# Think Create Learn
# www.thinkcreatelearn.co.uk
#
# ROSI games controller sample solution
#
# Use a games controller to control a robot

# ======================================================================================================
# Imports
# ======================================================================================================
from rosi import RosiRobot, RosiException 
from approxeng.input.selectbinder import ControllerResource

# The code will automatically detect the controller, but if it doesn't or you want to force a particular 
# controller type then uncomment one of these lines 
#
#from approxeng.input.dualshock3 import DualShock3
#from approxeng.input.dualshock4 import DualShock4
#from approxeng.input.xboxone import WiredXBoxOneSPad
#from approxeng.input.xboxone import WirelessXBoxOneSPad
#from approxeng.input.wii import WiiRemotePro
#from approxeng.input.wiimote import WiiMote
#from approxeng.input.rockcandy import RockCandy 
# 
# Then pass in the appropriate class name to the call
# to ControllerResource() as follows:
#       with ControllerResource(controller_class = DualShock3) as joystick:


# ======================================================================================================
# Main program
# ======================================================================================================
try:

    # Variable to indicate if we are still running
    running = True
    robot = RosiRobot()
    robot.start()

    with ControllerResource() as joystick:
        print ("Found joystick")
        while running and joystick.connected:

            presses = joystick.check_presses()
            
            if joystick.presses.start:
                # We want to exit the program                
                running = False
               
            if joystick.presses.cross:
                # We want to stop the robot
                robot.turnMotors(0, 0) 
                
            if joystick.presses.dleft:
                # We want to spin the robot left
                robot.turnMotors(-100, 100)

            if joystick.presses.dright:
                # We want to spin the robot left
                robot.turnMotors(100, -100)                
                
            if joystick.ly or joystick.rx:
                y = joystick.ly
                x = joystick.rx
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
               
            # Give the computer a bit of time to rest
            robot.wait(0.1)

    robot.finish()

except IOError:
    print("Unable to find any joystick")
except RosiException as e:
    print(e.value)
except KeyboardInterrupt:
    robot.finish()    
