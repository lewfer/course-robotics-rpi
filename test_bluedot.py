# Think Create Learn
# www.thinkcreatelearn.co.uk
#
# ROSI bluedot test
#

from bluedot import BlueDot

def sayHello():
    ''' Bluedot callback function to just say hello'''
    print("Hello")

def sayGoodbye():
    ''' Bluedot callback function to just say goodbye'''
    print("Goodbye")

def dpad(pos):
    ''' Bluedot callback function to implement dpad behaviour'''
    if pos.top:
        print("up")
    elif pos.bottom:
        print("down")
    elif pos.left:
        print("left")
    elif pos.right:
        print("right")
    elif pos.middle:
        print("fire")
    
def moveDistance(pos):
    ''' Bluedot callback function to show distance from centre'''
    if pos.top:
        print("top", pos.distance)
    elif pos.bottom:
        print("bottom", pos.distance)
    elif pos.left:
        print("left", pos.distance)
    elif pos.right:
        print("right", pos.distance)

def moveXY(pos):
    ''' Bluedot callback function to show x-y coordinates'''
    print("pos", pos.x, pos.y)    

def doHelloGoodbye():    
    bd = BlueDot()
    bd.when_pressed = sayHello
    bd.when_released = sayGoodbye

def doDoublePress():
    bd = BlueDot()
    bd.when_double_pressed = sayHello

def doDpad():        
    bd = BlueDot()
    bd.when_pressed = dpad

def doMoveDistance():
    bd = BlueDot()
    bd.when_pressed = moveDistance
    bd.when_moved = moveDistance

def doMoveXY():
    bd = BlueDot()
    bd.when_pressed = moveXY
    bd.when_moved = moveXY

# Uncomment just one of the following tests which set up blue dot
#doHelloGoodbye()
#doDoublePress()
doDpad()
#doMoveDistance()
#doMoveXY()

# Now wait for something to happen on the blue dot
while True:
    pass
