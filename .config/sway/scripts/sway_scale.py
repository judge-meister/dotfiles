#!/usr/bin/python3
"""script to adjust the screen scaling for a sway window manager"""
# Requires: sway

import os
import sys
import getopt
import json
from subprocess import check_output, CalledProcessError

HOME = os.environ["HOME"]
SCALERC = f"{HOME}/.config/sway/.scale"

def remember_scale(scale):
    """record scale in hidden file"""
    with open(SCALERC, 'w') as sc:
        sc.write(f"{scale:.2f}")


def read_scale():
    """read the remembered scale"""
    try:
        with open(SCALERC, 'r') as sc:
            try:
                scale=float(sc.read())
            except ValueError:
                scale=0.85
    except FileNotFoundError:
        scale=0.85
    return scale


def decrease(name, scale):
    """decrease the scaling"""
    scale = min(scale+0.05, 1.0)
    remember_scale(scale)
    call_swaymsg(name, f"{scale:.2f}")


def increase(name, scale):
    """increase the scaling"""
    scale = max(scale-0.05, 0.5)
    remember_scale(scale)
    call_swaymsg(name, f"{scale:.2f}")


def set_scale(name, scale):
    """set the screen scale"""
    remember_scale(scale)
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
    print("Usage: scale_sway.py [-h|-s|-r|-i|-d]")
    print(" -h    help/usage")
    print(" -r    report the scale")
    print(" -i|-d increment or decrement the scale")
    print(" -s    set the scale")


def main():
    """do stuff"""
    joutput = json.loads(check_output(['swaymsg', "-t", "get_outputs"], universal_newlines=True))
    name = joutput[0]['name']
    scale = float(joutput[0]['scale'])
    native = [int(joutput[0]['current_mode']['width']), int(joutput[0]['current_mode']['height'])]
    scaled = [int(native[0]/float(scale)), int(native[1]/float(scale))]

    opts, _args = getopt.getopt(sys.argv[1:], "hs:rdi", ["help", "default", "scale=", "report", "dec", "inc"])

    for opt, a in opts:
        if opt in ['-h', '--help']:
            usage()
            sys.exit()

        elif opt == "--default":
            set_scale(name, read_scale())

        elif opt in ['-r', '--report']:
            print(f"{scaled[0]}x{scaled[1]}({scale:.2f})")

        elif opt in ['-s', '--scale']:
           try:
               val=float(a)
               if val >= 0.0 and val <= 1.0:
                   print(f"call_swaymsg({name},{val})")
                   set_scale(name, val)
           except ValueError:
               sys.exit()
        elif opt in ['-d', '--dec']:
            decrease(name, scale)

        elif opt in ['-i', '--inc']:
            increase(name, scale)


if __name__ == '__main__':

    try:
        sway = check_output(['pidof', '/usr/bin/sway'], universal_newlines=True) != ''
        if not sway:
            print("not running sway")
            sys.exit()

        main()
    except CalledProcessError:
        sys.exit()
