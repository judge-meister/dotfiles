#!/usr/bin/env python3
"""
update screen with a random wallpaper
"""
# Requires: swaybg

import os
import sys
from subprocess import check_output
from subprocess import getstatusoutput as unix
import psutil
from random_wall import get_random_remote_pic, RemotePicError, \
                        download_remote_pic, get_random_local_pic, \
                        get_list_of_pictures

HOME = os.environ['HOME']

def swaybg(url):
    """doesn't need to kill off old swaybg"""
    #pids = [] #-1
    #for proc in psutil.process_iter():
    #    if 'swaybg' in proc.name():
    #        print(proc.name(), proc.pid)
    #        pids.append(proc.pid)

    os.system(f'swaymsg output "*" bg {url} fill')
    with open(f'{HOME}/.swaybgrc', 'w') as swbg:
        swbg.write(f'swaymsg output "*" bg {url} fill\n')
        os.system(f"chmod +x {HOME}/.swaybgrc")

    #if len(pids) > 0:
    #    for pid in pids:
    #        check_output(['kill', f'{pid}'])

def set_wallpaper(url):
    """call swaymsg output "*" bg {filename} fill if using sway"""
    if os.getenv('WAYLAND_DISPLAY','') != '':
        swaybg(url)

def get_current_wallpaper():
    """ """
    st, current = unix("ps -ef | grep \"swaybg -o\"|grep -v grep|sed 's|.*\(-i /[^ ]*\).*|\\1|g'|cut -d' ' -f2")
    #print(st, current)
    return current

def next_wallpaper():
    """ """
    wall_root = f"{HOME}/.config/sway/wallpapers"
    curr_wall = get_current_wallpaper()
    local_walls = get_list_of_pictures(wall_root)
    local_walls.sort()
    try:
        #print(curr_wall)
        #print(local_walls)
        #print(local_walls.index(curr_wall))
        next_wall = local_walls[local_walls.index(curr_wall)+1]
    except IndexError:
        next_wall = local_walls[0]
    swaybg(os.path.join(wall_root, next_wall))

def prev_wallpaper():
    """ """
    wall_root = f"{HOME}/.config/sway/wallpapers"
    curr_wall = get_current_wallpaper()
    local_walls = get_list_of_pictures(wall_root)
    local_walls.sort()
    try:
        prev_wall = local_walls[local_walls.index(curr_wall)-1]
    except IndexError:
        prev_wall = local_walls[-1]
    swaybg(os.path.join(wall_root, prev_wall))



def main():
    """ main """
    if len(sys.argv) > 1:
        if sys.argv[1] == "next":
            next_wallpaper()
        elif sys.argv[1] == "prev":
            prev_wallpaper()
        elif os.path.exists(sys.argv[1]):
            if os.path.isfile(sys.argv[1]):
                pic = sys.argv[1]
                set_wallpaper(f'{pic}')
                sys.exit()
            elif os.path.isdir(sys.argv[1]):
                pic = get_random_local_pic(sys.argv[1])
                print(f" {pic}")
                set_wallpaper(f'{pic}')
                sys.exit()
    else:
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
