#!/usr/bin/env python3
"""
update screen with a random wallpaper
"""
# Requires: swaybg

import os
import sys
from subprocess import check_output
import psutil
from random_wall import get_random_remote_pic, RemotePicError, \
                        download_remote_pic, get_random_local_pic


def swaybg(url):
    """doesn't need to kill off old swaybg"""
    #pids = [] #-1
    #for proc in psutil.process_iter():
    #    if 'swaybg' in proc.name():
    #        print(proc.name(), proc.pid)
    #        pids.append(proc.pid)

    os.system(f'swaymsg output "*" bg {url} fill')

    #if len(pids) > 0:
    #    for pid in pids:
    #        check_output(['kill', f'{pid}'])

def set_wallpaper(url):
    """call swaymsg output "*" bg {filename} fill if using sway"""
    if os.getenv('WAYLAND_DISPLAY','') != '':
        swaybg(url)

def main():
    """ main """
    if len(sys.argv) > 1:
        if os.path.exists(sys.argv[1]):
            if os.path.isfile(sys.argv[1]):
                pic = sys.argv[1]
                set_wallpaper(f'{pic}')
                sys.exit()
            elif os.path.isdir(sys.argv[1]):
                pic = get_random_local_pic(sys.argv[1])
                #print(f" {pic}")
                set_wallpaper(f'{pic}')
                sys.exit()

    try:
        pic = get_random_remote_pic()
        #print(f"{pic}")
        pic = download_remote_pic(pic)
        set_wallpaper(f"{pic}")

    except RemotePicError:
        pic = get_random_local_pic()
        set_wallpaper(f'{pic}')

    #print(pic)



if __name__ == '__main__':

    main()
