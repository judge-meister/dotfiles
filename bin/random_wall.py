#!/usr/bin/env python3
"""
update screen with a random wallpaper
"""

import os
import random
import urllib.request
from urllib.error import URLError
from bs4 import BeautifulSoup

# Requires: feh

# pylint: disable=line-too-long

TARGET_URL_PATH = "http://gallery/phpgallery/?opt=1_1000&path=/zdata/stuff.backup/sdc1/Wallpaper/wallpaper+16x9/goodfon.com/"

class RemotePicError(Exception):
    """ local exception class """
    #pass

def random_page():
    """random page"""
    pages = ['+1', '+2', '+3', '+4', '+5', '+6', '+7', '+8', '+9', '10']
    return pages[random.randint(0, len(pages)-1)]

def get_random_remote_pic():
    """ random remote pic """
    try:
        with urllib.request.urlopen(TARGET_URL_PATH+random_page()) as response:
            html_content = response.read()
            soup = BeautifulSoup(html_content, 'html.parser')

            anchors = soup.find_all('a')

            pict = ""
            while not pict.endswith("jpg") and not pict.endswith("png"):
                pict = anchors[random.randint(0, len(anchors)-1)].get('href')

            return pict

    except URLError as err:
        print("Unable to download page: "+str(err.reason))
        raise RemotePicError from URLError

def download_remote_pic(pic):
    """ download remote pic """
    filepath = "/home/judge/.wallpaper.img"
    try:
        with urllib.request.urlopen(f"http://gallery{pic}") as response:
            image_content = response.read()
            with open(filepath, 'wb') as fptr:
                fptr.write(image_content)
        return filepath

    except URLError as err:
        print("Unable to download image: "+str(err.reason))
        raise RemotePicError from URLError

def get_list_of_pictures(picpath):
    """get pic list"""
    paths = []
    for root, _dirn, filen in os.walk(os.path.join('/home/judge/Pictures', picpath), followlinks=True):
        for file in filen:
            paths.append(os.path.join(root, file))
    return paths

def get_random_local_pic():
    """ random local pic """
    pics = get_list_of_pictures()
    return pics[random.randint(0, len(pics)-1)]


def main():
    """ main """
    try:
        pict = get_random_remote_pic()
        os.system(f'feh --no-fehbg --bg-fill http://gallery{pict}')

    except RemotePicError:
        pict = get_random_local_pic()
        os.system(f'feh --no-fehbg --bg-fill {pict}')

    print(pict)


if __name__ == '__main__':

    main()
