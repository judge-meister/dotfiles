#!/usr/bin/python3
"""
screen scaler for X display
"""
# Requires: xorg-xrandr

import sys
import getopt
from subprocess import check_output

FACTOR=0.02
MINVAL=1.0
MAXVAL=2.0

xrandr = check_output(['xrandr'], universal_newlines=True)

class ScaleScrn:
    """scale the screen"""

    def __init__(self):
        """constructor"""
        self.native = []
        self.scaled = []
        self.find_native_res()
        self.find_scaled_res()
        self.name = ''
        self.find_screen_name()
        self.scale = 1.0
        self.get_scale()

    def get_scale(self):
        """calculate the current scale"""
        try:
            self.scale = float(self.scaled[0])/float(self.native[0])
        except IndexError:
            self.scale = 1.0

    def find_native_res(self):
        """find native resolution"""
        for line in xrandr.split('\n'):
            if line.endswith('+'):
                self.native = line.split()[0].split('x')

    def find_scaled_res(self):
        """find scaled resolution  """
        for line in xrandr.split('\n'):
            if line.find('connected primary') > -1:
                self.scaled = line.split()[3].replace('+0+0','').split('x')

    def find_screen_name(self):
        """find screen name"""
        for line in xrandr.split('\n'):
            if line.find('connected primary') > -1:
                self.name = line.split()[0]

    def show_scale(self):
        """show scale"""
        try:
            print(f"{self.scaled[0]}x{self.scaled[1]}({self.scale:.2f})")
        except IndexError:
            print(f"WxH({self.scale:.2f})")

    def decrease(self):
        """decrease scale"""
        self.scale = max(self.scale-FACTOR, MINVAL)
        self.call_xrandr(f"{self.scale:4.2f}")

    def increase(self):
        """increase scale"""
        self.scale = min(self.scale+FACTOR, MAXVAL)
        self.call_xrandr(f"{self.scale:4.2f}")


    def call_xrandr(self, scale): # xrandr --output LVDS-1 --scale 1.25
        """call xrandr to change scale"""
        check_output(['xrandr','--output', self.name, '--scale', scale], universal_newlines=True)


def usage():
    """usage"""
    print("Usage: scale_screen.py [-h|-s|-i|-d]")


def main():
    """main"""

    scalescrn = ScaleScrn()

    #native = find_native_res()
    #scaled = find_scaled_res()
    #scale = float(scaled[0])/float(native[0])
    #name = find_screen_name()

    opts, _args = getopt.getopt(sys.argv[1:], "hsdi", ["help", "scaled", "dec", "inc"])

    for opt, _arg in opts:
        if opt in ['-h', '--help']:
            usage()
            sys.exit()

        elif opt in ['-s', '--scale']:
            scalescrn.show_scale()

        elif opt in ['-d', '--dec']:
            scalescrn.decrease()

        elif opt in ['-i', '--inc']:
            scalescrn.increase()


if __name__ == '__main__':

    main()
