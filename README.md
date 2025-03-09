# Q-Learning for LEGO Mindstorms EV3

This Python script implements Q-learning to enable a LEGO Mindstorms EV3 robot to navigate its environment using light sensors, motors, and an infrared sensor. Designed for adaptive movement, the script allows the robot to learn and refine its behavior based on environmental data and predefined parameters.

## Features

- **Environment Configuration**: Configures sensor thresholds, robot speed, and turning rates.
- **Q-Table and Action Table**: Initializes and updates Q-learning tables to store rewards and actions for different states.
- **Robot Actions**: Defines movement functions based on sensor readings and criteria.
- **State and Action Selection**: Determines the robot’s state from sensor data and selects optimal actions using Q-values.
- **Learning and Running Modes**: Supports a learning phase to train the robot and a running mode to execute learned behaviors.

## Prerequisites

- [LEGO Mindstorms EV3](https://www.lego.com/en-us/themes/mindstorms) set with:
  - Light sensors
  - Motors
  - Infrared sensor
- Python environment with [Pybricks](https://pybricks.com/) installed for EV3 compatibility.
- USB or Bluetooth connection to upload and run the script on the EV3 brick.

## Installation

1. **Set Up the EV3**:

   - Assemble your LEGO Mindstorms EV3 robot with the required sensors and motors.
   - Ensure the EV3 brick is powered on and connected to your computer.

2. **Install Pybricks**:

   - Follow the [Pybricks installation guide](https://pybricks.com/get-started/) to set up the Python environment on your EV3.

3. **Clone the Repository**:
   ```bash
   git clone https://github.com/<your-username>/q-learning-ev3.git
   cd q-learning-ev3
   ```
4. **Upload the Script:**

   - Transfer the Python script (e.g., `main.py`) to the EV3 brick using Pybricks tools or a compatible IDE.

## Usage

### Running the Script

1. **Configure Parameters (optional):**

   - Open the script and adjust environment-specific settings (e.g., sensor thresholds, speed) as needed.

2. **Execute the Script:**

   - Run the script on the EV3 brick via Pybricks or your IDE.

   - The robot will begin in learning mode, adapting its behavior based on sensor data and rewards.

3. **Observe Behavior:**
   - Monitor the robot as it learns. After a set number of iterations, it switches to running mode to execute learned actions.

### Modes

- **Learning Mode:** The robot explores and updates its Q-table based on rewards.

- **Running Mode:** The robot uses the trained Q-table to navigate efficiently.

## Important Notes

- The script relies on Q-learning, a reinforcement learning technique, to adapt to the environment.

- Ensure sensors are calibrated and the environment is consistent for optimal learning.

- Modify the iteration threshold in the script to control when it transitions from learning to running mode.

## Dependencies

- **Python:** Compatible with Pybricks for EV3.

- **Pybricks:** Library for programming the EV3 in Python.

- **LEGO EV3 Hardware:** Light sensors, motors, and infrared sensor.
