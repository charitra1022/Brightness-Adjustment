# Brightness Adjustment
This utility adjusts the screen brightness of Windows machines using the Gamma Ramp values. This is totally based on software rendering and its changes are discarded as soon as the machine restarts or shuts down. This makes use of the **gdi32.dll** library of Windows, so it does not require any extra installaions and setup

## Requirements
1. Python 3 should be installed on the host machine.
2. For GUI, you should have **PyQT5** module installed on the system. Use **pip** to install it.

## Usage
This app can be used in two modes:-
1. **CLI** mode
2. **GUI** mode.

## CLI Mode
To use this app as a command-line utility, you can open command prompt in the same directory where all these files are present, and type the desired command in command prompt.

### Open help text:-

`python easyeyes`


### Set brightness percentage:-

`python easyeyes -b 30`

This will set the brightness to 30%


### Reset brightness:-
`python easyeyes -b 0`

or 

`python easyeyes -r`


## GUI Mode
For this mode, **PyQT5** module should be installed in the host python environment.

To launch the GUI, run **main.py** file, or type the following command in the command prompt:-

`python main.py`

Make sure that you are running the commands in the same directory where all the files are present, otherwise command prompt will give error.