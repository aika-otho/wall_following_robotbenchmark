from controller import Robot

def getDistance(sensor):
    
    return ((1000 - sensor.getValue()) / 1000) * 5

# Maximum speed for the velocity value of the wheels.
# Don't change this value.
MAX_SPEED = 5.24

# Get pointer to the robot.
robot = Robot()

# Get the time step of the current world.
timestep = int(robot.getBasicTimeStep())

# Get pointer to the robot wheels motors.
leftWheel = robot.getMotor('left wheel')
rightWheel = robot.getMotor('right wheel')

# We will use the velocity parameter of the wheels, so we need to
# set the target position to infinity.
leftWheel.setPosition(float('inf'))
rightWheel.setPosition(float('inf'))

# Get and enable the distance sensors.
s3 = robot.getDistanceSensor("so3")
s3.enable(timestep)
s0 = robot.getDistanceSensor("so0")
s0.enable(timestep)
s15 = robot.getDistanceSensor("so15")
s15.enable(timestep)
s2 = robot.getDistanceSensor("so2")
s2.enable(timestep)
s1 = robot.getDistanceSensor("so1")
s1.enable(timestep)

# Move forward until we are 50 cm away from the wall.
leftWheel.setVelocity(MAX_SPEED)
rightWheel.setVelocity(MAX_SPEED)
while robot.step(timestep) != -1:
    if getDistance(s3) < 0.4:
        break

# Rotate clockwise until the wall is to our left.
leftWheel.setVelocity(MAX_SPEED)
rightWheel.setVelocity(-MAX_SPEED)
while robot.step(timestep) != -1:
    # Rotate until there is a wall to our left, and nothing in front of us.
    if getDistance(s0) < 1:
        break

# Main loop.
while robot.step(timestep) != -1:

    ratio = getDistance(s0) / getDistance(s15)
    
    # Rotate the robot to the 90º left if it detects something 0.4 meters away from the front sensor.
    if getDistance(s3) < 0.4:
        
        leftWheel.setVelocity(MAX_SPEED)
        rightWheel.setVelocity(-MAX_SPEED)
        
        robot.step(500)
    
    # Steer the robot to the right if the right-front sensor detects a wall that is closer than 0.8 meters.
    elif getDistance(s2) < .8:
        print("que tal")
        leftWheel.setVelocity(MAX_SPEED)
        rightWheel.setVelocity(MAX_SPEED * 0.1)
        robot.step(400)

    # Too close to the wall, we need to turn right. Uses the ratio between the front-side left and back-side left sensors.
    elif ratio < 1:
        leftWheel.setVelocity(MAX_SPEED)
        rightWheel.setVelocity(MAX_SPEED * 0.6)

    # Too far from the wall, we need to turn left. Uses the same ratio.
    elif ratio > 1:
        leftWheel.setVelocity(MAX_SPEED * 0.6)
        rightWheel.setVelocity(MAX_SPEED)
    
    # Steer the robot to the left if both the front-side left and back-side left sensor detects a wall 
    # that is closer than 0.5 meters.
    elif getDistance(s0) >= .5 and getDistance(s15) >= .5:
        print("hola")
        leftWheel.setVelocity(MAX_SPEED * 0.1)
        rightWheel.setVelocity(MAX_SPEED)
        robot.step(400)
        leftWheel.setVelocity(MAX_SPEED)
        rightWheel.setVelocity(MAX_SPEED)
        robot.step(400)
        
    # We are in the right direction.
    else:
        leftWheel.setVelocity(MAX_SPEED)
        rightWheel.setVelocity(MAX_SPEED)

# Stop the robot when we are done.
leftWheel.setVelocity(0)
rightWheel.setVelocity(0)