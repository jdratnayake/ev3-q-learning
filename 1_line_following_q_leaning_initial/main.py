#!/usr/bin/env pybricks-micropython

from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, ColorSensor
from pybricks.parameters import Port
from pybricks.tools import wait
from pybricks.robotics import DriveBase
from random import randint

#Robot parameters
WHITE_VALUE = 50
BLACK_VALUE = 20
TURN_ANGLE = 2
DRIVE_SPEED = 20

N = 3

EV3_ACTION = 1
EV3_STATE = 1

MODE='TRAINING'
gamma = 0.8
num_of_episodes = 1

#Reward-Table
RewardTable = [[0]* N for i in range(N)]
RewardTable[0][0] = -10
RewardTable[0][1] = -10
RewardTable[0][2] = 50

RewardTable[1][0] = 50
RewardTable[1][1] = -5
RewardTable[1][2] = -5

RewardTable[2][0] = -10
RewardTable[2][1] = 50
RewardTable[2][2] = -10

#Action-Table
ActionTable = [[1]* N for i in range(N)]
ActionTable[0][0] = 1
ActionTable[0][1] = 1
ActionTable[0][2] = 1

ActionTable[1][0] = 1
ActionTable[1][1] = 1
ActionTable[1][2] = 1

ActionTable[2][0] = 1
ActionTable[2][1] = 1
ActionTable[2][2] = 1

#Q-Table
QTable = [[0]* N for i in range(N)]
QTable = [[0, 0, 250.0], [250.0, 0, 0], [0, 250.0, 0]]

# Initialize EV3 Brick
ev3 = EV3Brick()

# Define Motors
left_motor = Motor(Port.B)
right_motor = Motor(Port.A)

# Define light sensor
light_sensor = ColorSensor(Port.S4)

# Initialize a robot instance
robot = DriveBase(left_motor, right_motor, wheel_diameter=18, axle_track=190)

# Check State
def set_state(sr):
    if sr < BLACK_VALUE:
        return 1
    elif sr >= BLACK_VALUE and sr <= WHITE_VALUE:
        return 2
    elif sr > WHITE_VALUE:
        return 3

#Motor Drive
def MoveForward():
    while(light_sensor.reflection()>= BLACK_VALUE and light_sensor.reflection() <= WHITE_VALUE):
        robot.straight(20)

def TurnRight():
    while not(light_sensor.reflection() > BLACK_VALUE and light_sensor.reflection() < WHITE_VALUE):
        robot.turn(-TURN_ANGLE)

def TurnLeft():
    while not(light_sensor.reflection() > BLACK_VALUE and light_sensor.reflection() < WHITE_VALUE):
        robot.turn(TURN_ANGLE)

def goto_next(current):
    max_reward = max(QTable[current])
    return QTable[current].index(max_reward)

#Actions 
def CTA():
    if EV3_ACTION == 1:
        MoveForward()
        return set_state(light_sensor.reflection())
    elif EV3_ACTION == 2:
        TurnLeft()
        return set_state(light_sensor.reflection())
    elif EV3_ACTION == 3:
        TurnRight()
        return set_state(light_sensor.reflection())
    

while True:
    ev3.screen.draw_text(40, 50, num_of_episodes)
    if(MODE == 'TRAINING'):
        if(num_of_episodes > 10):
            MODE='RUNNING'
            print(QTable)
        print("Episode: ", num_of_episodes)
        reward_for_this_episode = 0
        state = EV3_STATE -1
        all_possible_states = []
        while reward_for_this_episode < 250:
            # select action for the state randomly
            action = randint(0,(N - 1))
            while ActionTable[state][action] == 0:
                action = randint(0, (N - 1)) #get a random action
            
            temp_data = []
            for i, j in enumerate(ActionTable[state]):
                temp_data.append(QTable[state][i] * j)
            max_reward_for_next_state = max(temp_data)
            QTable[state][action] = RewardTable[state][action] + gamma * max_reward_for_next_state
            reward_for_this_episode = reward_for_this_episode + RewardTable[state][action]
            all_possible_states.append(state + 1)

            EV3_ACTION = action + 1
            EV3_STATE = CTA()
            state = EV3_STATE - 1
        
        print("Training Finished: \nState List Length:", len(all_possible_states), "; State List: ", all_possible_states, "; Total Rewards: ", reward_for_this_episode, "\n")
        print("Q Table: ", QTable)
        num_of_episodes += 1

    elif(MODE == 'RUNNING'):
        EV3_ACTION = goto_next(EV3_STATE - 1) + 1
        EV3_STATE = CTA()
    
    elif(MODE == 'DISPARA'):
        print(light_sensor.reflection())
        wait(1000)
    ev3.screen.clear()