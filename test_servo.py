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
    print("1")
    robot.armMoveAngle(0, 0)
    robot.wait(1)
    print("2")
    robot.armMoveAngle(0, 90)
    robot.wait(1)
    print("3")
    robot.armMoveAngle(0, 180)
    robot.wait(1)

    robot.finish()

except RosiException as e:
    print(e.value)
except KeyboardInterrupt:
    robot.finish()  