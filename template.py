# Think Create Learn
# www.thinkcreatelearn.co.uk
#
# ROSI template

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

    # ******** DO SOMETHING HERE ********

    robot.finish()

except RosiException as e:
    print(e.value)
except KeyboardInterrupt:
    robot.finish()  