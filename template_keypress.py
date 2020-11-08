# Think Create Learn
# www.thinkcreatelearn.co.uk
#
# ROSI template for remote control using key presses

# ======================================================================================================
# Imports
# ======================================================================================================
from rosi import RosiRobot, RosiException 
import curses

# ======================================================================================================
# Constants
# ======================================================================================================


# ======================================================================================================
# Global variables
# ======================================================================================================


# ======================================================================================================
# Functions
# ======================================================================================================
def handleKeys(window):
    # Variable to indicate if we are still running
    running = True

    while running:
        key = window.getch()    # get a key press
        curses.flushinp()       # clear out all other key presses (so we don't buffer)
        if key != -1:
            if key==curses.KEY_UP:
                print("KEY_UP")

            elif key==curses.KEY_DOWN: 
                print("KEY_DOWN") 

            elif key==curses.KEY_LEFT:
                print("KEY_LEFT")
                
            elif key==curses.KEY_RIGHT:
                print("KEY_RIGHT")

            elif key==ord('a') or key==ord('A') :
                print("a")

            else: 
                print("Unhandled key",str(key))

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
