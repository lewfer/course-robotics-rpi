# Think Create Learn
# www.thinkcreatelearn.co.uk
#
# ROSI obstacle avoidance sample solution
#
# Moves around the room, using the ultrasonic sensor to avoid hitting walls

# ======================================================================================================
# Imports
# ======================================================================================================
from rosi import RosiRobot, RosiException 
import time
import math


# ======================================================================================================
# Constants
# ======================================================================================================

SONAR_NUM_DISTANCES_TO_KEEP  = 5 


# ======================================================================================================
# Global variables
# ======================================================================================================
# We will take a number of readings rather than just one so we can ignore spurious readings
global_sonarLastDistances = []    


# ======================================================================================================
# Functions
# ======================================================================================================

# ------------------------------------------------------------------------------------------------------
# Spin for a given angle.  -ve is anticlockwise, +ve clockwise
# ------------------------------------------------------------------------------------------------------
def spinAngle(degrees):
    robot.turnMotors(int(100 * math.copysign(1,degrees)), int(100 * math.copysign(1,-degrees)))
    time.sleep(10.42 * abs(degrees) / 10 / 360)  # My robot takes 10.42 secs to spin 10 times                                           
    robot.turnMotors(0,0)
    time.sleep(2)  # !!wait so we can see what just happened

# ------------------------------------------------------------------------------------------------------
# Take a number of readings and fill the history
# ------------------------------------------------------------------------------------------------------
def fillSonarDistanceHistory(): 
    global global_sonarLastDistances

    for i in range(0,SONAR_NUM_DISTANCES_TO_KEEP):
        distance = round(robot.readSonarDistance(),2)
        print("Fill distance:", distance, " cm")
        global_sonarLastDistances.append(distance)  
        if (len(global_sonarLastDistances)>SONAR_NUM_DISTANCES_TO_KEEP): 
            global_sonarLastDistances.pop(0) # remove the first one 

# ------------------------------------------------------------------------------------------------------
# Take evasive action when we encounter an obstacle 
# ------------------------------------------------------------------------------------------------------
def escapeObstacle():  
    global global_sonarLastDistances
    
    # Try a left turn
    spinAngle(-90)
    fillSonarDistanceHistory() 
    if (min(global_sonarLastDistances)>20): 
        return # we are free to turn left

    # Turn right instead
    spinAngle(180)  # we've already gone 90 left, so need 180 right    
    fillSonarDistanceHistory() 
    if (min(global_sonarLastDistances)>20): 
        return # we are free to turn right

    print ("We didn't find an exit!")


# ======================================================================================================
# Main program
# ======================================================================================================
try:

    print( 'Press CTRL+C to quit')
    robot = RosiRobot()
    robot.start()

    global_sonarLastDistances = []

    # Keep running until told to stop
    while True:
        # Get the distance measurement from the sonar sensor
        distance = round(robot.readSonarDistance(),2)  
        print("Distance:", distance, " cm")

        # Save the last few distance measurements so we can avoid spurious readings
        global_sonarLastDistances.append(distance) 
        if (len(global_sonarLastDistances)>SONAR_NUM_DISTANCES_TO_KEEP): 
            global_sonarLastDistances.pop(0) # remove the first one 

        # Take action based on the distance
        if (min(global_sonarLastDistances)<20): 
            # If the lowest reading was less than 20cm we should stop
            lMotorSpeed = 0 
            rMotorSpeed = 0  
            if (max(global_sonarLastDistances)<20):      
                # If the highest reading was less than 20cm assume we really are seeing an obstacle, so escape from it
                escapeObstacle() 
        elif (min(global_sonarLastDistances)<50):  
            # If the lowest reading was less than 50cm we should slow down
            lMotorSpeed = 30  
            rMotorSpeed = 30 
        elif (min(global_sonarLastDistances)<200):    
            # If the lowest reading was less than 200cm we should proceed slowly
            lMotorSpeed = 50   
            rMotorSpeed = 50  
        else:                        
            # Otherwise the lowest reading must be > 200 so proceed at top speed
            lMotorSpeed = 100  
            rMotorSpeed = 100   

        # Turn the motors at the selected speed
        robot.turnMotors(lMotorSpeed,rMotorSpeed)

    robot.finish()

except RosiException as e:
    print(e.value)
except KeyboardInterrupt:
    robot.finish()    
    
    
