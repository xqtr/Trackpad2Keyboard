#!/usr/bin/python3
# -*- coding: utf8 -*-

'''
Trackpad2Keyboard emulation
===========================================================

A program to emulate mouse movement and mouse button clicks into keyboard
keys, for use with programs in a plain terminal. No XWindows/GUI needed.

Requirements:
- evdev
- keyboard
- Dependencies also listed in requirements.txt

License: GPL-3.0-or-later

Copyright (c) 2024 [XQTR]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

Author: XQTR
Email: xqtr@gmx.com // xqtr.xqtr@gmail.com
GitHub: https://github.com/xqtr/Trackpad2Keyboard
Version: 1.0.0
Last Updated: 2024/12/15

Usage:
    sudo python3 t2k.py
   
'''

from evdev import InputDevice, categorize, ecodes
from os.path import isfile, isdir, exists, join
import time
import keyboard  # Import the keyboard library
import json
import argparse 

settings = {}

def read_settings(fname):
    # Read settings from a configuration source
    global settings
    with open(fname, 'r') as json_file:
        settings = json.load(json_file)

def create_default_settings(fname):
    # Create a default settings file
    default_settings = {
        "ignore": 1,  # Default ignore time in seconds
        "threshold": 10,  # Default movement threshold
        "lclick": "enter",  # Default left click emulation
        "rclick": "esc",  # Default right click emulation
        "mclick": "tab",  # Default middle click emulation
        "up": "up",  # Default up key emulation
        "down": "down",  # Default down key emulation
        "left": "left",  # Default left key emulation
        "right": "right",  # Default right key emulation
        "dev": "/dev/input/event0"  # Default device path
    }
    with open(fname, 'w') as json_file:
        json.dump(default_settings, json_file, indent=4)  # Write the default settings to the file
    print(f'Default settings file created at: {fname}')

def emulate_keypress(key):
    # Emulate a key press
    keyboard.press(key)
    keyboard.release(key)
    #print(key)

def my_list():
    print('*** my_list(): begin.')
    devices = map(InputDevice, list_devices())
    for dev in devices:
        print('%-20s %-32s %s' % (dev.fn, dev.name, dev.phys))
        print('*** my_list(): end.')

def monitor_device(dev):
    global settings
    ignore_time = settings['ignore']  # Time in seconds to ignore events
    last_event_time = time.time()  # Initialize the last event time
    movement_threshold = settings['threshold']  # Threshold for movement in units
    x_movement = 0  # Accumulated movement in X direction
    y_movement = 0  # Accumulated movement in Y direction

    for event in dev.read_loop():
        current_time = time.time()

        if event.type == ecodes.EV_KEY:
            if event.value == 1:  # Button pressed
                if event.code == ecodes.BTN_LEFT:
                    #print('Left mouse button clicked.')
                    emulate_keypress(settings["lclick"])  # Emulate pressing the Enter key
                elif event.code == ecodes.BTN_RIGHT:
                    #print('Right mouse button clicked.')
                    emulate_keypress(settings["rclick"])
                elif event.code == ecodes.BTN_MIDDLE:
                    #print('Middle mouse button clicked.')
                    emulate_keypress(settings["mclick"])
        
        if current_time - last_event_time < ignore_time:
            continue  # Ignore events for the specified time
        direction = ""
        if event.type == ecodes.EV_REL:  # Capture mouse movement
            if event.code == ecodes.REL_X:
                x_movement += event.value
                if abs(x_movement) >= movement_threshold:
                    direction = 'Right' if x_movement > 0 else 'Left'
                    #print(f'Mouse moved {direction} by {abs(x_movement)} units in X direction.')
                    x_movement = 0  # Reset accumulated movement after printing
                    last_event_time = current_time  # Update the last event time
            elif event.code == ecodes.REL_Y:
                y_movement += event.value
                if abs(y_movement) >= movement_threshold:
                    direction = 'Down' if y_movement > 0 else 'Up'
                    #print(f'Mouse moved {direction} by {abs(y_movement)} units in Y direction.')
                    y_movement = 0  # Reset accumulated movement after printing
                    last_event_time = current_time  # Update the last event time
            
            if direction == "Right": 
                emulate_keypress(settings['right'])
            elif direction == "Left":
                emulate_keypress(settings["left"])
            elif direction == "Up":
                emulate_keypress(settings["up"])
            elif direction == "Down":
                emulate_keypress(settings["down"])

if __name__ == "__main__" :
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Mouse to keyboard emulator.')
    parser.add_argument('-s', '--settings', type=str, default='settings.json',
                        help='Path to the settings JSON file (default: settings.json)')
    parser.add_argument('-c', '--create', action='store_true',
                        help='Create a default settings JSON file')
    parser.add_argument('-p', '--process', type=str, 
                        help='Name of the process to monitor (optional)')

    # Parse the arguments
    args = parser.parse_args()

    if args.create:
        create_default_settings(args.settings)  # Create the default settings file
    else:
        settings_file = args.settings  # Get the settings file from the argument
        read_settings(settings_file)
        dev_path = settings['dev']
        if(exists(dev_path)):
            device = InputDevice(dev_path)
            try:
                device.grab()
                monitor_device(device)
            except KeyboardInterrupt :
                device.ungrab()
                print('User aborted the program.')
