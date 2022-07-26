#!/usr/bin/env python3

import os
import sys
import json
from subprocess import getstatusoutput as unix

PAGE=""

def get_sway_config():
    """"""
    st, content = unix("swaymsg -t get_config")
    if st == 0:
        return json.loads(content)["config"].split("\n")
    else:
        return []

def pretty_keys(keys):
    """"""
    return keys.replace('Shift', '[Shift]').replace('Ctrl', '[Ctrl]')\
               .replace('$mod', '[Super]').replace('$alt', '[Alt]')

def printTo(str):
    """"""
    global PAGE
    PAGE += str+'\n'

def parse(config):
    """"""
    padding = 2
    inBlock = False
    ignore = False
    for ln in config:
        cfg = ln.split()
        if len(cfg) == 0 or cfg[0] == '#':
            continue
        if ' '.join(cfg).find("nag start") > -1:
            ignore = True
        elif ' '.join(cfg).find("nag end") > -1:
            ignore = False
        if ignore:
            continue
        #print(cfg)
        if cfg[0] == "bindsym":
            #print(cfg)
            if "--release" in cfg:
                cfg.remove("--release")
            if "--no-repeat" in cfg:
                cfg.remove("--no-repeat")
            pad = " " * padding
            if ' '.join(cfg).find(" workspace number ") > -1 or \
               ' '.join(cfg).find(" /tmp/sovpipe") > -1 :
                continue

            printTo(f"{pad}{pretty_keys(cfg[1]):<23} => {' '.join(cfg[2:])}")
        elif cfg[0] == "mode":
            padding = 4
            inBlock = True
            printTo(f"  mode {cfg[1]}")
            #print("  }")
        elif cfg[0] == "}":
            padding = 2
            if inBlock:
                inBlock = False
                printTo(f"  {cfg[0]}")
        elif cfg[0] == "#=":
            if len(cfg) > 1:
                if ' '.join(cfg[1:]) == "Switch Workspace":
                    printTo("  -- Switch to or Move Container to Workspace --")
                    printTo("  [Super]+0..9            => switch to workspace 0..9")
                elif ' '.join(cfg[1:]) == "Move Focused Container to Workspace":
                    printTo("  [Super]+[Shift]+0..9    => move container to workspace 0..9")
                else:
                    printTo(f"  -- {' '.join(cfg[1:])} --")
            else:
                printTo(f"")
        elif cfg[0] == '':
            printTo("")


def main():
    printTo("\n  SwayWM Key Bindings")
    printTo("  ===================\n")
    config = get_sway_config()
    parse(config)
    _st, _out = unix(f"echo '{PAGE}' | yad --text-info --geometry=1000x600 ")


if __name__ == '__main__':
    #PAGE = ""
    main()
