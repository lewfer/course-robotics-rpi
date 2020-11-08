# Think Create Learn
# www.thinkcreatelearn.co.uk
#
# ROSI reset
# Reset to stop motors

from rosi import RosiRobot, RosiException

try:

    robot = RosiRobot()

    robot.start()

    robot.finish()

except RosiException as e:
    print(e.value)
