#!/usr/bin/env pybricks-micropython

from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, ColorSensor, InfraredSensor
from pybricks.parameters import Port
from pybricks.tools import wait
from pybricks.robotics import DriveBase
from random import randint

# Environmental data
WHITE_VALUE = 21
BLACK_VALUE = 7
threshold = (WHITE_VALUE + BLACK_VALUE) / 2.0
CRITICAL_DISTANCE = 10 # Used for obstacle avoidance


#Robot data
DRIVE_SPEED = 20
TURN_RATE = 25


# Algorithm data
N = 4
EV3_ACTION = 0 # Initialize
MODE = 'LEARNING'
# MODE = "RUNNING"
gamma = 0.8
TOLERANCE = 2.5
# Always TURN_RIGHT_BACKWARD_TOLERANCE_FRACTION > FORWARD_TOLERANCE_FRACTION
FORWARD_TOLERANCE_FRACTION = 1.5
TURN_RIGHT_BACKWARD_TOLERANCE_FRACTION = 3


RewardTable = [ [-10, -10, 50, -10],
                [50, -5, -5, -10],
                [-10, 50, -10, -10],
                [-10, -10, -10, 50]]

ActionTable = [ [1, 1, 1, 1],
                [1, 1, 1, 1],
                [1, 1, 1, 1],
                [1, 1, 1, 1]]

QTable = [  [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]]
# QTable = [  [0, 0, 250.0, 0],
#             [250.0, 0, 0, 0],
#             [0, 250.0, 0, 0],
#             [0, 0, 0, 250.0]]


# Initialize EV3 Brick
ev3 = EV3Brick()

# Define Motors
left_motor = Motor(Port.B)
right_motor = Motor(Port.A)

# Define light & ir sensors
light_sensor = ColorSensor(Port.S4)
ir_sensor = InfraredSensor(Port.S1)

# Initialize a robot instance
robot = DriveBase(left_motor, right_motor, wheel_diameter=18, axle_track=190)

def Left():
    if (light_sensor.reflection() > threshold):
        robot.drive(DRIVE_SPEED, -TURN_RATE)
        wait(5)

def Forward():
    if (light_sensor.reflection() > (threshold - FORWARD_TOLERANCE_FRACTION * TOLERANCE)):
        robot.drive(DRIVE_SPEED, 0)
        wait(5)

def Right():
    if (light_sensor.reflection() > (threshold - TURN_RIGHT_BACKWARD_TOLERANCE_FRACTION * TOLERANCE)):
        robot.drive(DRIVE_SPEED, TURN_RATE)
        wait(5)

def Backward():
    if not(light_sensor.reflection() > (threshold - TURN_RIGHT_BACKWARD_TOLERANCE_FRACTION * TOLERANCE)):
        robot.drive(0, 0)
        wait(50)
        robot.drive(-DRIVE_SPEED * 2, 0)
        # robot.stop()
        wait(5)

# state 0 = right
# state 1 = forward
# state 2 = left
# state 3 = backward
def get_current_state(light_sensor_reading):
    if (light_sensor_reading > threshold):
        next_state = 2
    else:
        if (light_sensor_reading > (threshold - FORWARD_TOLERANCE_FRACTION * TOLERANCE)):
            next_state = 1
        else:
            if (light_sensor_reading > (threshold - TURN_RIGHT_BACKWARD_TOLERANCE_FRACTION * TOLERANCE)):
                next_state = 0
            else:
                next_state = 3
    
    return next_state

def find_action(current_state):
    next_action = QTable[current_state].index(max(QTable[current_state]))
    return next_action

def execute_action():

    if EV3_ACTION == 0:
        Forward()
    elif EV3_ACTION == 1:
        Left()
    elif EV3_ACTION == 2:
        Right()
    elif EV3_ACTION == 3:
        Backward()
    
    next_state = get_current_state(light_sensor.reflection())

    return next_state

# EV3_STATE = 0 # Initialize
EV3_STATE = get_current_state(light_sensor.reflection()) # Initialize
count = 1
while True:
    ev3.screen.draw_text(40, 50, count)

    if(MODE == 'LEARNING'):
        if(count > 500):
            MODE = 'RUNNING'
            print(QTable)
            continue

        print("Count: ", count)
        reward_sum = 0
        state = EV3_STATE

        # Goal = (reward_sum >= 250)
        while reward_sum < 250:
            # select action for the state randomly
            action = randint(0,(N - 1))
            while ActionTable[state][action] == 0:
                action = randint(0, (N - 1)) #get a random action
            
            EV3_ACTION = action
            EV3_STATE = execute_action()
            
            next_state_max_q_value = max(QTable[EV3_STATE][i] * j for i, j in enumerate(ActionTable[EV3_STATE]))
            QTable[state][action] = RewardTable[state][action] + gamma * next_state_max_q_value
            reward_sum = reward_sum + RewardTable[state][action]
            
            state = EV3_STATE
        
        print("Q Table: ", QTable)
        count += 1

    elif(MODE == 'RUNNING'):
        if (ir_sensor.distance() < CRITICAL_DISTANCE):
            robot.turn(80)
            TURN_RATE = -1 * TURN_RATE
            robot.stop()
        else:
            EV3_ACTION = find_action(EV3_STATE)
            EV3_STATE = execute_action()

    ev3.screen.clear()