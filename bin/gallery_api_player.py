#!/usr/bin/env python3

"""
provide a list of links as options to navigate
use mpv to play video media
think of something for image galleries
"""
# Requires: mpv, qutebrowser, curl

import os
import sys
import getopt
import urllib.parse
from subprocess import getstatusoutput as unix

# curl -s http://gallery/phpgallery/?path=/zvideos/torrents/ | piclister.py \
#       | grep -E 'phpgallery.*path|phpgallery.*media'

TORRENT_URL="/phpgallery/?path=/zvideos/torrents/"
MOVIE_URL="/phpgallery/?path=/zdata/Elements/RARBG/"
FILTER=r" | piclister.py | grep -E 'phpgallery.*path|phpgallery.*media|\.jpg$|\.png$' " \
       r"| grep -v -E '/\.pics/|/images/template/engage.png'"
CURL="curl -s "

def playvideo(url):
    """play the video url"""
    print(f"mpv \"http://gallery{url}\" ")
    stt, out = unix(f"mpv \"http://gallery{url}\" ")
    if stt != 0:
        print(f"{stt} {out}")

def showimages(url):
    """show image in qutebrowser"""
    stt, out = unix(f"qutebrowser \"http://gallery{url}\" ")
    if stt != 0:
        print(f"{stt} {out}")

def mainloop(url):
    """the main loop"""
    # pylint: disable=too-many-branches

    finished = False
    while not finished:
        #print(f"\n{CURL} \"http://gallery{url}\" {FILTER}\n")
        path = urllib.parse.parse_qs(urllib.parse.urlparse(url).query)['path'][0]
        print(f"\n  ----  [ {path} ]  ----\n")
        _st, out = unix(f"{CURL} \"http://gallery{url}\" {FILTER}")
        lines = out.split('\n')
        if len(lines) >= 7:
            navigation = lines[:7]
            lines = lines[7:]
            choice = {}
            choice[0] = ("Quit", "Quit")
            choice[1] = ("Previous", navigation[0])
            choice[2] = ("Up", navigation[3])
            choice[3] = ("Next", navigation[6])
            idx=4
            for line in lines:
                if line.find('IMAGES') > 0:
                    pass
                else:
                    choice[idx] = (urllib.parse.unquote(os.path.basename(line)), line)
                    idx += 1

            for i in range(idx):
                print(f"{i}. {choice[i][0]}")

            print("")
            done = False
            while not done:
                value = input("Choose a number (or search): ")
                try:
                    if value == "q":
                        value = 0
                    num = int(value)
                    if num in range(0, idx):
                        done = True
                    else:
                        print(f"Invalid option, got {num}")

                except ValueError:
                    url = url+"&s="+value
                    num=-1
                    #print("Invalid: not a number")
                    done = True

            if num > -1:
                if choice[num][0] == "Quit":
                    finished = True
                else:
                    if choice[num][1].find("/?media=") > -1:
                        playvideo(choice[num][1])
                    elif choice[num][1].find("large=") > -1:
                        showimages(choice[num][1])
                    else:
                        url = choice[num][1]
        else:
            finished = True
            print(f"Error: {out}")

def usage():
    """"""
    print(f"Usage: {sys.argv[0]} [-h -t -m]")
    print("   -h   help/usage")
    print("   -t   torents")
    print("   -m   movies")


def main():
    """main"""
    opts, args = getopt.getopt(sys.argv[1:], "htm", ["help", "movies", "torrents"])
    if len(opts) == 0:
        usage()
        sys.exit()

    for opt, args in opts:
        if opt in ['-h', '--help']:
            usage()
            sys.exit()
        elif opt in ['-t', '--torrents']:
            mainloop(TORRENT_URL)
        elif opt in ['-m', '--movies']:
            mainloop(MOVIE_URL)



if __name__ == "__main__":
    main()
