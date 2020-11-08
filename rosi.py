# Think Create Learn
#
# Think Create Learn
# www.thinkcreatelearn.co.uk 
#
# Code for simple robot programming
# version 22-oct-20

# ======================================================================================================
# Import the modules we will need
# ======================================================================================================

import sys
import time
import piconzero3 as pz
import math    
import RPi.GPIO as GPIO, time 


# ======================================================================================================
# Set up constants
# ======================================================================================================

# Define our motor ids for the Picon Zero controller
MOTOR_LEFT = 1
MOTOR_RIGHT = 0

# Define the pins we connected the line following sensor to 
LINE_FOLLOW_PIN_LEFT = 4
LINE_FOLLOW_PIN_CENTRE = 17
LINE_FOLLOW_PIN_RIGHT = 18

# Line following values
BLACK = 0
WHITE = 1

# Define Sonar Pin (Uses same pin for both Ping and Echo)
SONAR_PIN = 20 

# Define the values we will need for ultrasonics
SONAR_SPEED_OF_SOUND = 343                                            # metres per second 
SONAR_MAX_DISTANCE = 1                                                # metres  
SONAR_MAX_WAIT = float(SONAR_MAX_DISTANCE) / SONAR_SPEED_OF_SOUND * 2 # seconds  

# Spin direction
CLOCKWISE = 1
ANTICLOCKWISE = -1

# Picon Zero config settings for setInputConfig
PICONZERO_INPUT_DIGITAL = 0         # read digital values 0 or 1
PICONZERO_INPUT_ANALOG = 1          # read analog values in range 0 to 1023
PICONZERO_INPUT_TEMPERATURE = 2     # DS18B20 temperature sensor

# Picon Zero config settings for setOutputConfig
PICONZERO_OUTPUT_DIGITAL = 0        # output high or low
PICONZERO_OUTPUT_PWM = 1            # output 0 to 100% duty cycle
PICONZERO_OUTPUT_SERVO = 2          # output 0 to 180 degrees
PICONZERO_OUTPUT_NEOPIXEL = 3       # output pixel no 0 to 255 (only output channel 5)

