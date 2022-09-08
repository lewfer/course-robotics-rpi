# Think Create Learn
# www.thinkcreatelearn.co.uk
#
# ROSI template for remote control using a games controller


# ======================================================================================================
# Imports
# ======================================================================================================
from rosi import RosiRobot
from approxeng.input.selectbinder import ControllerResource


# ======================================================================================================
# Main program
# ======================================================================================================
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
            # ******** DO SOMETHING HERE ********
            print("Cross")
            
        if joystick.dleft:
            # ******** DO SOMETHING HERE ********    
            print("D Left")           

        if joystick.dright:
            # ******** DO SOMETHING HERE ********  
            print("D Right")             
            
        if joystick.ly:
            # ******** DO SOMETHING HERE ********    
            print("Stick Left Y ", joystick.ly) 
                            
        # Give the computer a bit of time to rest
        robot.wait(0.1)

robot.finish()
