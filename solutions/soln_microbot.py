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
ubit = microbit.Microbit(adapter_addr='B8:27:EB:8F:0A:60',
                         device_addr='C4:82:D1:D6:F6:40')

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

    print(accel, buttona)

    # Respond to the values
    if y<-0.5:       # forward
        robot.turnMotors(100, 100)
    elif y>0.5:      # backward
        robot.turnMotors(-100, -100)
    elif x<-0.5:     # left
        robot.turnMotors(-100, 100)
    elif x>0.5:      # right
        robot.turnMotors(100, -100)
    else:
        robot.turnMotors(0, 0)

ubit.disconnect()
robot.finish()