class RosiRobot:
    def __init__(self):

        # Flags to indicate robot state
        self._started = False
        #self._calibratedSpeed = False
        #self._calibratedSpins = False
        self._tracing = False
        self._forceCalibration = False

        # Default settings for a slow robot
        self.robotName = "Unknown"
        self.wheelDiameterInMillimetres = 32
        self.wheelSpacingInMillimetres = 111   # distance between wheels (centre to centre)
        self.motorMaxSpeedRPM = 80

        # Calibration settings for a slow robot
        self._calibratedSpeedMillimetresPerSecond = [1, 11, 22, 33, 44, 56, 67, 78, 89, 111]
        self._calibratedSpinsPerSecond = 0.333

        # Movement limits for the servos
        self.armLimitMin = [0,0,0,0,0,0]
        self.armLimitMax = [180,180,180,180,180,180]

        # Number of light sensors
        self.numLightSensors = 1

    # ======================================================================================================
    # Define Public Functions: Setting up and Resetting
    # ======================================================================================================

    # ------------------------------------------------------------------------------------------------------
    # Start the robot
    # ------------------------------------------------------------------------------------------------------
    def start(self):
        # Default settings
        wheelDiameterInMillimetres = 60
        wheelSpacingInMillimetres = 123
        motorMaxSpeedRPM = 240
        #calibratedSpinsPerSecond = 0.959693
        self.autoCalibrateSpeed()
        self.calibrateSpins(52, 60)

        # Attempt to read settings from file (if no file then we stick with the defaults)
        self._readSettings()

        # Set up the hardware
        self.reset()
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)            

        # Set up the GPIO pins for the line follower
        chan_list = [LINE_FOLLOW_PIN_LEFT,LINE_FOLLOW_PIN_CENTRE, LINE_FOLLOW_PIN_RIGHT]  
        GPIO.setup(chan_list, GPIO.IN)    

        # Set the flag to say that the robot started successfully
        self._started = True

    # ------------------------------------------------------------------------------------------------------
    # Stop the robot and turn off the controller
    # ------------------------------------------------------------------------------------------------------
    def finish(self):
        pz.cleanup()
        pz.stop()

    # ------------------------------------------------------------------------------------------------------
    # Reset the robot, e.g. if something went wrong
    # ------------------------------------------------------------------------------------------------------
    def reset(self):
        # Reset the Picon Zero to its defaults
        pz.stop()
        pz.init()



    # ======================================================================================================
    # Define Public Functions: Moving
    # ======================================================================================================

    # ------------------------------------------------------------------------------------------------------
    # Stop the robot from moving
    # ------------------------------------------------------------------------------------------------------
    def stop(self):
        pz.setMotor(MOTOR_LEFT,0)
        pz.setMotor(MOTOR_RIGHT,0)

    # ------------------------------------------------------------------------------------------------------
    # Move the robot forward for a given time period
    # ------------------------------------------------------------------------------------------------------
    def forwardTime(self, motorSpeed=100, seconds=0):
        self._trace ("Command: Forward {} seconds".format(seconds))
        self._moveTime(motorSpeed, seconds)

    # ------------------------------------------------------------------------------------------------------
    # Move the robot backward for a given time period
    # ------------------------------------------------------------------------------------------------------
    def backwardTime(self, motorSpeed=100, seconds=0):
        self._trace ("Command: Backward {} seconds".format(seconds))
        self._moveTime(-motorSpeed, seconds)

    # ------------------------------------------------------------------------------------------------------
    # Move the robot forward a given distance
    # ------------------------------------------------------------------------------------------------------
    def forwardDistance(self, motorSpeed=100, metres=0, centimetres=0, millimetres=0):
        self._trace ("Command: Forward Distance {} metres, {} centimetres, {} millimetres at speed {}".format(metres, centimetres, millimetres, motorSpeed))
        self._moveDistance(motorSpeed, metres, centimetres, millimetres)

    # ------------------------------------------------------------------------------------------------------
    # Move the robot backward a given distance
    # ------------------------------------------------------------------------------------------------------
    def backwardDistance(self, motorSpeed=100, metres=0, centimetres=0, millimetres=0):
        self._trace ("Command: Backward Distance {} metres, {} centimetres, {} millimetres at speed {}".format(metres, centimetres, millimetres, motorSpeed))
        self._moveDistance(-motorSpeed, metres, centimetres, millimetres)

    # ------------------------------------------------------------------------------------------------------
    # Spin the robot right on the spot
    # ------------------------------------------------------------------------------------------------------
    def spinRight(self):
        self._trace ("Command: Spin Right")
        self._spinAngle(90)

    # ------------------------------------------------------------------------------------------------------
    # Spin the robot left on the spot
    # ------------------------------------------------------------------------------------------------------
    def spinLeft(self):
        self._trace ("Command: Spin Left")
        self._spinAngle(-90)

    # ------------------------------------------------------------------------------------------------------
    # Spin the robot a specific angle
    # -ve is anticlockwise, +ve clockwise
    # ------------------------------------------------------------------------------------------------------
    def spinAngle(self, angle):
        self._trace ("Command: Spin Angle")
        self._spinAngle(angle)

    # ------------------------------------------------------------------------------------------------------
    # Spin the robot for the specified time
    # -1 is anticlockwise, +1 clockwise
    # ------------------------------------------------------------------------------------------------------
    def spinTime(self, seconds, direction=1):
        self._trace ("Command: Spin Time")
        self._spinTime(seconds, direction)   

    # ------------------------------------------------------------------------------------------------------
    # Start the motors turning at the given speeed (don't stop them)
    # ------------------------------------------------------------------------------------------------------
    def turnMotors(self, leftSpeed=100, rightSpeed=100):
        self._trace ("Command: turnMotors R={} L={}".format(leftSpeed, rightSpeed))
        self._turnMotors(int(leftSpeed), int(rightSpeed))
        


    # ======================================================================================================
    # Define Public Functions: Detecting using the Light Sensor
    # ======================================================================================================

    # ------------------------------------------------------------------------------------------------------
    # Check if the light sensor is seeing BLACK,BLACK,BLACK
    # ------------------------------------------------------------------------------------------------------
    def lightSensorSeeingBlob(self):
        self._trace ("Command: Is Light Sensor Seeing Blob?")    
        if self.numLightSensors==1:
            return self._readLightSensor()==BLACK
        elif self.numLightSensors==2:
            return self._readLightSensor()==(BLACK,BLACK)
        else:    
            return self._readLightSensor()==(BLACK,BLACK,BLACK)

    # ------------------------------------------------------------------------------------------------------
    # Check if the light sensor is seeing the specified values
    # ------------------------------------------------------------------------------------------------------
    def lightSensorSeeing(self, left, centre, right):
        self._trace ("Command: Is Light Sensor Seeing {} {} {}?".format(self._blackWhite(left), self._blackWhite(centre), self._blackWhite(right)))    
        return self._readLightSensor()==(left, centre, right)

    # ------------------------------------------------------------------------------------------------------
    # Read the values from the light sensor and return as a tuple (left, centre, right)
    # ------------------------------------------------------------------------------------------------------
    def readLightSensor(self):
        self._trace ("Command: readLightSensor")    
        return self._readLightSensor()

    # ------------------------------------------------------------------------------------------------------
    # Read the values from the single light sensor 
    # ------------------------------------------------------------------------------------------------------
    def readSingleLightSensor(self):
        self._trace ("Command: readSingleLightSensor")    
        return self._readSingleLightSensor()

    # ------------------------------------------------------------------------------------------------------
    # Swap the values of BLACK and WHITE (some sensors are reversed)
    # ------------------------------------------------------------------------------------------------------
    def swapBW(self):
        if self.BLACK==0:
            self.BLACK=1
            self.WHITE=0
        else:
            self.BLACK=0
            self.WHITE=1

    # ======================================================================================================
    # Define Public Functions: Detecting using the Ultrasonics Sensor
    # ======================================================================================================

    # ------------------------------------------------------------------------------------------------------
    # Read the time for the sonar signal to bounce to and from the object
    # ------------------------------------------------------------------------------------------------------
    def readSonarTime(self): 
        self._trace ("Command: readSonarTime")    
        return self._readSonarTime()

    # ------------------------------------------------------------------------------------------------------
    # Read distance from ultrasonic sensor  
    # ------------------------------------------------------------------------------------------------------
    def readSonarDistance(self):
        self._trace ("Command: _readSonarDistance")    
        return self._readSonarDistance()



    # ======================================================================================================
    # Define Public Functions: Calibrating
    # ======================================================================================================

    # ------------------------------------------------------------------------------------------------------
    # Calibrate the robot linear speed
    # ------------------------------------------------------------------------------------------------------
    def calibrateSpeed(self, millimetres, seconds, motorSpeed=0):
        millimetresPerSecond = millimetres / seconds

        # If motorSpeed is 0 (i.e. not provided) then fill the whole list based on extrapolation from 100
        if motorSpeed == 0:
            self._calibratedSpeedMillimetresPerSecond[9] = round(millimetresPerSecond)      # 91-100
            self._calibratedSpeedMillimetresPerSecond[8] = round(millimetresPerSecond*8/10) # 81-90
            self._calibratedSpeedMillimetresPerSecond[7] = round(millimetresPerSecond*7/10) # 71-80
            self._calibratedSpeedMillimetresPerSecond[6] = round(millimetresPerSecond*6/10) # 61-70
            self._calibratedSpeedMillimetresPerSecond[5] = round(millimetresPerSecond*5/10) # 51-60
            self._calibratedSpeedMillimetresPerSecond[4] = round(millimetresPerSecond*4/10) # 41-50
            self._calibratedSpeedMillimetresPerSecond[3] = round(millimetresPerSecond*3/10) # 31-40
            self._calibratedSpeedMillimetresPerSecond[2] = round(millimetresPerSecond*2/10) # 21-30
            self._calibratedSpeedMillimetresPerSecond[1] = round(millimetresPerSecond*1/10) # 11-20
            self._calibratedSpeedMillimetresPerSecond[0] = 1                         # 1-10 - we know this is too slow to move!
        else:
            self._calibratedSpeedMillimetresPerSecond[int((motorSpeed-1)/10)] = millimetresPerSecond
        #_calibratedSpeed = True        
    
    # ------------------------------------------------------------------------------------------------------
    # Calibrate the robot spin speed
    # ------------------------------------------------------------------------------------------------------
    def calibrateSpins(self, spins, seconds):
        self._calibratedSpinsPerSecond = spins / seconds
        #_calibratedSpins = True

    # ------------------------------------------------------------------------------------------------------
    # Calculate the wheel circumference
    # ------------------------------------------------------------------------------------------------------
    def wheelCircumferenceInMillimetres(self):
        return math.pi*self.wheelDiameterInMillimetres

    # ------------------------------------------------------------------------------------------------------
    # Calculate the theoretical max speed based on the wheel circumference and motor speed
    # ------------------------------------------------------------------------------------------------------
    def theoreticalSpeedInMillimetresPersSecond(self):
        return self.wheelCircumferenceInMillimetres() * self.motorMaxSpeedRPM / 60

    # ------------------------------------------------------------------------------------------------------
    # Automatically calibrate the robot based on wheel diameter, wheel spacing and motor rpm
    # ------------------------------------------------------------------------------------------------------
    def autoCalibrateSpeed(self):
        # Actual speed is roughly 0.72 times theoretical speed for the motors we use
        self.calibrateSpeed(self.theoreticalSpeedInMillimetresPersSecond() * 0.72, 1)


    # ======================================================================================================
    # Define Public Functions: Robot Arm
    # ======================================================================================================

    def armMoveAngle(self, servo, angle):
        self._trace ("Command: Arm {} Move {} degrees".format(servo, angle))
        self._armMove(servo, angle)


    # ======================================================================================================
    # Define Public Functions: Helper Functions
    # ======================================================================================================

    # ------------------------------------------------------------------------------------------------------
    # Wait for a specific time period
    # ------------------------------------------------------------------------------------------------------
    def wait(self, seconds):
        time.sleep(seconds)

    # ------------------------------------------------------------------------------------------------------
    # Wait for Enter to be pressed
    # ------------------------------------------------------------------------------------------------------
    def waitForKey(self):
        input("Press Enter")

    # ------------------------------------------------------------------------------------------------------
    # Turn tracing messages on
    # ------------------------------------------------------------------------------------------------------
    def tracingOn(self):
        self._tracing = True

    # ------------------------------------------------------------------------------------------------------
    # Turn tracing messages off
    # ------------------------------------------------------------------------------------------------------
    def tracingOff(self):
        self._tracing = False

    # ------------------------------------------------------------------------------------------------------
    # Set settings from our standard robots
    # ------------------------------------------------------------------------------------------------------
    def settings(self, name):
        self.robotName = name
        if name.lower()=="floella":
            wheelDiameterInMillimetres = 60
            wheelSpacingInMillimetres = 123
            motorMaxSpeedRPM = 240
            #calibratedSpinsPerSecond = 0.959693
            calibrateSpeed()
            calibrateSpins(52, 60)        
        elif name.lower()=="gertrude":
            wheelDiameterInMillimetres = 42
            wheelSpacingInMillimetres = 140
            motorMaxSpeedRPM = 240
            calibrateSpeed(millimetres=2090, seconds=5)
            calibrateSpins(spins=40,seconds=30) 
        elif name.lower()=="edwina":
            wheelDiameterInMillimetres = 32
            wheelSpacingInMillimetres = 114
            motorMaxSpeedRPM = 80
            calibrateSpeed(millimetres=1110, seconds=10)
            calibrateSpins(spins=19.8, seconds=60)
        else:
            raise RosiException("Oops!  I don't know about a robot called {}".format(robotName))


    # ======================================================================================================
    # Define Private Functions
    # ======================================================================================================

    # ------------------------------------------------------------------------------------------------------
    # Private function to check that the robot has been initialised
    # ------------------------------------------------------------------------------------------------------
    def _check(self):
        if not self._started:
            raise RosiException("Oops!  You can't use your robot until you have started it")
        return True

    # ------------------------------------------------------------------------------------------------------
    # Private function to output a trace message if _tracing is on.
    # ------------------------------------------------------------------------------------------------------
    def _trace(self, *args):
        if self._tracing:
            message = "..."
            for arg in args:
                message += str(arg)
            print (message)
  
    # ------------------------------------------------------------------------------------------------------
    # Private function to wait for a short time to buffer between actions (makes movements more accurate)
    # ------------------------------------------------------------------------------------------------------
    def _bufferWait(self):
        time.sleep(0.5)

    # ------------------------------------------------------------------------------------------------------
    # Private function to move a set distance.  Robot must have correct calibration settings beforehand.
    # ------------------------------------------------------------------------------------------------------
    def _moveDistance(self, motorSpeed=100, metres=0, centimetres=0, millimetres=0, indent=1):
        if self._check():
            # Convert distance to seconds
            seconds = 0
            millimetresPerSecond = self._calibratedSpeedMillimetresPerSecond[int((abs(motorSpeed)-1)/10)]
            distanceMillimetres = metres * 1000 + centimetres*10 + millimetres
            seconds = float(distanceMillimetres) / millimetresPerSecond
            self._trace ("{:{}}Move Distance {} millimetres (calculated as {} seconds at speed {})".format(" ", indent*3, distanceMillimetres, round(seconds,3), motorSpeed))

            # Move for that many seconds
            self._moveTime(motorSpeed, seconds, indent+1)

    # ------------------------------------------------------------------------------------------------------
    # Private function to move the robot forward or backward for a given time period
    # ------------------------------------------------------------------------------------------------------
    def _moveTime(self, motorSpeed=100, seconds=0, indent=1):
        if self._check():
            self._trace ("{:{}}Move for {} seconds at speed {}".format(" ", indent*3, round(seconds,3), motorSpeed))
            pz.setMotor(MOTOR_LEFT, motorSpeed)
            pz.setMotor(MOTOR_RIGHT, motorSpeed)
            time.sleep(seconds)
            self.stop()
            self._bufferWait()

    # ------------------------------------------------------------------------------------------------------
    # Private function to set the motors turning at the given speed
    # ------------------------------------------------------------------------------------------------------
    def _turnMotors(self, leftSpeed=100, rightSpeed=100, indent=1):
        if self._check():
            self._trace ("{:{}}Turn motors at L={} R={}".format(" ", indent*3, leftSpeed, rightSpeed))
            pz.setMotor(MOTOR_LEFT, leftSpeed)
            pz.setMotor(MOTOR_RIGHT, rightSpeed)

    # ------------------------------------------------------------------------------------------------------
    # Private function to spin the robot on the spot by a given angle.  Robot must have correct calibration 
    # settings beforehand. -ve is anticlockwise, +ve clockwise
    # ------------------------------------------------------------------------------------------------------
    def _spinAngle(self, degrees, indent=1):     
        if self._check():
            pz.setMotor(MOTOR_LEFT, int(100 * math.copysign(1,degrees)))
            pz.setMotor(MOTOR_RIGHT, int(100 * math.copysign(1,-degrees)))
            seconds = abs(degrees) / 360.0 / self._calibratedSpinsPerSecond

            self._trace ("{:{}}Spin Angle {} for {} seconds".format(" ", indent*3, degrees, round(seconds,2)))
            time.sleep(seconds)                                        
            self.stop()
            self._bufferWait()

    # ------------------------------------------------------------------------------------------------------
    # Private function to spin the robot on the spot for a given time
    # -ve is anticlockwise, +ve clockwise
    # ------------------------------------------------------------------------------------------------------
    def _spinTime(self, seconds, direction=1, indent=1):     
        if self._check():
            pz.setMotor(MOTOR_LEFT, int(100 * math.copysign(1,direction)))
            pz.setMotor(MOTOR_RIGHT, int(100 * math.copysign(1,-direction)))

            self._trace ("{:{}}Spin for {} seconds".format(" ", indent*3, seconds))
            time.sleep(seconds)                                        
            self.stop()
            self._bufferWait()
       
    # ------------------------------------------------------------------------------------------------------
    # Private function to read the 3 values from the line sensor
    # ------------------------------------------------------------------------------------------------------
    def _readLightSensor(self, indent=1):  
        if self._check():
            # Read from the GPIO pins
            left = GPIO.input(LINE_FOLLOW_PIN_LEFT)
            centre = GPIO.input(LINE_FOLLOW_PIN_CENTRE)
            right = GPIO.input(LINE_FOLLOW_PIN_RIGHT)
            if self.numLightSensors==1:
                self._trace ("{:{}}Seeing {}".format(" ", indent*3, self._blackWhite(centre)))
                return centre
            elif self.numLightSensors==2:
                self._trace ("{:{}}Seeing {} {}".format(" ", indent*3, self._blackWhite(left), self._blackWhite(right)))
                return (left, right)
            else:
                self._trace ("{:{}}Seeing {} {} {}".format(" ", indent*3, self._blackWhite(left), self._blackWhite(centre), self._blackWhite(right)))
                return (left, centre, right)


    # ------------------------------------------------------------------------------------------------------
    # Private function to translate the value from the sensor to a friendly name
    # ------------------------------------------------------------------------------------------------------
    def _blackWhite(self, bw):
        if bw==BLACK:
            return "BLACK"
        else:
            return "WHITE"

    # ------------------------------------------------------------------------------------------------------
    # Private function to read the signal bounce time from the ultrasonic sensor 
    # ------------------------------------------------------------------------------------------------------
    def _readSonarTime(self, indent=1): 
        if self._check():
            # Send 10us pulse to trigger the ultrasonic module
            GPIO.setup(SONAR_PIN, GPIO.OUT)
            GPIO.output(SONAR_PIN, True)
            time.sleep(0.00001)
            GPIO.output(SONAR_PIN, False)

            # Switch to input mode
            GPIO.setup(SONAR_PIN, GPIO.IN)
            
            # Start the clock
            start = time.time()

            # Wait for sensor to go high - pulse sent
            count=time.time()
            while GPIO.input(SONAR_PIN)==0 and time.time()-count<SONAR_MAX_WAIT:
                start = time.time()

            # Wait for sensor to go low - echo has come back
            count=time.time()
            stop=count
            while GPIO.input(SONAR_PIN)==1 and time.time()-count<SONAR_MAX_WAIT:
                stop = time.time()
                
            # Calculate pulse length
            elapsed = stop-start

            self._trace ("{:{}}Time {}".format(" ", indent*3, elapsed))

            return elapsed

    # ------------------------------------------------------------------------------------------------------
    # Private function to read the distance from the ultrasonic sensor  
    # ------------------------------------------------------------------------------------------------------
    def _readSonarDistance(self, indent=1): 
        if self._check():
            t = self._readSonarTime()
        
            # Distance is time x speed of sound
            distance = t * SONAR_SPEED_OF_SOUND * 100
            
            # That was the distance there and back so halve the value
            distance = distance / 2

            self._trace ("{:{}}Distance {}".format(" ", indent*3, distance))
            
            return distance  

    # ------------------------------------------------------------------------------------------------------
    # Private function to read settings from a file
    # ------------------------------------------------------------------------------------------------------
    def _readSettings(self):
        try:
            f = open("rosi.settings")
            lines = f.readlines()
            _trace("Reading settings from rosi.settings:")
            for line in lines:
                setting = line.split("=")
                if len(setting)==2:
                    _trace(setting)
                    name = setting[0].strip().lower()
                    value = setting[1].strip()
                    if name == "wheelDiameterInMillimetres".lower():
                        self.wheelDiameterInMillimetres = int(value)
                    elif name == "wheelSpacingInMillimetres".lower():
                        self.wheelSpacingInMillimetres = int(value)
                    elif name == "motorMaxSpeedRPM".lower():
                        self.motorMaxSpeedRPM = int(value)
                    elif name == "calibrateSpeed".lower():
                        params = value.split(",")
                        self.calibrateSpeed(millimetres=int(params[0]), seconds=int(params[1]))
                    elif name == "calibrateSpins".lower():
                        params = value.split(",")
                        self.calibrateSpins(spins=float(params[0]), seconds=int(params[1]))
            f.close()
        except FileNotFoundError:
            pass

    # ------------------------------------------------------------------------------------------------------
    # Show the robot settings
    # ------------------------------------------------------------------------------------------------------
    def printSettings(self):
        print ("Robot Settings:")
        print ("-----------------------------------------------------------")
        print ("Robot name ", self.robotName)
        print ("Wheel diameter ", self.wheelDiameterInMillimetres)
        print ("Motor max speed", self.motorMaxSpeedRPM)
        print ("Wheel circumference ", round(self.wheelCircumferenceInMillimetres(),2))
        print ("Theoretical Speed in Millimetre Per Second ",  round(self.theoreticalSpeedInMillimetresPersSecond(),2))
        print ("Calibrated Speed in Millimetres Per Second", self._calibratedSpeedMillimetresPerSecond)
        print ("Calibrated Spins per Second", round(self._calibratedSpinsPerSecond,2))
        print ("\n")

    # ------------------------------------------------------------------------------------------------------
    # Private function to move an arm servo
    # ------------------------------------------------------------------------------------------------------
    def _armMove(self, servo, angle):
        if self._check():
            # Don't allow movements beyond limits
            if angle >= self.armLimitMin[servo] and angle <= self.armLimitMax[servo]:
                pz.setOutputConfig(servo, PICONZERO_OUTPUT_SERVO)
                pz.setOutput(servo, angle)
                print("move")
            else:
                self._trace("Angle {} is out of range for servo {}".format(angle, servo))
                print("no move")
  

    class Button():
        def __init__(self, channel, pullup=True):
            self.channel = channel
            pz.setInputConfig(channel, PICONZERO_INPUT_DIGITAL, pullup) 

        def isPressed(self):
            return pz.readInput(self.channel)==0

        def waitForPress(self):
            while pz.readInput(self.channel)==1:
                pass

        def waitForRelease(self):
            while pz.readInput(self.channel)==0:
                pass

    class AnalogueIn():
        def __init__(self, channel):
            self.channel = channel
            pz.setInputConfig(channel, PICONZERO_INPUT_ANALOG)  

        def read(self):
            return pz.readInput(self.channel)

    class Led():
        def __init__(self, channel):
            self.channel = channel
            pz.setOutputConfig(channel, PICONZERO_OUTPUT_PWM)  

        def on(self, brightness=100):
            pz.setOutput(self.channel, brightness)

        def off(self):
            pz.setOutput(self.channel, 0)



