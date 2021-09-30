#!/usr/bin/env python
import argparse
from backend import apply_brightness
import os

description = """
=========
EASY EYES
=========
Adjusts Screen Brightness on Windows Systems.
"""

epilog = """
Running without any arguments will launch this help text.
"""


parser = argparse.ArgumentParser(prog='easyeyes', formatter_class=argparse.RawTextHelpFormatter,
                                 description=description, epilog=epilog, prefix_chars="-")

parser.add_argument('-b', '--brightness', metavar='<value>', action='store', type=int,
                    help="Sets the brightness level given in percentages. 0 resets to default.")

parser.add_argument('-r', '--reset', action='store_true',
                    help='Resets the brightness to default value.')

args = parser.parse_args()

if not any(vars(args).values()) and not (args.brightness == 0):
    # when no parameter is passed, this block executes
    try:
        os.system("python easyeyes.py -h")
    except Exception as e:
        pass

else:
    if args.brightness:
        brightness = apply_brightness(args.brightness)
        print("Brightness successfully set to", brightness)

    if args.brightness == 0:
        brightness = apply_brightness(100)
        print("Brightness reverted to defaults.")

    if args.reset:
        brightness = apply_brightness(100)
        print("Brightness reverted to defaults.")
