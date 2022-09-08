# Think Create Learn
# www.thinkcreatelearn.co.uk
#
# ROSI template for obstacle avoidance

# ======================================================================================================
# Imports
# ======================================================================================================
from rosi import RosiRobot


# ======================================================================================================
# Main program
# ======================================================================================================
print( 'Press CTRL+C to quit')

robot = RosiRobot()
robot.start()

# Keep running until told to stop
while True:

    # Get the time measurement from the sonar sensor
    time = round(robot.readSonarTime(),6)  
    print(f"Time: {time:.6f} seconds")

    # Get the distance measurement from the sonar sensor
    #distance = round(robot.readSonarDistance(),2)  
    #print(f"Distance: {distance} cm")

    # ******** DO SOMETHING HERE ********  

    robot.wait(seconds=0.1)

robot.finish()

    
