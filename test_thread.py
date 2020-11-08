# Think Create Learn
# www.thinkcreatelearn.co.uk
#
# ROSI template

# ======================================================================================================
# Imports
# ======================================================================================================
from rosi import RosiRobot, RosiException 
from threading import Thread


def ledFlash():
    while True:
        led.on()
        robot.wait(1)
        led.off()
        robot.wait(1)


# ======================================================================================================
# Main program
# ======================================================================================================
try:
    robot = RosiRobot()

    robot.start()

    led = robot.Led(0)

    # Start thread
    ledThread = Thread(target=ledFlash)
    ledThread.start()

    while True:
        robot.turnMotors(100,100)
        robot.wait(5)
        robot.turnMotors(-100,-100)
        robot.wait(5)

    robot.finish()

except RosiException as e:
    print(e.value)
except KeyboardInterrupt:
    robot.finish()  