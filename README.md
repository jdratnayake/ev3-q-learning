# Q-Learning for LEGO Mindstorms EV3

This Python script utilizes Q-learning to navigate a LEGO Mindstorms EV3 robot in an environment with light sensors, motors, and an infrared sensor. The script is designed to enable the robot to learn and adapt its behavior for movement based on environmental data and predefined parameters.

## Functionality

The script features:

- **Environment Configuration:** Sets up environmental and robot-specific data such as sensor thresholds, robot speed, and turning rates.
- **Q-Table and Action Table:** Initializes and updates tables for Q-learning, storing rewards and actions taken in various states.
- **Robot Actions:** Defines functions for the robot to move in different directions based on sensor readings and predefined criteria.
- **State and Action Selection:** Determines the current state based on sensor readings and selects the best action using Q-values.
- **Learning and Running Modes:** Operates in learning and running modes, allowing the robot to learn from its actions and later execute learned behaviors.

## How to Use

### Requirements

- LEGO Mindstorms EV3 set
- Python environment compatible with Pybricks for EV3

### Running the Script

1. Ensure the script is uploaded and executed on the LEGO Mindstorms EV3.
2. Adjust the environmental and robot-specific parameters if needed.
3. Run the script to observe the robot's learning process or its execution based on learned behavior.

### Important Notes

- The script utilizes Q-learning principles for adaptive behavior based on rewards and predefined actions.
- Modes: The script operates in learning mode initially, transitioning to running mode after a predefined number of learning iterations.
