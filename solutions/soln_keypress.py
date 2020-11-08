# Think Create Learn
# www.thinkcreatelearn.co.uk
#
# ROSI keypress sample solution.
#
# Use keyboard key presses to control a robot


# ======================================================================================================
# Imports
# ======================================================================================================
from rosi import RosiRobot, RosiException 
import curses


# ======================================================================================================
# Functions
# ======================================================================================================
def handleKeys(window):    
    # Variable to indicate if we are still running
    running = True

    defaultSpeed = 20    
    speed = defaultSpeed
    leftDirection = 0
    rightDirection = 0

    while running:
        key = window.getch()    # get a key press
        curses.flushinp()       # clear out all other key presses (so we don't buffer)
        if key != -1:
            # UP cursor key
            if key==curses.KEY_UP:
                print("KEY_UP")
                
                if (leftDirection==0 or rightDirection==0):
                    # Currently stopped or turning so go straight forward
                    leftDirection = 1
                    rightDirection = 1
                    speed = defaultSpeed
                elif leftDirection==1 and rightDirection==1:
                    # Currently going forwards so increase forward speed
                    speed += 10
                    if speed > 100:
                        speed = 100                       
                else:
                    # Must be going backward, so decrease speed
                    speed -= 10
                    if speed < 0:
                        # Speed has gone negative, so move forward
                        speed = 10   
                        leftDirection = 1
                        rightDirection = 1  
                    

            # DOWN cursor key
            elif key==curses.KEY_DOWN: 
                print("KEY_DOWN") 
              
                if leftDirection==0 or rightDirection==0:
                    # Currently stopped or turning so go straight back
                    leftDirection = -1
                    rightDirection = -1
                    speed = defaultSpeed
                elif leftDirection==-1 and rightDirection==-1:
                    # Currently going backwards so increase backward speed
                    speed += 10
                    if speed > 100:
                        speed = 100   
                else:
                    # Must be going forward, so decrease speed
                    speed -= 10
                    if speed < 0:
                        # Speed has gone negative, so move backward
                        speed = 10   
                        leftDirection = -1
                        rightDirection = -1

            # Tab or space key
            elif key==9 or key==ord(' '):
                # Stop
                speed = 0 
                leftDirection = 0
                rightDirection = 0                              

            # LEFT cursor key
            elif key==curses.KEY_LEFT:
                print("KEY_LEFT")
                
                if leftDirection==0 and rightDirection==1:
                    # Already turning left so increase speed
                    speed += 10
                    if speed > 100:
                        speed = 100            
                else:          
                    # Turn left at current speed
                    leftDirection = 0
                    rightDirection = 1
                
            # Turn right
            elif key==curses.KEY_RIGHT:
                print("KEY_RIGHT")

                if leftDirection==1 and rightDirection==0:
                    # Already turning right so increase speed
                    speed += 10
                    if speed > 100:
                        speed = 100     
                else:                
                    # Turn right at current speed
                    leftDirection = 1
                    rightDirection = 0

            # K key
            elif key==ord('k'):
                print("k")

                # Quit
                running = False

            else: 
                print("Unhandled key",str(key))

            # Now turn the motors according to the selected speed
            print("Speed ", speed)
            robot.turnMotors(speed*leftDirection, speed*rightDirection)              
   

            # Give the computer a bit of time to rest
            robot.wait(0.1)

# ======================================================================================================
# Main program
# ======================================================================================================
try:
    robot = RosiRobot()
    
    robot.start()

    curses.wrapper(handleKeys)

    robot.finish()

except IOError as e:
    print(e)
except RosiException as e:
    print(e.value)
except KeyboardInterrupt:
    robot.finish()    
