#!/usr/bin/python3
"""script to adjust the screen scaling for a sway window manager"""
# Requires: sway

import sys
import getopt
import json
from subprocess import check_output



def decrease(name, scale):
    """decrease the scaling"""
    scale = min(scale+0.05, 1.0)
    call_swaymsg(name, f"{scale:.2f}")


def increase(name, scale):
    """increase the scaling"""
    scale = max(scale-0.05, 0.5)
    call_swaymsg(name, f"{scale:.2f}")


def call_swaymsg(name, scale): # swaymsg 'output LVDS-1 scale 0.80'
    """sway uses reciprical of scale value"""
    ret = json.loads( check_output(['swaymsg', 'output', name, 'scale', scale],
                                   universal_newlines=True) )
    if not ret[0]['success']:
        print(ret[0]['success'])
        print("error occured changing resolution")


def usage():
    """print usage"""
    print("Usage: scale_sway.py [-h|-s|-i|-d]")


def main():
    """do stuff"""
    joutput = json.loads(check_output(['swaymsg', "-t", "get_outputs"], universal_newlines=True))
    name = joutput[0]['name']
    scale = float(joutput[0]['scale'])
    native = [int(joutput[0]['current_mode']['width']), int(joutput[0]['current_mode']['height'])]
    scaled = [int(native[0]/float(scale)), int(native[1]/float(scale))]

    opts, _args = getopt.getopt(sys.argv[1:], "hsdi", ["help", "scaled", "dec", "inc"])

    for opt, _a in opts:
        if opt in ['-h', '--help']:
            usage()
            sys.exit()

        elif opt in ['-s', '--scale']:
            print(f"{scaled[0]}x{scaled[1]}({scale:.2f})")

        elif opt in ['-d', '--dec']:
            decrease(name, scale)

        elif opt in ['-i', '--inc']:
            increase(name, scale)


if __name__ == '__main__':

    sway = check_output(['pidof', '/usr/bin/sway'], universal_newlines=True) != ''
    if not sway:
        print("not running sway")
        sys.exit()

    main()
