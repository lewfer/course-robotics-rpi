# Think Create Learn
# www.thinkcreatelearn.co.uk
#
# ROSI games controller sample solution
#
# Use a games controller to control a robot

# ======================================================================================================
# Imports
# ======================================================================================================
import time
from bluezero import microbit
from rosi import RosiRobot

# ======================================================================================================
# Main program
# ======================================================================================================
robot = RosiRobot()
robot.start()

# Connect to the microbit
# Replace xx:xx:xx:xx:xx:xx with your Pi's Bluetooth address
# Replace yy:yy:yy:yy:yy:yy with your Microbit's Bluetooth address
ubit = microbit.Microbit(adapter_addr='xx:xx:xx:xx:xx:xx',
                         device_addr='yy:yy:yy:yy:yy:yy')

ubit.connect()

# Read values from the Microbit and control the robot
buttona = 0
buttonb = 0
while not (buttona==1 and buttonb==1):
    # Read values from the microbit
    accel = ubit.accelerometer
    x = accel[0]
    y = accel[1]
    z = accel[2]
    buttona = ubit.button_a
    buttonb = ubit.button_b

    print(x, y, z, buttona, buttonb)

    # Respond to the values
    # TODO

ubit.disconnect()
robot.finish()