# ------------------------------------------------------------------------------------------------------
# Get all the command line arguments
# ------------------------------------------------------------------------------------------------------
def getCommandArguments():
    return sys.argv[1:]

# ------------------------------------------------------------------------------------------------------
# Get an int command line argument
# ------------------------------------------------------------------------------------------------------
def getIntArgument(number, default):
    try:
        if len(sys.argv) < number+2:
            rv = default
        else:
            rv =  int(sys.argv[number-1])
    except ValueError:
        raise RosiException("Oops!  You provided the argument '{}' which couldn't be converted to an integer".format(sys.argv[number-1]))
    else:
        return rv

# ------------------------------------------------------------------------------------------------------
# Get a string command line argument
# ------------------------------------------------------------------------------------------------------
def getStringArgument(number, default):
    if len(sys.argv) < number+2:
        rv = default
    else:
        rv =  sys.argv[number-1]
    return sys.argv[number-1]

# ------------------------------------------------------------------------------------------------------
# Get a float command line argument
# ------------------------------------------------------------------------------------------------------
def getFloatArgument(number, default):
    try:
        if len(sys.argv) < number+2:
            rv = default
        else:
            rv =  float(sys.argv[number-1])
    except ValueError:
        raise RosiException("Oops!  You provided the argument '{}' which couldn't be converted to a float".format(sys.argv[number-1]))
    else:
        return rv




# ------------------------------------------------------------------------------------------------------
# Exception to raise if something goes wrong
# ------------------------------------------------------------------------------------------------------
class RosiException(Exception):
    def __init__(self, value):
        self.value = value
    
    def __str__(self):
        return repr(self.value)        