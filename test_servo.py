# Think Create Learn
# www.thinkcreatelearn.co.uk
#
# ROSI template

# ======================================================================================================
# Imports
# ======================================================================================================
from rosi import RosiRobot


# ======================================================================================================
# Main program
# ======================================================================================================
robot = RosiRobot()
robot.start()

# Move servo on pin 5 through different angles
print("1")
robot.armMoveAngle(5, 0)
robot.wait(1)
print("2")
robot.armMoveAngle(5, 90)
robot.wait(1)
print("3")
robot.armMoveAngle(5, 180)
robot.wait(1)

robot.finish()
