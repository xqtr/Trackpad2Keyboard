# Trackpad2Keyboard

## Overview
The Mouse to Keyboard Emulator is a Python application that allows users to emulate keyboard inputs based on mouse movements and button clicks. This tool is particularly useful for users who want to control their computer using mouse gestures instead of traditional keyboard inputs, in plain terminal, like Linux TTY.

## Features
- Emulates left, right, and middle mouse button clicks as keyboard keys.
- Maps mouse movements to keyboard arrow keys.
- Configurable settings through a JSON file.

## Requirements
To run this project, you need to have the following Python packages installed:
- `evdev`
- `keyboard`

You can install the required packages using pip:
`pip install evdev keyboard`

Additionally, ensure that you have the necessary permissions to access input devices on your system.

## Installation
1. Clone the repository or download the source code.
2. Navigate to the project directory.
3. Install the required dependencies as mentioned above.

## Usage
To run the emulator, use the following command:
`sudo python3 t2k.py`


### Command Line Options
- `-s`, `--settings`: Specify the path to the settings JSON file (default: `settings.json`).
- `-c`, `--create`: Create a default settings JSON file.
- `-p`, `--process`: Name of the process to monitor (optional).

### Example
To create a default settings file, run:

`sudo python3 t2k.py --create`

To run the emulator with the default settings:

`sudo python3 t2k.py`

## Configuration
The settings are stored in a JSON file. You can customize the following parameters:
- `ignore`: Time in seconds to ignore events.
- `threshold`: Movement threshold for mouse movements.
- `lclick`: Key to emulate for left mouse click (default: "enter").
- `rclick`: Key to emulate for right mouse click (default: "esc").
- `mclick`: Key to emulate for middle mouse click (default: "tab").
- `up`, `down`, `left`, `right`: Keys to emulate for mouse movements.
- `dev`: Path to the input device (default: "/dev/input/event0").

Play with the `ignore` and `threshold` values to make the program more sensitive or not.

To get the correct event# path for your device use this command:
`python -m evdev.evtest`

Select the device from the list and check if it's the correct one, by using it and see that it "spits" text on the screen.

## License
This project is licensed under the GPL-3.0-or-later License. See the LICENSE file for more details.

## Author
- **XQTR**
- Email: xqtr@gmx.com / xqtr.xqtr@gmail.com
- GitHub: [XQTR GitHub](https://github.com/xqtr/Trackpad2Keyboard)
