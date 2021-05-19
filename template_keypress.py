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

    # Turn off the delay, so getch() doesn't wait for a key
    window.nodelay(True)

    while running:
        key = window.getch()    # get a key press
        curses.flushinp()       # clear out all other key presses (so we don't buffer)

        if key==curses.KEY_UP:
            print("KEY_UP\r")

        elif key==curses.KEY_DOWN: 
            print("KEY_DOWN\r") 

        elif key==curses.KEY_LEFT:
            print("KEY_LEFT\r")
            
        elif key==curses.KEY_RIGHT:
            print("KEY_RIGHT\r")

        elif key==ord('a') or key==ord('A') :
            print("a\r")

        elif key!= -1: 
            print("Unhandled key",str(key),"\r")

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
